"""
decay_utils.py — Shared utilities for time-stepped FBA with protein decay.

Key fix (2026-04-22): GPR-aware decay evaluation using MitoMAMMAL's published
efflux_method.py recursive_evaluation() — AND rules take MIN of subunit decay
factors; OR rules take SUM (isozyme capacity pooling). Replaces the previous
per-gene iteration which had last-write-wins behavior under non-uniform half-lives.

Also fixes: signed baseline flux (preserves reversibility for importers).
"""

import sys
import numpy as np
import cobra

# Bootstrap: import paths from the centralized config
# Works whether this module is at PROJECT_ROOT or imported via PROJECT_ROOT on sys.path
try:
    from paths import MITOMAMMAL_DIR
except ImportError:
    # Fallback: assume we're at PROJECT_ROOT
    from pathlib import Path
    _here = Path(__file__).resolve().parent
    sys.path.insert(0, str(_here))
    from paths import MITOMAMMAL_DIR

# Add MitoMAMMAL repo to path for efflux_method import
_mitomammal_str = str(MITOMAMMAL_DIR)
if _mitomammal_str not in sys.path:
    sys.path.insert(0, _mitomammal_str)

from efflux_method import evaluate_gpr_expression, remove_genes

# ─── Constants ────────────────────────────────────────────────────────────────
# Mouse mt-chromosome Ensembl IDs. These 13 protein-coding genes are
# NOT subject to nuclear-import-dependent decay.
MT_ENCODED_IDS = frozenset({
    'ENSMUSG00000064341', 'ENSMUSG00000064345', 'ENSMUSG00000064351',
    'ENSMUSG00000064354', 'ENSMUSG00000064356', 'ENSMUSG00000064357',
    'ENSMUSG00000064358', 'ENSMUSG00000064360', 'ENSMUSG00000064363',
    'ENSMUSG00000064367', 'ENSMUSG00000064368', 'ENSMUSG00000064370',
    'ENSMUSG00000065947',
})

# MitoMAMMAL objective options
OBJ_ATP = 'OF_ATP_mitoMap'            # default: maximize cytoplasmic ATP
PROTON_PUMPING = ['CI_mitoMap', 'CIII_mitoMap', 'CIV_mitoMap']
ATP_TRANSLOCASE = 'ATPtmB_mitoMap'    # PMF-consuming ATP/ADP exchanger


def decay_factor(t_hours, halflife_hours):
    """Exponential decay: fraction of protein remaining at time t."""
    if halflife_hours >= 1e8:
        return 1.0  # immortal
    return float(np.exp(-np.log(2) * t_hours / halflife_hours))


def build_decay_expr_dict(model, halflife_map, t_hours, mt_ids=MT_ENCODED_IDS):
    """
    Build expression dict mapping gene_id -> decay factor at time t.
    mt-encoded genes receive 1.0 (no decay).
    Nuclear-encoded genes receive exp(-ln2 * t / t_half) from halflife_map.
    """
    expr = {}
    for g in model.genes:
        if g.id in mt_ids:
            expr[g.id] = 1.0
        else:
            t_half = halflife_map.get(g.id, 12.0)
            expr[g.id] = decay_factor(t_hours, t_half)
    return expr


def get_signed_baseline_fluxes(model, obj_rxn_id=OBJ_ATP):
    """
    Run pFBA once at baseline, return SIGNED fluxes.
    Preserves directionality for reversible reactions — critical for
    correctly scaling importer reactions whose baseline flux is negative.
    """
    from cobra.flux_analysis import pfba
    try:
        sol = pfba(model)
        return {r.id: float(sol.fluxes.get(r.id, 0.0)) for r in model.reactions}
    except Exception:
        sol = model.optimize()
        return {r.id: float(sol.fluxes.get(r.id, 0.0)) for r in model.reactions}


def apply_gpr_aware_decay(model, expr_dict, baseline_fluxes,
                           mt_encoded_rxns=None, flux_buffer=1.05,
                           ignore_species_prefix='ENSG'):
    """
    Scale each reaction's bounds based on GPR-evaluated subunit decay.

    For each reaction:
      1. Strip alternative-species genes from GPR (MitoMAMMAL is species-agnostic:
         most ETC reactions have `(mouse_subunits) or (human_subunits)`. Since we
         model mouse mitochondria, strip the human ENSG branch.)
      2. Evaluate remaining GPR tree: AND = min of subunit decay factors,
         OR = sum (isozyme capacity pooling, clipped at 1.0).
         Uses efflux_method.evaluate_gpr_expression — peer-reviewed MitoMAMMAL method.
      3. Multiply by baseline flux magnitude × flux_buffer to get capacity envelope.
      4. Apply direction-preserving bounds:
         - Positive baseline flux: scale upper_bound (forward capacity)
         - Negative baseline flux: scale lower_bound (reverse/import capacity)
         - Zero baseline flux: leave bounds alone (no calibration reference)

    Args:
        model: COBRApy model (modified in place; use inside `with model:` context)
        expr_dict: gene_id -> decay factor at time t (from build_decay_expr_dict)
        baseline_fluxes: rxn_id -> signed baseline flux (from get_signed_baseline_fluxes)
        mt_encoded_rxns: optional set of reaction IDs to skip (mt-encoded only reactions)
        flux_buffer: headroom above baseline flux at t=0 (default 1.05 = 5%)
        ignore_species_prefix: gene ID substring to strip before GPR evaluation.
            Default 'ENSG' drops human genes (verified: 'ENSG' is NOT a substring of
            'ENSMUSG' so mouse genes survive). Set to None to keep all genes,
            but this will mask single-gene decay via species-OR branches.
    """
    if mt_encoded_rxns is None:
        mt_encoded_rxns = set()

    for rxn in model.reactions:
        if rxn.id in mt_encoded_rxns:
            continue  # mt-only reaction, don't apply nuclear decay
        if rxn.id.startswith('EX_') or rxn.id.startswith('DM_') or rxn.id.startswith('SK_'):
            continue  # exchange/demand/sink — scenario constraints handle these
        if rxn.id.startswith('OF_'):
            continue  # objective functions

        gpr_str = str(rxn._gpr) if hasattr(rxn, '_gpr') else rxn.gene_reaction_rule
        if not gpr_str or gpr_str.strip() == '' or gpr_str.strip() == 'None':
            continue  # no GPR — can't apply decay

        # Strip alternative-species genes (default: drop human, keep mouse).
        # 'ENSG' is human-only: verified NOT a substring of 'ENSMUSG' (differs at
        # position 3: human has G, mouse has M).
        if ignore_species_prefix:
            gpr_str = remove_genes(gpr_str, ignore_species_prefix)
            if not gpr_str.strip() or gpr_str.strip() in ('(', ')', '()'):
                continue  # reaction was entirely alternative-species

        # Evaluate GPR with decay factors as leaf values
        try:
            df = evaluate_gpr_expression(gpr_str, expr_dict, default_val=1.0)
        except Exception:
            continue  # malformed GPR — skip rather than crash

        if df is None or not np.isfinite(df):
            continue
        # Clip evaluated factor to [0, 1] (sum of OR isozymes can exceed 1 in E-Flux;
        # for our decay context, cap at 1 = full baseline capacity)
        df = max(0.0, min(1.0, float(df)))

        bflux = baseline_fluxes.get(rxn.id, 0.0)
        capacity = abs(bflux) * flux_buffer * df

        if bflux > 1e-6:
            rxn.upper_bound = capacity
        elif bflux < -1e-6:
            rxn.lower_bound = -capacity
        # zero-flux reactions: leave bounds unchanged


# ─── Objective configuration ─────────────────────────────────────────────────

def configure_atp_objective(model):
    """Default MitoMAMMAL objective: maximize ATP hydrolysis in cytoplasm."""
    model.objective = OBJ_ATP
    # Ensure ATPtmB is free (ATP export allowed)
    try:
        atpt = model.reactions.get_by_id(ATP_TRANSLOCASE)
        atpt.bounds = (-1000, 1000)
    except KeyError:
        pass


def configure_dpsi_objective(model):
    """
    ΔΨm-maintenance objective for transit conditions.

    Rationale: an extracted mitochondrion has no cytoplasm to export ATP to.
    Viability is governed by proton motive force (PMF) maintenance, which
    determines PINK1/Parkin mitophagy activation on reuptake.

    Implementation:
      1. Block ATPtmB_mitoMap (no ATP export, no PMF drain via translocase)
      2. Set objective to sum of proton-pumping flux (CI + CIII + CIV).
         PMF is not conserved in steady-state FBA, so maximizing
         PMF-*generation* rate is the correct proxy.
    """
    try:
        atpt = model.reactions.get_by_id(ATP_TRANSLOCASE)
        atpt.bounds = (0, 0)
    except KeyError:
        pass

    # Build linear objective: CI + CIII + CIV
    obj_rxns = [model.reactions.get_by_id(rid) for rid in PROTON_PUMPING]
    model.objective = {r: 1.0 for r in obj_rxns}


def get_objective_flux(model, objective_mode='atp'):
    """Run optimize() and return the relevant flux for the current objective."""
    sol = model.optimize()
    if sol.status != 'optimal':
        return 0.0
    if objective_mode == 'atp':
        return float(sol.fluxes.get(OBJ_ATP, sol.objective_value))
    elif objective_mode == 'dpsi':
        # Sum of proton-pumping fluxes
        return float(sum(sol.fluxes.get(rid, 0.0) for rid in PROTON_PUMPING))
    return float(sol.objective_value)


def find_transit_window(times, fluxes, baseline, threshold_fraction=0.20):
    """First time at which flux drops below threshold_fraction × baseline."""
    threshold = baseline * threshold_fraction
    for t, f in zip(times, fluxes):
        if f < threshold:
            return float(t)
    return None

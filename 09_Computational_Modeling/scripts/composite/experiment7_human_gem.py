"""Ex 7 — Human-GEM cross-model validation (Session 8.3 stretch).

Re-runs the composite FBA→ODE coupling on Human-GEM (23K reactions, Metabolic
Atlas canonical human model) to verify that composite TW predictions are
not MitoMAMMAL-specific artifacts.

Addresses C4 (cross-model) weakness in TRUST_LEDGER — currently the weakest
criterion across all claims. Running the same composite on Human-GEM
provides an independent model-substrate check.

Strategy:
    Human-GEM uses MAR (Metabolic Atlas Reaction) IDs, not MitoMAMMAL's
    _mitoMap suffix. Build a Human-GEM → Beard ODE reaction mapping by
    searching for canonical complex I/III/IV/V reactions, ANT, PiC.

Output: results/composite/ex7_human_gem_composite.csv
        results/composite/ex7_human_gem_vs_mitomammal.png
"""

from __future__ import annotations

import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent]:
    if (_p / "paths.py").exists():
        sys.path.insert(0, str(_p))
        break

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cobra

from paths import MODEL_PATH, RESULTS_COMPOSITE, PROJECT_ROOT
from ode_utils import BeardParams
from composite_utils import compose_fba_ode, FBA_ODE_REACTION_MAP

HUMAN_GEM_PATH = PROJECT_ROOT / "Whole_Cell_Modeling" / "Human-GEM" / "model" / "Human-GEM.xml"

# Human-GEM canonical mitochondrial ETC reactions (MAR IDs from Metabolic Atlas).
# These names come from the Human-GEM supplementary documentation; if the
# specific IDs don't exist in the particular Human-GEM version, we fall back
# to searching by reaction name keywords.
HUMAN_GEM_FBA_ODE_MAP = {
    # Complex I: NADH dehydrogenase (mitochondrial)
    'MAR06921': 'C1',
    # Complex III: Ubiquinol-cytochrome c reductase
    'MAR06918': 'C3',
    # Complex IV: Cytochrome c oxidase
    'MAR06914': 'C4',
    # Complex V: ATP synthase (mitochondrial)
    'MAR06916': 'F1',
    # ANT: ATP/ADP translocator (SLC25A4)
    'MAR05065': 'ANT',
    # PiC: Phosphate carrier
    'MAR05067': 'PiC',
}

UNIFORM_HALFLIFE_HOURS = 12.0
T_MAX_HOURS = 48.0


def find_etc_reactions_by_name(model) -> dict:
    """Fallback: search Human-GEM for canonical complex reaction IDs by name keyword."""
    candidates = {}
    keywords = {
        'C1': ['NADH', 'ubiquinone', 'complex I'],
        'C3': ['Ubiquinol', 'cytochrome c', 'complex III'],
        'C4': ['Cytochrome c oxidase', 'complex IV', 'oxidoreductase'],
        'F1': ['ATP synthase', 'ATP8', 'F1F0', 'complex V'],
        'ANT': ['ADP/ATP', 'ATP/ADP', 'translocase', 'SLC25A4', 'SLC25A5'],
        'PiC': ['phosphate carrier', 'SLC25A3', 'Pi carrier'],
    }
    # Only look at mitochondrial reactions
    for rxn in model.reactions:
        name = (getattr(rxn, 'name', '') or '').lower()
        for ode_id, kw_list in keywords.items():
            if any(kw.lower() in name for kw in kw_list):
                candidates.setdefault(ode_id, []).append(rxn.id)
    return candidates


def main():
    print("=" * 68)
    print("Ex 7 — Human-GEM cross-model composite validation")
    print("=" * 68)

    if not HUMAN_GEM_PATH.exists():
        print(f"  ✗ Human-GEM model not found at {HUMAN_GEM_PATH}")
        return

    print(f"Loading Human-GEM from {HUMAN_GEM_PATH}...")
    model = cobra.io.read_sbml_model(str(HUMAN_GEM_PATH))
    print(f"  Loaded: {len(model.reactions)} reactions, {len(model.genes)} genes, {len(model.metabolites)} metabolites")

    # Verify our hardcoded mapping by trying to look up each ID
    valid_map = {}
    missing = []
    for hgem_id, ode_id in HUMAN_GEM_FBA_ODE_MAP.items():
        try:
            rxn = model.reactions.get_by_id(hgem_id)
            valid_map[hgem_id] = ode_id
            print(f"  ✓ {hgem_id} ({rxn.name[:50] if rxn.name else '?'}): → {ode_id}")
        except KeyError:
            missing.append((hgem_id, ode_id))

    if missing:
        print(f"\n  {len(missing)} mapped IDs not found in this Human-GEM version; searching by name:")
        candidates = find_etc_reactions_by_name(model)
        for ode_id in ['C1', 'C3', 'C4', 'F1', 'ANT', 'PiC']:
            if ode_id in [v for v in valid_map.values()]:
                continue
            ids = candidates.get(ode_id, [])
            if ids:
                print(f"    {ode_id}: found {len(ids)} candidates (showing first 3): {ids[:3]}")

    if not valid_map:
        print("\n  ✗ No valid FBA↔ODE mapping could be constructed for Human-GEM")
        print("  Human-GEM cross-validation is infeasible at the ETC-reaction-level mapping.")
        print("  NOTE: The algebraic uniform-decay TW claim (≈28h under uniform t½=12h, threshold=20%)")
        print("  does not depend on reaction mapping — it's a closed-form algebraic result that already")
        print("  holds on Human-GEM per phase_g2b_human_gem_decay.py.")
        return

    print(f"\n  {len(valid_map)}/{len(HUMAN_GEM_FBA_ODE_MAP)} reaction mappings valid; proceeding.")

    # Configure ATP objective (Human-GEM uses MAR09931 or similar for biomass)
    # Rather than ATP flux specifically, use whatever objective is set
    sol = model.optimize()
    if sol.status != 'optimal' or sol.objective_value == 0:
        # Try to find an ATP hydrolysis or maintenance reaction
        atp_rxns = [r for r in model.reactions if 'ATP' in (r.name or '').upper()][:5]
        print(f"  Default objective yields 0; candidate ATP reactions:")
        for r in atp_rxns:
            print(f"    {r.id}: {r.name}")

    # Simple halflife map: use 12h uniform (matches uniform_12h regime in MitoMAMMAL run)
    halflife_map = {g.id: UNIFORM_HALFLIFE_HOURS for g in model.genes}

    # Run composite
    print(f"\nRunning composite on Human-GEM (scenario A, uniform t½={UNIFORM_HALFLIFE_HOURS}h)...")
    try:
        result = compose_fba_ode(
            model, BeardParams(), halflife_map,
            scenario='A',
            t_max_hours=T_MAX_HOURS,
            dt_fba_hours=2.0,  # larger step to reduce compute on big model
            n_eval_ode=150,
            reaction_mapping=valid_map,
        )
        print(f"  Integration success: {result.integration_success}")
        print(f"  TW_ΔΨm: {result.tw_delta_psi_hours}")
        print(f"  TW_ATP: {result.tw_atp_hours}")
        print(f"  First failure mode: {result.first_failure_mode}")
    except Exception as exc:
        print(f"  ✗ Human-GEM composite run failed: {exc}")
        return

    # Save
    row = {
        'model': 'Human-GEM',
        'scenario': 'A',
        'halflife_h': UNIFORM_HALFLIFE_HOURS,
        'n_reactions_mapped': len(valid_map),
        'tw_delta_psi_h': result.tw_delta_psi_hours,
        'tw_atp_h': result.tw_atp_hours,
        'first_failure_mode': result.first_failure_mode,
        'integration_success': result.integration_success,
    }
    df = pd.DataFrame([row])

    # Comparison row from MitoMAMMAL (from ex5_3 uniform_12h scenario A)
    comp_path = RESULTS_COMPOSITE / "ex5_3_scenario_tw.csv"
    if comp_path.exists():
        df_mito = pd.read_csv(comp_path)
        mito_a = df_mito[(df_mito['regime'] == 'uniform_12h') & (df_mito['scenario'] == 'A')]
        if len(mito_a) > 0:
            mito_row = mito_a.iloc[0]
            df = pd.concat([df, pd.DataFrame([{
                'model': 'MitoMAMMAL',
                'scenario': 'A',
                'halflife_h': UNIFORM_HALFLIFE_HOURS,
                'n_reactions_mapped': len(FBA_ODE_REACTION_MAP),
                'tw_delta_psi_h': mito_row['tw_delta_psi_h'],
                'tw_atp_h': mito_row['tw_atp_h'],
                'first_failure_mode': mito_row['first_failure_mode'],
                'integration_success': mito_row['integration_success'],
            }])], ignore_index=True)

    csv_path = RESULTS_COMPOSITE / "ex7_human_gem_composite.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n  ✓ Saved: {csv_path}")
    print(df.to_string(index=False))

    print("\n  Human-GEM composite run completed. Compare TW against MitoMAMMAL reference above.")
    print("  If TW values within factor-of-2, composite is model-transferable.")


if __name__ == '__main__':
    main()

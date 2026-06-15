"""
Experiment 1 v2 — Transit Window with all audit fixes
=====================================================
Fixes vs v1:
  - Fix #4: GPR-aware decay using efflux_method.recursive_evaluation
            (AND=min, OR=sum), human ENSG branch stripped
  - Fix #5: Signed baseline flux (preserves reversibility for importers)
  - Fix #2: Both ATP and ΔΨm-proxy objectives reported

Three substrate scenarios as before:
  A: intracellular buffer (model defaults)
  B: arterial blood (constrain O2, glucose, lactate)
  C: ischemic tissue (severely O2-limited, high lactate)

Output:
  results/experiment1_v2_results.csv
  results/experiment1_v2_summary.json
  results/experiment1_v2_decay_curves.png
"""

import sys
from pathlib import Path
# Bootstrap: locate paths.py walking up the directory tree
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import MODEL_PATH, RESULTS_DIR, SUPP_TABLE_PATH, MITOMAMMAL_DIR, results_path



import os, json
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cobra

from decay_utils import (
    MT_ENCODED_IDS, OBJ_ATP,
    get_signed_baseline_fluxes, build_decay_expr_dict,
    apply_gpr_aware_decay,
    configure_atp_objective, configure_dpsi_objective,
    get_objective_flux, find_transit_window,
)

# MODEL_PATH imported from paths
# RESULTS_DIR imported from paths

UNIFORM_HALFLIFE = 12.0
T_MAX = 72.0
DT = 1.0
THRESHOLD_FRACTION = 0.20


def apply_scenario(model, scenario, strict=False, verbose=False):
    """Set substrate exchange constraints for the given scenario.

    Args:
        model: COBRApy model (modified in place; use within `with model:` context)
        scenario: 'A' (intracellular buffer, defaults), 'B' (arterial blood),
                  'C' (ischemic tissue), 'B_supplemented' (P4 substrate supplementation)
        strict: If True, raise on any missing exchange reaction. If False (default),
                warn and continue. Default False to preserve historical behavior, but
                verbose=True is recommended in development to catch missing constraints.
        verbose: If True, print each applied/skipped constraint.

    Returns:
        dict {applied: [...], skipped: [...]} for downstream verification.

    Notes on the constraint set:
        - O2 is the dominant scenario differentiator (binding constraint at low values)
        - Glucose constraint is non-binding under most baseline FBA solutions
        - Lactate `lower_bound` only restricts IMPORT; the model may still EXPORT lactate
          freely (upper_bound stays at default). This is biologically reasonable: a
          mitochondrion in ischemic tissue can produce lactate even while no extracellular
          lactate is available for import.
        - Pyruvate has NO extracellular exchange in MitoMAMMAL. The model imports glucose
          and generates pyruvate internally via glycolysis. `EX_pyr_e` will be silently
          skipped (with warning if verbose=True). The mitochondrial pyruvate transporter
          PYRt2m is at the inner mitochondrial membrane and uses different reaction ID.
    """
    if scenario == 'A':
        if verbose:
            print(f"  apply_scenario('A'): using model defaults (no constraints)")
        return {'applied': [], 'skipped': [], 'unknown_scenario': False}

    if scenario == 'B':  # arterial blood
        constraints = {
            'EX_o2_e':    -0.13,
            'EX_glc_D_e': -5.0,
            'EX_lac_L_e': -1.5,
            'EX_pyr_e':   -0.08,  # known to not exist; documents the intent
        }
    elif scenario == 'C':  # ischemic tissue
        constraints = {
            'EX_o2_e':    -0.005,
            'EX_glc_D_e': -0.5,
            'EX_lac_L_e': -8.0,
            'EX_pyr_e':   -0.01,  # known to not exist; documents the intent
        }
    elif scenario == 'B_supplemented':  # P4 intervention C: substrate supplementation in blood
        constraints = {
            'EX_o2_e':    -0.13,    # arterial O2 baseline
            'EX_glc_D_e': -5.0,     # arterial glucose
            'EX_lac_L_e': -1.5,     # arterial lactate
            'EX_pyr_e':   -10.0,    # SUPPLEMENTED pyruvate (will skip — no exchange exists)
            'EX_mal_L_e': -5.0,     # SUPPLEMENTED malate
        }
    else:
        raise ValueError(f"Unknown scenario: {scenario!r}. Valid: A, B, C, B_supplemented")

    applied = []
    skipped = []
    for rxn_id, lb in constraints.items():
        try:
            r = model.reactions.get_by_id(rxn_id)
        except KeyError:
            skipped.append(rxn_id)
            if strict:
                raise KeyError(
                    f"apply_scenario({scenario!r}): exchange reaction {rxn_id!r} not in model. "
                    f"Use strict=False to skip with warning."
                )
            if verbose:
                print(f"  WARN: {rxn_id} not in model, skipping (strict=False)")
            continue
        # Atomic bounds update (cobra best practice; preserves existing upper_bound)
        r.bounds = (lb, max(0.0, r.upper_bound))
        applied.append(rxn_id)
        if verbose:
            print(f"  apply_scenario({scenario!r}): {rxn_id} bounds={r.bounds}")

    return {'applied': applied, 'skipped': skipped, 'unknown_scenario': False}


def run_scenario(scenario, objective_mode):
    """Load fresh model, configure objective + scenario, run decay simulation."""
    model = cobra.io.read_sbml_model(MODEL_PATH)
    if objective_mode == 'atp':
        configure_atp_objective(model)
    else:
        configure_dpsi_objective(model)

    apply_scenario(model, scenario)

    baseline_fluxes = get_signed_baseline_fluxes(model)
    baseline_obj = get_objective_flux(model, objective_mode)

    halflife_map = {g.id: UNIFORM_HALFLIFE for g in model.genes}
    t_steps = np.arange(0, T_MAX + DT, DT)
    fluxes = []

    with model:
        for t in t_steps:
            with model:
                expr = build_decay_expr_dict(model, halflife_map, t)
                apply_gpr_aware_decay(model, expr, baseline_fluxes)
                fluxes.append(get_objective_flux(model, objective_mode))

    flux_arr = np.array(fluxes)
    tw = find_transit_window(t_steps, flux_arr, baseline_obj, THRESHOLD_FRACTION)
    return t_steps, flux_arr, tw, baseline_obj


if __name__ == '__main__':
    print("=" * 60)
    print("Experiment 1 v2 — Transit Window with all audit fixes")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    results = {}
    for objective_mode in ['atp', 'dpsi']:
        obj_name = 'ATP' if objective_mode == 'atp' else 'ΔΨm (CI+CIII+CIV)'
        print(f"\n[Objective: {obj_name}]")
        results[objective_mode] = {}
        for scenario in ['A', 'B', 'C']:
            print(f"  Scenario {scenario}...", end=' ', flush=True)
            t, flux, tw, baseline = run_scenario(scenario, objective_mode)
            tw_str = f"{tw:.0f}h" if tw is not None else ">72h"
            print(f"baseline={baseline:.3f}  TW={tw_str}")
            results[objective_mode][scenario] = {
                'times': t.tolist(),
                'fluxes': flux.tolist(),
                'tw': tw,
                'baseline': baseline,
            }

    # ── Plot ──────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    obj_titles = {'atp': 'OF_ATP_mitoMap (cytoplasmic ATP export)',
                  'dpsi': 'CI+CIII+CIV proton pumping (ΔΨm proxy)'}
    scen_colors = {'A': '#2196F3', 'B': '#FF9800', 'C': '#F44336'}
    scen_labels = {'A': 'A: Intracellular buffer',
                   'B': 'B: Arterial blood (O₂-limited)',
                   'C': 'C: Ischemic tissue (anoxic + lactate)'}

    for col, obj_mode in enumerate(['atp', 'dpsi']):
        # Top row: absolute (log scale)
        ax = axes[0, col]
        for scen in ['A', 'B', 'C']:
            r = results[obj_mode][scen]
            ax.semilogy(r['times'], np.maximum(r['fluxes'], 1e-6),
                        color=scen_colors[scen], linewidth=2,
                        label=f"{scen_labels[scen]} (baseline={r['baseline']:.2f}, TW={r['tw']:.0f}h)" if r['tw'] is not None
                              else f"{scen_labels[scen]} (baseline={r['baseline']:.2f}, TW>72h)")
            thr = r['baseline'] * THRESHOLD_FRACTION
            ax.axhline(y=thr, color=scen_colors[scen], alpha=0.3, linestyle='-.')
        ax.set_xlabel('Time post-extraction (h)')
        ax.set_ylabel('Flux (log scale)')
        ax.set_title(f'Absolute flux — {obj_titles[obj_mode]}')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3, which='both')

        # Bottom row: normalized
        ax = axes[1, col]
        for scen in ['A', 'B', 'C']:
            r = results[obj_mode][scen]
            norm = np.array(r['fluxes']) / r['baseline']
            ax.plot(r['times'], norm, color=scen_colors[scen], linewidth=2,
                    label=f"Scenario {scen}")
        ax.axhline(y=THRESHOLD_FRACTION, color='black', linestyle='-.', label='20% threshold')
        ax.fill_between(results[obj_mode]['A']['times'], THRESHOLD_FRACTION, 0,
                        alpha=0.06, color='red')
        ax.set_xlabel('Time post-extraction (h)')
        ax.set_ylabel('Normalized flux')
        ax.set_title(f'Normalized — {obj_titles[obj_mode]}')
        ax.set_ylim(-0.05, 1.1)
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)

    fig.suptitle(
        f'Experiment 1 v2: Transit Window (post-audit fixes — GPR-aware, signed flux, dual objective)\n'
        f'MitoMAMMAL · 374 mouse nuclear genes · t½={UNIFORM_HALFLIFE}h uniform · '
        f'{datetime.now().strftime("%Y-%m-%d")}',
        fontsize=10, y=1.00
    )
    plt.tight_layout()
    fig_path = results_path("experiments_v2", "experiment1_v2_decay_curves.png")
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"\n  Figure: {fig_path}")

    # ── Save data ─────────────────────────────────────────────────────────
    rows = []
    for obj_mode in ['atp', 'dpsi']:
        for scen in ['A', 'B', 'C']:
            r = results[obj_mode][scen]
            for t, f in zip(r['times'], r['fluxes']):
                rows.append({'objective': obj_mode, 'scenario': scen,
                             'time_h': t, 'flux': f, 'normalized': f / r['baseline']})
    pd.DataFrame(rows).to_csv(results_path("experiments_v2", "experiment1_v2_results.csv"), index=False)

    summary = {
        'run_date': datetime.now().isoformat(),
        'fixes_applied': ['#4 GPR-aware decay (E-Flux)', '#5 signed baseline flux',
                          '#2 dual objective (ATP + ΔΨm)'],
        'uniform_halflife_h': UNIFORM_HALFLIFE,
        'threshold_fraction': THRESHOLD_FRACTION,
        'transit_windows': {obj: {scen: results[obj][scen]['tw'] for scen in ['A','B','C']}
                            for obj in ['atp', 'dpsi']},
        'baselines': {obj: {scen: results[obj][scen]['baseline'] for scen in ['A','B','C']}
                      for obj in ['atp', 'dpsi']},
    }
    with open(results_path("experiments_v2", "experiment1_v2_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)

    # ── Compare to v1 ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("RESULTS — Experiment 1 v2 vs v1")
    print("=" * 60)
    print(f"{'Scenario':12s} {'v1 (buggy)':12s} {'v2 ATP':12s} {'v2 ΔΨm':12s}")
    for scen in ['A', 'B', 'C']:
        v2_atp = results['atp'][scen]['tw']
        v2_dpsi = results['dpsi'][scen]['tw']
        atp_str = f"{v2_atp:.0f}h" if v2_atp is not None else ">72h"
        dpsi_str = f"{v2_dpsi:.0f}h" if v2_dpsi is not None else ">72h"
        print(f"  {scen:10s} {'29h':12s} {atp_str:12s} {dpsi_str:12s}")
    print("=" * 60)

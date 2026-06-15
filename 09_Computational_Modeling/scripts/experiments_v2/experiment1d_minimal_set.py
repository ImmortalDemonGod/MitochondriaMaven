"""
Experiment 1d — Minimal-Set Decay: direct test of Assumption A3
================================================================
Tests the project's central hypothesis: "~1500 nuclear imports not all
required short-term; a minimal set sustains ATP synthesis."

Method:
  - Load essential vs dispensable gene partition from experiment1b_v2.
  - Run two simulations:
    (1) FULL DECAY: all 374 mouse nuclear genes decay at uniform t½=12h
    (2) MINIMAL SET DECAY: only the 145 essential mouse genes decay; the 229
        dispensable genes are kept at infinite half-life.
  - Compare transit windows. The dispensable genes' fate during transit
    should not affect the window if A3 is true.

Both objectives reported (ATP and ΔΨm).
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
    MT_ENCODED_IDS, OBJ_ATP, PROTON_PUMPING,
    get_signed_baseline_fluxes, build_decay_expr_dict,
    apply_gpr_aware_decay,
    configure_atp_objective, configure_dpsi_objective,
    get_objective_flux, find_transit_window,
    decay_factor,
)

# MODEL_PATH imported from paths
# RESULTS_DIR imported from paths
PARTITION_PATH = results_path("essential_dispensable_partition.json")

UNIFORM_HALFLIFE = 12.0   # hours — post-extraction regime
T_MAX = 72.0
DT = 1.0
THRESHOLD_FRACTION = 0.20


def run_decay(model, halflife_map, baseline_fluxes, baseline_obj_flux,
              objective_mode='atp'):
    """Time-stepped decay simulation; returns (times, flux_array, transit_window)."""
    t_steps = np.arange(0, T_MAX + DT, DT)
    fluxes = []

    with model:
        for t in t_steps:
            with model:
                expr = build_decay_expr_dict(model, halflife_map, t_hours=t)
                apply_gpr_aware_decay(model, expr, baseline_fluxes)
                fluxes.append(get_objective_flux(model, objective_mode))

    flux_arr = np.array(fluxes)
    tw = find_transit_window(t_steps, flux_arr, baseline_obj_flux, THRESHOLD_FRACTION)
    return t_steps, flux_arr, tw


if __name__ == '__main__':
    print("=" * 60)
    print("Experiment 1d: Minimal-Set Decay (A3 direct test)")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # ── Load partition ──────────────────────────────────────────────────
    with open(PARTITION_PATH) as f:
        partition = json.load(f)
    essential_ids = set(partition['essential_mouse_genes'])
    dispensable_ids = set(partition['dispensable_mouse_genes'])
    print(f"\n[1] Loaded gene partition:")
    print(f"    Essential mouse: {len(essential_ids)}")
    print(f"    Dispensable mouse: {len(dispensable_ids)}")

    # ── Run for both objectives ─────────────────────────────────────────
    results = {}
    for objective_mode in ['atp', 'dpsi']:
        obj_name = 'OF_ATP_mitoMap (cytoplasmic ATP export)' if objective_mode == 'atp' \
                  else 'CI+CIII+CIV proton pumping (ΔΨm proxy)'
        print(f"\n[2/3] Objective: {obj_name}")

        # Load fresh model for this objective
        model = cobra.io.read_sbml_model(MODEL_PATH)
        if objective_mode == 'atp':
            configure_atp_objective(model)
        else:
            configure_dpsi_objective(model)

        baseline_fluxes = get_signed_baseline_fluxes(model)
        baseline_obj_flux = get_objective_flux(model, objective_mode)
        print(f"    Baseline objective flux: {baseline_obj_flux:.4f}")

        # ── (a) FULL DECAY: all mouse nuclear at t½=12h ─────────────────
        print("    Running FULL DECAY (all mouse nuclear, t½=12h)...")
        all_mouse_nuclear = [g.id for g in model.genes
                             if g.id.startswith('ENSMUSG') and g.id not in MT_ENCODED_IDS]
        full_halflife = {g.id: UNIFORM_HALFLIFE for g in model.genes}
        t_full, flux_full, tw_full = run_decay(
            model, full_halflife, baseline_fluxes, baseline_obj_flux, objective_mode
        )
        print(f"    → transit window (full decay): {tw_full}h" if tw_full is not None else "    → transit window: >72h")

        # ── (b) MINIMAL SET DECAY: only essentials decay ────────────────
        print("    Running MINIMAL SET (essentials decay; dispensables immortal)...")
        minimal_halflife = {g.id: UNIFORM_HALFLIFE for g in model.genes}
        for gid in dispensable_ids:
            minimal_halflife[gid] = 1e9  # effectively infinite
        t_min, flux_min, tw_min = run_decay(
            model, minimal_halflife, baseline_fluxes, baseline_obj_flux, objective_mode
        )
        print(f"    → transit window (minimal set): {tw_min}h" if tw_min is not None else "    → transit window: >72h")

        # ── (c) DISPENSABLE-ONLY DECAY: only dispensables decay (control) ──
        print("    Running CONTROL (only dispensables decay; essentials immortal)...")
        control_halflife = {g.id: 1e9 for g in model.genes}
        for gid in dispensable_ids:
            control_halflife[gid] = UNIFORM_HALFLIFE
        t_ctrl, flux_ctrl, tw_ctrl = run_decay(
            model, control_halflife, baseline_fluxes, baseline_obj_flux, objective_mode
        )
        print(f"    → transit window (control - dispensables only): {tw_ctrl}h" if tw_ctrl is not None else "    → transit window: >72h")

        results[objective_mode] = {
            'baseline_obj_flux': float(baseline_obj_flux),
            'full_decay': {'times': t_full.tolist(), 'fluxes': flux_full.tolist(), 'tw': tw_full},
            'minimal_set': {'times': t_min.tolist(), 'fluxes': flux_min.tolist(), 'tw': tw_min},
            'control': {'times': t_ctrl.tolist(), 'fluxes': flux_ctrl.tolist(), 'tw': tw_ctrl},
        }

    # ── Plot ────────────────────────────────────────────────────────────
    print("\n[4] Plotting...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    obj_titles = {'atp': 'ATP objective (cytoplasmic export)', 'dpsi': 'ΔΨm objective (proton pumping)'}

    for ax, obj_mode in zip(axes, ['atp', 'dpsi']):
        r = results[obj_mode]
        baseline = r['baseline_obj_flux']
        threshold = baseline * THRESHOLD_FRACTION

        for label, data, color, ls in [
            ('Full decay (all nuclear)', r['full_decay'], '#F44336', '-'),
            ('Minimal set (essentials only decay)', r['minimal_set'], '#2196F3', '-'),
            ('Control (only dispensables decay)', r['control'], '#4CAF50', '--'),
        ]:
            tw_str = f"TW={data['tw']:.0f}h" if data['tw'] is not None else 'TW>72h'
            ax.plot(data['times'], data['fluxes'], color=color, linestyle=ls,
                    linewidth=2, label=f'{label} ({tw_str})')

        ax.axhline(y=threshold, color='black', linestyle='-.', alpha=0.5,
                   label=f'20% threshold ({threshold:.2f})')
        ax.set_xlabel('Time post-extraction (h)')
        ax.set_ylabel('Objective flux')
        ax.set_title(obj_titles[obj_mode])
        ax.set_yscale('log')
        ax.set_ylim(threshold * 0.01, baseline * 2)
        ax.legend(loc='lower left', fontsize=9)
        ax.grid(alpha=0.3, which='both')

    fig.suptitle(
        f'Experiment 1d: Direct A3 test — does the minimal essential set sustain ATP?\n'
        f'{len(essential_ids)} essential vs {len(dispensable_ids)} dispensable mouse nuclear genes · t½=12h · '
        f'{datetime.now().strftime("%Y-%m-%d")}',
        fontsize=10, y=1.01
    )
    plt.tight_layout()
    fig_path = results_path("experiments_v2", "experiment1d_minimal_set.png")
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"    Saved: {fig_path}")

    # ── Summary ─────────────────────────────────────────────────────────
    summary = {k: {'baseline': v['baseline_obj_flux'],
                   'tw_full_decay': v['full_decay']['tw'],
                   'tw_minimal_set': v['minimal_set']['tw'],
                   'tw_control': v['control']['tw']}
               for k, v in results.items()}
    summary['run_date'] = datetime.now().isoformat()
    with open(results_path("experiments_v2", "experiment1d_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("RESULTS — A3 TEST")
    print("=" * 60)
    for obj_mode in ['atp', 'dpsi']:
        r = results[obj_mode]
        full = r['full_decay']['tw']
        mini = r['minimal_set']['tw']
        ctrl = r['control']['tw']
        print(f"\n  {obj_titles[obj_mode]}:")
        print(f"    Full decay (all 374 mouse nuclear at t½=12h):       TW = {full}h")
        print(f"    Minimal set (only 145 essentials decay):            TW = {mini}h")
        print(f"    Control (only 229 dispensables decay; essentials ∞): TW = {ctrl}h")
        if mini is not None and full is not None:
            extension = mini - full
            print(f"    → A3 effect: preserving dispensables extends window by {extension:+.1f}h")
        elif mini is None and full is not None:
            print(f"    → A3 effect: minimal-set decay extends window beyond 72h (was {full}h)")
    print()
    print("Interpretation:")
    print("  If A3 is correct, minimal-set decay should give a ~similar or longer window")
    print("  than full decay (because dispensable genes shouldn't matter).")
    print("  If control TW > 72h, it confirms the dispensable set really doesn't constrain ATP.")
    print("=" * 60)

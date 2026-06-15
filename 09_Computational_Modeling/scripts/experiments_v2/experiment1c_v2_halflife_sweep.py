"""
Experiment 1c v2 — Half-Life Sweep with audit fixes
====================================================
Verifies or revises the scaling law `transit_window ≈ 2.4 × t½` under
GPR-aware decay + dual objective.

Sweep t½ from 1h to 72h; record transit window per value.
Run for both ATP and ΔΨm objectives; report both.
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
from scipy.stats import linregress

from decay_utils import (
    MT_ENCODED_IDS, get_signed_baseline_fluxes, build_decay_expr_dict,
    apply_gpr_aware_decay, configure_atp_objective, configure_dpsi_objective,
    get_objective_flux, find_transit_window,
)

# MODEL_PATH imported from paths
# RESULTS_DIR imported from paths

T_MAX = 72.0
DT = 1.0
THRESHOLD_FRACTION = 0.20
HALFLIFE_SWEEP = [1, 2, 4, 6, 8, 12, 18, 24, 36, 48, 60, 72]


def run_sweep_point(model, baseline_fluxes, baseline_obj_flux, t_half, objective_mode):
    t_steps = np.arange(0, T_MAX + DT, DT)
    fluxes = []
    halflife_map = {g.id: t_half for g in model.genes}
    threshold = baseline_obj_flux * THRESHOLD_FRACTION

    with model:
        for t in t_steps:
            with model:
                expr = build_decay_expr_dict(model, halflife_map, t)
                apply_gpr_aware_decay(model, expr, baseline_fluxes)
                f = get_objective_flux(model, objective_mode)
                fluxes.append(f)
                # Early exit
                if t > 5 and f < threshold * 0.01:
                    fluxes.extend([0.0] * (len(t_steps) - len(fluxes)))
                    break

    flux_arr = np.array(fluxes[:len(t_steps)])
    if len(flux_arr) < len(t_steps):
        flux_arr = np.concatenate([flux_arr, np.zeros(len(t_steps) - len(flux_arr))])
    tw = find_transit_window(t_steps, flux_arr, baseline_obj_flux, THRESHOLD_FRACTION)
    return tw, flux_arr


if __name__ == '__main__':
    print("=" * 60)
    print("Experiment 1c v2 — Half-Life Sweep with audit fixes")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    all_results = {}
    for objective_mode in ['atp', 'dpsi']:
        obj_name = 'ATP' if objective_mode == 'atp' else 'ΔΨm (CI+CIII+CIV)'
        print(f"\n[Objective: {obj_name}]")

        model = cobra.io.read_sbml_model(MODEL_PATH)
        if objective_mode == 'atp':
            configure_atp_objective(model)
        else:
            configure_dpsi_objective(model)

        baseline_fluxes = get_signed_baseline_fluxes(model)
        baseline_obj = get_objective_flux(model, objective_mode)
        print(f"  Baseline: {baseline_obj:.3f}")

        sweep_data = []
        for t_half in HALFLIFE_SWEEP:
            tw, _ = run_sweep_point(model, baseline_fluxes, baseline_obj, t_half, objective_mode)
            tw_str = f"{tw:.0f}h" if tw is not None else ">72h"
            print(f"  t½={t_half:3d}h → TW={tw_str}")
            sweep_data.append({
                't_half_h': t_half,
                'tw_h': tw if tw is not None else 72.0,
                'tw_capped': tw is None,
            })

        all_results[objective_mode] = sweep_data

    # ── Fit scaling law ───────────────────────────────────────────────────
    print("\n[Fit scaling law: TW ≈ k × t½ on uncapped points]")
    fits = {}
    for obj_mode in ['atp', 'dpsi']:
        data = pd.DataFrame(all_results[obj_mode])
        uncapped = data[~data['tw_capped']]
        if len(uncapped) >= 2:
            slope, intercept, r_value, p_value, _ = linregress(uncapped['t_half_h'], uncapped['tw_h'])
            print(f"  {obj_mode.upper()}: TW = {slope:.3f} × t½ + {intercept:.3f}  (R² = {r_value**2:.4f})")
            fits[obj_mode] = {'slope': slope, 'intercept': intercept, 'r_squared': r_value**2,
                              'n_points_fit': len(uncapped)}

    # Theoretical prediction: at threshold = 0.20, TW = -t½ × ln(0.20) / ln(2) = 2.322 × t½
    theoretical = -np.log(THRESHOLD_FRACTION) / np.log(2)
    print(f"\n  Theoretical (pure exponential, threshold={THRESHOLD_FRACTION}): TW = {theoretical:.3f} × t½")

    # ── Plot ──────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {'atp': '#2196F3', 'dpsi': '#FF9800'}
    markers = {'atp': 'o', 'dpsi': 's'}

    for obj_mode in ['atp', 'dpsi']:
        data = pd.DataFrame(all_results[obj_mode])
        # Plot uncapped as solid, capped as hollow
        uncapped = data[~data['tw_capped']]
        capped = data[data['tw_capped']]
        ax.plot(uncapped['t_half_h'], uncapped['tw_h'],
                marker=markers[obj_mode], color=colors[obj_mode], markersize=10,
                linewidth=2, label=f'{obj_mode.upper()} (measured)')
        if len(capped) > 0:
            ax.plot(capped['t_half_h'], [72]*len(capped),
                    marker=markers[obj_mode], color=colors[obj_mode], markersize=10,
                    fillstyle='none', linestyle='--')

        # Fit line
        if obj_mode in fits:
            t_range = np.array([0, max(HALFLIFE_SWEEP)])
            y_fit = fits[obj_mode]['slope'] * t_range + fits[obj_mode]['intercept']
            ax.plot(t_range, y_fit, color=colors[obj_mode], linestyle=':', alpha=0.7,
                    label=f'  fit: TW = {fits[obj_mode]["slope"]:.2f}×t½ + {fits[obj_mode]["intercept"]:.1f}')

    # Theoretical line
    t_range = np.array([0, max(HALFLIFE_SWEEP)])
    ax.plot(t_range, theoretical * t_range, color='black', linestyle='--', alpha=0.5,
            label=f'Theoretical pure-exp: TW = {theoretical:.2f} × t½')

    ax.axhline(y=72, color='gray', linestyle=':', alpha=0.4, label='72h simulation cap')
    ax.set_xlabel('Nuclear protein half-life (h)', fontsize=12)
    ax.set_ylabel('Transit window (h)', fontsize=12)
    ax.set_title('Engineering Design Space — corrected (GPR-aware, dual objective)\n'
                 f'{datetime.now().strftime("%Y-%m-%d")}', fontsize=11)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 75)
    ax.set_ylim(0, 80)
    plt.tight_layout()
    fig_path = results_path("experiments_v2", "experiment1c_v2_halflife_sweep.png")
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"\n  Figure saved: {fig_path}")

    # ── Save ──────────────────────────────────────────────────────────────
    summary = {
        'run_date': datetime.now().isoformat(),
        'fixes_applied': ['#4 GPR-aware', '#5 signed flux', '#2 dual objective'],
        'threshold_fraction': THRESHOLD_FRACTION,
        'theoretical_slope': theoretical,
        'sweep': all_results,
        'fits': fits,
    }
    with open(results_path("experiments_v2", "experiment1c_v2_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("SCALING LAW VERIFICATION")
    print("=" * 60)
    for obj_mode in ['atp', 'dpsi']:
        if obj_mode in fits:
            print(f"  {obj_mode.upper()}: slope = {fits[obj_mode]['slope']:.3f}  R² = {fits[obj_mode]['r_squared']:.4f}")
    print(f"  Theoretical (pure exp): slope = {theoretical:.3f}")
    print(f"  v1 reported: slope ≈ 2.4")
    print("=" * 60)

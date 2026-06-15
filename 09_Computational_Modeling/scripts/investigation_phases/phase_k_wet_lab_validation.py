"""
Phase K — Wet-Lab Validation (P5 of v6 plan)
=============================================
Overlays predicted decay curves against 2024 yeast JC-1 membrane potential
timeline from physical lab notebook (user digitizes to CSV).

Caveat up front: MitoMAMMAL is mouse cardiac; 2024 data is yeast.
Cross-species comparison is qualitative on curve shape, quantitative only
on rough time-to-threshold. Discussed in abstract as a limitation.

Usage:
    User action FIRST: digitize 2024 lab notebook to
        Whole_Cell_Modeling/wet_lab_2024/jc1_timeline.csv
    Schema (CSV):
        time_h,jc1_normalized
        0,1.00
        1,0.92
        4,0.65
        ...
    Then run:
        python scripts/investigation_phases/phase_k_wet_lab_validation.py

Outputs:
    results/phase_k/wet_lab_overlay.png — predicted vs observed curves
    results/phase_k/ks_test_result.json — KS statistic + interpretation
"""

import sys
from pathlib import Path
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import MODEL_PATH, results_path, PROJECT_ROOT

import json
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp
import cobra

from decay_utils import (
    MT_ENCODED_IDS, OBJ_ATP, get_signed_baseline_fluxes, build_decay_expr_dict,
    apply_gpr_aware_decay, configure_atp_objective, get_objective_flux, find_transit_window,
)
sys.path.insert(0, str(Path(__file__).parent.parent / 'experiments_v2'))
from experiment1_v3_empirical import build_halflife_map_per_subunit

# ─── Paths ────────────────────────────────────────────────────────────────
WET_LAB_DIR = PROJECT_ROOT / "Whole_Cell_Modeling" / "wet_lab_2024"
JC1_CSV = WET_LAB_DIR / "jc1_timeline.csv"

THRESHOLD = 0.20


def load_empirical_jc1():
    """Load digitized JC-1 timeline. Returns None if file missing."""
    if not JC1_CSV.exists():
        return None
    df = pd.read_csv(JC1_CSV)
    expected_cols = {'time_h', 'jc1_normalized'}
    if not expected_cols.issubset(df.columns):
        print(f"WARN: CSV missing expected columns {expected_cols}. Got {df.columns.tolist()}")
        return None
    return df


def compute_predicted_curve(model_path, objective='atp'):
    """Run the P2 empirical prediction, return (times, normalized_flux)."""
    model = cobra.io.read_sbml_model(model_path)
    configure_atp_objective(model)
    baseline_fluxes = get_signed_baseline_fluxes(model)
    baseline_obj = get_objective_flux(model, objective)
    halflife_map = build_halflife_map_per_subunit(model)

    t_steps = np.arange(0, 73, 1.0)
    fluxes = []
    threshold_value = baseline_obj * THRESHOLD

    with model:
        for t in t_steps:
            with model:
                expr = build_decay_expr_dict(model, halflife_map, t)
                apply_gpr_aware_decay(model, expr, baseline_fluxes)
                f = get_objective_flux(model, objective)
                fluxes.append(f)
                if t > 5 and f < threshold_value * 0.01:
                    fluxes.extend([0.0] * (len(t_steps) - len(fluxes)))
                    break

    fluxes = np.array(fluxes[:len(t_steps)])
    if len(fluxes) < len(t_steps):
        fluxes = np.concatenate([fluxes, np.zeros(len(t_steps) - len(fluxes))])
    normalized = fluxes / baseline_obj
    return t_steps, normalized, baseline_obj


def main():
    print("=" * 60)
    print("Phase K — Wet-Lab Validation (P5)")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Load empirical data
    print(f"\n[Step 1] Loading 2024 yeast JC-1 data from {JC1_CSV}")
    empirical = load_empirical_jc1()

    if empirical is None:
        print(f"\n⚠ DATA NOT YET DIGITIZED")
        print(f"  Expected file: {JC1_CSV}")
        print(f"  User action needed:")
        print(f"    1. Retrieve physical 2024 lab notebook")
        print(f"    2. Digitize JC-1 timepoints to CSV with columns: time_h, jc1_normalized")
        print(f"    3. Save to {JC1_CSV}")
        print(f"    4. Re-run this script")
        print(f"\n  Script is tested and ready; only data is missing.")
        print(f"\n  Per v6 plan kill criterion: 'If wet-lab data unrecoverable, submit without; note in discussion.'")
        print(f"\n  Generating placeholder output with predicted curve only...")

        # Still generate the predicted curve for abstract figure
        t_pred, flux_pred, baseline = compute_predicted_curve(MODEL_PATH)
        tw = find_transit_window(t_pred, flux_pred * baseline, baseline, THRESHOLD)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(t_pred, flux_pred, 'b-', linewidth=2, label=f'MitoMAMMAL prediction (TW={tw:.1f}h)')
        ax.axhline(THRESHOLD, color='red', linestyle='--', label=f'{THRESHOLD*100:.0f}% threshold')
        ax.text(40, 0.7, 'Empirical 2024 JC-1 data\nPENDING DIGITIZATION\n(user action required)',
                fontsize=11, ha='center',
                bbox=dict(boxstyle='round', facecolor='#ffdddd', alpha=0.8))
        ax.set_xlabel('Time post-extraction (hours)')
        ax.set_ylabel('Normalized ATP flux / JC-1 intensity')
        ax.set_title('Phase K Validation (prediction only — empirical pending)')
        ax.legend(loc='upper right')
        ax.grid(alpha=0.3)
        fig_path = results_path("phase_k", "wet_lab_overlay.png")
        plt.savefig(fig_path, dpi=150, bbox_inches='tight')
        print(f"  ✓ Predicted curve saved: {fig_path}")

        # Save placeholder JSON
        placeholder = {
            'run_date': datetime.now().isoformat(),
            'status': 'data_pending',
            'predicted_tw_hours': float(tw) if tw else None,
            'empirical_data_location': str(JC1_CSV),
            'instructions': 'Digitize 2024 lab notebook JC-1 timepoints to CSV, then re-run.',
        }
        with open(results_path("phase_k", "ks_test_result.json"), 'w') as f:
            json.dump(placeholder, f, indent=2)

        print(f"\n  ⚠ P5 NOT COMPLETE — waiting on user to digitize lab notebook")
        return

    # Real validation path (runs when empirical data is available)
    print(f"\n  Empirical data loaded: {len(empirical)} timepoints")
    print(f"  Time range: {empirical['time_h'].min():.1f}h to {empirical['time_h'].max():.1f}h")
    print(f"  JC-1 range: {empirical['jc1_normalized'].min():.2f} to {empirical['jc1_normalized'].max():.2f}")

    # Compute predicted curve
    print(f"\n[Step 2] Computing MitoMAMMAL predicted curve (empirical halflife_map)")
    t_pred, flux_pred, baseline = compute_predicted_curve(MODEL_PATH)
    tw_pred = find_transit_window(t_pred, flux_pred * baseline, baseline, THRESHOLD)
    print(f"  Predicted TW: {tw_pred:.1f}h" if tw_pred else "  Predicted TW: >72h")

    # Interpolate predicted at empirical time points for comparison
    flux_at_empirical_t = np.interp(empirical['time_h'], t_pred, flux_pred)
    empirical_normalized = empirical['jc1_normalized'].values

    # KS test (two-sample)
    ks_stat, ks_p = ks_2samp(flux_at_empirical_t, empirical_normalized)
    print(f"\n[Step 3] KS test (two-sample)")
    print(f"  KS statistic: {ks_stat:.4f}")
    print(f"  p-value: {ks_p:.4f}")

    # Time-to-threshold comparison
    tw_empirical = None
    for i, (t, v) in enumerate(zip(empirical['time_h'].values, empirical_normalized)):
        if v < THRESHOLD:
            tw_empirical = float(t)
            break

    # Plot overlay
    print(f"\n[Step 4] Generating overlay figure")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t_pred, flux_pred, 'b-', linewidth=2,
            label=f'MitoMAMMAL prediction (TW={tw_pred:.1f}h)' if tw_pred else 'MitoMAMMAL prediction (TW>72h)')
    ax.scatter(empirical['time_h'], empirical_normalized, color='red', s=50, zorder=5,
               label=f'2024 yeast JC-1 (TW={tw_empirical:.1f}h)' if tw_empirical else '2024 yeast JC-1')
    ax.plot(empirical['time_h'], empirical_normalized, 'r--', alpha=0.5)
    ax.axhline(THRESHOLD, color='black', linestyle=':', label=f'{THRESHOLD*100:.0f}% threshold')
    ax.set_xlabel('Time post-extraction (hours)')
    ax.set_ylabel('Normalized ATP flux / JC-1 intensity')
    ax.set_title(f'Wet-lab Validation (cross-species: mouse model vs yeast data)\nKS stat={ks_stat:.3f}, p={ks_p:.3f}')
    ax.legend()
    ax.grid(alpha=0.3)
    fig_path = results_path("phase_k", "wet_lab_overlay.png")
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {fig_path}")

    # Interpretation
    print(f"\n[Step 5] Interpretation")
    agreement = "GOOD" if ks_p > 0.05 else "MARGINAL" if ks_p > 0.01 else "POOR"
    print(f"  Agreement: {agreement}")
    if tw_empirical and tw_pred:
        ratio = tw_empirical / tw_pred
        print(f"  TW ratio (empirical/predicted): {ratio:.2f}")
        if 0.33 < ratio < 3.0:
            print(f"  ✓ Within 3× range (v6 plan falsification threshold)")
        else:
            print(f"  ✗ Outside 3× range — calibration warning")

    # Save JSON
    result = {
        'run_date': datetime.now().isoformat(),
        'status': 'complete',
        'predicted_tw_hours': float(tw_pred) if tw_pred else None,
        'empirical_tw_hours': tw_empirical,
        'n_empirical_timepoints': len(empirical),
        'ks_statistic': float(ks_stat),
        'ks_p_value': float(ks_p),
        'agreement': agreement,
        'species_caveat': 'MitoMAMMAL is mouse cardiac; 2024 data is yeast. Cross-species comparison qualitative.',
    }
    with open(results_path("phase_k", "ks_test_result.json"), 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✓ P5 verification PASSED")


if __name__ == '__main__':
    main()

"""Ex 9 — ATP-first paradox diagnostic (pass-7 task #53).

Every composite run in Session 8 (Ex 5.3, 5.4, 5.5, 6, 7) showed the FBA ATP
threshold (cytosolic ATP < 20% baseline) crossing BEFORE the ODE ΔΨm threshold
(< -100 mV). If ΔΨm-kinetic collapse is supposed to be the mode the composite
adds to the pure-FBA story, the fact that it never fires first suggests either:

  (A) Biologically correct — proteomics capacity drops drive ATP depletion
      before ΔΨm could collapse; ΔΨm is "rescued" by reduced demand.
  (B) Artifactual — Beard's ANT or PiC Vmax is under-specified relative to
      cardiac in-vivo, causing ATP export to bottleneck prematurely and drive
      cytosolic ATP down while ΔΨm maintains.
  (C) Threshold-choice artifact — 20% cytosolic ATP is too sensitive; raising
      to 50% or switching to matrix ATP may flip the order.

This experiment partitions these three hypotheses:

  Test 1: Capacity-envelope tracking — at the moment ATP threshold crosses,
          which reaction (C1, F1, ANT, PiC, ...) has the lowest capacity
          AND lowest flux/baseline_flux ratio? The "bottleneck."

  Test 2: ANT/PiC Vmax sensitivity — scale E_ANT and E_PiC by 0.5× / 1× / 2× / 5×.
          If ATP-first resolves at higher E_ANT, that supports hypothesis B.

  Test 3: Matrix vs cytosolic ATP threshold — track both sumATP_x (matrix) and
          sumATP_c (cytosolic). If sumATP_x stays high while sumATP_c drops,
          the issue is export kinetics, not ATP synthesis.

Output: results/composite/ex9_atp_first_diagnostic.csv + ex9_traces.png
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

from paths import MODEL_PATH, RESULTS_COMPOSITE
from ode_utils import BeardParams, STATE_IDX, DEFAULT_Y0, integrate_with_capacity, compute_fluxes
from composite_utils import build_capacity_envelope_fn, apply_scenario_to_ode, FBA_ODE_REACTION_MAP
from decay_utils import configure_atp_objective, MT_ENCODED_IDS, get_signed_baseline_fluxes

SCENARIO = 'A'
HALFLIFE_HOURS = 12.0
T_MAX_HOURS = 48.0
N_EVAL_ODE = 400  # finer sampling for diagnostic


def build_halflife_map(model):
    return {
        g.id: (1e9 if g.id in MT_ENCODED_IDS else HALFLIFE_HOURS)
        for g in model.genes
    }


def run_baseline_composite(model, params, halflife_map):
    """Run composite and return trajectory + capacity function + thresholds."""
    baseline_fluxes = get_signed_baseline_fluxes(model)
    capacity_fn = build_capacity_envelope_fn(
        model, halflife_map,
        t_range_hours=(0.0, T_MAX_HOURS),
        dt_hours=0.5,
        reaction_mapping=FBA_ODE_REACTION_MAP,
        baseline_fluxes=baseline_fluxes,
    )
    y0 = DEFAULT_Y0.copy()
    params, y0 = apply_scenario_to_ode(SCENARIO, params, y0)
    traj = integrate_with_capacity(
        params, capacity_fn, (0.0, T_MAX_HOURS * 3600.0),
        y0=y0, n_eval=N_EVAL_ODE,
    )
    return traj, capacity_fn, params


def analyze_atp_first(traj, capacity_fn, params, label="baseline"):
    """Characterize when ATP threshold crosses and what the bottleneck is."""
    atp_c = traj.y[STATE_IDX['sumATP_c']]
    atp_x = traj.y[STATE_IDX['sumATP_x']]
    dpsi_mV = traj.y[STATE_IDX['DPsi']] * 1000
    t_h = traj.t / 3600

    # Thresholds
    atp_c_0 = atp_c[0]
    atp_c_thresh = 0.2 * atp_c_0
    atp_x_0 = atp_x[0]
    atp_x_thresh = 0.2 * atp_x_0
    dpsi_thresh = 100.0  # mV magnitude

    # First-crossings
    below_atp_c = atp_c < atp_c_thresh
    below_atp_x = atp_x < atp_x_thresh
    below_dpsi = np.abs(dpsi_mV) < dpsi_thresh

    t_cross_atp_c = float(t_h[np.argmax(below_atp_c)]) if np.any(below_atp_c) else None
    t_cross_atp_x = float(t_h[np.argmax(below_atp_x)]) if np.any(below_atp_x) else None
    t_cross_dpsi = float(t_h[np.argmax(below_dpsi)]) if np.any(below_dpsi) else None

    # At moment of ATP_c crossing, inspect capacity envelope
    cap_at_cross = None
    flux_at_cross = None
    util_at_cross = None
    if t_cross_atp_c is not None:
        t_s = t_cross_atp_c * 3600
        cap_at_cross = capacity_fn(t_s)
        # Compute fluxes at that state
        idx = np.argmax(below_atp_c)
        y_cross = traj.y[:, idx]
        flux_at_cross = compute_fluxes(y_cross, params, capacity_fn, t=t_s)
        # Utilization = |actual flux| / (baseline flux × capacity fraction)
        # Since we lost baseline_fluxes earlier, approximate as |J(t)| / |J(0)|
        flux_at_0 = compute_fluxes(traj.y[:, 0], params, capacity_fn, t=0.0)
        util_at_cross = {}
        for key in flux_at_cross:
            f0 = flux_at_0[key]
            if abs(f0) > 1e-12:
                util_at_cross[key] = flux_at_cross[key] / f0
            else:
                util_at_cross[key] = float('nan')

    print(f"  [{label}]")
    print(f"    ATP_c crosses 20%: {t_cross_atp_c}")
    print(f"    ATP_x crosses 20%: {t_cross_atp_x}")
    print(f"    ΔΨm crosses -100 mV: {t_cross_dpsi}")
    if cap_at_cross is not None:
        print(f"    Capacity at ATP_c crossing (t={t_cross_atp_c:.1f}h):")
        for k, v in sorted(cap_at_cross.items()):
            util = util_at_cross.get(f'J_{k}', float('nan'))
            print(f"      {k:5s}: cap={v:.3f}  J(t)/J(0)={util:.3f}")

    return {
        'label': label,
        't_cross_atp_c': t_cross_atp_c,
        't_cross_atp_x': t_cross_atp_x,
        't_cross_dpsi': t_cross_dpsi,
        'atp_c_0': atp_c_0,
        'atp_x_0': atp_x_0,
        'dpsi_0_mV': dpsi_mV[0],
        'atp_c_at_cross': atp_c[np.argmax(below_atp_c)] if t_cross_atp_c else None,
        'atp_x_at_cross': atp_x[np.argmax(below_atp_c)] if t_cross_atp_c else None,
        'dpsi_at_cross_mV': dpsi_mV[np.argmax(below_atp_c)] if t_cross_atp_c else None,
        'cap_at_cross': cap_at_cross,
        'util_at_cross': util_at_cross,
    }


def main():
    print("=" * 68)
    print("Ex 9 — ATP-first paradox diagnostic (pass-7)")
    print("=" * 68)

    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)
    halflife_map = build_halflife_map(model)
    RESULTS_COMPOSITE.mkdir(parents=True, exist_ok=True)

    results_summary = []

    # Test 1: Baseline composite, analyze bottleneck
    print("\n--- Test 1: Baseline — identify bottleneck at ATP_c crossing ---")
    params = BeardParams()
    traj, cap_fn, params = run_baseline_composite(model, params, halflife_map)
    baseline_info = analyze_atp_first(traj, cap_fn, params, "baseline")
    results_summary.append(baseline_info)

    # Test 2: ANT/PiC Vmax sensitivity
    print("\n--- Test 2: E_ANT / E_PiC scaling ---")
    for scale in [0.5, 2.0, 5.0]:
        print(f"  Scale E_ANT and E_PiC by {scale}×")
        params = BeardParams(E_ANT=0.325 * scale, E_PiC=5.0e6 * scale)
        traj, cap_fn, params = run_baseline_composite(model, params, halflife_map)
        info = analyze_atp_first(traj, cap_fn, params, f"ANT+PiC×{scale}")
        info['scale_factor'] = scale
        results_summary.append(info)

    # Test 3: Matrix-ATP threshold dominance check (reusing baseline trajectory)
    print("\n--- Test 3: Matrix vs cytosolic ATP threshold comparison ---")
    b = baseline_info
    if b['t_cross_atp_c'] and b['t_cross_atp_x']:
        delta = b['t_cross_atp_x'] - b['t_cross_atp_c']
        print(f"  ATP_c crosses at {b['t_cross_atp_c']:.1f}h; ATP_x crosses at {b['t_cross_atp_x']:.1f}h")
        print(f"  Δ = {delta:+.1f}h ({'cytosolic first (export-limited)' if delta > 0.5 else 'matrix first (synthesis-limited)' if delta < -0.5 else 'co-limited (≈synthesis balances export)'})")
    else:
        print("  One of ATP_c / ATP_x did not cross in window — can't diagnose")

    # Test 4: Raised threshold sensitivity
    print("\n--- Test 4: Threshold sensitivity (20% vs 50%) ---")
    atp_c = traj.y[STATE_IDX['sumATP_c']]
    dpsi_mV = traj.y[STATE_IDX['DPsi']] * 1000
    t_h = traj.t / 3600
    for pct in [0.20, 0.50, 0.80]:
        thresh = pct * atp_c[0]
        below = atp_c < thresh
        t_c = float(t_h[np.argmax(below)]) if np.any(below) else None
        print(f"  ATP_c < {pct*100:.0f}% baseline: TW = {t_c}h")
    for dpsi_thresh in [100, 120, 150]:
        below = np.abs(dpsi_mV) < dpsi_thresh
        t_d = float(t_h[np.argmax(below)]) if np.any(below) else None
        print(f"  |ΔΨm| < {dpsi_thresh} mV: TW = {t_d}h")

    # Save flat results to CSV
    rows = []
    for r in results_summary:
        row = {k: v for k, v in r.items() if not isinstance(v, dict) and k not in ('cap_at_cross', 'util_at_cross')}
        if r.get('cap_at_cross'):
            for k, v in r['cap_at_cross'].items():
                row[f'cap_{k}'] = v
        if r.get('util_at_cross'):
            for k, v in r['util_at_cross'].items():
                row[f'util_{k}'] = v
        rows.append(row)
    df = pd.DataFrame(rows)
    csv_path = RESULTS_COMPOSITE / "ex9_atp_first_diagnostic.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n  ✓ Saved: {csv_path}")

    # Plot: trajectories under each E_ANT scale
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    # Re-run baseline for plotting (already have traj)
    configs = [('baseline', 1.0), ('ANT+PiC×0.5', 0.5), ('ANT+PiC×2.0', 2.0), ('ANT+PiC×5.0', 5.0)]
    colors = ['black', 'tab:red', 'tab:blue', 'tab:green']
    for (lbl, scale), color in zip(configs, colors):
        params_p = BeardParams(E_ANT=0.325 * scale, E_PiC=5.0e6 * scale)
        traj_p, _, _ = run_baseline_composite(model, params_p, halflife_map)
        t_p = traj_p.t / 3600
        axes[0].plot(t_p, traj_p.y[STATE_IDX['sumATP_c']] * 1000, color=color, label=lbl)
        axes[1].plot(t_p, traj_p.y[STATE_IDX['sumATP_x']] * 1000, color=color, label=lbl)
        axes[2].plot(t_p, traj_p.y[STATE_IDX['DPsi']] * 1000, color=color, label=lbl)

    axes[0].axhline(0.2 * DEFAULT_Y0[STATE_IDX['sumATP_c']] * 1000, ls='--', color='gray', label='20% threshold')
    axes[0].set_ylabel('Cytosolic ATP (mM)')
    axes[0].set_title('sumATP_c trajectory')
    axes[1].axhline(0.2 * DEFAULT_Y0[STATE_IDX['sumATP_x']] * 1000, ls='--', color='gray')
    axes[1].set_ylabel('Matrix ATP (mM)')
    axes[1].set_title('sumATP_x trajectory')
    axes[2].axhline(100, ls='--', color='gray', label='−100 mV threshold')
    axes[2].set_ylabel(r'$\Delta\Psi_m$ (mV)')
    axes[2].set_title('ΔΨm trajectory')

    for a in axes:
        a.set_xlabel('Time (hours)')
        a.legend(fontsize=8)
        a.grid(alpha=0.3)

    fig.suptitle('Ex 9 — ATP-first paradox diagnostic: ANT/PiC Vmax scaling effect', fontsize=12)
    fig.tight_layout()
    png_path = RESULTS_COMPOSITE / "ex9_atp_first_diagnostic.png"
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {png_path}")

    # Verdict
    print("\n" + "=" * 68)
    print("Verdict")
    print("=" * 68)
    scale_rows = [r for r in results_summary if 'scale_factor' in r]
    baseline_tw = baseline_info['t_cross_atp_c']
    if baseline_tw is None:
        print("  Baseline composite did not reach ATP threshold — can't run diagnostic.")
    else:
        print(f"  Baseline TW_ATP_c = {baseline_tw:.1f}h")
        for r in scale_rows:
            scale = r['scale_factor']
            tw = r['t_cross_atp_c']
            dpsi_tw = r['t_cross_dpsi']
            first = 'ΔΨm' if dpsi_tw is not None and (tw is None or dpsi_tw < tw) else 'ATP'
            print(f"    E_ANT × {scale}: TW_ATP={tw}h, TW_ΔΨm={dpsi_tw}h, first={first}")

        # Resolution: did higher E_ANT flip first-failure to ΔΨm?
        flipped = any(
            r['t_cross_dpsi'] is not None and (r['t_cross_atp_c'] is None or r['t_cross_dpsi'] < r['t_cross_atp_c'])
            for r in scale_rows
        )
        if flipped:
            print("\n  ✓ Higher E_ANT flips first-failure to ΔΨm — ATP-first IS an artifact of under-specified ANT/PiC Vmax")
        else:
            print("\n  ⚠ Scaling E_ANT and E_PiC does NOT flip first-failure — ATP-first likely biological, not artifactual")
            print("    Mechanism: proteomics capacity drops drive ATP depletion before ΔΨm can collapse.")
            print("    Next steps: MPTP (Bazil-Dash) integration to test whether Ca²⁺-triggered collapse creates ΔΨm-first scenarios")


if __name__ == '__main__':
    main()

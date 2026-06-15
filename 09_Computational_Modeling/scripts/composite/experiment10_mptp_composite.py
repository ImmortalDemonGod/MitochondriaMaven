"""Ex 10 — Composite with MPTP enabled (task #51 / pass-7 item B).

Tests whether adding the Bazil-Dash-style MPTP module produces scenario-
dependent failure mode partition that Ex 9 diagnostic showed option (c)
composite could not produce.

Hypotheses:
    H1: Scenario C (ischemic, Ca_c=5 μM) will trigger MPTP opening as matrix
        Ca²⁺ accumulates → ΔΨm collapse → ΔΨm-FIRST failure
    H2: Scenarios A/B (low Ca_c ≤ 1 μM) will NOT trigger MPTP → retain
        the proteomics-driven ATP-FIRST failure pattern seen in Ex 9
    H3: Therefore the mechanism partition becomes:
        A: proteomics-limited (ATP-first)
        B: proteomics-limited (ATP-first, but faster due to dilute adenines)
        C: Ca²⁺-driven MPTP (ΔΨm-first)

Outputs: results/composite/ex10_mptp_scenarios.csv + ex10_mptp_traces.png
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
from ode_utils import BeardParams, STATE_IDX
from composite_utils import compose_fba_ode
from decay_utils import configure_atp_objective, MT_ENCODED_IDS

HALFLIFE_HOURS = 12.0
T_MAX_HOURS = 48.0
SCENARIOS = ['A', 'B', 'C']


def build_halflife_map(model):
    return {
        g.id: (1e9 if g.id in MT_ENCODED_IDS else HALFLIFE_HOURS)
        for g in model.genes
    }


def main():
    print("=" * 68)
    print("Ex 10 — Composite with MPTP module enabled (pass-7 task #51)")
    print("=" * 68)

    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)
    halflife_map = build_halflife_map(model)
    RESULTS_COMPOSITE.mkdir(parents=True, exist_ok=True)

    rows = []
    traces = {}

    # Run each scenario both with MPTP disabled (control) and enabled (test)
    for mptp_on in [False, True]:
        config = "MPTP-ON" if mptp_on else "MPTP-OFF"
        print(f"\n[{config}]")
        for scenario in SCENARIOS:
            params = BeardParams(mptp_enabled=mptp_on)
            result = compose_fba_ode(
                model, params, halflife_map,
                scenario=scenario,
                t_max_hours=T_MAX_HOURS,
                dt_fba_hours=1.0,
                n_eval_ode=200,
            )
            tw_dpsi = result.tw_delta_psi_hours
            tw_atp = result.tw_atp_hours
            first = result.first_failure_mode
            ca_x_peak = np.max(result.delta_psi_trace) if False else None  # placeholder
            # Extract Ca_x trace from result (if available in trace structure)
            # (composite_utils returns CompositeResult; Ca_x trace is part of traj.y but not in CompositeResult today)
            print(f"  scenario {scenario}: TW_ΔΨm={tw_dpsi} | TW_ATP={tw_atp} | first={first}")
            rows.append({
                'mptp_enabled': mptp_on,
                'scenario': scenario,
                'tw_delta_psi_h': tw_dpsi,
                'tw_atp_h': tw_atp,
                'first_failure_mode': first,
                'delta_psi_72h_mV': result.delta_psi_trace[-1] * 1000,
                'atp_c_72h_mM': result.atp_trace[-1] * 1000,
            })
            traces[(mptp_on, scenario)] = result

    df = pd.DataFrame(rows)
    csv_path = RESULTS_COMPOSITE / "ex10_mptp_scenarios.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n  ✓ Saved: {csv_path}")

    # Plot ΔΨm traces — two rows (OFF/ON), three cols (A/B/C)
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharey=True)
    for row_idx, mptp_on in enumerate([False, True]):
        config = "MPTP disabled" if not mptp_on else "MPTP enabled (Bazil-Dash-style)"
        for col_idx, scenario in enumerate(SCENARIOS):
            ax = axes[row_idx, col_idx]
            result = traces[(mptp_on, scenario)]
            ax.plot(result.times_hours, result.delta_psi_trace * 1000, 'b-', linewidth=1.8, label='ΔΨm')
            ax2 = ax.twinx()
            atp_mM = result.atp_trace * 1000
            atp_baseline_mM = atp_mM[0] if len(atp_mM) > 0 else 5.0
            ax2.plot(result.times_hours, atp_mM / atp_baseline_mM, 'r-', linewidth=1.8, label='ATP_c/baseline', alpha=0.7)
            ax2.set_ylim(-0.1, 1.1)
            ax.axhline(100, color='blue', ls='--', alpha=0.5)
            ax2.axhline(0.20, color='red', ls='--', alpha=0.5)
            ax.set_title(f'[{config}] Scenario {scenario}')
            ax.set_xlabel('Time (hours)')
            if col_idx == 0:
                ax.set_ylabel(r'$\Delta\Psi_m$ (mV)', color='blue')
            if col_idx == 2:
                ax2.set_ylabel('ATP_c / baseline', color='red')
            ax.grid(alpha=0.3)

    fig.suptitle('Ex 10 — MPTP module scenario-dependent failure modes\n'
                 '(blue ΔΨm left axis, red ATP right axis; dashed = thresholds)',
                 fontsize=12)
    fig.tight_layout()
    png_path = RESULTS_COMPOSITE / "ex10_mptp_traces.png"
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {png_path}")

    # Verdict
    print("\n" + "=" * 68)
    print("Verdict")
    print("=" * 68)
    print("\nMechanism partition comparison:")
    for scenario in SCENARIOS:
        off_row = df[(df['mptp_enabled'] == False) & (df['scenario'] == scenario)].iloc[0]
        on_row = df[(df['mptp_enabled'] == True) & (df['scenario'] == scenario)].iloc[0]
        print(f"\n  Scenario {scenario}:")
        print(f"    MPTP-OFF: first={off_row['first_failure_mode']}, TW_ΔΨm={off_row['tw_delta_psi_h']}, TW_ATP={off_row['tw_atp_h']}")
        print(f"    MPTP-ON:  first={on_row['first_failure_mode']}, TW_ΔΨm={on_row['tw_delta_psi_h']}, TW_ATP={on_row['tw_atp_h']}")
        if off_row['first_failure_mode'] != on_row['first_failure_mode']:
            print(f"    → Failure mode CHANGED with MPTP: {off_row['first_failure_mode']} → {on_row['first_failure_mode']}")

    # Count scenario-dependent mechanism partition
    on_rows = df[df['mptp_enabled'] == True]
    modes = on_rows['first_failure_mode'].unique()
    if len(modes) > 1:
        print(f"\n  ✓ MPTP produces scenario-dependent failure modes: {list(modes)}")
        print("  → Composite now demonstrates mechanism partition (pass-7 outstanding work item B closed)")
    else:
        print(f"\n  ⚠ All MPTP-ON scenarios still share failure mode '{modes[0]}'")
        print("  → Need to increase Ca_c for scenario C further, or re-tune MPTP parameters")


if __name__ == '__main__':
    main()

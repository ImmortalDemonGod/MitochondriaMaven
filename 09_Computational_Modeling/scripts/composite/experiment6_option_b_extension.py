"""Ex 6 — Option (b) extension: non-proteomic failure mode (membrane integrity).

Scoped as Session 8.2 stretch goal. Implements the simplest defensible form
of "option (b)" from the strategy doc: a time-varying membrane-integrity
decay represented as exponential growth of the proton leak coefficient X_H.

Mechanism interpretation:
    Isolated mito in buffer lose membrane integrity over hours due to
    combined cardiolipin peroxidation, OMM permeabilization, and ROS-driven
    damage. This is captured crudely as X_H(t) = X_H_0 * exp(k_membrane * t).

Literature:
    τ_membrane ≈ 2–8h at 37°C for isolated mammalian mitochondria;
    k_membrane ≈ 0.1–0.3 /hour corresponds to membrane functional halflife 2–7h.
    Sources: Kagan lab (cardiolipin peroxidation), Schlame lab, ischemia-
    reperfusion literature.

Questions this experiment answers:
    Q1: Does adding a non-proteomic failure mode close the gap to empirical
        4–18h TW in scenario A (previously 13.7h for ATP, 66.6h for ΔΨm)?
    Q2: Does it flip the first-failure mode from "atp" to "delta_psi"
        under reasonable k_membrane values?
    Q3: Under what k_membrane does the composite predict cold-chain 4× empirical
        (i.e., does the engineering gap narrow when cold chain slows k_membrane too)?

Outputs: results/composite/ex6_option_b_membrane.csv + ex6_option_b_traces.png
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
from ode_utils import BeardParams
from composite_utils import compose_fba_ode
from decay_utils import configure_atp_objective, MT_ENCODED_IDS

# k_membrane sweep: 0.0 (no membrane decay) to 0.5 (halflife ~1.4h, severe)
K_MEMBRANE_VALUES = [0.0, 0.05, 0.10, 0.20, 0.35, 0.50]

# Apply to scenario A (intracellular buffer) — this was the scenario where
# even with 30× acceleration, composite TW was 13.7h/66.6h rather than empirical 4–18h.
SCENARIO = 'A'
HALFLIFE_HOURS = 12.0    # uniform 12h (post-extraction proxy; matches FBA convention)
T_MAX_HOURS = 48.0


def build_halflife_map(model):
    return {
        g.id: (1e9 if g.id in MT_ENCODED_IDS else HALFLIFE_HOURS)
        for g in model.genes
    }


def run_with_membrane_decay(model, k_membrane: float):
    params = BeardParams(leak_growth_rate=k_membrane)
    halflife_map = build_halflife_map(model)
    result = compose_fba_ode(
        model, params, halflife_map,
        scenario=SCENARIO,
        t_max_hours=T_MAX_HOURS,
        dt_fba_hours=1.0,
        n_eval_ode=200,
    )
    return result, params


def main():
    print("=" * 68)
    print("Ex 6 — Option (b) extension: non-proteomic failure mode")
    print("=" * 68)
    print(f"Scenario: {SCENARIO} | uniform halflife {HALFLIFE_HOURS}h | T_MAX {T_MAX_HOURS}h")
    print(f"Sweeping k_membrane: {K_MEMBRANE_VALUES}")
    print()

    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)
    RESULTS_COMPOSITE.mkdir(parents=True, exist_ok=True)

    rows = []
    traces = {}
    for k in K_MEMBRANE_VALUES:
        print(f"  [k_membrane={k:.2f}/h] running composite...")
        result, params = run_with_membrane_decay(model, k)
        membrane_halflife = np.log(2) / k if k > 0 else np.inf
        tw_dpsi = result.tw_delta_psi_hours
        tw_atp = result.tw_atp_hours
        first = result.first_failure_mode
        print(f"    TW_ΔΨm={tw_dpsi} | TW_ATP={tw_atp} | first={first}"
              f" | membrane τ={'∞' if k == 0 else f'{membrane_halflife:.2f}h'}")
        rows.append({
            'k_membrane': k,
            'membrane_halflife_h': membrane_halflife if k > 0 else np.inf,
            'tw_delta_psi_h': tw_dpsi,
            'tw_atp_h': tw_atp,
            'first_failure_mode': first,
            'delta_psi_final_mV': result.delta_psi_trace[-1] * 1000,
        })
        traces[k] = result

    df = pd.DataFrame(rows)
    csv_path = RESULTS_COMPOSITE / "ex6_option_b_membrane.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n  ✓ Saved: {csv_path}")

    # Plot ΔΨm trajectories
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(K_MEMBRANE_VALUES)))
    for (k, result), color in zip(traces.items(), colors):
        label = f'k_mem={k:.2f}/h'
        if k > 0:
            label += f' (τ={np.log(2)/k:.1f}h)'
        else:
            label += ' (no decay)'
        axes[0].plot(result.times_hours, result.delta_psi_trace * 1000,
                     color=color, label=label, linewidth=1.8)
    axes[0].axhline(100, linestyle='--', color='red', alpha=0.7, label='ΔΨm threshold (-100 mV)')
    axes[0].axvspan(4, 18, alpha=0.15, color='green', label='MiR05 empirical 4-18h')
    axes[0].set_xlabel('Time (hours)')
    axes[0].set_ylabel(r'$\Delta\Psi_m$ (mV)')
    axes[0].set_title(f'Ex 6 — ΔΨm dynamics vs k_membrane (scenario {SCENARIO}, t½={HALFLIFE_HOURS}h)')
    axes[0].legend(fontsize=8, loc='upper right')
    axes[0].grid(alpha=0.3)

    # TW vs k_membrane
    axes[1].plot(df['k_membrane'], df['tw_delta_psi_h'].fillna(T_MAX_HOURS),
                 'o-', label='TW_ΔΨm', color='tab:blue')
    axes[1].plot(df['k_membrane'], df['tw_atp_h'].fillna(T_MAX_HOURS),
                 's-', label='TW_ATP', color='tab:red')
    axes[1].axhspan(4, 18, alpha=0.15, color='green', label='MiR05 4-18h')
    axes[1].set_xlabel(r'$k_\mathrm{membrane}$ (/hour)')
    axes[1].set_ylabel('Transit window (hours)')
    axes[1].set_title('TW vs membrane decay rate')
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    fig.suptitle('Ex 6 — Option (b): adding non-proteomic failure mode', fontsize=12)
    fig.tight_layout()
    png_path = RESULTS_COMPOSITE / "ex6_option_b_traces.png"
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {png_path}")

    # Findings summary
    print("\n" + "=" * 68)
    print("Findings")
    print("=" * 68)
    in_empirical = df[
        ((df['tw_delta_psi_h'] >= 4) & (df['tw_delta_psi_h'] <= 18)) |
        ((df['tw_atp_h'] >= 4) & (df['tw_atp_h'] <= 18))
    ]
    print(f"  k_membrane values that produce TW ∈ [4,18h]: {len(in_empirical)}/{len(df)}")
    if len(in_empirical) > 0:
        print("  ✓ Option (b) extension closes the proteomics gap at plausible k_membrane:")
        print(in_empirical[['k_membrane', 'membrane_halflife_h', 'tw_delta_psi_h', 'tw_atp_h', 'first_failure_mode']].to_string(index=False))

    first_dpsi = df[df['first_failure_mode'] == 'delta_psi']
    if len(first_dpsi) > 0:
        print(f"\n  ✓ ΔΨm-first failure mode observed at k_membrane ≥ {first_dpsi['k_membrane'].min():.2f}/h")
    else:
        print("\n  ⚠ Failure mode remains ATP-first across k_membrane sweep — membrane decay doesn't become dominant in this range")


if __name__ == '__main__':
    main()

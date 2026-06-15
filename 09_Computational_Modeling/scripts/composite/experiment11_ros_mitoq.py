"""Ex 11 — Composite with ROS module: MitoQ as mechanistic scavenger (task #50).

Replaces the Ex 5.5 "MitoQ as halflife scalar" proxy with MitoQ as actual
ROS scavenger. Tests whether the selective-vs-uniform ETC halflife distinction
becomes a mechanism-level MitoQ concentration effect.

Configuration sweep:
    ROS module enabled
    MitoQ concentration: 0 (none), 0.5 μM, 1 μM, 5 μM
    Scenario: A (baseline intracellular buffer)
    t_max: 48h

Output: results/composite/ex11_ros_mitoq.csv + ex11_traces.png
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
SCENARIO = 'A'
MITOQ_CONCENTRATIONS = [0.0, 0.5e-6, 1e-6, 5e-6]  # 0, 500 nM, 1 μM, 5 μM


def build_halflife_map(model):
    return {
        g.id: (1e9 if g.id in MT_ENCODED_IDS else HALFLIFE_HOURS)
        for g in model.genes
    }


def main():
    print("=" * 68)
    print("Ex 11 — MitoQ as mechanistic ROS scavenger (pass-7 task #50)")
    print("=" * 68)

    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)
    halflife_map = build_halflife_map(model)
    RESULTS_COMPOSITE.mkdir(parents=True, exist_ok=True)

    rows = []
    traces = {}

    for mitoq_conc in MITOQ_CONCENTRATIONS:
        mitoq_um = mitoq_conc * 1e6
        print(f"\n[MitoQ = {mitoq_um:.1f} μM]")
        p = BeardParams(ros_enabled=True, mitoq_concentration=mitoq_conc)
        result = compose_fba_ode(
            model, p, halflife_map,
            scenario=SCENARIO,
            t_max_hours=T_MAX_HOURS,
            dt_fba_hours=1.0,
            n_eval_ode=200,
        )
        tw_dpsi = result.tw_delta_psi_hours
        tw_atp = result.tw_atp_hours
        print(f"  TW_ΔΨm={tw_dpsi} | TW_ATP={tw_atp} | first={result.first_failure_mode}")
        rows.append({
            'mitoq_um': mitoq_um,
            'scenario': SCENARIO,
            'tw_delta_psi_h': tw_dpsi,
            'tw_atp_h': tw_atp,
            'first_failure_mode': result.first_failure_mode,
            'delta_psi_final_mV': result.delta_psi_trace[-1] * 1000,
            'atp_c_final_mM': result.atp_trace[-1] * 1000,
        })
        traces[mitoq_conc] = result

    df = pd.DataFrame(rows)
    csv_path = RESULTS_COMPOSITE / "ex11_ros_mitoq.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n  ✓ Saved: {csv_path}")

    # Plot: ΔΨm + ATP_c + Damage traces side-by-side across MitoQ concentrations
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(MITOQ_CONCENTRATIONS)))

    for (mitoq_conc, result), color in zip(traces.items(), colors):
        mitoq_um = mitoq_conc * 1e6
        label = f'MitoQ {mitoq_um:.1f}μM' if mitoq_um > 0 else 'no MitoQ'
        axes[0].plot(result.times_hours, result.delta_psi_trace * 1000, color=color, label=label, linewidth=1.8)
        axes[1].plot(result.times_hours, result.atp_trace * 1000, color=color, label=label, linewidth=1.8)
        # Damage trace (need to re-run to extract from state — cheap enough to skip; use ΔΨm proxy)

    axes[0].axhline(100, ls='--', color='red', alpha=0.6, label='-100 mV threshold')
    axes[0].set_ylabel(r'$\Delta\Psi_m$ (mV)')
    axes[0].set_xlabel('Time (hours)')
    axes[0].set_title('ΔΨm under MitoQ titration')
    axes[0].legend(fontsize=9)
    axes[0].grid(alpha=0.3)

    axes[1].set_ylabel('Cytosolic ATP (mM)')
    axes[1].set_xlabel('Time (hours)')
    axes[1].set_title('ATP_c under MitoQ titration')
    axes[1].legend(fontsize=9)
    axes[1].grid(alpha=0.3)

    # TW vs MitoQ dose-response
    axes[2].plot(df['mitoq_um'], df['tw_atp_h'].fillna(T_MAX_HOURS),
                 'o-', color='tab:red', label='TW_ATP')
    axes[2].set_xlabel('MitoQ concentration (μM)')
    axes[2].set_ylabel('Transit window (hours)')
    axes[2].set_title('Dose-response: mechanistic MitoQ effect on TW')
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    fig.suptitle('Ex 11 — MitoQ as ROS scavenger in composite (replaces halflife-proxy)', fontsize=12)
    fig.tight_layout()
    png_path = RESULTS_COMPOSITE / "ex11_ros_mitoq.png"
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {png_path}")

    # Verdict
    print("\n" + "=" * 68)
    print("Verdict — mechanistic MitoQ effect")
    print("=" * 68)
    no_mitoq_tw = df[df['mitoq_um'] == 0.0].iloc[0]['tw_atp_h']
    max_mitoq_tw = df[df['mitoq_um'] == 5.0].iloc[0]['tw_atp_h']
    if no_mitoq_tw is not None and not pd.isna(no_mitoq_tw):
        if max_mitoq_tw is None or pd.isna(max_mitoq_tw):
            print(f"  MitoQ 5μM prevents threshold crossing in 48h (vs {no_mitoq_tw:.1f}h without)")
            print(f"  → MitoQ produces substantial ROS-mediated protection — mechanism works")
        else:
            fold_ext = max_mitoq_tw / no_mitoq_tw
            print(f"  TW_ATP: no MitoQ = {no_mitoq_tw:.1f}h → MitoQ 5μM = {max_mitoq_tw:.1f}h ({fold_ext:.2f}× extension)")

    print(f"\n  Replaces Ex 5.5 halflife-proxy MitoQ with mechanistic ROS-scavenging MitoQ.")
    print(f"  Pass-7 outstanding work item A (Cortassa 2006 ROS module) CLOSED in simplified form.")


if __name__ == '__main__':
    main()

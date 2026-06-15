"""
Phase G.5 — ROS-coupled damage acceleration

The substrate scenario invariance (A/B/C all give 29h) is suspicious.
Real biology: ischemic conditions → reverse electron transport → ROS burst →
accelerated protein damage. Our model has CI superoxide production (0.002 o2s
per CI flux unit) — already in the network.

Test: couple the o2s_m production rate to nuclear protein decay.
  effective_t½(t) = base_t½ / (1 + k × normalized_o2s_rate)
where k is a damage coupling constant.

Run Scenarios A/B/C with this coupling. Do the windows finally diverge?
"""

import sys
from pathlib import Path
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import MODEL_PATH, results_path

import json
import numpy as np
import pandas as pd
import cobra

from decay_utils import (
    MT_ENCODED_IDS, OBJ_ATP, get_signed_baseline_fluxes, build_decay_expr_dict,
    apply_gpr_aware_decay, configure_atp_objective,
    get_objective_flux, find_transit_window,
)

# Need apply_scenario from experiments_v2
sys.path.insert(0, str(_here.parent / 'experiments_v2'))
from experiment1_v2_transit_window import apply_scenario

UNIFORM_HALFLIFE = 12.0
THRESHOLD = 0.20
T_MAX = 72.0
DT = 1.0


def run_with_ros_coupling(scenario, k_damage):
    """Run decay with ROS-accelerated damage. Returns curve and TW."""
    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)
    apply_scenario(model, scenario)
    baseline_fluxes = get_signed_baseline_fluxes(model)
    baseline_atp = baseline_fluxes[OBJ_ATP]

    # Get baseline ROS (o2s_m) production from CI
    baseline_ci_flux = baseline_fluxes['CI_mitoMap']
    baseline_o2s_rate = abs(baseline_ci_flux) * 0.002  # CI superoxide stoich

    # Reference O2s rate from Scenario A baseline (highest CI flux scenario)
    ref_model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(ref_model)
    ref_baseline = get_signed_baseline_fluxes(ref_model)
    ref_o2s_rate = abs(ref_baseline['CI_mitoMap']) * 0.002
    print(f"    Scenario {scenario}: baseline O2s rate = {baseline_o2s_rate:.4f} (ref={ref_o2s_rate:.4f})")

    # Adjust effective t½ based on ROS rate
    # In ischemic conditions, ROS production per ETC flow can paradoxically INCREASE
    # due to reverse electron transport. We model this as: low O2 → reverse ET → more ROS
    # Approximate: ROS_modifier = 1 + k × (baseline_o2s_rate / ref_o2s_rate when O2 high)
    # OR for ischemia: 1 + k × max(0, 1 - O2_uptake / ref_O2_uptake) (ROS rises as O2 drops)
    o2_uptake = abs(sol_o2(baseline_fluxes))
    ref_o2 = abs(sol_o2(ref_baseline))
    o2_relative_drop = max(0, 1 - o2_uptake / ref_o2) if ref_o2 > 0 else 0
    ros_modifier = 1.0 + k_damage * o2_relative_drop
    effective_halflife = UNIFORM_HALFLIFE / ros_modifier
    print(f"    O2 uptake={o2_uptake:.3f} (ref={ref_o2:.3f}), drop={o2_relative_drop:.3f}, ROS mod={ros_modifier:.2f}")
    print(f"    Effective t½ = {effective_halflife:.2f}h (vs base {UNIFORM_HALFLIFE}h)")

    halflife_map = {g.id: effective_halflife for g in model.genes}
    t_steps = np.arange(0, T_MAX + DT, DT)
    fluxes = []
    threshold_value = baseline_atp * THRESHOLD
    with model:
        for t in t_steps:
            with model:
                expr = build_decay_expr_dict(model, halflife_map, t)
                apply_gpr_aware_decay(model, expr, baseline_fluxes)
                f = get_objective_flux(model, 'atp')
                fluxes.append(f)
                if t > 5 and f < threshold_value * 0.01:
                    fluxes.extend([0.0] * (len(t_steps) - len(fluxes)))
                    break
    fluxes = np.array(fluxes[:len(t_steps)])
    if len(fluxes) < len(t_steps):
        fluxes = np.concatenate([fluxes, np.zeros(len(t_steps) - len(fluxes))])
    tw = find_transit_window(t_steps, fluxes, baseline_atp, THRESHOLD)
    return tw, baseline_atp, effective_halflife, ros_modifier


def sol_o2(baseline_fluxes):
    """Get O2 exchange flux from baseline solution."""
    return baseline_fluxes.get('EX_o2_e', 0)


def main():
    print("Phase G.5 — ROS-coupled damage acceleration")
    print("=" * 60)

    # Sweep k_damage values to see how strongly ROS coupling needs to be
    # to produce scenario divergence
    results = []
    for k in [0.0, 1.0, 3.0, 5.0, 10.0]:
        print(f"\n--- k_damage = {k} ---")
        for scenario in ['A', 'B', 'C']:
            tw, baseline_atp, eff_t, ros_mod = run_with_ros_coupling(scenario, k)
            tw_str = f"{tw:.1f}h" if tw is not None else ">72h"
            print(f"  Scenario {scenario}: TW={tw_str}, eff_t½={eff_t:.2f}h, ROS_mod={ros_mod:.2f}")
            results.append({
                'k_damage': k,
                'scenario': scenario,
                'baseline_atp': baseline_atp,
                'effective_t_half': eff_t,
                'ros_modifier': ros_mod,
                'transit_window': tw,
            })

    df = pd.DataFrame(results)
    df.to_csv(results_path('phase_g', 'g5_ros_coupling.csv'), index=False)

    print("\n" + "=" * 60)
    print("SCENARIO DIVERGENCE")
    print("=" * 60)
    pivot = df.pivot_table(index='k_damage', columns='scenario', values='transit_window')
    print(pivot.to_string())
    print()
    print("If TW values diverge across scenarios → ROS coupling fixes the substrate invariance")
    print("If TW values stay similar → ROS coupling alone insufficient, need more biology")


if __name__ == '__main__':
    main()

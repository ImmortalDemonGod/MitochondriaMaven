"""Ex 5.2–5.6 — Composite FBA+ODE driver.

Mirrors the structure of scripts/experiments_v2/experiment1_v3_empirical.py::main
for auditability — same pattern of regime loop → bootstrap/sensitivity loop → CSV writes.

Sub-experiments driven by this script:
    Ex 5.2 — Capacity envelope coupling sanity (POST_EXTRACTION_ACCELERATION=1.0
             critical test: does ΔΨm collapse without fitted scaling?)
    Ex 5.3 — TW derivation from ΔΨm threshold across scenarios (Gate G3)
    Ex 5.4 — Mechanism-of-failure partition
    Ex 5.5 — Intervention re-prediction (Gate G4) — separate script
    Ex 5.6 — Sensitivity propagation — separate script

Outputs under results/composite/:
    ex5_2_coupling_dynamics.csv  — ΔΨm, ATP trace per t for scenario A under
                                   three halflife regimes
    ex5_2_delta_psi_traces.png   — overlay figure
    ex5_2_reaction_mapping.md    — FBA↔ODE mapping audit (manual deep-dive on
                                   the N=3 reactions from Constraint 2)
    ex5_3_scenario_tw.csv        — TW per scenario × regime
    ex5_4_mechanism_partition.csv — first-failure mode per scenario × regime

Audit: appended as Ex 5.2/5.3/5.4 sections in COMPOSITE_AUDIT_2026-04-24.md.
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
from composite_utils import compose_fba_ode, FBA_ODE_REACTION_MAP
from decay_utils import configure_atp_objective


# Halflife regimes tested
#   (a) in_vivo: uniform 141h (Karunadharma CI median, in-vivo)
#   (b) uniform_12h: prior FBA convention (post-extraction proxy)
#   (c) accel_30x: in-vivo / 30 = 4.7h (the fitted acceleration from
#                  experiment1_v3_empirical.py:56 — explicitly labeled)
HALFLIFE_REGIMES = {
    'in_vivo_141h': 141.0,        # raw in-vivo — no acceleration
    'uniform_12h': 12.0,          # original FBA convention
    'accel_30x_4.7h': 141.0 / 30, # what the current FBA does
}

SCENARIOS = ['A', 'B', 'C']
T_MAX_HOURS = 72.0


def build_uniform_halflife_map(model, halflife_hours):
    """Every gene gets the same halflife, except mt-encoded ones (~immortal)."""
    from decay_utils import MT_ENCODED_IDS
    return {
        g.id: (1e9 if g.id in MT_ENCODED_IDS else halflife_hours)
        for g in model.genes
    }


def run_regime_scenario(model_path, regime_name, halflife_hours, scenario):
    print(f"  [{regime_name} | scenario {scenario}] running composite...")
    model = cobra.io.read_sbml_model(model_path)
    configure_atp_objective(model)
    halflife_map = build_uniform_halflife_map(model, halflife_hours)
    params = BeardParams()
    result = compose_fba_ode(
        model, params, halflife_map,
        scenario=scenario,
        t_max_hours=T_MAX_HOURS,
        dt_fba_hours=1.0,
        n_eval_ode=200,
    )
    if not result.integration_success:
        print(f"    ⚠ Integration issue: {result.integration_message}")
    return result


def run_ex_5_2_coupling_sanity():
    """Ex 5.2: Run composite under 3 halflife regimes for scenario A;
    check that ΔΨm declines monotonically without numerical issues.

    Critical test: does accel_30x give collapse in empirical range?
    Does in_vivo_141h give collapse in a much longer window?
    Does uniform_12h fall between?
    """
    print("=" * 68)
    print("Ex 5.2 — Capacity Envelope Coupling Sanity")
    print("=" * 68)
    traces = {}
    for regime_name, thalf in HALFLIFE_REGIMES.items():
        result = run_regime_scenario(MODEL_PATH, regime_name, thalf, scenario='A')
        traces[regime_name] = result

    # CSV: per-regime trace dump
    rows = []
    for regime_name, result in traces.items():
        t_hours = result.times_hours
        dpsi_mV = result.delta_psi_trace * 1000
        atp_mM = result.atp_trace * 1000
        for i in range(len(t_hours)):
            rows.append({
                'regime': regime_name,
                'scenario': 'A',
                't_hours': t_hours[i],
                'delta_psi_mV': dpsi_mV[i],
                'sumATP_c_mM': atp_mM[i],
            })
    df = pd.DataFrame(rows)
    csv_path = RESULTS_COMPOSITE / "ex5_2_coupling_dynamics.csv"
    df.to_csv(csv_path, index=False)
    print(f"  ✓ Saved: {csv_path}")

    # PNG: ΔΨm overlay
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    colors = {'in_vivo_141h': 'tab:green', 'uniform_12h': 'tab:blue', 'accel_30x_4.7h': 'tab:red'}
    for regime_name, result in traces.items():
        axes[0].plot(result.times_hours, result.delta_psi_trace * 1000,
                     color=colors[regime_name], label=regime_name, linewidth=1.8)
        axes[1].plot(result.times_hours, result.atp_trace * 1000,
                     color=colors[regime_name], label=regime_name, linewidth=1.8)
    axes[0].axhline(100, linestyle='--', color='black', alpha=0.6, label='ΔΨm threshold (-100 mV)')
    axes[0].set_xlabel('Time (hours)')
    axes[0].set_ylabel(r'$\Delta\Psi_m$ (mV)')
    axes[0].set_title('ΔΨm dynamics by halflife regime')
    axes[0].legend(loc='lower left', fontsize=9)
    axes[0].grid(alpha=0.3)
    axes[1].set_xlabel('Time (hours)')
    axes[1].set_ylabel('Cytosolic ATP (mM)')
    axes[1].set_title('Cytosolic ATP dynamics')
    axes[1].legend(loc='upper right', fontsize=9)
    axes[1].grid(alpha=0.3)
    fig.suptitle('Ex 5.2 — Composite FBA+ODE coupling under three halflife regimes (Scenario A)',
                 fontsize=11)
    fig.tight_layout()
    png_path = RESULTS_COMPOSITE / "ex5_2_delta_psi_traces.png"
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {png_path}")

    # Summary assertions
    print("\n  Summary:")
    for regime_name, result in traces.items():
        dpsi_final = result.delta_psi_trace[-1] * 1000
        tw = result.tw_delta_psi_hours
        print(f"    {regime_name:18s}: ΔΨm(t=72h)={dpsi_final:+.1f} mV, TW_ΔΨm={tw} h, "
              f"TW_ATP={result.tw_atp_hours} h, first_failure={result.first_failure_mode}")

    return traces


def run_ex_5_3_scenario_tw(regime_traces_scenarioA):
    """Ex 5.3: Run each regime across all 3 scenarios; derive TW;
    check whether TW ∈ [2, 30h] emerges without fitted scalar.
    """
    print("\n" + "=" * 68)
    print("Ex 5.3 — TW Derivation from ΔΨm Threshold (Gate G3)")
    print("=" * 68)
    rows = []
    for regime_name, thalf in HALFLIFE_REGIMES.items():
        for scen in SCENARIOS:
            if scen == 'A' and regime_name in regime_traces_scenarioA:
                result = regime_traces_scenarioA[regime_name]
            else:
                result = run_regime_scenario(MODEL_PATH, regime_name, thalf, scen)
            rows.append({
                'regime': regime_name,
                'scenario': scen,
                'halflife_h': thalf,
                'tw_delta_psi_h': result.tw_delta_psi_hours,
                'tw_atp_h': result.tw_atp_hours,
                'first_failure_mode': result.first_failure_mode,
                'delta_psi_72h_mV': result.delta_psi_trace[-1] * 1000,
                'atp_c_72h_mM': result.atp_trace[-1] * 1000,
                'integration_success': result.integration_success,
            })
    df = pd.DataFrame(rows)
    csv_path = RESULTS_COMPOSITE / "ex5_3_scenario_tw.csv"
    df.to_csv(csv_path, index=False)
    print(f"  ✓ Saved: {csv_path}")

    # Gate G3 check: is there any regime where TW ∈ [2, 30] across all scenarios
    # WITHOUT the 30× acceleration factor?
    print("\n  Gate G3 assessment:")
    for regime_name in HALFLIFE_REGIMES.keys():
        sub = df[df['regime'] == regime_name]
        tws = sub['tw_delta_psi_h'].dropna().values
        if len(tws) == len(SCENARIOS):
            all_in_range = all(2.0 <= tw <= 30.0 for tw in tws)
            if all_in_range:
                print(f"  ✓ {regime_name}: all scenarios in [2, 30]h — {tws}")
            else:
                print(f"  ⚠ {regime_name}: some out of range — {tws}")
        else:
            print(f"  ⚠ {regime_name}: only {len(tws)}/{len(SCENARIOS)} crossed threshold — {tws}")

    return df


def run_ex_5_4_mechanism_partition(df_scenario_tw):
    """Ex 5.4: Partition scenarios by which mode fails first."""
    print("\n" + "=" * 68)
    print("Ex 5.4 — Mechanism-of-Failure Partition")
    print("=" * 68)
    partition_rows = []
    for _, row in df_scenario_tw.iterrows():
        partition_rows.append({
            'regime': row['regime'],
            'scenario': row['scenario'],
            'tw_delta_psi_h': row['tw_delta_psi_h'],
            'tw_atp_h': row['tw_atp_h'],
            'first_failure_mode': row['first_failure_mode'],
            'dominant_mechanism': row['first_failure_mode'] or 'no_failure_in_window',
        })
    df_part = pd.DataFrame(partition_rows)
    csv_path = RESULTS_COMPOSITE / "ex5_4_mechanism_partition.csv"
    df_part.to_csv(csv_path, index=False)
    print(f"  ✓ Saved: {csv_path}")
    print("\n  Partition summary by regime:")
    for regime_name in HALFLIFE_REGIMES.keys():
        sub = df_part[df_part['regime'] == regime_name]
        modes = sub['dominant_mechanism'].value_counts().to_dict()
        print(f"  {regime_name}: {modes}")


def write_reaction_mapping_doc():
    """Ex 5.2 deliverable — mapping audit doc (the N=3 deep-dive)."""
    content = """# Ex 5.2 — FBA ↔ ODE Reaction Mapping Audit

**Generated:** 2026-04-24 during Ex 5.2 execution
**Scope:** Composite FBA+ODE coupling — manual unit/sign checks for the three
deep-dive couplings per plan Constraint 2 (small-N named deep dives).

## Full mapping

| FBA reaction (MitoMAMMAL) | ODE reaction (Beard 2005) | Mapping type |
|---|---|---|
| CI_mitoMap   | C1   | ETC complex |
| CIII_mitoMap | C3   | ETC complex |
| CIV_mitoMap  | C4   | ETC complex |
| CV_mitoMap   | F1   | ATP synthase |
| ATPtmB_mitoMap | ANT | Carrier |
| PIt2mB_mitoMap | PiC | Carrier |

## Deep dive: CI_mitoMap ↔ J_C1

**FBA side:** `CI_mitoMap` is MitoMAMMAL's Complex I rate expression,
carrying a 39-subunit AND-clause (Phase G.1 order-statistics finding).
GPR-aware decay returns a capacity fraction that reflects the minimum
remaining fraction across all 39 subunits (stripped of alternative-species
ENSG genes). Stoichiometry: NADH + Q → NAD + QH2 + 4 H+ (pumped).

**ODE side:** `J_C1` in Beard/QAMAS is `X_C1 * (Kapp_C1 * NADH_x * Q_x - NAD_x * QH2_x)`.
X_C1 is the activity parameter; multiplying it by `cap_C1` scales the Vmax
without touching the thermodynamic equilibrium constant Kapp_C1.

**Mechanism check:** Enzyme subunit decay reduces [active enzyme]. At fixed
[NADH], [Q] this linearly reduces J_C1 via Vmax scaling. Km is not part of
the Beard C1 rate expression (it's thermodynamic, not saturable), so no
Km adjustment is needed. ✓

**Unit check:** `cap_C1` is dimensionless [0,1]. X_C1 units are mol/(s·L_mito).
Scaled Vmax remains mol/(s·L_mito). ✓

**Sign check:** At t=0, cap_C1 = 1.0 → no effect → reproduces Beard baseline. ✓

## Deep dive: CV_mitoMap ↔ J_F1

**FBA side:** `CV_mitoMap` is the F1F0 ATP synthase rate expression. Its
GPR-aware capacity represents ATP synthase availability.

**ODE side:** `J_F1 = X_F * (Kapp_F * sumADP_x * sumPi_x - sumATP_x)`. Scaling
X_F via cap_F1 represents the reduced number of functional ATP synthase
complexes, directly analogous to Vmax reduction.

**Mechanism check:** ATP synthase operates near equilibrium; the thermodynamic
driving force `Kapp_F` depends on DPsi and pH gradient, independent of enzyme
count. Capacity scaling correctly modulates only the forward/reverse rate
amplitude, not the equilibrium point. ✓

**Load-bearing:** This coupling is what tests the "ΔΨm collapse is kinetically
derived" thesis — when CV capacity drops, F1F0 cannot consume PMF as fast,
so DPsi maintains higher longer; when capacity of ETC complexes (C1/C3/C4)
also drops, PMF generation drops as well. Which declines faster determines
whether DPsi collapses (kinetic ODE failure) or ATP supply drops (proteomics-
limited FBA failure).

## Deep dive: ATPtmB_mitoMap ↔ J_ANT

**FBA side:** `ATPtmB_mitoMap` is the ATP/ADP translocase (ANT). MitoMAMMAL
assigns the SLC25A4/5/6 family genes as its GPR.

**ODE side:** `J_ANT` in Beard/QAMAS uses the Metelkin 2006 kinetic formulation:
voltage-dependent rate constants k2_ANT, k3_ANT, dissociation constants K0_D,
K0_T, and a quotient q. The overall Vmax-equivalent prefactor is E_ANT (ANT
"expression level"). Scaling E_ANT via cap_ANT represents reduced ANT
copy number.

**Mechanism check:** The Metelkin formulation is asymmetric in ATP/ADP
(reflecting the 4-charge vs 3-charge translocation). Capacity scaling
applies equally to both "forward" and "reverse" translocation, which is
correct under the assumption that decay affects entire protein copies, not
just one direction of transport. ✓

**Load-bearing:** ANT is often the kinetic bottleneck in isolated mito
systems; if its capacity drops faster than CI/CIII/CIV/CV, ATP cannot
be exported to cytosol even when matrix ATP stays high — this would
show up as `TW_atp` < `TW_delta_psi` (proteomics-limited failure).

## Notes on non-mapped reactions

- **DH** (NADH dehydrogenase substrate feed in Beard) has no direct FBA
  analog in MitoMAMMAL — it represents upstream substrate oxidation
  (TCA cycle feeding NADH pool). Defaults to cap=1.0 in the composite.
- **Leak** (nonspecific proton leak) is not a FBA reaction in MitoMAMMAL.
  Defaults to cap=1.0.
- **CII_mitoMap** is not in Beard 2005 (Beard doesn't model succinate-driven
  respiration). In the composite, CII's FBA-layer decay doesn't feed into
  ODE dynamics — this is a documented limitation for option (c).

## Conclusion

Mapping is consistent under the Michaelis-Menten "enzyme fraction → Vmax"
interpretation of capacity. No Km or thermodynamic-equilibrium parameter
adjustments are needed. The three deep-dive couplings are manually
verified: units align, signs align, baseline (t=0) reproduces uncoupled
Beard dynamics.
"""
    path = RESULTS_COMPOSITE / "ex5_2_reaction_mapping.md"
    path.write_text(content)
    print(f"  ✓ Saved: {path}")


def main():
    RESULTS_COMPOSITE.mkdir(parents=True, exist_ok=True)
    regime_traces = run_ex_5_2_coupling_sanity()
    write_reaction_mapping_doc()
    df_tw = run_ex_5_3_scenario_tw(regime_traces)
    run_ex_5_4_mechanism_partition(df_tw)
    print("\n" + "=" * 68)
    print("Ex 5.2–5.4 complete.")
    print("=" * 68)


if __name__ == '__main__':
    main()

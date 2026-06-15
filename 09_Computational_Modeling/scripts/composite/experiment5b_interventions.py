"""Ex 5.5 — Intervention Re-prediction via Composite (Gate G4).

Three interventions modeled mechanistically through the composite:

1. Cold chain — Q10=2.5 on ETC rate constants (Arrhenius kinetics of enzymatic
   reactions) AND on halflife map (slower proteolysis at 4°C). Both scale
   symmetrically. Tested with T_MAX=240h to remove the 72h cap artifact from
   the pure-FBA experiment4_interventions.py.

2. MitoQ — reduces ROS-driven selective proteolysis of ETC subunits. Modeled
   in the halflife layer as extension of halflives for ETC vs non-ETC genes.
   Selective variant: only ETC genes extended. Uniform variant: all genes extended.

3. Substrate supplementation — elevated matrix substrate concentrations increase
   X_DH (NADH production), which feeds more NADH into Beard ETC.

Comparison baseline: `results/phase_j/intervention_delta_tw.csv` (pure-FBA
intervention ΔTW under fitted 30× factor).

Outputs: results/composite/{ex5_5_intervention_composite.csv,
         ex5_5_intervention_comparison.png}
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

from paths import MODEL_PATH, RESULTS_COMPOSITE, RESULTS_PHASE_J
from ode_utils import BeardParams
from composite_utils import compose_fba_ode, FBA_ODE_REACTION_MAP
from decay_utils import configure_atp_objective, MT_ENCODED_IDS

# ── Intervention parameters (with explicit provenance flagging) ───────

Q10 = 2.5                          # DocInsight Batch 4.3 placeholder (labeled in ledger)
T_REF_C = 37.0
T_COLD_C = 4.0
# rate factor when cooling from 37→4°C (2.5^-3.3 ≈ 1/18)
COLD_RATE_SCALAR = Q10 ** ((T_COLD_C - T_REF_C) / 10.0)
# halflife factor: halflives LENGTHEN by 1/rate = 18
COLD_HL_SCALAR = 1.0 / COLD_RATE_SCALAR

MITOQ_HALFLIFE_EXTENSION = 1.35    # literature range 1.20–1.50; placeholder midpoint
SUBSTRATE_DH_BOOST = 2.0           # 2× X_DH as boundary-condition proxy

# Use accel_30x_4.7h as the intervention baseline (since this is the regime
# where composite predicts any crossing at all). Empirical halflives per the
# fitted-30x interpretation.
BASELINE_HALFLIFE_HOURS = 141.0 / 30.0  # 4.7h

SCENARIO_PRIMARY = 'A'             # intracellular buffer baseline
T_MAX_BASELINE = 72.0              # baseline sim window (hours)
T_MAX_COLD = 240.0                 # extended window for cold chain
T_MAX_EXTENDED = 144.0             # 6-day window for MitoQ/substrate to reach threshold

# ETC reaction IDs in MitoMAMMAL (for selective MitoQ) — mirrors
# experiment4_interventions.ETC_REACTION_IDS convention
ETC_REACTION_IDS = {
    'CI_mitoMap', 'CII_mitoMap', 'CIII_mitoMap',
    'CIV_mitoMap', 'CV_mitoMap', 'ATPtmB_mitoMap',
}


def build_halflife_map_baseline(model):
    """Uniform 4.7h for nuclear-encoded, immortal for mt-encoded."""
    return {
        g.id: (1e9 if g.id in MT_ENCODED_IDS else BASELINE_HALFLIFE_HOURS)
        for g in model.genes
    }


def build_halflife_map_mitoq(model, selective: bool):
    """Extended halflives under MitoQ ROS protection.

    Selective: only ETC genes (those in GPRs of ETC_REACTION_IDS) extended.
    Uniform: all genes extended.
    """
    etc_gene_ids = set()
    if selective:
        for rxn_id in ETC_REACTION_IDS:
            try:
                rxn = model.reactions.get_by_id(rxn_id)
                etc_gene_ids.update(g.id for g in rxn.genes)
            except KeyError:
                continue

    halflife_map = {}
    for g in model.genes:
        if g.id in MT_ENCODED_IDS:
            halflife_map[g.id] = 1e9
            continue
        base = BASELINE_HALFLIFE_HOURS
        if selective:
            if g.id in etc_gene_ids:
                halflife_map[g.id] = base * MITOQ_HALFLIFE_EXTENSION
            else:
                halflife_map[g.id] = base
        else:
            halflife_map[g.id] = base * MITOQ_HALFLIFE_EXTENSION
    return halflife_map


def build_halflife_map_cold_chain(model):
    """Halflives lengthen by 1/Q10^((T_ref-T_cold)/10) at 4°C storage."""
    return {
        g.id: (1e9 if g.id in MT_ENCODED_IDS else BASELINE_HALFLIFE_HOURS * COLD_HL_SCALAR)
        for g in model.genes
    }


def make_cold_chain_params() -> BeardParams:
    """Beard params with ETC rates scaled by Q10 factor (slower at 4°C)."""
    p = BeardParams()
    p.X_C1 *= COLD_RATE_SCALAR
    p.X_C3 *= COLD_RATE_SCALAR
    p.X_C4 *= COLD_RATE_SCALAR
    p.X_F *= COLD_RATE_SCALAR
    p.E_ANT *= COLD_RATE_SCALAR
    p.E_PiC *= COLD_RATE_SCALAR
    p.X_DH *= COLD_RATE_SCALAR
    p.X_H *= COLD_RATE_SCALAR
    # X_AtC (cytosolic ATP hydrolysis) models recipient-cell demand;
    # during cold storage, there is no recipient demand, so also reduce it.
    p.X_AtC *= COLD_RATE_SCALAR
    return p


def make_substrate_supp_params() -> BeardParams:
    """Beard params with elevated X_DH modeling more substrate → NADH production."""
    p = BeardParams()
    p.X_DH *= SUBSTRATE_DH_BOOST
    return p


def run_intervention(label, halflife_map_fn, params_fn, t_max_h, model):
    print(f"  [{label}] running composite (t_max={t_max_h}h)...")
    params = params_fn()
    halflife_map = halflife_map_fn(model)
    result = compose_fba_ode(
        model, params, halflife_map,
        scenario=SCENARIO_PRIMARY,
        t_max_hours=t_max_h,
        dt_fba_hours=1.0,
        n_eval_ode=200,
    )
    print(f"    TW_ΔΨm={result.tw_delta_psi_hours}h | TW_ATP={result.tw_atp_hours}h | first={result.first_failure_mode}")
    return result


def load_fba_intervention_reference():
    """Load the pure-FBA intervention ΔTW table for side-by-side comparison."""
    path = RESULTS_PHASE_J / "intervention_delta_tw.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    # Filter to scenario A and keep the intervention rows we re-predict
    return df[df['scenario'] == SCENARIO_PRIMARY].copy()


def main():
    print("=" * 68)
    print("Ex 5.5 — Intervention Re-prediction via Composite (Gate G4)")
    print("=" * 68)
    print(f"Cold chain rate scalar: {COLD_RATE_SCALAR:.4f} (ETC rates → {COLD_RATE_SCALAR:.1%} of baseline)")
    print(f"Cold chain halflife scalar: {COLD_HL_SCALAR:.2f}x (halflives lengthen 18-fold)")
    print()

    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)
    RESULTS_COMPOSITE.mkdir(parents=True, exist_ok=True)

    # Baseline composite (no intervention) at accel_30x halflife
    print("[baseline composite — no intervention]")
    baseline = run_intervention(
        'baseline', build_halflife_map_baseline, lambda: BeardParams(),
        T_MAX_BASELINE, model,
    )

    # Cold chain — requires extended T_MAX to escape cap
    print("[cold chain (Q10=2.5, 4°C)]")
    cold = run_intervention(
        'cold_chain', build_halflife_map_cold_chain, make_cold_chain_params,
        T_MAX_COLD, model,
    )

    # MitoQ selective (extend sim to catch ΔΨm threshold)
    print("[MitoQ selective (35% ETC halflife extension)]")
    mitoq_sel = run_intervention(
        'mitoq_selective',
        lambda m: build_halflife_map_mitoq(m, selective=True),
        lambda: BeardParams(),
        T_MAX_EXTENDED, model,
    )

    # MitoQ uniform
    print("[MitoQ uniform (35% halflife extension for all genes)]")
    mitoq_uni = run_intervention(
        'mitoq_uniform',
        lambda m: build_halflife_map_mitoq(m, selective=False),
        lambda: BeardParams(),
        T_MAX_EXTENDED, model,
    )

    # Substrate supplementation
    print("[substrate_supp (2× X_DH NADH supply)]")
    subst = run_intervention(
        'substrate_supp', build_halflife_map_baseline, make_substrate_supp_params,
        T_MAX_EXTENDED, model,
    )

    # ── Assemble results ────────────────────────────────────────
    results = {
        'baseline': baseline,
        'cold_chain': cold,
        'mitoq_selective': mitoq_sel,
        'mitoq_uniform': mitoq_uni,
        'substrate_supp': subst,
    }

    rows = []
    baseline_tw = baseline.tw_delta_psi_hours
    for label, r in results.items():
        dpsi_tw = r.tw_delta_psi_hours
        atp_tw = r.tw_atp_hours
        # Use ΔΨm threshold as primary TW metric (matches Gate G3 convention)
        tw_primary = dpsi_tw if dpsi_tw is not None else (atp_tw if atp_tw is not None else None)
        if tw_primary is None or baseline_tw is None:
            delta_tw = None
            fold_ext = None
        else:
            delta_tw = tw_primary - baseline_tw
            fold_ext = tw_primary / baseline_tw if baseline_tw > 0 else None
        rows.append({
            'intervention': label,
            'scenario': SCENARIO_PRIMARY,
            'baseline_tw_h': baseline_tw,
            'intervention_tw_delta_psi_h': dpsi_tw,
            'intervention_tw_atp_h': atp_tw,
            'delta_tw_h': delta_tw,
            'fold_extension': fold_ext,
            'first_failure_mode': r.first_failure_mode,
            'delta_psi_final_mV': r.delta_psi_trace[-1] * 1000,
            'hits_sim_cap': (dpsi_tw is None and atp_tw is None),
        })
    df = pd.DataFrame(rows)
    csv_path = RESULTS_COMPOSITE / "ex5_5_intervention_composite.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n  ✓ Saved: {csv_path}")

    # ── Gate G4 check ────────────────────────────────────────────
    print("\nGate G4 assessment:")
    cold_row = df[df['intervention'] == 'cold_chain'].iloc[0]
    if cold_row['hits_sim_cap']:
        print(f"  ✗ Cold chain hits T_MAX={T_MAX_COLD}h cap — no finite TW — G4 FAIL")
        gate_g4 = False
    else:
        print(f"  ✓ Cold chain TW finite ({cold_row['intervention_tw_delta_psi_h']}h for ΔΨm, "
              f"{cold_row['intervention_tw_atp_h']}h for ATP) — G4 PASS")
        gate_g4 = True

    # MitoQ selective vs uniform comparison
    sel = df[df['intervention'] == 'mitoq_selective'].iloc[0]
    uni = df[df['intervention'] == 'mitoq_uniform'].iloc[0]
    sel_tw = sel['intervention_tw_delta_psi_h'] or sel['intervention_tw_atp_h']
    uni_tw = uni['intervention_tw_delta_psi_h'] or uni['intervention_tw_atp_h']
    print(f"\n  MitoQ selective TW: {sel_tw}h")
    print(f"  MitoQ uniform TW:   {uni_tw}h")
    if sel_tw and uni_tw and sel_tw > uni_tw:
        print(f"  → selective > uniform (reverses Phase J finding)")
    elif sel_tw and uni_tw and uni_tw > sel_tw:
        print(f"  → uniform > selective (confirms Phase J finding)")

    # ── Side-by-side comparison with pure FBA ────────────────────
    fba_ref = load_fba_intervention_reference()
    if fba_ref is not None:
        print(f"\n  Pure-FBA reference loaded from {RESULTS_PHASE_J / 'intervention_delta_tw.csv'}")
        print(fba_ref.to_string(index=False))
    else:
        print("\n  [No pure-FBA reference found for comparison]")

    # ── Plot ─────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: TW comparison
    labels = list(results.keys())
    tws = []
    for label in labels:
        r = results[label]
        tw = r.tw_delta_psi_hours if r.tw_delta_psi_hours is not None else r.tw_atp_hours
        tws.append(tw if tw is not None else (T_MAX_COLD if label == 'cold_chain' else T_MAX_BASELINE))
    colors = ['gray', '#4488ff', '#44bb44', '#88ddbb', '#ff8844']
    bars = axes[0].bar(labels, tws, color=colors)
    axes[0].set_ylabel('Transit window (hours)')
    axes[0].set_title('Composite TW by intervention (Scenario A)')
    axes[0].axhline(T_MAX_BASELINE, linestyle=':', color='black', alpha=0.5, label=f'Baseline T_MAX={T_MAX_BASELINE}h')
    plt.setp(axes[0].get_xticklabels(), rotation=15, ha='right')
    for bar, tw in zip(bars, tws):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                     f"{tw:.0f}h", ha='center', fontsize=9)

    # Right: composite vs pure-FBA side by side (if reference available)
    if fba_ref is not None:
        # Map intervention names; pure FBA uses same labels in its CSV
        interventions = ['cold_chain', 'mitoq_selective', 'mitoq_uniform', 'substrate_supp']
        composite_deltas = []
        fba_deltas = []
        for iv in interventions:
            c_row = df[df['intervention'] == iv].iloc[0]
            c_tw = c_row['intervention_tw_delta_psi_h'] or c_row['intervention_tw_atp_h'] or T_MAX_COLD
            baseline_row = df[df['intervention'] == 'baseline'].iloc[0]
            b_tw = baseline_row['intervention_tw_delta_psi_h'] or baseline_row['intervention_tw_atp_h'] or T_MAX_BASELINE
            composite_deltas.append(c_tw - b_tw)

            f_row = fba_ref[fba_ref['intervention'] == iv]
            fba_deltas.append(float(f_row['delta_tw'].iloc[0]) if len(f_row) > 0 else 0.0)

        x = np.arange(len(interventions))
        width = 0.38
        axes[1].bar(x - width/2, composite_deltas, width, label='Composite', color='#2266cc')
        axes[1].bar(x + width/2, fba_deltas, width, label='Pure FBA (phase_j)', color='#cc6622')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(interventions, rotation=15, ha='right')
        axes[1].set_ylabel(r'$\Delta$TW (hours)')
        axes[1].set_title('Composite vs pure-FBA ΔTW')
        axes[1].legend()
        axes[1].grid(axis='y', alpha=0.3)
    else:
        axes[1].text(0.5, 0.5, 'No pure-FBA reference\navailable for comparison',
                     ha='center', va='center', transform=axes[1].transAxes)

    fig.suptitle('Ex 5.5 — Composite intervention re-prediction (Scenario A)', fontsize=12)
    fig.tight_layout()
    png_path = RESULTS_COMPOSITE / "ex5_5_intervention_comparison.png"
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    print(f"\n  ✓ Saved: {png_path}")

    print("\n" + "=" * 68)
    print(f"Ex 5.5 complete. Gate G4: {'PASS' if gate_g4 else 'FAIL'}")
    print("=" * 68)


if __name__ == '__main__':
    main()

"""
Phase G.1 — Order-statistics test
=================================
Critical test: is the heterogeneity finding (TW=8h under lognormal σ=0.6) an FBA
contribution, or pure order-statistics algebra?

Method:
  Build a non-FBA model where each AND-clause has effective_t½ = min(N samples
  from lognormal). Apply pure exponential decay. Compute TW. Compare to FBA result.

Hypothesis: if FBA agrees with order-statistics prediction, the "heterogeneity
finding" is algebra, not FBA-specific. If FBA differs, the network adds something.
"""

import sys
from pathlib import Path
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import MODEL_PATH, results_path, investigation_doc

import json
import numpy as np
import pandas as pd
import cobra

from decay_utils import (
    MT_ENCODED_IDS, OBJ_ATP, get_signed_baseline_fluxes, build_decay_expr_dict,
    apply_gpr_aware_decay, configure_atp_objective,
    get_objective_flux, find_transit_window,
)

UNIFORM_HALFLIFE = 12.0
THRESHOLD = 0.20
T_MAX = 72.0


def compute_and_clause_sizes(model):
    """Return dict reaction_id -> N (number of mouse nuclear AND-linked subunits)."""
    sizes = {}
    for rxn in model.reactions:
        gpr = rxn.gene_reaction_rule
        if not gpr or 'or' in gpr.lower():
            # Skip OR-rule reactions and reactions without GPR
            continue
        # Pure AND-rule: count mouse nuclear genes
        mouse_nuclear = [
            g.id for g in rxn.genes
            if g.id.startswith('ENSMUSG') and g.id not in MT_ENCODED_IDS
        ]
        if mouse_nuclear:
            sizes[rxn.id] = len(mouse_nuclear)
    return sizes


def order_statistic_min_t_half(N, log_mu, log_sigma, n_samples=10000):
    """Empirical expectation of min over N lognormal samples.
    Returns mean and 95% CI of the minimum."""
    mins = []
    for _ in range(n_samples):
        samples = np.exp(np.random.normal(log_mu, log_sigma, N))
        mins.append(np.min(samples))
    return np.mean(mins), np.percentile(mins, [2.5, 97.5])


def predict_tw_from_order_stats(model, log_sigma):
    """Predict TW analytically: effective_t½ for ATP-producing pathway = min across
    the LARGEST AND-clause that's required for ATP. Pure exp decay from there."""
    np.random.seed(42)
    log_mu = np.log(UNIFORM_HALFLIFE)

    # ETC reactions are required for ATP. The largest AND-clause among them
    # determines the effective t½ (since min across the largest clause = smallest).
    etc_rxns = ['CI_mitoMap', 'CII_mitoMap', 'CIII_mitoMap', 'CIV_mitoMap', 'CV_mitoMap']
    clause_sizes = []
    for rid in etc_rxns:
        try:
            r = model.reactions.get_by_id(rid)
            mouse_nuc = [g.id for g in r.genes
                         if g.id.startswith('ENSMUSG') and g.id not in MT_ENCODED_IDS]
            if mouse_nuc:
                clause_sizes.append((rid, len(mouse_nuc)))
        except KeyError:
            continue

    print(f"  ETC AND-clause sizes (mouse nuclear): {clause_sizes}")

    # The reaction with the LARGEST AND clause has the FASTEST effective t½
    # (because min over more samples is smaller)
    largest_clause = max(clause_sizes, key=lambda x: x[1])
    rid, N = largest_clause
    mean_min, ci = order_statistic_min_t_half(N, log_mu, log_sigma)
    print(f"  Largest ETC AND-clause: {rid} with {N} mouse nuclear subunits")
    print(f"  E[min over {N} lognormal(median=12h, σ={log_sigma}) samples] = {mean_min:.2f}h (95% CI: {ci[0]:.2f}-{ci[1]:.2f})")

    # Pure exp prediction: TW = -t½ × log₂(threshold)
    predicted_tw = -mean_min * np.log(THRESHOLD) / np.log(2)
    return predicted_tw, mean_min, ci, rid, N


def run_fba_at_log_sigma(model, baseline_fluxes, baseline_atp, log_sigma, n_trials=20):
    """Run actual FBA simulation at given log_sigma. Return mean TW."""
    np.random.seed(42)
    log_mu = np.log(UNIFORM_HALFLIFE)
    tws = []
    for trial in range(n_trials):
        halflife_map = {}
        for g in model.genes:
            halflife_map[g.id] = float(np.exp(np.random.normal(log_mu, log_sigma)))

        t_steps = np.arange(0, T_MAX + 1, 1)
        fluxes = []
        with model:
            for t in t_steps:
                with model:
                    expr = build_decay_expr_dict(model, halflife_map, t)
                    apply_gpr_aware_decay(model, expr, baseline_fluxes)
                    atp = get_objective_flux(model, 'atp')
                    fluxes.append(atp)
                    if atp < baseline_atp * THRESHOLD * 0.01 and t > 2:
                        fluxes.extend([0.0] * (len(t_steps) - len(fluxes)))
                        break
        fluxes = np.array(fluxes[:len(t_steps)])
        if len(fluxes) < len(t_steps):
            fluxes = np.concatenate([fluxes, np.zeros(len(t_steps) - len(fluxes))])
        tw = find_transit_window(t_steps, fluxes, baseline_atp, THRESHOLD)
        tws.append(tw if tw is not None else 72)
    return np.mean(tws), np.std(tws), np.min(tws), np.max(tws)


def main():
    print("=" * 60)
    print("Phase G.1 — Order Statistics vs FBA")
    print("=" * 60)

    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)
    baseline_fluxes = get_signed_baseline_fluxes(model)
    baseline_atp = baseline_fluxes[OBJ_ATP]
    print(f"Baseline ATP: {baseline_atp:.3f}")

    # Test across log_sigma values
    results = []
    for log_sigma in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        print(f"\n--- log_sigma = {log_sigma} ---")
        if log_sigma == 0:
            # Trivial case: all genes at 12h, TW = analytical
            analytical = -UNIFORM_HALFLIFE * np.log(THRESHOLD) / np.log(2)
            os_pred = analytical
            mean_min, ci, rid, N = UNIFORM_HALFLIFE, (UNIFORM_HALFLIFE, UNIFORM_HALFLIFE), 'N/A', 0
            print(f"  Analytical (uniform): TW = {analytical:.2f}h")
        else:
            os_pred, mean_min, ci, rid, N = predict_tw_from_order_stats(model, log_sigma)
            print(f"  Order-statistics prediction: TW = {os_pred:.2f}h")

        print(f"  Running FBA simulation (20 trials)...")
        fba_mean, fba_std, fba_min, fba_max = run_fba_at_log_sigma(model, baseline_fluxes, baseline_atp, log_sigma)
        print(f"  FBA observed: mean TW = {fba_mean:.2f}h (std={fba_std:.2f}, range=[{fba_min:.0f},{fba_max:.0f}])")

        gap = fba_mean - os_pred
        print(f"  Gap (FBA - order-stats): {gap:+.2f}h")

        results.append({
            'log_sigma': log_sigma,
            'order_stats_predicted_tw': float(os_pred),
            'os_min_t_half': float(mean_min),
            'os_min_t_half_ci_low': float(ci[0]),
            'os_min_t_half_ci_high': float(ci[1]),
            'largest_clause_rxn': rid,
            'largest_clause_size': N,
            'fba_mean_tw': float(fba_mean),
            'fba_std_tw': float(fba_std),
            'fba_min_tw': float(fba_min),
            'fba_max_tw': float(fba_max),
            'gap_fba_minus_os': float(gap),
        })

    # Save and summarize
    df = pd.DataFrame(results)
    df.to_csv(results_path('phase_g', 'g1_order_stats_vs_fba.csv'), index=False)
    print(f"\n✓ Saved to {results_path('phase_g', 'g1_order_stats_vs_fba.csv')}")

    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)
    print("\nIf gap < 1h: the heterogeneity finding is order-statistics algebra.")
    print("If gap > 3h: the FBA network adds non-trivial content.")
    print()
    print(f"{'log_sigma':12s} {'OS pred':10s} {'FBA mean':10s} {'Gap':10s}")
    for r in results:
        print(f"  {r['log_sigma']:>10.1f} {r['order_stats_predicted_tw']:>9.2f}h {r['fba_mean_tw']:>9.2f}h {r['gap_fba_minus_os']:+9.2f}h")

    # Quantitative verdict
    avg_gap = np.mean([abs(r['gap_fba_minus_os']) for r in results if r['log_sigma'] > 0])
    print(f"\nMean |gap| across heterogeneous cases: {avg_gap:.2f}h")
    if avg_gap < 1:
        print("→ VERDICT: Heterogeneity finding is order-statistics algebra. FBA contributes essentially nothing.")
    elif avg_gap < 3:
        print("→ VERDICT: Mostly algebra, but FBA adds modest network content (1-3h).")
    else:
        print("→ VERDICT: FBA network adds substantial content beyond order statistics.")

    return results


if __name__ == '__main__':
    main()

"""
Experiment 1b: Gene Sensitivity — Engineering Target Ranking
=============================================================
For each nuclear-encoded gene, compute its leverage on the transit window.

Two-stage approach:
  Stage 1: Single knockout impact score for all 769 nuclear genes (fast — one FBA each).
           Ranks genes by how much ATP drops when their protein is fully depleted.
  Stage 2: Complex-level sensitivity — for each ETC complex, set ALL its nuclear subunits
           to infinite half-life (t½ → ∞), re-run the full 72h time-stepped simulation,
           record Δtransit window vs baseline.

Output:
  results/gene_knockout_scores.csv      — ranked knockout impacts for all 769 genes
  results/complex_sensitivity.csv       — complex-level Δtransit window
  results/sensitivity_figure.png        — bar chart of Δtransit per complex

Run with:
    /opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/python experiment1b_gene_sensitivity.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cobra
from cobra.flux_analysis import pfba
import os
import json
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────
MODEL_PATH = "/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml"
RESULTS_DIR = "/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

MT_ENCODED_IDS = {
    'ENSMUSG00000064341', 'ENSMUSG00000064345', 'ENSMUSG00000064351',
    'ENSMUSG00000064354', 'ENSMUSG00000064356', 'ENSMUSG00000064357',
    'ENSMUSG00000064358', 'ENSMUSG00000064360', 'ENSMUSG00000064363',
    'ENSMUSG00000064367', 'ENSMUSG00000064368', 'ENSMUSG00000064370',
    'ENSMUSG00000065947'
}

# ETC complex → constituent reaction IDs in MitoMAMMAL
ETC_COMPLEXES = {
    'Complex I':   ['CI_mitoMap'],
    'Complex II':  ['CII_mitoMap'],
    'Complex III': ['CIII_mitoMap'],
    'Complex IV':  ['CIV_mitoMap'],
    'Complex V':   ['CV_mitoMap'],
    'ATPtranslocase': ['ATPtmB_mitoMap'],
}

OBJ_RXN = 'OF_ATP_mitoMap'
DEFAULT_HALFLIFE = 12.0        # hours — baseline regime
INFINITE_HALFLIFE = 1e9        # effectively immortal
REUPTAKE_THRESHOLD = 0.20      # 20% of scenario baseline
BASELINE_TRANSIT_WINDOW = 29.0 # hours — from Experiment 1 Scenario A


# ─── Shared utilities (duplicated from experiment1 to keep scripts independent) ──

def decay_factor(t_hours, halflife_hours):
    return np.exp(-np.log(2) * t_hours / halflife_hours)


def get_baseline_fluxes(model):
    try:
        sol = pfba(model)
        return {r.id: abs(sol.fluxes.get(r.id, 0.0)) for r in model.reactions}
    except Exception:
        sol = model.optimize()
        return {r.id: abs(sol.fluxes.get(r.id, 0.0)) for r in model.reactions}


def get_atp_flux(model):
    try:
        sol = pfba(model)
        if sol.status == 'optimal':
            return sol.fluxes.get(OBJ_RXN, 0.0)
        return 0.0
    except Exception:
        sol = model.optimize()
        return sol.objective_value if sol.status == 'optimal' else 0.0


def apply_decay_all(model, nuclear_genes, halflife_map, t_hours, baseline_fluxes):
    """Apply flux-relative decay to all nuclear genes at time t."""
    for gene in nuclear_genes:
        t_half = halflife_map.get(gene.id, DEFAULT_HALFLIFE)
        if t_half >= INFINITE_HALFLIFE:
            continue  # immortal — no decay applied
        df = decay_factor(t_hours, t_half)
        for rxn in gene.reactions:
            bflux = baseline_fluxes.get(rxn.id, 0.0)
            if bflux > 1e-6:
                rxn.upper_bound = max(0.0, bflux * 1.05 * df)
            else:
                rxn.upper_bound = max(0.0, rxn.upper_bound * df)


def find_transit_window(times, atp_fluxes, baseline_atp, threshold_fraction=REUPTAKE_THRESHOLD):
    threshold = baseline_atp * threshold_fraction
    for i, flux in enumerate(atp_fluxes):
        if flux < threshold:
            return times[i]
    return None  # never crossed


def run_timed_fba(model, nuclear_genes, halflife_map,
                  t_max=72, dt=1.0):
    """Run time-stepped FBA with given halflife_map. Returns (times, atp_fluxes, transit_window)."""
    t_steps = np.arange(0, t_max + dt, dt)
    atp_fluxes = []

    with model:
        baseline_fluxes = get_baseline_fluxes(model)
        baseline_atp = get_atp_flux(model)

        for t in t_steps:
            with model:
                apply_decay_all(model, nuclear_genes, halflife_map, t, baseline_fluxes)
                atp_fluxes.append(get_atp_flux(model))

    atp_arr = np.array(atp_fluxes)
    tw = find_transit_window(t_steps, atp_arr, baseline_atp)
    return t_steps, atp_arr, tw, baseline_atp


# ─── Stage 1: Gene knockout scoring ──────────────────────────────────────────

def run_gene_knockout_stage(model, nuclear_genes, baseline_atp, baseline_fluxes):
    """
    For each nuclear gene, knock out all its reactions (upper_bound → 0)
    and record the resulting ATP flux drop.

    Returns a DataFrame sorted by impact descending.
    Runtime: ~769 FBA calls, typically <30 seconds.
    """
    print(f"\n[Stage 1] Gene knockout scoring ({len(nuclear_genes)} genes)...")
    records = []

    for i, gene in enumerate(nuclear_genes):
        if i % 100 == 0:
            print(f"  ... {i}/{len(nuclear_genes)}")

        with model:
            # Zero out all reactions associated with this gene
            for rxn in gene.reactions:
                rxn.upper_bound = 0.0
                rxn.lower_bound = max(rxn.lower_bound, 0.0)

            atp = get_atp_flux(model)

        impact = baseline_atp - atp
        impact_pct = (impact / baseline_atp * 100) if baseline_atp > 0 else 0.0

        # Which complex does this gene primarily belong to?
        complex_membership = []
        for complex_name, rxn_ids in ETC_COMPLEXES.items():
            for rxn_id in rxn_ids:
                try:
                    rxn = model.reactions.get_by_id(rxn_id)
                    if gene in rxn.genes:
                        complex_membership.append(complex_name)
                except Exception:
                    pass

        # Sum of baseline fluxes for all gene-associated reactions
        flux_sum = sum(baseline_fluxes.get(rxn.id, 0) for rxn in gene.reactions)

        records.append({
            'gene_id': gene.id,
            'n_reactions': len(gene.reactions),
            'baseline_flux_sum': round(flux_sum, 6),
            'atp_after_ko': round(atp, 6),
            'atp_impact': round(impact, 6),
            'atp_impact_pct': round(impact_pct, 4),
            'complex': ', '.join(complex_membership) if complex_membership else 'Other',
        })

    df = pd.DataFrame(records).sort_values('atp_impact', ascending=False).reset_index(drop=True)
    df.insert(0, 'rank', range(1, len(df) + 1))
    return df


# ─── Stage 2: Complex-level time-stepped sensitivity ─────────────────────────

def run_complex_sensitivity(model, nuclear_genes, baseline_tw):
    """
    For each ETC complex, set ALL nuclear-encoded subunits to infinite half-life
    (immortal), keep all other nuclear genes at DEFAULT_HALFLIFE.
    Run full 72h simulation, record transit window.
    Δtransit = new_tw - baseline_tw.

    Also runs an 'All immortal' control (all 769 nuclear genes immortal).
    """
    print(f"\n[Stage 2] Complex-level sensitivity ({len(ETC_COMPLEXES)} complexes + controls)...")

    # Build complex → set of nuclear gene objects
    complex_gene_sets = {}
    for complex_name, rxn_ids in ETC_COMPLEXES.items():
        genes_in_complex = set()
        for rxn_id in rxn_ids:
            try:
                rxn = model.reactions.get_by_id(rxn_id)
                for g in rxn.genes:
                    if g.id not in MT_ENCODED_IDS:
                        genes_in_complex.add(g.id)
            except Exception:
                pass
        complex_gene_sets[complex_name] = genes_in_complex
        print(f"  {complex_name}: {len(genes_in_complex)} nuclear subunits")

    records = []

    # Baseline (all at DEFAULT_HALFLIFE)
    base_halflife_map = {g.id: DEFAULT_HALFLIFE for g in nuclear_genes}
    _, _, tw_baseline, baseline_atp = run_timed_fba(model, nuclear_genes, base_halflife_map)
    tw_baseline = tw_baseline if tw_baseline is not None else 72.0
    print(f"\n  Baseline transit window: {tw_baseline:.1f}h (should match Exp1: {baseline_tw}h)")

    # Each complex immortalized
    for complex_name, immortal_ids in complex_gene_sets.items():
        halflife_map = {g.id: DEFAULT_HALFLIFE for g in nuclear_genes}
        for gid in immortal_ids:
            halflife_map[gid] = INFINITE_HALFLIFE

        _, _, tw, _ = run_timed_fba(model, nuclear_genes, halflife_map)
        tw = tw if tw is not None else ">72h"
        delta = (tw - tw_baseline) if isinstance(tw, float) else (72.0 - tw_baseline)
        delta_str = f"+{delta:.1f}h" if delta >= 0 else f"{delta:.1f}h"

        print(f"  {complex_name:20s}  n_immortal={len(immortal_ids):3d}  "
              f"transit_window={str(tw):8s}  Δ={delta_str}")

        records.append({
            'complex': complex_name,
            'n_immortal_subunits': len(immortal_ids),
            'transit_window_hours': tw if isinstance(tw, float) else 72.0,
            'delta_transit_hours': delta,
            'transit_window_str': str(tw) if isinstance(tw, float) else '>72h',
        })

    # Control: ALL nuclear genes immortal
    all_immortal_map = {g.id: INFINITE_HALFLIFE for g in nuclear_genes}
    _, _, tw_all, _ = run_timed_fba(model, nuclear_genes, all_immortal_map)
    tw_all = tw_all if tw_all is not None else ">72h"
    print(f"  {'All immortal':20s}  n_immortal={len(nuclear_genes):3d}  "
          f"transit_window={str(tw_all):8s}  (upper bound)")
    records.append({
        'complex': 'All nuclear (control)',
        'n_immortal_subunits': len(nuclear_genes),
        'transit_window_hours': tw_all if isinstance(tw_all, float) else 72.0,
        'delta_transit_hours': (tw_all - tw_baseline) if isinstance(tw_all, float) else (72.0 - tw_baseline),
        'transit_window_str': str(tw_all) if isinstance(tw_all, float) else '>72h',
    })

    return pd.DataFrame(records), tw_baseline


# ─── Plot ─────────────────────────────────────────────────────────────────────

def plot_sensitivity(complex_df, ko_df, baseline_tw, output_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left: complex-level Δtransit window
    plot_df = complex_df[complex_df['complex'] != 'All nuclear (control)'].copy()
    plot_df = plot_df.sort_values('delta_transit_hours', ascending=True)

    colors = ['#2196F3' if d > 0 else '#EF5350' for d in plot_df['delta_transit_hours']]
    bars = ax1.barh(plot_df['complex'], plot_df['delta_transit_hours'], color=colors)
    ax1.axvline(x=0, color='black', linewidth=0.8)
    ax1.set_xlabel('Δ Transit window (hours vs baseline)', fontsize=11)
    ax1.set_title(f'Complex-level sensitivity\n(Baseline transit window: {baseline_tw:.0f}h)', fontsize=11)
    ax1.grid(True, alpha=0.3, axis='x')

    for bar, (_, row) in zip(bars, plot_df.iterrows()):
        label = f"+{row['delta_transit_hours']:.1f}h" if row['delta_transit_hours'] >= 0 else f"{row['delta_transit_hours']:.1f}h"
        x_pos = bar.get_width() + 0.1 if bar.get_width() >= 0 else bar.get_width() - 0.1
        ax1.text(x_pos, bar.get_y() + bar.get_height()/2,
                 f"{label} ({row['n_immortal_subunits']} subunits)",
                 va='center', fontsize=8)

    # Right: top 20 genes by knockout impact
    top20 = ko_df.head(20)
    colors2 = ['#F44336' if 'Complex V' in str(r['complex']) else
               '#FF9800' if 'Complex I' in str(r['complex']) else
               '#4CAF50' if 'Complex III' in str(r['complex']) else '#9C27B0'
               for _, r in top20.iterrows()]

    ax2.barh(range(len(top20)), top20['atp_impact_pct'], color=colors2[::-1])
    ax2.set_yticks(range(len(top20)))
    ax2.set_yticklabels([f"{r['gene_id'][:20]} ({r['complex'][:8]})"
                         for _, r in top20.iloc[::-1].iterrows()], fontsize=7)
    ax2.set_xlabel('ATP flux drop on knockout (% of baseline)', fontsize=11)
    ax2.set_title('Top 20 genes by knockout impact\n(proxy for transit window leverage)', fontsize=11)
    ax2.grid(True, alpha=0.3, axis='x')

    fig.suptitle(
        'Experiment 1b: Gene Sensitivity Analysis — Engineering Target Ranking\n'
        f'MitoMAMMAL (560 rxns, 782 genes) · Baseline transit window: {baseline_tw:.0f}h · '
        f'{datetime.now().strftime("%Y-%m-%d")}',
        fontsize=10, y=1.01
    )
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n  Figure saved: {output_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print("Experiment 1b: Gene Sensitivity Analysis")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    print("\n[0] Loading model...")
    model = cobra.io.read_sbml_model(MODEL_PATH)
    nuclear_genes = [g for g in model.genes if g.id not in MT_ENCODED_IDS]
    print(f"    Nuclear genes: {len(nuclear_genes)}")

    print("\n[0b] Running baseline pFBA...")
    base_sol = pfba(model)
    baseline_atp = base_sol.fluxes.get(OBJ_RXN, 0.0)
    baseline_fluxes = {r.id: abs(base_sol.fluxes.get(r.id, 0.0)) for r in model.reactions}
    print(f"    Baseline ATP: {baseline_atp:.4f}")

    # ── Stage 1 ──────────────────────────────────────────────────────────────
    ko_df = run_gene_knockout_stage(model, nuclear_genes, baseline_atp, baseline_fluxes)

    ko_path = os.path.join(RESULTS_DIR, 'gene_knockout_scores.csv')
    ko_df.to_csv(ko_path, index=False)
    print(f"\n  Saved: {ko_path}")

    print(f"\n  Top 10 genes by knockout impact:")
    print(ko_df[['rank','gene_id','complex','n_reactions','atp_impact_pct']].head(10).to_string(index=False))

    zero_impact = (ko_df['atp_impact'] == 0).sum()
    print(f"\n  Genes with zero knockout impact: {zero_impact} / {len(ko_df)}")
    print(f"  (These are metabolically redundant or carry no flux at baseline)")

    # ── Stage 2 ──────────────────────────────────────────────────────────────
    complex_df, tw_baseline = run_complex_sensitivity(model, nuclear_genes, BASELINE_TRANSIT_WINDOW)

    complex_path = os.path.join(RESULTS_DIR, 'complex_sensitivity.csv')
    complex_df.to_csv(complex_path, index=False)
    print(f"\n  Saved: {complex_path}")

    # ── Figure ───────────────────────────────────────────────────────────────
    fig_path = os.path.join(RESULTS_DIR, 'sensitivity_figure.png')
    plot_sensitivity(complex_df, ko_df, tw_baseline, fig_path)

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"\nBaseline transit window: {tw_baseline:.1f}h")
    print(f"\nComplex-level Δtransit window (immortalizing all nuclear subunits):")
    print(complex_df[['complex','n_immortal_subunits','transit_window_str','delta_transit_hours']].to_string(index=False))

    print(f"\nTop 10 genes by knockout impact:")
    print(ko_df[['rank','gene_id','complex','atp_impact_pct']].head(10).to_string(index=False))

    # Save summary JSON for abstract use
    summary = {
        'run_date': datetime.now().isoformat(),
        'baseline_transit_window_hours': tw_baseline,
        'complex_sensitivity': complex_df.to_dict(orient='records'),
        'top10_knockout_genes': ko_df.head(10)[['rank','gene_id','complex','atp_impact_pct']].to_dict(orient='records'),
        'total_nuclear_genes_scored': len(ko_df),
        'zero_impact_genes': int((ko_df['atp_impact'] == 0).sum()),
    }
    with open(os.path.join(RESULTS_DIR, 'experiment1b_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("Abstract language:")
    best_complex = complex_df[complex_df['complex'] != 'All nuclear (control)'].sort_values(
        'delta_transit_hours', ascending=False).iloc[0]
    print(f"  Immortalizing {best_complex['complex']} subunits ({best_complex['n_immortal_subunits']} genes)")
    print(f"  extends the transit window by {best_complex['delta_transit_hours']:.1f}h")
    print(f"  (from {tw_baseline:.0f}h to {best_complex['transit_window_hours']:.0f}h),")
    print(f"  identifying it as the highest-leverage engineering target.")
    print("=" * 60)

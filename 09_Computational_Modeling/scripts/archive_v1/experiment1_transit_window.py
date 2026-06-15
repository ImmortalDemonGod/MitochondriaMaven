"""
Experiment 1: Transit Viability Window — Time-Stepped FBA
==========================================================
Predicts how long extracted mitochondria maintain ATP synthesis
as nuclear-encoded ETC proteins decay post-extraction.

Output: decay curves (ATP flux vs time) for three substrate scenarios.
The transit window = time at which ATP flux drops below the reuptake threshold.

Run with:
    /opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/python experiment1_transit_window.py

Results saved to:
    09_Computational_Modeling/results/transit_window_results.csv
    09_Computational_Modeling/results/decay_curves.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cobra
from cobra.flux_analysis import pfba
import os
import json
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────
MODEL_PATH = "/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml"
HALFLIVES_PATH = "/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/protein_halflives.csv"
RESULTS_DIR = "/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# ─── MT-encoded gene IDs (mouse mt chromosome — do not decay these) ───────────
MT_ENCODED_IDS = {
    'ENSMUSG00000064341',  # mt-Nd1
    'ENSMUSG00000064345',  # mt-Nd2
    'ENSMUSG00000064351',  # mt-Co1
    'ENSMUSG00000064354',  # mt-Co2
    'ENSMUSG00000064356',  # mt-Cytb
    'ENSMUSG00000064357',  # mt-Co3
    'ENSMUSG00000064358',  # mt-Atp8
    'ENSMUSG00000064360',  # mt-Nd3
    'ENSMUSG00000064363',  # mt-Atp6
    'ENSMUSG00000064367',  # mt-Nd5
    'ENSMUSG00000064368',  # mt-Nd4
    'ENSMUSG00000064370',  # mt-Nd6
    'ENSMUSG00000065947',  # mt-Nd4l
}

# ─── Reuptake viability threshold ─────────────────────────────────────────────
# From mitophagy literature: PINK1/Parkin activates when ΔΨm drops ~20-30%.
# Approximated as: ATP flux < 20% of baseline → organelle non-viable for reuptake.
# Update this once DocInsight returns the quantitative threshold.
REUPTAKE_THRESHOLD_FRACTION = 0.20

# ─── Half-life assignments ────────────────────────────────────────────────────
# Three-regime model (used until DocInsight returns empirical values).
# Once protein_halflives.csv exists, switch to load_halflives_from_csv().
#
# Regimes (in hours):
#   FAST   = 2h   — assembly factors, peripheral subunits, import machinery
#   MEDIUM = 12h  — core catalytic subunits (NDUFS1, SDHA, UQCRC1, COX4, ATP5A)
#   SLOW   = 48h  — structural/scaffold, membrane-embedded subunits
#
# Default: all nuclear-encoded proteins assigned MEDIUM (12h) for first run.
# This gives a conservative mid-range estimate. Adjust after empirical data.
DEFAULT_HALFLIFE_HOURS = 12.0


def load_halflives_from_csv(path, model_genes):
    """Load empirical half-lives from protein_halflives.csv if it exists.

    Returns dict: gene_id -> half_life_hours.
    Missing genes get DEFAULT_HALFLIFE_HOURS.
    """
    halflives = {}
    if not os.path.exists(path):
        print(f"  [INFO] {path} not found — using regime defaults ({DEFAULT_HALFLIFE_HOURS}h for all)")
        return halflives
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        halflives[row['gene_id']] = float(row['t_half_hours'])
    print(f"  [INFO] Loaded {len(halflives)} empirical half-lives from CSV")
    return halflives


def build_halflife_map(model, mt_encoded_ids, empirical=None):
    """Build gene_id -> half_life_hours for all nuclear-encoded genes."""
    halflife_map = {}
    empirical = empirical or {}
    for g in model.genes:
        if g.id in mt_encoded_ids:
            continue  # mt-encoded: not subject to import-dependent decay
        halflife_map[g.id] = empirical.get(g.id, DEFAULT_HALFLIFE_HOURS)
    return halflife_map


def decay_factor(t_hours, halflife_hours):
    """Exponential decay: P(t) / P(0) = exp(-ln2 * t / t_half)"""
    return np.exp(-np.log(2) * t_hours / halflife_hours)


def apply_decay_to_model(model, nuclear_genes, halflife_map, t_hours,
                          baseline_bounds, baseline_fluxes, flux_buffer=1.05):
    """Scale upper bounds of nuclear-gene-associated reactions by decay factor.

    Uses FLUX-RELATIVE scaling: UB at time t = baseline_flux * decay_factor * buffer.
    This ensures the constraint binds from the first time step (physically: the
    maximum achievable reaction rate declines as enzyme pool depletes).

    For reactions with zero baseline flux, falls back to bound-relative scaling.
    flux_buffer: small multiplier above baseline flux so t=0 is unconstrained (1.05 = 5% headroom).
    """
    for gene in nuclear_genes:
        t_half = halflife_map[gene.id]
        df = decay_factor(t_hours, t_half)
        for rxn in gene.reactions:
            bflux = baseline_fluxes.get(rxn.id, 0.0)
            if bflux > 1e-6:
                # Flux-relative: capacity = baseline flux * decay * headroom
                new_ub = bflux * flux_buffer * df
            else:
                # Zero-flux reaction: fall back to bound-relative scaling
                original_ub = baseline_bounds[rxn.id]['upper_bound']
                new_ub = original_ub * df
            rxn.upper_bound = max(0.0, new_ub)


def get_atp_flux(model, obj_rxn_id='OF_ATP_mitoMap'):
    """Run pFBA and return ATP objective flux. Returns 0 on infeasibility."""
    try:
        sol = pfba(model)
        if sol.status == 'optimal':
            return sol.fluxes.get(obj_rxn_id, 0.0)
        return 0.0
    except Exception:
        # Fall back to plain FBA if pFBA fails
        sol = model.optimize()
        if sol.status == 'optimal':
            return sol.objective_value
        return 0.0


def get_baseline_bounds(model):
    """Snapshot current upper and lower bounds for all reactions."""
    return {
        r.id: {'upper_bound': r.upper_bound, 'lower_bound': r.lower_bound}
        for r in model.reactions
}


def get_baseline_fluxes(model, obj_rxn_id='OF_ATP_mitoMap'):
    """Run pFBA at t=0 and return flux for every reaction.

    Used to set capacity-relative upper bounds: instead of scaling the
    arbitrary UB=1000, we scale the reaction's ACTUAL flux capacity.
    This makes the decay constraint bind from the first time step.
    """
    try:
        sol = pfba(model)
        return {r.id: abs(sol.fluxes.get(r.id, 0.0)) for r in model.reactions}
    except Exception:
        sol = model.optimize()
        return {r.id: abs(sol.fluxes.get(r.id, 0.0)) for r in model.reactions}


def apply_scenario_constraints(model, scenario):
    """
    Apply substrate exchange constraints for each scenario.

    Scenario A — Intracellular buffer: model defaults (no change)
    Scenario B — Arterial blood: constrain to physiological plasma concentrations
    Scenario C — Ischemic tissue: low O2, high lactate, low glucose

    Exchange reaction IDs are inferred from metabolite naming conventions in
    MitoMAMMAL. Actual IDs verified by inspecting model.reactions.
    Update these after model inspection if IDs differ.
    """
    if scenario == 'A':
        return  # use model defaults

    # Find exchange reactions by metabolite name patterns
    exchange_targets = {}
    if scenario == 'B':
        # Arterial blood concentrations (mM), from HMDB / literature
        # Lower bound = minimum uptake rate (negative = import into system)
        exchange_targets = {
            'pyr': -0.08,    # pyruvate ~0.08 mM arterial
            'o2':  -0.13,    # O2 ~0.13 mM arterial pO2
            'glc': -5.0,     # glucose ~5 mM
            'mal': -0.02,    # malate ~0.02 mM
            'lac': -1.5,     # lactate ~1.5 mM arterial
        }
    elif scenario == 'C':
        # Ischemic tissue: severely O2-limited, high lactate, low substrate
        exchange_targets = {
            'pyr': -0.01,    # pyruvate very low
            'o2':  -0.005,   # near-anoxic
            'glc': -0.5,     # glucose low
            'mal': -0.005,
            'lac': -8.0,     # lactate elevated
        }

    for rxn in model.reactions:
        if 'EX_' not in rxn.id and 'Exchange' not in rxn.id:
            continue
        rxn_id_lower = rxn.id.lower()
        for metabolite_key, lb in exchange_targets.items():
            if metabolite_key in rxn_id_lower:
                rxn.lower_bound = lb


def run_experiment(model, nuclear_genes, halflife_map, scenario,
                   t_max_hours=72, dt_hours=1.0,
                   obj_rxn_id='OF_ATP_mitoMap'):
    """
    Run time-stepped FBA for one substrate scenario.

    Returns:
        times: array of time points (hours)
        atp_fluxes: array of ATP flux at each time point
    """
    t_steps = np.arange(0, t_max_hours + dt_hours, dt_hours)
    atp_fluxes = []

    print(f"\n  Running Scenario {scenario} ({len(t_steps)} time steps)...")

    with model:  # outer context: apply scenario constraints
        apply_scenario_constraints(model, scenario)
        baseline_bounds = get_baseline_bounds(model)

        # Baseline at t=0 (no decay yet) — used for flux-relative scaling
        baseline_atp = get_atp_flux(model, obj_rxn_id)
        baseline_fluxes = get_baseline_fluxes(model, obj_rxn_id)
        print(f"  Baseline ATP flux (t=0, Scenario {scenario}): {baseline_atp:.4f}")

        for i, t in enumerate(t_steps):
            with model:  # inner context: apply decay at this time step
                apply_decay_to_model(model, nuclear_genes, halflife_map, t,
                                     baseline_bounds, baseline_fluxes)
                atp = get_atp_flux(model, obj_rxn_id)
                atp_fluxes.append(atp)

            if i % 12 == 0:
                print(f"    t={t:.1f}h  ATP={atp:.4f}  ({atp/baseline_atp*100:.1f}% of baseline)")

    return t_steps, np.array(atp_fluxes)


def find_transit_window(times, atp_fluxes, baseline_atp, threshold_fraction):
    """Return time at which ATP flux drops below threshold. None if never crossed."""
    threshold = baseline_atp * threshold_fraction
    for i, flux in enumerate(atp_fluxes):
        if flux < threshold:
            return times[i], threshold
    return None, baseline_atp * threshold_fraction


def plot_decay_curves(results, threshold_fraction, output_path):
    """Generate the killer figure: two panels.

    Left: Absolute ATP flux (shows substrate-limited capacity difference).
    Right: Normalized to t=0 baseline (shows transit window convergence).
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = {'A': '#2196F3', 'B': '#FF9800', 'C': '#F44336'}
    labels = {
        'A': 'Scenario A: Intracellular buffer\n(baseline = {:.1f})'.format(results['A']['baseline']),
        'B': 'Scenario B: Arterial blood\n(baseline = {:.2f})'.format(results['B']['baseline']),
        'C': 'Scenario C: Ischemic tissue\n(baseline = {:.2f})'.format(results['C']['baseline']),
    }
    linestyles = {'A': '-', 'B': '--', 'C': ':'}

    # ── Left panel: Absolute ATP flux (log scale) ─────────────────────────────
    for scenario in ['A', 'B', 'C']:
        r = results[scenario]
        ax1.semilogy(r['times'], np.maximum(r['atp_fluxes'], 1e-6),
                     color=colors[scenario],
                     linestyle=linestyles[scenario],
                     linewidth=2.5,
                     label=labels[scenario])
        # Threshold line per scenario
        threshold = r['baseline'] * threshold_fraction
        ax1.axhline(y=threshold, color=colors[scenario], alpha=0.3,
                    linewidth=1, linestyle='-.')
        # Mark transit window
        tw = r['transit_window_hours']
        if tw is not None:
            ax1.axvline(x=tw, color=colors[scenario], alpha=0.25, linewidth=1)

    ax1.set_xlabel('Time post-extraction (hours)', fontsize=11)
    ax1.set_ylabel('ATP flux (mmol/gDW/h, log scale)', fontsize=11)
    ax1.set_title('Absolute ATP Production\nacross substrate scenarios', fontsize=11)
    ax1.legend(loc='upper right', fontsize=8)
    ax1.set_xlim(0, results['A']['times'][-1])
    ax1.grid(True, alpha=0.3, which='both')
    ax1.annotate('Dashed lines: 20% reuptake\nviability threshold per scenario',
                 xy=(0.02, 0.02), xycoords='axes fraction', fontsize=7,
                 verticalalignment='bottom')

    # ── Right panel: Normalized (0-1) ─────────────────────────────────────────
    for scenario in ['A', 'B', 'C']:
        r = results[scenario]
        normalized = r['atp_fluxes'] / r['baseline']
        ax2.plot(r['times'], normalized,
                 color=colors[scenario],
                 linestyle=linestyles[scenario],
                 linewidth=2.5,
                 label=f'Scenario {scenario}')
        tw = r['transit_window_hours']
        if tw is not None:
            ax2.axvline(x=tw, color=colors[scenario], alpha=0.4, linewidth=1)
            ax2.annotate(f'  {tw:.0f}h', xy=(tw, threshold_fraction + 0.02),
                         fontsize=9, color=colors[scenario], fontweight='bold')

    ax2.axhline(y=threshold_fraction, color='black', linestyle='-.', linewidth=1.5,
                label=f'Threshold ({threshold_fraction*100:.0f}% of t=0)')
    ax2.fill_between(results['A']['times'], threshold_fraction, 0,
                     alpha=0.06, color='red', label='Non-viable zone')

    ax2.set_xlabel('Time post-extraction (hours)', fontsize=11)
    ax2.set_ylabel('Normalized ATP flux (fraction of t=0)', fontsize=11)
    ax2.set_title('Normalized ATP Decay\n(transit window convergence)', fontsize=11)
    ax2.legend(loc='upper right', fontsize=8)
    ax2.set_xlim(0, results['A']['times'][-1])
    ax2.set_ylim(-0.05, 1.12)
    ax2.grid(True, alpha=0.3)

    # ── Shared annotation ─────────────────────────────────────────────────────
    fig.suptitle(
        'Time-Dependent ATP Flux Decay in Extracted Mammalian Mitochondria\n'
        'MitoMAMMAL genome-scale model (560 rxns, 782 genes) · '
        f'Nuclear proteins: 769 · Half-life: {DEFAULT_HALFLIFE_HOURS}h (uniform, pre-empirical) · '
        f'{datetime.now().strftime("%Y-%m-%d")}',
        fontsize=10, y=1.01
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n  Figure saved: {output_path}")
    return fig


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("Experiment 1: Transit Viability Window")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Load model
    print("\n[1] Loading MitoMAMMAL model...")
    model = cobra.io.read_sbml_model(MODEL_PATH)
    print(f"    Reactions: {len(model.reactions)}, Genes: {len(model.genes)}, "
          f"Metabolites: {len(model.metabolites)}")

    # Classify genes
    print("\n[2] Classifying genes...")
    nuclear_genes = [g for g in model.genes if g.id not in MT_ENCODED_IDS]
    mt_genes = [g for g in model.genes if g.id in MT_ENCODED_IDS]
    print(f"    MT-encoded: {len(mt_genes)}, Nuclear: {len(nuclear_genes)}")

    # Load half-lives
    print("\n[3] Loading protein half-lives...")
    empirical_halflives = load_halflives_from_csv(HALFLIVES_PATH, model.genes)
    halflife_map = build_halflife_map(model, MT_ENCODED_IDS, empirical_halflives)
    print(f"    Half-life map: {len(halflife_map)} nuclear genes")
    unique_halflives = set(halflife_map.values())
    print(f"    Unique half-life values: {sorted(unique_halflives)}")

    # Get baseline (Scenario A, t=0)
    print("\n[4] Running baseline FBA (Scenario A, t=0)...")
    baseline_sol = model.optimize()
    BASELINE_ATP = baseline_sol.objective_value
    THRESHOLD = BASELINE_ATP * REUPTAKE_THRESHOLD_FRACTION
    print(f"    Baseline ATP flux: {BASELINE_ATP:.4f}")
    print(f"    Reuptake threshold ({REUPTAKE_THRESHOLD_FRACTION*100:.0f}%): {THRESHOLD:.4f}")

    # Run all three scenarios
    print("\n[5] Running time-stepped FBA (3 scenarios, t=0-72h)...")
    results = {}
    for scenario in ['A', 'B', 'C']:
        times, atp_fluxes = run_experiment(
            model, nuclear_genes, halflife_map,
            scenario=scenario,
            t_max_hours=72,
            dt_hours=1.0,
            obj_rxn_id='OF_ATP_mitoMap'
        )
        # Use SCENARIO-SPECIFIC baseline (atp_fluxes[0]) for threshold.
        # The transit window is defined relative to each scenario's own initial
        # ATP output — not relative to the intracellular buffer baseline.
        scenario_baseline = atp_fluxes[0]
        tw_time, tw_threshold = find_transit_window(
            times, atp_fluxes, scenario_baseline, REUPTAKE_THRESHOLD_FRACTION
        )
        results[scenario] = {
            'times': times,
            'atp_fluxes': atp_fluxes,
            'baseline': scenario_baseline,
            'transit_window_hours': tw_time,
        }
        # Use `is not None` to avoid Python truthiness bug with tw_time=0.0
        status = f"{tw_time:.1f}h" if tw_time is not None else ">72h (never crossed threshold)"
        print(f"\n  *** Scenario {scenario} transit window: {status} ***")

    # Save results CSV
    print("\n[6] Saving results...")
    rows = []
    for scenario, r in results.items():
        for t, flux in zip(r['times'], r['atp_fluxes']):
            rows.append({
                'scenario': scenario,
                'time_hours': t,
                'atp_flux': flux,
                'normalized_flux': flux / BASELINE_ATP,
            })
    df_out = pd.DataFrame(rows)
    csv_path = os.path.join(RESULTS_DIR, 'transit_window_results.csv')
    df_out.to_csv(csv_path, index=False)
    print(f"    CSV saved: {csv_path}")

    # Save summary JSON
    summary = {
        'run_date': datetime.now().isoformat(),
        'model': 'MitoMAMMAL 6_universal_mito_model.xml',
        'reactions': len(model.reactions),
        'genes_total': len(model.genes),
        'genes_nuclear': len(nuclear_genes),
        'genes_mt_encoded': len(mt_genes),
        'halflife_regime_hours': DEFAULT_HALFLIFE_HOURS,
        'empirical_halflives_loaded': len(empirical_halflives),
        'baseline_atp_flux': BASELINE_ATP,
        'reuptake_threshold_fraction': REUPTAKE_THRESHOLD_FRACTION,
        'transit_windows': {
            s: (r['transit_window_hours'] if r['transit_window_hours'] else '>72h')
            for s, r in results.items()
        }
    }
    json_path = os.path.join(RESULTS_DIR, 'experiment1_summary.json')
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"    Summary JSON: {json_path}")

    # Plot
    print("\n[7] Generating decay curve figure...")
    fig_path = os.path.join(RESULTS_DIR, 'decay_curves.png')
    plot_decay_curves(results, REUPTAKE_THRESHOLD_FRACTION, fig_path)

    # Final summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Model: MitoMAMMAL ({len(model.reactions)} reactions, {len(model.genes)} genes)")
    print(f"Nuclear proteins subject to decay: {len(nuclear_genes)}")
    print(f"Protein half-life (regime, pre-empirical): {DEFAULT_HALFLIFE_HOURS}h")
    print(f"Baseline ATP flux: {BASELINE_ATP:.4f}")
    print(f"Reuptake threshold: {THRESHOLD:.4f} ({REUPTAKE_THRESHOLD_FRACTION*100:.0f}% of baseline)")
    print()
    for scenario, r in results.items():
        tw = r['transit_window_hours']
        tw_str = f"{tw:.1f}h" if tw is not None else ">72h"
        print(f"  Scenario {scenario}: transit window = {tw_str}")
    print()
    print("Abstract language (fill in after DocInsight empirical data):")
    for scenario, r in results.items():
        tw = r['transit_window_hours']
        tw_str = f"approximately {tw:.0f} hours" if tw is not None else "greater than 72 hours"
        scen_names = {'A': 'intracellular buffer', 'B': 'arterial blood', 'C': 'ischemic tissue'}
        print(f"  Under {scen_names[scenario]} conditions, ATP flux falls below the")
        print(f"  estimated reuptake threshold at {tw_str} post-extraction.")
    print("=" * 60)

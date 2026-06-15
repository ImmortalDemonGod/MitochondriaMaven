"""
Experiment 1c: Half-Life Sweep — Transit Window vs Protein Stability
====================================================================
Vary the uniform nuclear protein half-life from 1h to 72h.
For each t½, run the full 72h time-stepped FBA (Scenario A).
Output: transit window vs t½ curve — the engineering design space.

This answers: "To achieve a transit window of N hours, proteins must be
stabilized to at least t½ = X hours."

Run with:
    /opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/python experiment1c_halflife_sweep.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cobra
from cobra.flux_analysis import pfba
import os, json
from datetime import datetime

MODEL_PATH = "/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml"
RESULTS_DIR = "/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

MT_ENCODED_IDS = {
    'ENSMUSG00000064341','ENSMUSG00000064345','ENSMUSG00000064351',
    'ENSMUSG00000064354','ENSMUSG00000064356','ENSMUSG00000064357',
    'ENSMUSG00000064358','ENSMUSG00000064360','ENSMUSG00000064363',
    'ENSMUSG00000064367','ENSMUSG00000064368','ENSMUSG00000064370',
    'ENSMUSG00000065947'
}
OBJ_RXN = 'OF_ATP_mitoMap'
REUPTAKE_THRESHOLD = 0.20

# Half-life values to sweep (hours)
HALFLIFE_SWEEP = [1, 2, 4, 6, 8, 12, 18, 24, 36, 48, 60, 72]


def run_sweep_point(model, nuclear_genes, baseline_fluxes, baseline_atp, t_half):
    """Run full 72h time-stepped FBA for a single uniform half-life value.

    Uses plain model.optimize() (not pFBA) in the inner loop — much faster
    when bounds collapse at low t½ values. pFBA only needed for baseline.
    """
    t_steps = np.arange(0, 73, 1.0)
    atp_fluxes = []
    threshold = baseline_atp * REUPTAKE_THRESHOLD

    with model:
        for t in t_steps:
            with model:
                df = np.exp(-np.log(2) * t / t_half)
                for gene in nuclear_genes:
                    for rxn in gene.reactions:
                        bflux = baseline_fluxes.get(rxn.id, 0.0)
                        if bflux > 1e-6:
                            rxn.upper_bound = max(0.0, bflux * 1.05 * df)
                        else:
                            rxn.upper_bound = max(0.0, rxn.upper_bound * df)
                sol = model.optimize()
                atp = sol.objective_value if sol.status == 'optimal' else 0.0
                atp_fluxes.append(atp)

                # Early exit: once we've dropped below threshold and it won't recover, stop
                if t > 5 and atp < threshold * 0.01:
                    # Fill remainder with 0
                    remaining = len(t_steps) - len(atp_fluxes)
                    atp_fluxes.extend([0.0] * remaining)
                    break

    atp_arr = np.array(atp_fluxes[:len(t_steps)])
    # Pad if early exit left array short
    if len(atp_arr) < len(t_steps):
        atp_arr = np.concatenate([atp_arr, np.zeros(len(t_steps) - len(atp_arr))])

    tw = None
    for i, flux in enumerate(atp_arr):
        if flux < threshold:
            tw = t_steps[i]
            break
    return tw, atp_arr


if __name__ == '__main__':
    print("=" * 60)
    print("Experiment 1c: Half-Life Sweep")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    model = cobra.io.read_sbml_model(MODEL_PATH)
    nuclear_genes = [g for g in model.genes if g.id not in MT_ENCODED_IDS]

    sol = pfba(model)
    baseline_atp = sol.fluxes.get(OBJ_RXN, 0.0)
    baseline_fluxes = {r.id: abs(sol.fluxes.get(r.id, 0.0)) for r in model.reactions}
    print(f"\nBaseline ATP: {baseline_atp:.4f}")
    print(f"Threshold (20%): {baseline_atp * REUPTAKE_THRESHOLD:.4f}")
    print(f"\nSweeping {len(HALFLIFE_SWEEP)} half-life values: {HALFLIFE_SWEEP}")

    records = []
    all_curves = {}

    for t_half in HALFLIFE_SWEEP:
        print(f"\n  t½ = {t_half:3d}h ...", end=' ', flush=True)
        tw, atp_arr = run_sweep_point(model, nuclear_genes, baseline_fluxes, baseline_atp, t_half)
        tw_str = f"{tw:.0f}h" if tw is not None else ">72h"
        print(f"transit window = {tw_str}")
        records.append({
            't_half_hours': t_half,
            'transit_window_hours': tw if tw is not None else 72.0,
            'transit_window_str': tw_str,
            'exceeded_72h': tw is None,
        })
        all_curves[t_half] = atp_arr

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(RESULTS_DIR, 'halflife_sweep.csv'), index=False)

    # Save all decay curves
    curve_df = pd.DataFrame(
        {f't_half_{th}h': all_curves[th] for th in HALFLIFE_SWEEP},
        index=np.arange(0, 73, 1.0)
    )
    curve_df.index.name = 'time_hours'
    curve_df.to_csv(os.path.join(RESULTS_DIR, 'halflife_sweep_curves.csv'))

    # ── Figure ───────────────────────────────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left: transit window vs half-life
    ax1.plot(df['t_half_hours'], df['transit_window_hours'],
             'o-', color='#2196F3', linewidth=2.5, markersize=8)
    ax1.axhline(y=72, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='72h limit')

    # Annotate key regime values
    for _, row in df.iterrows():
        if row['t_half_hours'] in [2, 12, 48]:
            ax1.annotate(f"  t½={row['t_half_hours']}h\n  →{row['transit_window_str']}",
                         xy=(row['t_half_hours'], row['transit_window_hours']),
                         fontsize=8, color='#333')

    ax1.set_xlabel('Nuclear protein half-life (hours)', fontsize=12)
    ax1.set_ylabel('Transit window (hours to 20% threshold)', fontsize=12)
    ax1.set_title('Engineering Design Space\nTransit Window vs Protein Stability', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 75)
    ax1.set_ylim(0, 80)

    # Shade regime regions
    ax1.axvspan(0, 4, alpha=0.07, color='#F44336', label='Fast regime (<4h)')
    ax1.axvspan(4, 24, alpha=0.07, color='#FF9800', label='Medium regime (4-24h)')
    ax1.axvspan(24, 75, alpha=0.07, color='#4CAF50', label='Slow regime (>24h)')
    ax1.legend(fontsize=8, loc='upper left')

    # Right: decay curves for select half-lives
    select = [2, 6, 12, 24, 48]
    colors = ['#F44336', '#FF5722', '#2196F3', '#4CAF50', '#1B5E20']
    t_steps = np.arange(0, 73, 1.0)

    for th, color in zip(select, colors):
        norm = all_curves[th] / baseline_atp
        ax2.plot(t_steps, norm, color=color, linewidth=2,
                 label=f't½ = {th}h → TW = {records[HALFLIFE_SWEEP.index(th)]["transit_window_str"]}')

    ax2.axhline(y=REUPTAKE_THRESHOLD, color='black', linestyle='-.', linewidth=1.5,
                label=f'{REUPTAKE_THRESHOLD*100:.0f}% threshold')
    ax2.fill_between(t_steps, REUPTAKE_THRESHOLD, 0, alpha=0.06, color='red')
    ax2.set_xlabel('Time post-extraction (hours)', fontsize=12)
    ax2.set_ylabel('Normalized ATP flux (fraction of t=0)', fontsize=12)
    ax2.set_title('Decay Curves at Selected Half-Lives', fontsize=12)
    ax2.legend(fontsize=8)
    ax2.set_xlim(0, 72)
    ax2.set_ylim(-0.05, 1.1)
    ax2.grid(True, alpha=0.3)

    fig.suptitle(
        'Experiment 1c: Half-Life Sweep — Transit Window Engineering Space\n'
        f'MitoMAMMAL · 769 nuclear genes · Scenario A (intracellular buffer) · '
        f'{datetime.now().strftime("%Y-%m-%d")}',
        fontsize=10, y=1.01
    )
    plt.tight_layout()
    fig_path = os.path.join(RESULTS_DIR, 'halflife_sweep_figure.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"\nFigure saved: {fig_path}")

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(df[['t_half_hours','transit_window_str']].to_string(index=False))

    print("\nAbstract language:")
    tw_12 = df[df['t_half_hours'] == 12]['transit_window_hours'].values[0]
    tw_2  = df[df['t_half_hours'] == 2]['transit_window_hours'].values[0]
    tw_48 = df[df['t_half_hours'] == 48]['transit_window_hours'].values[0]
    print(f"  Fast regime (t½ = 2h):   transit window ≈ {tw_2:.0f}h")
    print(f"  Medium regime (t½ = 12h): transit window ≈ {tw_12:.0f}h  ← baseline result")
    print(f"  Slow regime (t½ = 48h):  transit window ≈ {tw_48:.0f}h")
    print(f"  Extending protein half-life from 12h to 48h extends the transit window")
    print(f"  by {tw_48 - tw_12:.0f}h, establishing protein stability as the primary engineering lever.")
    print("=" * 60)

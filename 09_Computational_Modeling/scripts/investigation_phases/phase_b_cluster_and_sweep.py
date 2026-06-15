"""
Phase B.2 — Functional clustering of 145 essentials
Phase B.5 — Single-gene immortalization sweep over all 145

B.2 categorizes by gene symbol prefix (ETC structural vs assembly vs TCA vs transport)
B.5 runs 145 full time-stepped simulations, immortalizing one gene at a time,
    records Δtransit window. Ranks genes by solo leverage.
"""

import sys
from pathlib import Path
# Bootstrap: locate paths.py walking up the directory tree
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import MODEL_PATH, RESULTS_DIR, SUPP_TABLE_PATH, MITOMAMMAL_DIR, results_path



import json
import os
from datetime import datetime
import numpy as np
import pandas as pd
import cobra

from decay_utils import (
    MT_ENCODED_IDS, OBJ_ATP,
    get_signed_baseline_fluxes, build_decay_expr_dict,
    apply_gpr_aware_decay,
    configure_atp_objective,
    get_objective_flux, find_transit_window,
)

# MODEL_PATH imported from paths
# RESULTS_DIR imported from paths
ANNOTATED_PATH = results_path("essential_genes_annotated.csv")
PARTITION_PATH = results_path("essential_dispensable_partition.json")

UNIFORM_HALFLIFE = 12.0
T_MAX = 72.0
DT = 1.0
THRESHOLD_FRACTION = 0.20
BASELINE_TW = 29.0


# ─── B.2 — Functional clustering ──────────────────────────────────────────

def classify_gene(symbol, go_bp, go_cc):
    """Categorize a gene based on symbol prefix + GO terms."""
    sym = str(symbol).upper() if symbol and not isinstance(symbol, float) else ''
    go_bp = str(go_bp) if go_bp and not (isinstance(go_bp, float) and pd.isna(go_bp)) else ''
    go_cc = str(go_cc) if go_cc and not (isinstance(go_cc, float) and pd.isna(go_cc)) else ''

    # ETC structural subunits (Complex I-V)
    if sym.startswith('NDUF'):
        if 'AF' in sym or 'assembly' in (go_bp or '').lower():
            return 'CI assembly factor'
        return 'CI structural'
    if sym.startswith(('SDHA', 'SDHB', 'SDHC', 'SDHD', 'SDHAF')):
        return 'CII structural/assembly'
    if sym.startswith('UQCR') or sym == 'CYC1':
        return 'CIII structural'
    if sym.startswith('TTC') and 'cytochrome' in (go_bp or '').lower():
        return 'CIII assembly factor'
    if sym.startswith('BCS1'):
        return 'CIII assembly factor'
    if sym.startswith(('COX', 'SURF1', 'SCO1', 'SCO2', 'COA')):
        if sym.startswith(('COX')) and any(sym.endswith(suf) for suf in
                                            ['4', '5A', '5B', '6A', '6B', '6C', '7A', '7B', '7C', '8A', '8B']):
            return 'CIV structural'
        if sym.startswith('COX') and any(x in sym for x in ['10', '11', '15', '17', '19', '20']):
            return 'CIV assembly factor'
        return 'CIV assembly factor'
    if sym.startswith('ATP5') or sym.startswith('USMG') or sym.startswith('MT-ATP'):
        return 'CV structural'
    if sym in ('TMEM70', 'ATPAF1', 'ATPAF2'):
        return 'CV assembly factor'

    # TCA cycle
    if any(x in sym for x in ['CS', 'ACO2', 'IDH', 'OGDH', 'SUCLA', 'SUCLG', 'FH']):
        return 'TCA cycle'
    if sym in ('MDH2', 'MDH1'):
        return 'TCA cycle'

    # Transporters (SLC25 family)
    if sym.startswith('SLC25'):
        return 'SLC25 transporter'

    # Mitoribosomal
    if sym.startswith(('MRPL', 'MRPS')):
        return 'Mitoribosomal'

    # Fatty acid oxidation
    if any(sym.startswith(x) for x in ['ACAD', 'HADH', 'ECH', 'CPT', 'ACSS', 'ACSL']):
        return 'Fatty acid oxidation'

    # Other mitochondrial
    if 'mitochond' in (go_cc or '').lower():
        return 'Other mitochondrial'

    return 'Other / non-mitochondrial'


def phase_b2_clustering():
    print("[B.2] Functional clustering of essentials...")
    df = pd.read_csv(ANNOTATED_PATH)

    df['category'] = df.apply(
        lambda r: classify_gene(r['gene_symbol'], r.get('GO_biological_process', ''),
                                r.get('GO_cellular_component', '')),
        axis=1
    )

    print(f"\nFunctional distribution of {len(df)} essential genes:")
    counts = df['category'].value_counts()
    print(counts.to_string())

    # Mitochondrial vs non
    mito_count = df['GO_cellular_component'].str.contains('mitochond', case=False, na=False).sum()
    print(f"\n{mito_count}/{len(df)} ({mito_count/len(df)*100:.0f}%) annotated with mitochondrial GO cellular component")

    # Save clustered df
    df.to_csv(results_path("phase_b", "essential_genes_clustered.csv"), index=False)

    return df, counts


# ─── B.5 — Single-gene immortalization sweep ──────────────────────────────

def phase_b5_sweep(essential_df):
    print("\n[B.5] Single-gene immortalization sweep (145 simulations)...")

    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)
    baseline_fluxes = get_signed_baseline_fluxes(model)
    baseline_atp = baseline_fluxes[OBJ_ATP]
    threshold = baseline_atp * THRESHOLD_FRACTION
    print(f"  Baseline ATP: {baseline_atp:.4f}, threshold: {threshold:.4f}")

    essential_ids = essential_df['ensembl_id'].tolist()
    t_steps = np.arange(0, T_MAX + DT, DT)

    # Warm-up: get the full-decay reference curve
    print("  Running full-decay reference (all mouse nuclear at t½=12h)...")
    all_nuclear = [g.id for g in model.genes if g.id.startswith('ENSMUSG') and g.id not in MT_ENCODED_IDS]
    full_halflife = {g.id: UNIFORM_HALFLIFE for g in model.genes}
    full_curve = []
    with model:
        for t in t_steps:
            with model:
                expr = build_decay_expr_dict(model, full_halflife, t)
                apply_gpr_aware_decay(model, expr, baseline_fluxes)
                full_curve.append(get_objective_flux(model, 'atp'))
    full_tw = find_transit_window(t_steps, np.array(full_curve), baseline_atp, THRESHOLD_FRACTION)
    print(f"  Full-decay transit window: {full_tw:.1f}h (should match baseline 29h)")

    # Sweep: for each essential, set its t½=∞ alone, see how much TW extends
    records = []
    for i, gene_id in enumerate(essential_ids):
        if i % 20 == 0:
            print(f"  {i}/{len(essential_ids)} ...")

        halflife_map = {g.id: UNIFORM_HALFLIFE for g in model.genes}
        halflife_map[gene_id] = 1e9  # immortal

        curve = []
        with model:
            for t in t_steps:
                with model:
                    expr = build_decay_expr_dict(model, halflife_map, t)
                    apply_gpr_aware_decay(model, expr, baseline_fluxes)
                    atp = get_objective_flux(model, 'atp')
                    curve.append(atp)
                    if atp < threshold * 0.01 and t > 5:
                        curve.extend([0.0] * (len(t_steps) - len(curve)))
                        break
        curve = np.array(curve[:len(t_steps)])
        if len(curve) < len(t_steps):
            curve = np.concatenate([curve, np.zeros(len(t_steps) - len(curve))])

        tw = find_transit_window(t_steps, curve, baseline_atp, THRESHOLD_FRACTION)
        delta_tw = (tw - full_tw) if (tw is not None and full_tw is not None) else None
        records.append({
            'ensembl_id': gene_id,
            'tw_hours': tw if tw is not None else 72.0,
            'delta_tw_hours': delta_tw if delta_tw is not None else (72.0 - full_tw),
            'tw_exceeds_72h': tw is None,
        })

    sweep_df = pd.DataFrame(records)
    # Join with annotations
    sweep_df = sweep_df.merge(essential_df[['ensembl_id', 'gene_symbol', 'full_name', 'complex', 'atp_impact_pct']],
                              on='ensembl_id', how='left')
    sweep_df = sweep_df.sort_values('delta_tw_hours', ascending=False).reset_index(drop=True)
    sweep_df.insert(0, 'rank', range(1, len(sweep_df) + 1))

    out_path = results_path("phase_b", "single_gene_leverage.csv")
    sweep_df.to_csv(out_path, index=False)
    print(f"  ✓ Saved: {out_path}")

    return sweep_df, full_tw


# ─── Main ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print(f"Phase B.2 + B.5 — {datetime.now().isoformat()}")
    print("=" * 60)

    df_clustered, cluster_counts = phase_b2_clustering()

    sweep_df, full_tw = phase_b5_sweep(df_clustered)

    print("\n" + "=" * 60)
    print("SINGLE-GENE LEVERAGE RESULTS")
    print("=" * 60)
    print(f"\nFull-decay reference transit window: {full_tw:.1f}h")
    print(f"\nTop 15 genes by Δtransit window when immortalized alone:")
    print(sweep_df.head(15)[['rank', 'gene_symbol', 'complex', 'atp_impact_pct', 'delta_tw_hours']].to_string(index=False))

    # Distribution
    print(f"\nDistribution of Δtransit:")
    print(f"  Δ = 0h (no solo effect):       {(sweep_df['delta_tw_hours'] == 0).sum()}")
    print(f"  0 < Δ ≤ 1h (minor):            {((sweep_df['delta_tw_hours'] > 0) & (sweep_df['delta_tw_hours'] <= 1)).sum()}")
    print(f"  1 < Δ ≤ 5h (moderate):         {((sweep_df['delta_tw_hours'] > 1) & (sweep_df['delta_tw_hours'] <= 5)).sum()}")
    print(f"  5 < Δ ≤ 10h (significant):     {((sweep_df['delta_tw_hours'] > 5) & (sweep_df['delta_tw_hours'] <= 10)).sum()}")
    print(f"  Δ > 10h (bottleneck):          {(sweep_df['delta_tw_hours'] > 10).sum()}")

    # Save a summary
    summary = {
        'run_date': datetime.now().isoformat(),
        'full_decay_tw': full_tw,
        'functional_cluster_counts': cluster_counts.to_dict(),
        'leverage_tier_distribution': {
            'zero_effect': int((sweep_df['delta_tw_hours'] == 0).sum()),
            'minor_0_1h': int(((sweep_df['delta_tw_hours'] > 0) & (sweep_df['delta_tw_hours'] <= 1)).sum()),
            'moderate_1_5h': int(((sweep_df['delta_tw_hours'] > 1) & (sweep_df['delta_tw_hours'] <= 5)).sum()),
            'significant_5_10h': int(((sweep_df['delta_tw_hours'] > 5) & (sweep_df['delta_tw_hours'] <= 10)).sum()),
            'bottleneck_gt_10h': int((sweep_df['delta_tw_hours'] > 10).sum()),
        },
    }
    with open(results_path("phase_b", "phase_b_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n✓ Summary saved")

"""
Experiment 1b v2 — GPR-aware gene knockout scoring (corrected)
==============================================================
Fixes the v1 bug where setting UB=0 on all a gene's reactions over-killed
OR-rule reactions whose isozyme partners could still catalyze.

Method: for each nuclear gene, set its "expression" to 0 while all others
are 1.0, then evaluate reaction bounds through GPR (AND=min, OR=sum).
A reaction dies only if ALL AND-subunits require this gene or ALL OR-branches
contain this gene exclusively.

Output:
  results/gene_knockout_scores_v2.csv — corrected impact per gene
  results/experiment1b_v2_summary.json — before/after comparison

Run:
  /opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/python experiment1b_v2_gpr_knockout.py
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



import os, json
from datetime import datetime
import numpy as np
import pandas as pd
import cobra

from decay_utils import (
    MT_ENCODED_IDS, OBJ_ATP,
    get_signed_baseline_fluxes, apply_gpr_aware_decay,
)

# MODEL_PATH imported from paths
# RESULTS_DIR imported from paths


def run_gpr_aware_ko(model, nuclear_genes, baseline_fluxes, baseline_atp):
    """For each nuclear gene, knock out by setting its expr=0, let GPR handle the rest."""
    records = []
    # All genes "fully expressed" at baseline
    base_expr = {g.id: 1.0 for g in model.genes}

    n = len(nuclear_genes)
    for i, gene in enumerate(nuclear_genes):
        if i % 50 == 0:
            print(f"  {i}/{n} ...")

        expr = dict(base_expr)
        expr[gene.id] = 0.0  # protein absent

        with model:
            apply_gpr_aware_decay(model, expr, baseline_fluxes)
            sol = model.optimize()
            atp = sol.fluxes.get(OBJ_ATP, 0.0) if sol.status == 'optimal' else 0.0

        impact = baseline_atp - atp
        impact_pct = (impact / baseline_atp * 100) if baseline_atp > 0 else 0.0

        # Complex membership (by gene-reaction mapping)
        complexes = []
        for complex_name, rid in [('Complex I', 'CI_mitoMap'), ('Complex II', 'CII_mitoMap'),
                                   ('Complex III', 'CIII_mitoMap'), ('Complex IV', 'CIV_mitoMap'),
                                   ('Complex V', 'CV_mitoMap'),
                                   ('ATPtranslocase', 'ATPtmB_mitoMap')]:
            try:
                if gene in model.reactions.get_by_id(rid).genes:
                    complexes.append(complex_name)
            except KeyError:
                pass

        records.append({
            'gene_id': gene.id,
            'species': 'mouse' if gene.id.startswith('ENSMUSG') else 'human',
            'n_reactions': len(gene.reactions),
            'atp_after_ko': round(atp, 6),
            'atp_impact': round(impact, 6),
            'atp_impact_pct': round(impact_pct, 4),
            'complex': ', '.join(complexes) if complexes else 'Other',
        })

    df = pd.DataFrame(records).sort_values('atp_impact', ascending=False).reset_index(drop=True)
    df.insert(0, 'rank', range(1, len(df) + 1))
    return df


if __name__ == '__main__':
    print("=" * 60)
    print("Experiment 1b v2: GPR-aware gene knockout scoring")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    print("\n[1] Loading model...")
    model = cobra.io.read_sbml_model(MODEL_PATH)
    nuclear_genes = [g for g in model.genes if g.id not in MT_ENCODED_IDS]
    print(f"   Nuclear genes: {len(nuclear_genes)}")

    # Separate by species for reporting
    mouse_nuclear = [g for g in nuclear_genes if g.id.startswith('ENSMUSG')]
    human_nuclear = [g for g in nuclear_genes if g.id.startswith('ENSG')]
    print(f"   Mouse: {len(mouse_nuclear)}, Human: {len(human_nuclear)}")

    print("\n[2] Baseline FBA...")
    baseline_fluxes = get_signed_baseline_fluxes(model)
    baseline_atp = baseline_fluxes[OBJ_ATP]
    print(f"   Baseline ATP: {baseline_atp:.4f}")

    print(f"\n[3] GPR-aware knockout scoring (using ignore_species_prefix='ENSG' by default)...")
    df = run_gpr_aware_ko(model, nuclear_genes, baseline_fluxes, baseline_atp)

    # Save
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = results_path("experiments_v2", "gene_knockout_scores_v2.csv")
    df.to_csv(out_path, index=False)
    print(f"\n   Saved: {out_path}")

    # Compare against v1
    v1_path = results_path("experiments_v2", "gene_knockout_scores.csv")
    if os.path.exists(v1_path):
        v1 = pd.read_csv(v1_path)
        print("\n[4] Comparison vs v1 (buggy)...")
        v1_zero = (v1['atp_impact'] == 0).sum()
        v2_zero = (df['atp_impact'] == 0).sum()
        print(f"   v1 dispensable (zero impact): {v1_zero}/{len(v1)}")
        print(f"   v2 dispensable (zero impact): {v2_zero}/{len(df)}")
        print(f"   Δ (v2 - v1): {v2_zero - v1_zero:+d} genes")
        print()
        v1_strong = (v1['atp_impact_pct'] > 90).sum()
        v2_strong = (df['atp_impact_pct'] > 90).sum()
        print(f"   v1 strong essential (>90% impact): {v1_strong}")
        print(f"   v2 strong essential (>90% impact): {v2_strong}")

    # Species breakdown (since mouse-only GPR was used)
    mouse_df = df[df['species'] == 'mouse']
    human_df = df[df['species'] == 'human']
    print("\n[5] Species breakdown of v2 results:")
    print(f"   Mouse genes: {len(mouse_df)} | dispensable (zero impact): {(mouse_df['atp_impact'] == 0).sum()}")
    print(f"   Human genes: {len(human_df)} | dispensable (zero impact): {(human_df['atp_impact'] == 0).sum()}")
    print(f"   (All human genes should show zero impact since ENSG branch was stripped from GPR)")

    # Summary numbers
    mouse_dispensable = (mouse_df['atp_impact'] == 0).sum()
    mouse_essential = len(mouse_df) - mouse_dispensable
    print("\n[6] CORRECTED A3 test result (mouse nuclear genes only):")
    print(f"   Mouse nuclear total: {len(mouse_df)}")
    print(f"   Dispensable: {mouse_dispensable} ({mouse_dispensable / len(mouse_df) * 100:.1f}%)")
    print(f"   Essential:   {mouse_essential} ({mouse_essential / len(mouse_df) * 100:.1f}%)")

    print("\n   Top 10 mouse essentials by impact:")
    print(mouse_df[mouse_df['atp_impact'] > 0].head(10)[
        ['rank', 'gene_id', 'complex', 'atp_impact_pct']
    ].to_string(index=False))

    # Save summary
    summary = {
        'run_date': datetime.now().isoformat(),
        'method': 'GPR-aware (E-Flux min/sum, human ENSG stripped)',
        'total_nuclear_genes': len(nuclear_genes),
        'mouse_nuclear': len(mouse_df),
        'human_nuclear': len(human_df),
        'mouse_dispensable': int(mouse_dispensable),
        'mouse_essential': int(mouse_essential),
        'mouse_strong_essential_90pct': int((mouse_df['atp_impact_pct'] > 90).sum()),
        'baseline_atp': baseline_atp,
    }
    with open(results_path("experiments_v2", "experiment1b_v2_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print(f"DONE. Saved to {out_path}")
    print("=" * 60)

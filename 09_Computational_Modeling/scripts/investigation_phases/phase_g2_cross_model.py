"""
Phase G.2 — Cross-model validation in Human-GEM mitochondrial subset.

Question: do our findings (29h algebraic, heterogeneity → 8h, ~150 essentials)
hold in a different mammalian metabolic model?

Method: filter Human-GEM (SysBioChalmers) for mitochondrial compartment ('m').
Replicate baseline FBA + uniform decay + heterogeneous decay test.
"""

import sys
from pathlib import Path
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import PROJECT_ROOT, results_path

import json
import numpy as np
import cobra

HUMAN_GEM_PATH = PROJECT_ROOT / "Whole_Cell_Modeling" / "Human-GEM" / "model" / "Human-GEM.xml"


def main():
    print("Phase G.2 — Human-GEM cross-validation")
    print("=" * 60)

    print("Loading Human-GEM (this may take a minute)...")
    model = cobra.io.read_sbml_model(str(HUMAN_GEM_PATH))
    print(f"  Reactions: {len(model.reactions)}")
    print(f"  Metabolites: {len(model.metabolites)}")
    print(f"  Genes: {len(model.genes)}")
    print(f"  Compartments: {model.compartments}")

    # Identify mitochondrial reactions
    # In Human-GEM, compartments are encoded in metabolite IDs (e.g., MAM00001m for mitochondrial)
    mito_compartment_codes = ['m', 'MAM']  # try common names
    mito_mets = set()
    for m in model.metabolites:
        if m.compartment and ('m' == m.compartment.lower() or 'mito' in m.compartment.lower()):
            mito_mets.add(m.id)
    print(f"\n  Mitochondrial metabolites: {len(mito_mets)}")
    if mito_mets:
        print(f"  Sample: {list(mito_mets)[:5]}")

    # Mitochondrial reactions = those with at least one mitochondrial metabolite
    mito_rxns = [r for r in model.reactions
                 if any(m.id in mito_mets for m in r.metabolites)]
    print(f"  Reactions touching mitochondrion: {len(mito_rxns)}")

    # Identify ETC complexes (look for OXPHOS-related reactions)
    etc_keywords = ['complex', 'oxphos', 'cytochrome', 'nadh', 'atp synth']
    etc_rxns = [r for r in mito_rxns
                if any(kw in (r.name or '').lower() for kw in etc_keywords)]
    print(f"\n  Likely ETC reactions: {len(etc_rxns)}")
    for r in etc_rxns[:10]:
        print(f"    {r.id}: {r.name[:60] if r.name else '(no name)'}")

    # Try to find baseline ATP flux via standard objective
    print("\nAttempting baseline FBA...")
    try:
        sol = model.optimize()
        print(f"  Status: {sol.status}, objective: {sol.objective_value:.4f}")
    except Exception as e:
        print(f"  ERROR: {e}")
        return

    # Find ATP-related reactions
    atp_rxns = [r for r in model.reactions
                if 'atp' in r.id.lower() and r.id not in ['biomass_human', 'biomass_components']]
    print(f"\n  ATP-related reactions: {len(atp_rxns)}")

    # Save initial inspection
    summary = {
        'model': 'Human-GEM',
        'reactions': len(model.reactions),
        'metabolites': len(model.metabolites),
        'genes': len(model.genes),
        'mito_metabolites': len(mito_mets),
        'mito_reactions': len(mito_rxns),
        'etc_candidates': len(etc_rxns),
        'baseline_objective': float(sol.objective_value),
    }
    with open(results_path('phase_g', 'g2_human_gem_inspection.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n✓ Initial inspection saved.")
    print("Next step: deep gene essentiality analysis on mito subset (TBD).")
    print("\nKey question: does Human-GEM mito subset reproduce the FBA-as-algebra finding?")


if __name__ == '__main__':
    main()

"""
Phase A: Open the Black Box — mechanistic dissection of MitoMAMMAL.

Runs A.1 through A.5:
  A.1 — Trace ATP synthesis end-to-end through baseline FBA
  A.2 — Decode the PMF (proton-motive-force) abstraction
  A.3 — Decode all four objective functions
  A.4 — Map every exchange reaction
  A.5 — Compartmentalization audit

Output: MITOMAMMAL_DISSECTION.md with complete baseline biochemistry trace.
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
from paths import MODEL_PATH, RESULTS_DIR, SUPP_TABLE_PATH, MITOMAMMAL_DIR, results_path, investigation_doc



import cobra
from cobra.flux_analysis import pfba
import os
import json
import pandas as pd
from collections import defaultdict
from datetime import datetime

# MODEL_PATH imported from paths
OUTPUT_PATH = investigation_doc("MITOMAMMAL_DISSECTION.md")

FLUX_THRESHOLD = 0.01  # ignore fluxes this small for readability


def fmt_rxn(rxn, flux=None):
    flux_str = f"  flux={flux:+.3f}" if flux is not None else ""
    return f"{rxn.id:30s}  {rxn.reaction[:80]}{flux_str}"


def trace_metabolite_flux(sol, model, met_id, direction='producers'):
    """Return list of (reaction, stoichiometric_flux) for producers or consumers of met."""
    try:
        met = model.metabolites.get_by_id(met_id)
    except KeyError:
        return []
    results = []
    for rxn in met.reactions:
        flux = sol.fluxes.get(rxn.id, 0)
        stoich = rxn.metabolites[met]  # signed
        effective = stoich * flux  # positive = produces met
        if direction == 'producers' and effective > FLUX_THRESHOLD:
            results.append((rxn, effective))
        elif direction == 'consumers' and effective < -FLUX_THRESHOLD:
            results.append((rxn, effective))
    return sorted(results, key=lambda x: abs(x[1]), reverse=True)


def main():
    print("Phase A — MitoMAMMAL Dissection")
    print("=" * 60)

    model = cobra.io.read_sbml_model(MODEL_PATH)
    print(f"Loaded: {len(model.reactions)} rxns, {len(model.metabolites)} mets, {len(model.genes)} genes")
    print(f"Compartments: {model.compartments}")

    print("\nRunning baseline pFBA...")
    sol = pfba(model)
    print(f"Objective value: {sol.objective_value:.4f}, status: {sol.status}")

    out = []
    out.append(f"# MitoMAMMAL Dissection — Baseline Biochemistry Trace")
    out.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    out.append(f"**Model:** `6_universal_mito_model.xml` (from Chapman et al. 2024)")
    out.append(f"**Baseline solution:** pFBA, objective `OF_ATP_mitoMap` = {sol.fluxes['OF_ATP_mitoMap']:.4f}")
    out.append("")
    out.append("**Purpose:** Before running more experiments on this model, understand what it actually computes. This document traces the baseline FBA solution reaction-by-reaction to document the biochemistry, the abstractions, and the structural features that matter for our transit viability work.")
    out.append("")
    out.append("---")

    # ─── A.1 — Trace ATP synthesis end-to-end ──────────────────────────────
    print("\n[A.1] Tracing ATP synthesis end-to-end...")
    out.append("\n## A.1 — ATP Synthesis Pathway Trace")
    out.append("")
    out.append("Following the ATP molecule backwards from the objective to external substrates.")
    out.append("")

    # atp_c producers
    out.append("### Who produces cytoplasmic ATP (`atp_c`)?")
    producers = trace_metabolite_flux(sol, model, 'atp_c', 'producers')
    for rxn, flux in producers[:10]:
        out.append(f"- `{rxn.id}` ({flux:+.3f} atp_c/h): {rxn.reaction}")
    out.append("")

    out.append("### Who consumes cytoplasmic ATP (`atp_c`)?")
    consumers = trace_metabolite_flux(sol, model, 'atp_c', 'consumers')
    for rxn, flux in consumers[:10]:
        out.append(f"- `{rxn.id}` ({flux:+.3f} atp_c/h): {rxn.reaction}")
    out.append("")

    # Matrix ATP
    out.append("### Who produces matrix ATP (`atp_m`)?")
    prod_m = trace_metabolite_flux(sol, model, 'atp_m', 'producers')
    for rxn, flux in prod_m[:10]:
        out.append(f"- `{rxn.id}` ({flux:+.3f} atp_m/h): {rxn.reaction}")
    out.append("")

    out.append("### Who consumes matrix ATP (`atp_m`)?")
    cons_m = trace_metabolite_flux(sol, model, 'atp_m', 'consumers')
    for rxn, flux in cons_m[:10]:
        out.append(f"- `{rxn.id}` ({flux:+.3f} atp_m/h): {rxn.reaction}")
    out.append("")

    # Key intermediates
    out.append("### Reducing equivalent inputs — NADH")
    out.append("")
    out.append("**Matrix NADH producers (top 5):**")
    for rxn, flux in trace_metabolite_flux(sol, model, 'nadh_m', 'producers')[:5]:
        out.append(f"- `{rxn.id}` ({flux:+.3f}): {rxn.reaction[:90]}")
    out.append("")
    out.append("**Matrix NADH consumers (top 5):**")
    for rxn, flux in trace_metabolite_flux(sol, model, 'nadh_m', 'consumers')[:5]:
        out.append(f"- `{rxn.id}` ({flux:+.3f}): {rxn.reaction[:90]}")
    out.append("")

    # FADH2 via ubiquinol q10h2_m
    out.append("### Reducing equivalent inputs — ubiquinol (electron carrier after CII)")
    out.append("")
    try:
        out.append("**q10h2_m producers:**")
        for rxn, flux in trace_metabolite_flux(sol, model, 'q10h2_m', 'producers')[:5]:
            out.append(f"- `{rxn.id}` ({flux:+.3f}): {rxn.reaction[:90]}")
        out.append("")
        out.append("**q10h2_m consumers:**")
        for rxn, flux in trace_metabolite_flux(sol, model, 'q10h2_m', 'consumers')[:5]:
            out.append(f"- `{rxn.id}` ({flux:+.3f}): {rxn.reaction[:90]}")
    except Exception as e:
        out.append(f"(q10h2_m not found: {e})")
    out.append("")

    # ETC flux summary
    out.append("### ETC complex flux summary (baseline)")
    out.append("")
    out.append("| Reaction | Flux | Role |")
    out.append("|---|---|---|")
    for rid, role in [('CI_mitoMap', 'NADH→Q, pumps PMF'),
                      ('CII_mitoMap', 'FADH2→Q (no pumping)'),
                      ('CIII_mitoMap', 'QH2→cyt c, pumps PMF'),
                      ('CIV_mitoMap', 'cyt c→O2, pumps PMF'),
                      ('CV_mitoMap', 'ADP+Pi→ATP, consumes PMF'),
                      ('ATPtmB_mitoMap', 'ATP/ADP exchange, consumes PMF'),
                      ('OF_ATP_mitoMap', 'cytoplasmic ATP hydrolysis (objective)')]:
        try:
            f = sol.fluxes[rid]
            out.append(f"| `{rid}` | {f:+.3f} | {role} |")
        except KeyError:
            out.append(f"| `{rid}` | N/A | (not found) |")
    out.append("")

    # ─── A.2 — Decode PMF abstraction ──────────────────────────────────────
    print("\n[A.2] Decoding PMF abstraction...")
    out.append("\n---\n")
    out.append("## A.2 — PMF (Proton-Motive-Force) Abstraction\n")
    out.append("MitoMAMMAL uses abstract `PMF_m` and `PMF_c` metabolites instead of explicit proton stoichiometry across compartments. Here's what these currencies do at baseline.")
    out.append("")

    for pmf_id in ['PMF_m', 'PMF_c']:
        try:
            met = model.metabolites.get_by_id(pmf_id)
            out.append(f"### `{pmf_id}`")
            out.append("")
            out.append(f"**Producers (stoich × flux > 0):**")
            total_prod = 0
            for rxn, net in trace_metabolite_flux(sol, model, pmf_id, 'producers'):
                stoich = rxn.metabolites[met]
                out.append(f"- `{rxn.id}` (stoich={stoich:+.3f}, flux={sol.fluxes[rxn.id]:+.3f}, produces {net:+.3f} {pmf_id}/h)")
                total_prod += net
            out.append(f"**Total {pmf_id} production: {total_prod:+.3f}/h**")
            out.append("")
            out.append(f"**Consumers (stoich × flux < 0):**")
            total_cons = 0
            for rxn, net in trace_metabolite_flux(sol, model, pmf_id, 'consumers'):
                stoich = rxn.metabolites[met]
                out.append(f"- `{rxn.id}` (stoich={stoich:+.3f}, flux={sol.fluxes[rxn.id]:+.3f}, consumes {net:+.3f} {pmf_id}/h)")
                total_cons += net
            out.append(f"**Total {pmf_id} consumption: {total_cons:+.3f}/h**")
            out.append(f"**Steady-state balance (should be ~0): {total_prod + total_cons:+.6f}**")
            out.append("")
        except KeyError:
            out.append(f"### `{pmf_id}` NOT PRESENT in model")
            out.append("")

    # ─── A.3 — Decode objective functions ──────────────────────────────────
    print("\n[A.3] Decoding objective functions...")
    out.append("\n---\n")
    out.append("## A.3 — Objective Functions\n")
    of_rxns = [r for r in model.reactions if r.id.startswith('OF_')]
    out.append(f"Model has {len(of_rxns)} objective functions (artificial sinks representing biomass demand):\n")
    for rxn in of_rxns:
        out.append(f"### `{rxn.id}` — {rxn.name}")
        out.append(f"- Stoichiometry: `{rxn.reaction}`")
        out.append(f"- Bounds: ({rxn.lower_bound}, {rxn.upper_bound})")
        out.append(f"- Baseline flux: {sol.fluxes[rxn.id]:+.3f}")
        out.append(f"- Is current objective? {rxn.id in [r.id for r in model.reactions if rxn in cobra.util.solver.linear_reaction_coefficients(model)]}")
        out.append("")

    # biomass_c investigation — the anomaly
    out.append("### The `biomass_c` mystery")
    out.append("`OF_ATP_mitoMap` produces `biomass_c` — what happens to it?\n")
    try:
        met = model.metabolites.get_by_id('biomass_c')
        out.append(f"**`biomass_c` metabolite:** {met.name or '(no name)'}")
        out.append(f"**Reactions touching biomass_c:**")
        for rxn in met.reactions:
            stoich = rxn.metabolites[met]
            flux = sol.fluxes[rxn.id]
            out.append(f"- `{rxn.id}` (stoich={stoich:+.1f}, flux={flux:+.3f})")
    except KeyError:
        out.append("`biomass_c` not a distinct metabolite (may be a named placeholder)")
    out.append("")

    # ─── A.4 — Exchange reactions ──────────────────────────────────────────
    print("\n[A.4] Mapping exchange reactions...")
    out.append("\n---\n")
    out.append("## A.4 — Exchange Reactions (Model Boundary)\n")
    ex_rxns = [r for r in model.reactions if r.id.startswith('EX_')]
    out.append(f"Model has {len(ex_rxns)} exchange reactions. Active ones at baseline (|flux| > {FLUX_THRESHOLD}):\n")
    out.append("| Reaction | Metabolite | Flux | Direction |")
    out.append("|---|---|---|---|")
    for rxn in sorted(ex_rxns, key=lambda r: abs(sol.fluxes[r.id]), reverse=True):
        flux = sol.fluxes[rxn.id]
        if abs(flux) < FLUX_THRESHOLD:
            continue
        # Exchange reactions typically have one external metabolite
        mets = list(rxn.metabolites.keys())
        met_name = mets[0].id if mets else '?'
        direction = 'import' if flux < 0 else 'export'
        out.append(f"| `{rxn.id}` | {met_name} | {flux:+.3f} | {direction} |")
    out.append("")

    # Count blocked/default-unlimited
    active = sum(1 for r in ex_rxns if abs(sol.fluxes[r.id]) > FLUX_THRESHOLD)
    out.append(f"**Summary:** {active} active out of {len(ex_rxns)} exchange reactions. "
               f"Most exchanges default to `lb=-1000, ub=1000` (unlimited), so substrate choice is driven by what pFBA finds optimal.")
    out.append("")

    # ─── A.5 — Compartmentalization ────────────────────────────────────────
    print("\n[A.5] Auditing compartmentalization...")
    out.append("\n---\n")
    out.append("## A.5 — Compartmentalization\n")
    out.append(f"**Compartments defined:** {model.compartments}\n")

    # Count metabolites per compartment
    comp_counts = defaultdict(int)
    for m in model.metabolites:
        comp_counts[m.compartment] += 1
    out.append("**Metabolites per compartment:**")
    for c, n in sorted(comp_counts.items()):
        name = model.compartments.get(c, '(unnamed)')
        out.append(f"- `{c}` ({name}): {n} metabolites")
    out.append("")

    # Transport reactions (change compartment)
    transport_count = 0
    for rxn in model.reactions:
        comps = set(m.compartment for m in rxn.metabolites)
        if len(comps) > 1:
            transport_count += 1
    out.append(f"**Transport reactions (span >1 compartment):** {transport_count} of {len(model.reactions)}\n")

    # ─── Summary ──────────────────────────────────────────────────────────
    out.append("\n---\n")
    out.append("## Summary: What MitoMAMMAL Actually Computes\n")
    out.append("**At baseline (Scenario A, OF_ATP_mitoMap objective):**")
    out.append(f"1. External substrate uptake via active exchanges: see A.4")
    out.append(f"2. Matrix oxidation generates NADH (flux through TCA, BCAA, FAO)")
    out.append(f"3. NADH → CI → ubiquinol → CIII → cyt c → CIV → O2 (electron transport)")
    out.append(f"4. CI + CIII + CIV pump PMF into a shared `PMF_m` pool")
    out.append(f"5. CV consumes PMF_m + ADP + Pi → matrix ATP")
    out.append(f"6. `ATPtmB_mitoMap` exports matrix ATP in exchange for cytoplasmic ADP (consumes PMF)")
    out.append(f"7. `OF_ATP_mitoMap` hydrolyzes cytoplasmic ATP → ADP + Pi + biomass_c (objective)")
    out.append(f"\n**The PMF abstraction is the crucial part:** rather than tracking explicit H+ ion fluxes between compartments, MitoMAMMAL uses a single `PMF_m` metabolite as proton-motive-force currency. This couples proton pumping (CI, CIII, CIV) to consumption (CV, ATPtmB) via mass balance in FBA.")
    out.append(f"\n**Implication for transit modeling:** the model's concept of 'mitochondrial viability' comes down to whether enough PMF is being pumped to drive ATP export. Our ΔΨm-proxy objective (maximize CI+CIII+CIV pumping) is aligned with this abstraction.")
    out.append("")
    out.append("---")
    out.append(f"\n*Generated by `phase_a_dissection.py` on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Raw solution saved to `results/phase_a_baseline_solution.csv`.*")

    # Save the output
    with open(OUTPUT_PATH, 'w') as f:
        f.write('\n'.join(out))
    print(f"\n✓ Wrote {OUTPUT_PATH}")

    # Also save the raw flux solution for later phases
    flux_df = pd.DataFrame({'reaction_id': list(sol.fluxes.index),
                            'flux': list(sol.fluxes.values)})
    flux_df['abs_flux'] = flux_df['flux'].abs()
    flux_df = flux_df.sort_values('abs_flux', ascending=False)
    flux_path = results_path("phase_a", "baseline_solution.csv")
    flux_df.to_csv(flux_path, index=False)
    print(f"✓ Saved flux solution: {flux_path}")


if __name__ == '__main__':
    main()

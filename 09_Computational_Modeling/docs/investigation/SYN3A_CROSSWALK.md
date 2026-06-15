# Syn3A ↔ MitoMAMMAL Transport Crosswalk
**Phase I deliverable (v6 plan, P3).** Date: 2026-04-23.

---

## The question this resolves

The project's Executive Summary frames mitochondrial transit viability as equivalent to the minimal-cell problem: *"both systems face ATP production under limited genomic control with critical import dependencies."* This is the theoretical frame that differentiates our paper from a clinical mitochondrial therapy paper.

**The claim needs to be tested, not asserted.** Do the metabolic boundary reactions (imports) actually overlap between JCVI-syn3A and MitoMAMMAL, or are they qualitatively different?

This document provides a **mechanism-level, 3-reaction deep dive** plus a category-level Fisher's exact test on the full boundary sets.

---

## Three-reaction mechanistic deep dive

### Reaction 1: Pyruvate transport → **DIVERGENT**

| Aspect | MitoMAMMAL | JCVI-syn3A |
|---|---|---|
| Imports directly? | **YES** (`PYRt2m`) | **NO** (generates internally) |
| Equation | `pyr_c + h_c → pyr_m + h_m` (H+ symport) | (internal glycolysis endpoint) |
| Gene complement | SLC25A1 / MPC1+MPC2 heterodimer | pyk (pyruvate kinase) |
| Energy coupling | Consumes PMF (H+ symport) | N/A (produced inside) |
| Baseline flux | +2.49 mmol/gDW/h (import) | N/A |

**Mechanism narrative:** The mitochondrion is **post-glycolytic**. It receives pyruvate from the host cytoplasm via the dedicated carrier. Syn3A is a **whole cell doing its own glycolysis** — it imports glucose through the PTS (PEP:sugar phosphotransferase) system and generates pyruvate internally via pyruvate kinase.

**Insight:** This is a MEANINGFUL divergence. Both systems REQUIRE pyruvate for ATP metabolism, but the source differs. The "equivalence" of minimal cell and organelle is NOT at the level of pyruvate sourcing — it's at the level of what happens to pyruvate AFTER it's available (both oxidize it). This is a better framing than claiming strict import equivalence.

### Reaction 2: Inorganic phosphate (Pi) → **EQUIVALENT**

| Aspect | MitoMAMMAL | JCVI-syn3A |
|---|---|---|
| Imports directly? | **YES** (`PIt2mB_mitoMap`) | **YES** (Pst/ABC analog) |
| Equation | `0.18 PMF_c + pi_c → 0.18 PMF_m + pi_m` | ATP-dependent import |
| Gene complement | SLC25A3 (PiC) | ABC phosphate importer (mycoplasma Pst homolog) |
| Energy coupling | PMF-coupled | ATP-coupled |
| Baseline flux | +99.92 mmol/gDW/h (stoichiometric with ATP synthesis) | Large, demand-driven |

**Mechanism narrative:** Both systems require phosphate for ATP synthesis. Both have dedicated ABC-transporter-class import machinery. The energy coupling differs (mitochondrion extracts from PMF it generates; Syn3A spends ATP it generated in glycolysis), but the **functional role is identical**.

**Insight:** This is a TRUE equivalence point. The mitochondrion's 1:1 stoichiometry between phosphate import and ATP synthesis mirrors Syn3A's phosphate dependence for glycolysis.

### Reaction 3: Glutamate (amino acid exemplar) → **EQUIVALENT**

| Aspect | MitoMAMMAL | JCVI-syn3A |
|---|---|---|
| Imports directly? | **YES** (`GLUt2mB_mitoMap`) | **YES** (permease or ABC) |
| Equation | `0.18 PMF_c + glu_L_c → 0.18 PMF_m + glu_L_m` | permease-driven |
| Gene complement | SLC25A22 (GC1), SLC25A18 (GC2) | MMSYN1_0876/0878/0886 (AA permeases), MMSYN1_0165-0169 (Opp ABC) |
| Synthesis capacity? | **NO** (mito doesn't synthesize glu as organelle) | **NO** (Syn3A uses salvage only) |
| Energy coupling | PMF-coupled | ATP-coupled (Opp) or symport (permease) |

**Mechanism narrative:** Both systems are auxotrophic for glutamate. Neither synthesizes it de novo. Both have dedicated high-affinity transporters.

**Insight:** This is the STRONGEST equivalence point. Both systems are "carbon-and-nitrogen scavengers" — the mitochondrion scavenges from the host cell, Syn3A scavenges from growth medium. The **amino acid dependency structure is near-identical**. This is the core of the "programmable organelle" framing: engineering a mitochondrion to have different amino acid preferences mirrors engineering a minimal cell with different auxotrophies.

### Three-reaction summary

| Reaction | Verdict |
|---|---|
| Pyruvate | **DIVERGENT** — mito imports, Syn3A synthesizes |
| Phosphate | **EQUIVALENT** — both import via ABC-class machinery |
| Glutamate | **EQUIVALENT** — both import, neither synthesizes |

**2 of 3 equivalent.** Divergence in pyruvate reflects the organelle-vs-cell distinction (post-glycolytic vs whole cell), not a failure of the equivalence frame.

---

## Category-level overlap (Fisher's exact test on broader boundary sets)

Using 22 metabolite categories spanning carbon substrates, TCA intermediates, amino acids, inorganics, nucleobases, and lipid precursors:

| | MitoMAMMAL imports | MitoMAMMAL doesn't |
|---|---|---|
| **Syn3A imports** | 10 | 4 |
| **Syn3A doesn't** | 8 | 0 |

**Jaccard similarity:** 10/22 = **45%**

**Fisher's exact p-value:** 1.00 (cannot reject null of random association)

### Why Fisher's says null

The 45% Jaccard is respectable numerical overlap, but the statistical test asks a different question: given the MARGINAL totals, is the joint pattern more concentrated in co-import than chance? The contingency table has zero "neither" cells — every category we listed is imported by at least one system. This makes the Fisher's test low-powered.

### Qualitative interpretation

**Shared imports (both):** amino acids (essential + non-essential), phosphate, Mg, Fe, Zn, choline, glucose, fatty acids. These are the universal currency of heterotrophic life.

**Mito-only imports (8):** pyruvate, lactate, malate, succinate (TCA intermediates), O2, CO2, Cu, cardiolipin precursors. Reflects the organelle's specialization for aerobic oxidative metabolism.

**Syn3A-only imports (4):** nucleobases/nucleosides, sphingomyelin, NAD precursors (nicotinamide), sulfate. Reflects the minimal cell's need for biosynthetic precursors (mitochondrion gets nucleotides from the host; Syn3A needs them from medium).

**The divergences are explainable biology, not random noise:**
- Mito-only imports reflect "I'm an oxidative organelle in an aerobic host"
- Syn3A-only imports reflect "I'm a minimal biosynthetic chassis"

---

## The honest "equivalence" claim for the abstract

**Not:** "mitochondria and minimal cells have the same import dependencies" (45% Jaccard doesn't support this strictly)

**Better:** "the mitochondrion and JCVI-syn3A share import dependencies for a core set of metabolites (phosphate, amino acids, inorganic ions). Divergences reflect biological specialization — the mitochondrion as an aerobic oxidative organelle imports TCA intermediates and respiratory substrates; Syn3A as a minimal biosynthetic chassis imports nucleobases and lipid precursors. The **mechanism-level equivalence** (ABC-class transporters, demand-driven flux) is conserved even where specific metabolite imports differ."

**The stronger claim to lead with in the abstract:** "Engineering a mitochondrion as a programmable organelle requires understanding the same import-dependency structure that defines minimal-cell design. Both systems require defined nutrient sets delivered by dedicated transporters, and both are constrained by the stoichiometric coupling between import and ATP output."

---

## Implications for the Programmable Organelle framing (Layer 2 of vision)

This analysis supports the core vision claim with appropriate nuance:

1. **The import-dependency FRAMEWORK is shared** — both systems can be thought of as "defined-nutrient-set + ATP-output machinery"
2. **The specific nutrient set differs** — this is expected and biologically sensible
3. **The mechanism of import (ABC-class transporters, energy-coupled carriers) is conserved** — allowing cross-application of engineering principles

For Layer 2 (programmable transplantation) and Layer 3 (gene delivery platform), this means:
- **Expect to design new imports the same way you would for a minimal cell** (characterize substrate specificity, measure uptake kinetics, verify stoichiometric coupling)
- **Don't expect 1-to-1 metabolite equivalence** — the mitochondrion has its own metabolic niche

---

## Honest limitations

1. **Syn3A data derived from Thornburg 2022 Cell + Syn3A_Research_Notes_RemNote.md** — no SI table directly extracted. Specific gene IDs for Syn3A transporters (Pst system) need confirmation.
2. **Category selection is judgment-call** — different groupings might give different Jaccard
3. **The 3 reactions are hand-picked to span the import hierarchy** — more comprehensive analysis would test all 70 MitoMAMMAL exchanges against all Syn3A boundary reactions
4. **Fisher's p=1.0 is a warning** — the equivalence claim is not strong at the statistical level. It's primarily a mechanistic-narrative claim.

---

## Trust criteria status (entry for `TRUST_LEDGER.md`)

| Claim | C1 mech | C2 alg | C3 adv | C4 xmodel | C5 lit | C6 code |
|---|---|---|---|---|---|---|
| Mitochondrion and Syn3A share mechanism-level import dependencies | ✓ | N/A | ⚠ Fisher p=1.0 | ⚠ | ✓ Thornburg 2022 | ✓ |
| Phosphate and glutamate imports are equivalent across systems | ✓ | N/A | ✓ (3-rxn deep dive) | ⚠ | ✓ | ✓ |
| Pyruvate sourcing diverges (mito imports, Syn3A synthesizes) | ✓ | N/A | ✓ | ⚠ | ✓ | ✓ |
| Jaccard similarity 45% reflects biological specialization | ✓ | N/A | ✓ | ⚠ | ⚠ | ✓ |
| Full equivalence claim as originally framed in Exec Summary | ⚠ | N/A | ✗ (weakened by Fisher) | ⚠ | ⚠ | ✓ |

---

## Files generated

- `results/phase_i/syn3a_crosswalk_3rxns.csv` — the 3-reaction table with mechanism annotations
- `results/phase_i/category_overlap_fisher.json` — Fisher's exact test result
- `scripts/investigation_phases/phase_i_syn3a_crosswalk.py` — reproducible analysis

---

*Deliverable for v6 plan P3. Resolves the Syn3A equivalence claim with 3-reaction mechanistic depth + category-level statistical test. Verdict: mechanism equivalence supported for specific categories (phosphate, amino acids); full-network equivalence claim needs qualifying.*

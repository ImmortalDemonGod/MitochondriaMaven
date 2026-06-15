# Strategy Critique, Assumption Audit, and Thesis Reframe
**Date:** 2026-04-21
**Source:** AI-assisted critical evaluation of Mitochondria Maven strategy
**Purpose:** Identify all assumptions underlying the project and its critique, map them to testable experiments

---

## The Project's Assumptions (Must Be True for Full Vision)

| ID | Assumption | Hidden dependency | Testable by |
|---|---|---|---|
| A1 | ATP depletion is the reversible root cause of biological death | Other hallmarks of aging (DNA damage, senescence, crosslinking) are downstream of energy deficits, not independent | Literature meta-analysis + bio-systems-engineering longitudinal data |
| A2 | Mitochondria can produce ATP in the extracellular environment | Bloodstream/ECF has sufficient substrates (pyruvate, malate, ADP) and won't trigger MPTP opening | MitoMAMMAL pFBA under blood substrate concentrations |
| A3 | ~1,500 nuclear imports are not all required for short-term function | Minimal set sustains ATP synthesis without structural/repair proteins | **MitoMAMMAL autonomy knockdown (primary q-bio experiment)** |
| A4 | Mitochondrial genome can be genetically engineered | mtDNA editing tools (DddA-CBEs, mitoTALENs) can overcome polyploidy and import barriers | Literature survey of current tools |
| A5 | Target cells will uptake transplanted mitochondria | Endocytosis/TNTs absorb them; mitophagy doesn't immediately destroy them | Already partially in literature corpus |
| A6 | Immune system won't reject transplanted mitochondria | DAMPs (formylated peptides, circular DNA) don't trigger sepsis | Future wet lab + immunology literature |

## The Critique's Assumptions (Must Be True for Critique to Hold)

| ID | Assumption | Hidden dependency | Counter-evidence |
|---|---|---|---|
| C1 | ETC proteins degrade rapidly due to ROS | No nuclear resupply = organelle "burns itself out" in hours | Miller Lab (OMRF) 2025: mitochondrial dynamics in muscle are SLOWER than assumed |
| C2 | Evolutionary gene transfer is irreversible | Can't re-pack ~1,500 genes into mt-genome | Engineering ≠ evolution; selective pressure was for integration, not independence |
| C3 | Bacterial/artificial engineering is easier than modifying mitochondria | Synthetic biology toolkit ports cleanly to alphaproteobacteria | Unproven — both paths face massive engineering challenges |
| C4 | ATP is proximate cause, not ultimate cause of aging | Cancer, amyloid, crosslinking are independent of ATP | ATP powers DNA repair, proteasome, autophagy — they ARE energy-dependent |
| C5 | Bloodstream is hostile to bare mitochondria | Cell-free mito are inactive or temporary | Stephens et al. 2020: intact functional mitochondria in mammalian blood |

## The Key Insight: Which Assumptions the Computational Modeling Tests

The MitoMAMMAL knockdown experiment directly tests: A2, A3, C1, C2, C5

This is why the q-bio computational work is the correct next step regardless of which side of the debate is right — it produces the quantitative data needed to resolve the standoff.

## The Thesis Reframe (Two Stages)

**Original thesis:** All biological death = ATP production failure → engineer autonomous mitochondria → immortality

**Reframe Stage 1 — "Cellular CPR":** ATP maintenance during acute crises (ischemia, trauma, hemorrhage) extends the viability window for medical intervention. Extracted mitochondria don't need to be autonomous — they need to survive transit and be reuptaken by target cells before protein stocks degrade below the mitophagy acceptance threshold.

**Reframe Stage 2 — "Transit Survivability":** The critical insight is that an extracted mitochondrion placed in the bloodstream has a CLOCK running — but if it is reuptaken by a cell before the clock runs out, nuclear import resumes and the mitochondrion lives. The engineering problem is not autonomy but transit window extension: how do you slow protein degradation and maintain membrane potential long enough for reuptake?

**Why the reframe is stronger:**
- Clinically actionable (existing mitotherapy literature supports it)
- Doesn't require full autonomy (hours of function suffices)
- Existing FDA frameworks for biologics
- Already supported by project's own literature corpus
- Doesn't trigger "Theranos Trap" concerns
- Computationally testable RIGHT NOW via time-stepped FBA

**The reframe doesn't abandon the long-term vision** — it sequences it. Transit survivability comes first (achievable with current extraction + preservation engineering). Full autonomy is the decade-horizon goal, informed by but not required for near-term applications.

**Implications for computational modeling:** The primary experiment is now a time-dependent viability decay model, not a static import ranking. The output is a predicted transit window (hours) under different conditions, not a gene list. The killer figure is a decay curve with a reuptake threshold line.

## Three Alternative Strategies (Worth Tracking, Not Pursuing Now)

| Alternative | Approach | Advantage | Disadvantage |
|---|---|---|---|
| A: Alphaproteobacterial engineering | Engineer free-living bacterium to act as ATP exporter | Already autonomous, full genome | Immunogenicity, regulatory, unproven |
| B: Synthetic vesicles | Artificial liposomes with purified ATP synthase + proton pumps | 100% control, no DNA issues | Extreme engineering challenge, no self-repair |
| C: Mitotherapy (preservation focus) | Accept limited viability, optimize extraction scale + preservation window | Clinically closest, existing literature | Doesn't achieve autonomy goal |

Current strategy (computational modeling + extraction optimization) is compatible with all three alternatives — the minimum import set analysis informs each one.

---

*Saved 2026-04-21. This document captures the strategic tension and maps it to testable computational experiments.*

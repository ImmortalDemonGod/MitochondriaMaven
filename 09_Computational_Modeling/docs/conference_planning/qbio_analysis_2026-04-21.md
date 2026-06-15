# q-bio Chicago 2026 — Reading Summary + Gap Analysis
**Date:** 2026-04-21
**Status:** Second pass. Updated with time-dependent decay model, substrate scenarios, and revised experimental design per assumption audit (see Strategy_Critique_and_Assumptions_2026-04-21.md).
**Deadline:** May 31, 2026 (abstract), July 27-30, 2026 (conference)
**Location:** University of Chicago, Biological Sciences Learning Center
**Cost:** $200 registration + ~$280 travel = ~$480 total

---

## 1. The Unified Thesis

Syn3A and Mitochondria Maven are one system:

```
THEORY: Syn3A whole-cell modeling
  "What are the minimal import dependencies for ATP production?"
      ↓ parametrizes
METHODS: Mitochondria Maven + MitoMAMMAL extension
  "How long is the functional transit window for extracted mitochondria?"
      ↓ validated by
EXPERIMENT: 2024 yeast extraction (Taguchi, JC-1)
  "Does the predicted transit window match observed JC-1 membrane potential decay?"
```

**Core claim:** Mitochondrial transplantation shows clinical promise but lacks a quantitative framework for predicting how long extracted mitochondria remain functional during extracellular transit. An extracted mitochondrion doesn't need permanent autonomy — it needs to survive long enough for cellular reuptake, at which point nuclear import resumes and protein stocks are replenished. No systematic computational framework exists for predicting this transit window.

**The novelty:** Nobody has connected Syn3A whole-cell modeling to mitochondrial transit viability. Nobody has used MitoMAMMAL's GPR rules combined with protein half-life data to predict the time-dependent decay of ATP production post-extraction. The idea is publishable — execution is the gap.

---

## 2. The Two Published Models

### 2A. Syn3A Whole-Cell Model (Luthey-Schulten Lab, UIUC)

**IMPORTANT CORRECTION:** The handoff document says "Covert lab (Stanford)." This is WRONG. The Syn3A model is from the **Luthey-Schulten Lab at University of Illinois at Urbana-Champaign**, in collaboration with the J. Craig Venter Institute. Senior author: **Zaida Luthey-Schulten**. Markus Covert's lab at Stanford did the *E. coli* whole-cell model (2012), not the Syn3A model. This must be correct in the abstract and all communications.

**Paper:** Thornburg ZR, Bianchi DM, Brier TA, Gilbert BR, Earnest TM, Melo MCR, et al. "Fundamental behaviors emerge from simulations of a living minimal cell." *Cell*, 185(2):345-360.e28, January 20, 2022.
- DOI: 10.1016/j.cell.2021.12.025
- PMID: 35063075
- PMCID: PMC9985924

**What it models:** Complete cell cycle of JCVI-syn3A, the minimal synthetic organism created by the Venter Institute. 493 genes (452 protein-coding), 543 kbp single circular chromosome.

**Architecture:** Hybrid stochastic-deterministic simulation integrating three methods communicating every 1 second:

| Layer | Method | What it handles |
|---|---|---|
| Metabolism | ODE (deterministic) | Central, nucleotide, lipid, cofactor, amino acid, ion metabolism |
| Genetic info processing | CME (stochastic) | Transcription, translation, tRNA charging, DNA replication |
| Spatial | RDME (stochastic-spatial) | Diffusion on 8nm lattice, spatial heterogeneity |

**Scale:**
- ~7,200 reactions (spatial model)
- 7,765 unique molecular species tracked
- 148 metabolites, 452 proteins/mRNAs, 29 tRNA types, 503 ribosomes
- Simulates complete cell cycle (~105 min doubling time)

**Key results relevant to us:**
- Detailed ATP energy budget: ~35,000 ATP/sec production rate
- Metabolic bottleneck identified: fructose-1,6-bisphosphate aldolase controls glycolysis flux
- Growth coordination emerges without explicit regulatory mechanisms
- Genome-wide mRNA half-life distributions emerge from the simulation

**Code repositories (GitHub, `Luthey-Schulten-Lab/`):**

| Repo | What | Hardware | Runtime |
|---|---|---|---|
| `Minimal_Cell` (107 stars) | Well-stirred model (CME+ODE). Python + odecell package. | CPU only | ~4 hrs per cell cycle |
| `Minimal_Cell_4DWCM` (47 stars) | 4D follow-up (2025). Adds chromosome dynamics (LAMMPS/Kokkos) and membrane dynamics (FreeDTS). | GPU required (CUDA) | ~8-10 hrs for 20 min of bio time |
| `Minimal_Cell_ComplexFormation` | Complex assembly extension | TBD | TBD |

**For q-bio purposes:** The well-stirred model (`Minimal_Cell` CME_ODE) is sufficient and runs on CPU in ~4 hours. No GPU needed for the core perturbation experiment.

### 2B. MitoMAMMAL (Habermann Lab)

**Paper:** "MitoMAMMAL: A genome-scale metabolic model of mammalian mitochondria." *Bioinformatics Advances*, 5(1):vbae172, November 2024.
- GitLab: gitlab.com/habermann_lab/mitomammal
- License: MIT

**What it models:** Mammalian mitochondrial metabolism.
- **560 metabolic reactions**
- **445 metabolites**
- **780 genes** (human and mouse orthologs mapped via gene-product-reaction rules)
- Built on MitoCore, extended with corrected GPR rules and missing DHODH/CoQ electron transport chain reactions

**Pathways covered:** TCA cycle, malate-aspartate shuttle, oxidative phosphorylation (OXPHOS)/ATP synthesis, glycine cleavage system, proline cycle, fatty acid oxidation, de novo pyrimidine synthesis.

**Software stack:**
```
conda create --name mitomammal python=3.8
conda install jupyter numpy pandas matplotlib cobra
```
Standard Python scientific stack + COBRApy. GLPK solver. No special hardware.

**Analysis method:** Parsimonious Flux Balance Analysis (pFBA) with adapted E-Flux algorithm. E-Flux selects organism-specific GPRs and constrains reaction bounds using expression data (90th-percentile normalization, 0-1 scaling; AND = min, OR = sum).

**Key files:**

| File | Purpose |
|---|---|
| `6_mitoMammal_model.xml` | Core SBML Level 3 model |
| `efflux_method.py` | E-Flux function for expression-based constraining |
| `proteomics_mouse_cardiac_vs_BAT.ipynb` | Mouse cardiac + BAT proteomics integration |
| `transcriptomic_human_BAT.ipynb` | Human brown adipocyte transcriptomics |
| `data/` | All datasets used in the study |

**Key results:**
- Cardiac metabolism (objective: maximize ATP hydrolysis): Predicted glycine import, lactate production, pyruvate partitioning
- BAT metabolism (objective: maximize UCP1 reaction): Predicted CoQ reduction via proline dehydrogenase, Complex II reversal, ATP synthase running in reverse

**Direct relevance to our framework:**

1. **The 780 GPR rules map every reaction to specific gene products.** Can directly cross-reference which are nuclear-encoded (~1,487 in mammals) vs. mitochondria-encoded (13 protein-coding genes). Simulate removal of nuclear contributions = direct test of how rapidly ATP production decays post-extraction.

2. **COBRApy + FBA infrastructure.** Standard SBML format. Can run gene-essentiality analysis (single/double knockouts), identify minimal reaction sets, merge with Syn3A COBRA model for hybrid metabolic network exploration.

3. **E-Flux method repurposable.** Could constrain the model to "mitochondrial-genome-only" expression, simulating metabolism without nuclear-encoded contributions.

4. **560 reactions vs. Syn3A's ~200 metabolic reactions.** Comparing the two defines exactly what a mitochondrion needs that a minimal cell doesn't have — and vice versa.

---

## 3. Miguel's Original Syn3A Code — Status

### Search Results (2026-04-21)

**Comprehensive filesystem search performed across:**
- `/Users/tomriddle1/` (all subdirectories)
- `/Volumes/Totallynotaharddrive/` (external drive, accessible)
- All git repositories in `/Users/tomriddle1/repos/`

**Result: NO Syn3A code found anywhere.**

- No Python files with syn3a/synth3a modeling code
- No Jupyter notebooks related to whole-cell or minimal cell modeling
- No cloned Luthey-Schulten or CovertLab repos
- No cloned MitoMAMMAL repo
- No Lux3 Lab paper located on filesystem

**Documentation says:**
- `Modeling_Overview.md`: "Status: Work exists in a separate location (not yet integrated into this project)"
- `INDEX.md`: "Synth3a whole-cell modeling — active; location TBD"
- Otter transcription (lines 149-158): "By trying to model the simplest possible organism, I basically realized that mitochondria were, in some ways a little bit more complicated, but in some ways very similar to that Syn3A organism... wholesale modeling on that level has been largely successful"

**Assessment:** The original modeling code is either on an inaccessible drive, was never version-controlled, or was done interactively and lost. For q-bio purposes, this doesn't matter — the path forward is building on Luthey-Schulten + MitoMAMMAL published code. The notebook transcription's claim that modeling was "largely successful" should be treated as conceptual insight (mitochondria ≈ Syn3A dynamics), not as reproducible computational results.

**The "Lux3 Lab" reference** in the Otter transcription has been identified as almost certainly the **Luthey-Schulten Lab** (UIUC) — "Lux3" is a mishearing or personal shorthand. The paper is the Thornburg et al. Cell 2022 paper already in our reference list.

---

## 4. The Competitive Landscape

| Group | What they do | Threat level |
|---|---|---|
| **Luthey-Schulten Lab (UIUC)** | Published THE Syn3A model (2022) + 4D extension (2025). Active. | HIGH — but they model the whole cell, not mitochondrial transit viability specifically |
| **Habermann Lab** | Published MitoMAMMAL (2024). Mitochondrial metabolism. | MEDIUM — they model mitochondrial metabolism but don't connect to minimal cells |
| **Karr Lab** | Original whole-cell modeling pioneer (2012 M. genitalium). Jonathan Karr moved to industry. Lab no longer active. | NONE — legacy framework, open source |
| **Covert Lab (Stanford)** | E. coli whole-cell models. Different organism. | LOW — wrong organism for our framing |

**The gap nobody occupies:** Connecting Syn3A minimal cell modeling TO mitochondrial transit viability prediction. Luthey-Schulten models the whole cell but doesn't ask "what does this mean for mitochondria?" Habermann models mitochondrial metabolism but doesn't predict post-extraction decay. The bridge — using minimal cell biology to inform time-dependent organelle viability — is the novel contribution.

**Field size:** Fewer than 50 people worldwide actively do whole-cell minimal cell simulation. Showing up at q-bio with independent results gets noticed.

---

## 5. Gap Analysis: What's Needed for the 350-Word Abstract

### What EXISTS right now

| Asset | Status | Usable for abstract? |
|---|---|---|
| ATP thesis framing | Fully articulated (IMOL-ERT, Otter transcription, science strategy) | YES |
| 114 screened papers on mitochondrial extraction | Complete, structured, in Mitochondria Maven | YES (background/context) |
| 2024 yeast extraction (Taguchi, JC-1) | Completed but data is in physical lab notebook, undigitized | Can claim existence, can't cite numbers without digitization |
| MitoMAMMAL model (560 reactions, COBRApy) | Published, code available on GitLab, NOT yet cloned | Available — need to clone and run |
| Syn3A model (493 genes, ODE/CME) | Published, code available on GitHub, NOT yet cloned | Available — need to clone and run |
| Computational biology capability | Demonstrated (50K-line RNA_PREDICT, arXiv paper, 185-test bio-systems library) | Credibility for "this person can actually do this" |

### What DOES NOT EXIST yet

| Gap | Severity | What's needed | Effort estimate |
|---|---|---|---|
| **No computational results** | CRITICAL | Zero simulations run. No perturbation data. No FBA outputs. Abstract must describe planned/preliminary work, not completed work. | 3-4 weeks of modeling work |
| **No merged Syn3A ↔ MitoMAMMAL framework** | CRITICAL | The core novel claim requires actually integrating these two models. The crosswalk table (which MitoMAMMAL reactions map to Syn3A import dependencies?) doesn't exist. | 1-2 weeks after both models are running |
| **No quantitative validation against extraction data** | HIGH | JC-1 viability timeline from 2024 is on paper, not digital. Connecting "how long mitochondria maintained membrane potential" to model predictions requires (a) digitized data and (b) a running model. | Dependent on lab notebook access |
| **Luthey-Schulten code not cloned/installed/run** | HIGH | Need to verify it runs on current hardware, understand the ODE metabolic model structure, identify ATP-related reactions for perturbation. | 1-2 days to clone + install, 1 day to run first simulation |
| **MitoMAMMAL not cloned/installed/run** | HIGH | Need to install COBRApy environment, load SBML model, run default pFBA, understand GPR rules structure. | 1 day to clone + install, 1 day for first FBA run |
| **~~Lux3 Lab paper unlocated~~** | RESOLVED | "Lux3 Lab" = Luthey-Schulten Lab (UIUC). Paper is Thornburg et al. Cell 2022, already referenced. | N/A |
| **Author attribution corrected** | LOW but IMPORTANT | All documents and the abstract must reference Luthey-Schulten Lab (UIUC), not "Covert lab (Stanford)." | Text corrections |

---

## 6. The Experimental Design (Computational)

### Experiment 1: Transit Viability Window Prediction (PRIMARY)

**Question:** How long can an extracted mitochondrion maintain sufficient ATP production during extracellular transit to remain viable for cellular reuptake?

**Key insight:** An extracted mitochondrion doesn't need to survive forever. It needs to survive transit — the time between extraction/injection and reuptake by a target cell. Once internalized, nuclear import machinery resumes and proteins are replenished. The engineering target is the **functional transit window**, not permanent autonomy.

**Method:**
1. Load `6_mitoMammal_model.xml` into COBRApy
2. Set objective function: maximize ATP hydrolysis
3. Run baseline pFBA → record full-complement ATP flux (F₀)
4. Identify all 780 GPR-mapped genes; classify as nuclear-encoded (~767) vs. mt-encoded (13)
5. Find published protein half-life data for ETC complexes:
   - Complex I (NADH dehydrogenase): t½ = ? hrs
   - Complex II (succinate dehydrogenase): t½ = ? hrs
   - Complex III (cytochrome bc1): t½ = ? hrs
   - Complex IV (cytochrome c oxidase): t½ = ? hrs
   - Complex V (ATP synthase): t½ = ? hrs
   - Sources: D₂O labeling studies, mass spec proteomics, BRENDA, PaxDb
6. Time-stepped decay simulation (no new protein synthesis during transit):
   ```
   For t = 0 to 72 hours (step = 0.5 hr):
       For each nuclear-encoded protein P:
           abundance(t) = P₀ × e^(-ln2 × t / t½_P)
           Update FBA upper bound for reactions dependent on P
       Run pFBA → record ATP flux F(t)
   ```
7. Run under THREE substrate scenarios:
   | Scenario | Models | Substrate constraints |
   |---|---|---|
   | A: Intracellular (baseline) | Mito inside a normal cell | MitoMAMMAL defaults |
   | B: Blood/ECF transit | Mito floating in bloodstream | Published blood metabolite concentrations (pyruvate ~0.05-0.1 mM, O₂ arterial, HMDB values) |
   | C: Ischemic tissue injection | Mito injected into oxygen-deprived tissue ("Cellular CPR") | Low O₂, high lactate, low glucose |
8. Define **minimum reuptake viability threshold**: the minimum ATP flux (or membrane potential proxy) below which a recipient cell's mitophagy system would destroy rather than integrate the mitochondrion. Estimate from published mitophagy activation literature.
9. Plot: ATP flux vs. time for all three scenarios, with horizontal dashed line at reuptake threshold.

**Output:** Three decay curves showing the **functional transit window** — the time between extraction and the point where function drops below reuptake viability. The shaded region above the threshold is the engineering design space.

**The killer figure:** Decay curves with "functional transit window" shaded, threshold line labeled, and annotations showing which interventions (antioxidant loading, cold chain, substrate supplementation, EV encapsulation) could extend the window.

### Experiment 1b: Single-Gene Impact on Transit Window

**Question:** Which single protein, if stabilized (half-life doubled), would extend the transit window the most?

**Method:**
1. For each of the 780 genes: double its t½ → re-run time-stepped simulation → record new transit window
2. Rank genes by Δ transit window (hours gained)

**Output:** Engineering target list — prioritized by impact on transit survivability, not just steady-state ATP flux. Directly actionable for preservation protocol design.

### Experiment 2: Syn3A Import Dependency Crosswalk (SUPPORTING)

**Question:** Which Syn3A metabolic reactions correspond to mitochondrial import pathways?

**Method:**
1. Run Syn3A well-stirred model (CME_ODE) for one cell cycle
2. Extract the ODE metabolic model component
3. Identify all reactions involving metabolites that cross the cell boundary (import/export)
4. Map these against MitoMAMMAL's import/export reactions
5. Build crosswalk table: Syn3A import dependency → MitoMAMMAL equivalent → nuclear-encoded or mt-encoded?

**Output:** Mapping showing shared import dependencies between the simplest cell and mitochondria. Frames the theoretical contribution — why minimal cell biology informs organelle engineering. Supporting context, not the headline result.

### Experiment 3: Validation Against Extraction Data

**Question:** Does the predicted transit window match observed viability in extracted mitochondria?

**Method:**
1. From Experiment 1, extract the predicted viability curve under Scenario A (intracellular-like buffer)
2. Compare against:
   - 2024 JC-1 membrane potential decay data (if digitizable from lab notebook)
   - Published mitochondrial isolation viability timelines from the 114-paper corpus
   - Published ETC activity decay rates post-extraction (literature search)
3. Quantify fit: does the model's predicted transit window match experimental observations within 2x?

**Output:** Model validation — predicted vs. observed viability window.

### Experiment 4: Intervention Modeling

**Question:** Which preservation interventions extend the transit window, and by how much?

**Method:** Re-run Experiment 1 with modified parameters:
| Intervention | Model change | Rationale |
|---|---|---|
| Antioxidant loading (NAC, MitoQ) | Reduce protein degradation rates by 30-50% | Less ROS damage during transit |
| Cold chain (4°C vs 37°C) | Apply Q₁₀ temperature coefficient to all degradation rates | Standard preservation practice |
| Substrate supplementation | Add pyruvate + malate + ADP to Scenario B constraints | Maintain substrates during blood transit |
| EV encapsulation | Combine reduced degradation + intracellular-like substrates | Natural delivery mechanism |

**Output:** Bar chart showing transit window extension for each intervention. Directly informs preservation protocol design.

---

## 7. Abstract Strategy

### Honest Framing Options

**Option A: Framework paper (safest, can write now)**
"We present a computational framework for..." — describes the approach, states preliminary results will be at conference.

**Option B: Transit window paper (strongest, needs 3 weeks of work first)**
"We predict..." — requires Experiment 1 (time-stepped FBA) to produce a decay curve and a transit window number. Much stronger but requires COBRApy + protein half-life data before May 31.

**Option C: Poster instead of talk (safety valve)**
Poster deadline is July 27. Three extra months but loses forcing function.

**Recommendation: Option B.** The time-stepped FBA is computationally cheap once COBRApy runs. The hard part is finding ETC protein half-life data — that's a literature search, not a modeling bottleneck. Achievable in 2-3 weeks.

### Draft Abstract Structure (350 words)

**Title:** Predicting the Functional Transit Window for Extracellular Mitochondria Using Genome-Scale Metabolic Modeling and Protein Turnover Kinetics

**Body outline:**

1. **Problem** (~60 words): Mitochondrial transplantation — injecting isolated mitochondria into ischemic tissue — shows clinical promise but lacks a quantitative framework for predicting how long extracted mitochondria remain functional during extracellular transit. Mammalian mitochondria encode only 13 proteins and depend on ~1,500 nuclear-encoded imports. Once extracted, protein stocks degrade without replacement. The critical question: how long is the functional transit window before reuptake viability is lost?

2. **Approach** (~70 words): We integrate MitoMAMMAL, a 560-reaction genome-scale metabolic model of mammalian mitochondria (780 genes; Bioinformatics Advances 2024), with published protein half-life data for electron transport chain complexes. The Luthey-Schulten lab's JCVI-syn3A whole-cell model (493 genes; Cell 2022) provides the theoretical frame: both systems face ATP production under limited genomic control with critical import dependencies.

3. **Method** (~100 words): Using MitoMAMMAL's gene-product-reaction rules in COBRApy, we model post-extraction ATP synthesis decay as a time-dependent process. Nuclear-encoded protein abundances decay exponentially based on published half-lives; FBA constraints are updated at each time step to reflect remaining catalytic capacity. We simulate three transit environments: intracellular buffer (baseline), arterial blood (published metabolite concentrations from HMDB), and ischemic tissue (low O₂, high lactate). A minimum reuptake viability threshold — below which recipient cell mitophagy destroys rather than integrates the organelle — defines the functional transit window. [INSERT PRELIMINARY NUMBERS: transit window = N hours under scenario X]

4. **Validation** (~50 words): Predicted decay curves are compared against published post-isolation viability timelines from a systematic review of 114 mitochondrial extraction studies and the authors' 2024 yeast extraction experiments (Taguchi-optimized, JC-1 membrane potential verified).

5. **Significance** (~70 words): This framework converts the question of mitochondrial viability from qualitative observation to quantitative prediction. By identifying which proteins degrade fastest during transit, we prioritize preservation interventions (antioxidant loading, cold chain, substrate supplementation) by predicted transit window extension. The approach directly informs clinical mitotherapy protocol design and provides a computational foundation for engineering mitochondria with extended extracellular survival — connecting whole-cell modeling to translational bioenergetics.

---

## 8. Timeline (41 Days to Abstract)

| Week | Dates | Action | Deliverable |
|---|---|---|---|
| **Week 1** | Apr 21-27 | Clone MitoMAMMAL + Minimal_Cell repos. Install COBRApy environment. Run baseline pFBA. Literature search: ETC protein half-lives + blood metabolite concentrations. | Both models running. Half-life dataset compiled. |
| **Week 2** | Apr 28 - May 4 | Experiment 1: Implement time-stepped FBA loop. Run Scenario A (intracellular baseline). Generate first decay curve. | First quantitative result: "transit window = N hours under buffer conditions" |
| **Week 3** | May 5-11 | Run Scenarios B (blood) and C (ischemic). Run Experiment 1b (single-gene stabilization impact). Define reuptake threshold from mitophagy literature. | Three decay curves + engineering target ranking |
| **Week 4** | May 12-18 | Experiment 2: Syn3A crosswalk table. Experiment 4: intervention modeling (antioxidants, cold chain, substrates, EV encapsulation). | Supporting analyses complete. Transit window extension quantified. |
| **Week 5** | May 19-25 | Write 350-word abstract with real numbers from decay curves. Iterate. Generate the killer figure (decay curves + threshold + transit window). | Draft abstract + figure |
| **May 31** | Deadline | Submit abstract. Register ($200). | DONE |
| **June-July** | Post-submission | Experiment 3 (validation vs. JC-1 data + literature). Build talk. Rehearse. | Presentation ready |
| **July 27-30** | Conference | Present at q-bio Chicago. | §3 unfrozen. |

---

## 9. Immediate Next Actions

1. **Clone repos:**
   - `git clone https://github.com/Luthey-Schulten-Lab/Minimal_Cell.git`
   - `git clone https://gitlab.com/habermann_lab/mitomammal.git`
   - Target location: `/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/`

2. **Install environments:**
   - MitoMAMMAL: `conda create --name mitomammal python=3.8 && conda install jupyter numpy pandas matplotlib cobra`
   - Syn3A: Check `Minimal_Cell/requirements.txt` or conda environment file

3. **Register for q-bio:** qbiochicago.org ($200). Abstract submission form comes with registration.

4. **Find the Lux3 Lab paper:** Web search for Lux3 Lab + Syn3A computational paper.

5. **Correct all documents:** Replace "Covert lab" with "Luthey-Schulten Lab (UIUC)" in handoff doc and all references.

---

## 10. Theranos Trap Check

This work is legitimate because:
- The ATP thesis is mechanistically specific and computationally testable
- Both published models (Syn3A + MitoMAMMAL) provide reproducible starting points with available code
- The operator has demonstrated computational biology capability (arXiv paper, 302 models, 50K-line pipeline)
- The 2024 wet lab extraction provides experimental grounding (not just theory)
- The abstract will describe work with real numbers from real simulations
- The conference audience (quantitative biologists) will evaluate the computational methodology, not marketing claims

This is NOT the Theranos Trap. The Theranos Trap would be submitting an abstract claiming "we have developed autonomous mitochondria" when the modeling hasn't started. This abstract says "we present a computational framework with preliminary perturbation results" — which will be true by May 31 if the timeline is executed.

---

## 11. Connection to Other Projects

| Project | How it connects | Action |
|---|---|---|
| **bio-systems-engineering** | Measures ATP thesis from exercise physiology angle (lactate, VO2max). Same thesis, different measurement. q-bio paper and ACSM paper are two angles on one thesis. | Cross-reference JOSS submission |
| **Mitochondria Maven (literature)** | 114 papers provide domain knowledge for interpreting model results. The 8-category taxonomy and 10 research questions structure the analysis. | RQ10 answered by this work |
| **2024 wet lab extraction** | Experimental validation for model predictions. JC-1 viability data is ground truth. | Digitize lab notebook if accessible |
| **Black Box** | Forensic audit methodology applicable to bioinformatics pipeline reproducibility. | Speculative cross-project |

---

## 12. Open Questions

1. **Where is the original Syn3A modeling code?** Operator says "largely successful" work exists. Not on accessible filesystem. On an old drive? In cloud storage? Interactive notebook that was never saved? Need to ask operator directly.

2. **What is the "Lux3 Lab" paper?** Referenced in Otter transcription as having "produced another computational paper on Syn3A." Cannot find this on the filesystem or via cursory search. May be the Luthey-Schulten paper under a different name, or a separate publication.

3. **Is the 2024 lab notebook accessible?** Physical paper notebook with day-by-day extraction protocols, Taguchi arrays, JC-1 measurements. If it can be photographed/scanned, it provides validation data. If not, the abstract relies on published viability data from the 114 screened papers instead.

4. **Hardware for Syn3A simulation?** The well-stirred model runs on CPU in ~4 hours. Current machine (Mac) should handle it. Need to verify Python environment compatibility (odecell package).

5. **COBRApy on Apple Silicon?** MitoMAMMAL requires COBRApy with GLPK solver. Need to verify conda installation works on current hardware. Known issues with some solver backends on ARM Macs.

---

*Analysis generated 2026-04-21. First pass — will iterate. All gaps are honest. No claimed results that don't exist.*

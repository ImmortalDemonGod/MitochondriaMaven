# Computational Modeling — Overview

**Last updated:** 2026-04-21
**Status:** Active — q-bio Chicago 2026 abstract deadline May 31

---

## The Unified Computational Thesis

Syn3A (theory layer) and Mitochondria Maven (methods layer) are one system. Both address the same question: **how does ATP production behave under limited genomic control with critical import dependencies?**

The key reframe (April 2026): the goal is not permanent mitochondrial autonomy — it is predicting the **functional transit window** during which extracted mitochondria remain viable enough for cellular reuptake. Once internalized by a target cell, nuclear import resumes and proteins are replenished.

## What Exists in This Folder

| File | What it is |
|---|---|
| `qbio_analysis_2026-04-21.md` | Master analysis: gap assessment, experimental design (4 experiments), abstract draft, timeline |
| `syn3a_notes_analysis_2026-04-21.md` | Analysis of Miguel's 4,622-line RemNote research journal on Syn3A |
| `Synth3a/Syn3A_Research_Notes_RemNote.md` | The original RemNote export (deep literature review, parameter extraction, tool catalog) |
| `Whole_Cell_Modeling/` | Empty — awaiting cloned repos |

## The Two Published Models We Build On

### 1. JCVI-syn3A Whole-Cell Model (Luthey-Schulten Lab, UIUC)
- **Paper:** Thornburg et al., "Fundamental behaviors emerge from simulations of a living minimal cell," *Cell* 185(2):345-360, 2022
- **Code:** github.com/Luthey-Schulten-Lab/Minimal_Cell (well-stirred: CPU, ~4hrs/cell cycle)
- **Scale:** 493 genes, ~7,200 reactions, hybrid ODE/CME/RDME
- **Key parameter:** ~35,000 ATP/sec production rate
- **NOTE:** This is NOT the Covert Lab (Stanford). The Covert Lab did E. coli. "Lux3 Lab" in earlier notes = Luthey-Schulten Lab.

### 2. MitoMAMMAL (Habermann Lab)
- **Paper:** "MitoMAMMAL: A genome-scale metabolic model of mammalian mitochondria," *Bioinformatics Advances* 5(1), 2024
- **Code:** gitlab.com/habermann_lab/mitomammal (COBRApy, Python 3.8, MIT license)
- **Scale:** 560 reactions, 445 metabolites, 780 genes (GPR rules for human + mouse)
- **Format:** SBML Level 3 + COBRApy pFBA

## Miguel's Original Syn3A Work — Status

**Assessment (April 2026):** The RemNote notes (4,622 lines) reveal deep literature review and parameter extraction from 8+ foundational papers, but NO completed simulation code was ever produced. "Largely successful" (from Otter transcription) refers to conceptual understanding — the realization that mitochondria and Syn3A share import-dependent ATP production dynamics. No code exists to recover. The path forward builds on the published Luthey-Schulten and MitoMAMMAL code.

## Planned Computational Experiments

See `qbio_analysis_2026-04-21.md` for full experimental design. Summary:

1. **Transit Viability Window Prediction (PRIMARY):** Time-stepped FBA modeling ATP decay post-extraction using protein half-life data. Three substrate scenarios (intracellular, blood, ischemic). Produces decay curves with reuptake viability threshold.
2. **Single-Gene Stabilization Impact:** Which protein, if made more durable, extends the transit window the most?
3. **Syn3A Crosswalk (SUPPORTING):** Map shared import dependencies between Syn3A and mitochondria.
4. **Intervention Modeling:** Quantify transit window extension from antioxidants, cold chain, substrate supplementation, EV encapsulation.

## Items Still Needed

- [ ] Clone Luthey-Schulten-Lab/Minimal_Cell from GitHub
- [ ] Clone habermann_lab/mitomammal from GitLab
- [ ] Install COBRApy environment (conda, Python 3.8, GLPK solver)
- [ ] Compile ETC protein half-life dataset from literature (Complex I-V)
- [ ] Compile blood/ECF metabolite concentrations from HMDB
- [ ] Define mitophagy reuptake viability threshold from literature
- [ ] Register for q-bio Chicago ($200) at qbiochicago.org

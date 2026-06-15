# Mitochondria Maven — Project Index

**Mission:** Build autonomous, programmable mitochondria capable of extracellular existence, scalable extraction, and transplantation — toward the goal of mastering biological energy production.

**Core thesis:** All biological death reduces to ATP production failure. Mitochondria are the intervention point.

---

## Project Structure

### 01_Vision_and_Strategy/
The *why* of the project — grand vision, testable hypotheses, and research landscape.

| File | Role |
|---|---|
| IMOL-ERT_Vision.docx | Business plan and overarching vision — organoids-on-chip, biological modification as "pull requests on biology" |
| Research_Hypotheses.docx | 5 testable hypotheses (enhanced efficiency, biogenesis/aging, oxidative stress, DNA repair, fusion/fission balance) |
| Exploratory_Landscape.docx | 8-topic AI-assisted research scaffold with 50+ cited sources |
| Project_Overview.docx | Master project document — objectives, categories, progress, gaps, resources, glossary |
| Notebook_Transcription_Otter.txt | Voice transcription of personal notebooks — contains 10 research questions, 8 experiments, lab history, cross-project context |
| Strategy_Critique_and_Assumptions_2026-04-21.md | Rigorous assumption audit (6 project assumptions, 5 critique assumptions), thesis reframe from "autonomy" to "transit survivability," maps assumptions to testable computational experiments |
| **Executive_Summary_2026-04-21.md** | **START HERE. Full project orientation: thesis, 4-layer vision, unified stack, what exists vs. doesn't, two research threads, computational path, assumptions, forcing functions, 5-week sprint. Read before any other file.** |
| **Programmable_Mitochondria_Vision_2026-04-21.md** | **The full long-range vision: 4-layer architecture from transit viability (Layer 1, q-bio 2026) through programmable transplantation, gene delivery platform, and autonomous extracellular operation. Synthesized from notebook transcriptions. The "pull request on biology" framing.** |

### 02_Methodology/
The *how* — search methodology, evaluation criteria, and analytical frameworks.

| File | Role |
|---|---|
| BSHR_Loop.txt | Brainstorm-Search-Hypothesize-Refine information foraging methodology |
| Inclusion_Exclusion_Criteria.docx | 8-category taxonomy with inclusion/exclusion rules per category |
| Paper_Ranking_Framework.docx | Top-10 paper ranking + 5-dimension re-analysis rubric (categorization, findings, methods, gaps, synthesis) |
| Literature_Mapping.docx | Taxonomy applied to 5 key papers — demonstrates the analytical pipeline |

### 03_Study_Registry/
The screened paper database — 114 studies, all meeting inclusion criteria (probability 0.93-0.99).

| File | Role |
|---|---|
| studies.csv | 114 papers: title, author, year (1955-2024), screening status, inclusion probability |
| references.ris | Citation data in RIS format |
| source_archive.zip | Original import bundle from literature search |

### 04_Source_Literature/
Primary source papers organized by research thrust.

| Subdirectory | Contents |
|---|---|
| Extraction_Methods/ | 93 PDFs — the primary corpus of mitochondrial extraction/isolation papers |
| Mitochondrial_Transfer/ | 7 .docx summaries — thematic papers on transfer mechanisms and therapeutic applications |
| Reference_Papers/ | 15 PDFs — broader context (synthetic cells, bioenergy, cell signaling, transplantation) |

### 05_Extracted_Data/
AI-processed data from the source literature — three tiers of extraction.

| Subdirectory | Contents | Schema |
|---|---|---|
| Structured_JSON/ | 91 files — one per paper | Chunks with: raw text, protocol, organisms, summary, entities, references, topics, hypothetical questions, knowledge triplets |
| PDF_Metadata/ | 22 files — author, dates, URLs | Document metadata only (NOT full text content) |
| Protocol_Summaries/ | 9 batch files (combined_content) | Standardized sections: Organism, Protocol, Yield, Assessment, Equipment, Purpose, Difficulty, Category |

### 06_Synthesis/
Cross-paper analysis and knowledge synthesis outputs.

| File/Dir | Role |
|---|---|
| Comparative_Analysis/ | 12 .docx documents — cross-paper pattern synthesis by batch |
| Annotated_Bibliography.docx | Literature organized by the 8 research categories |
| Consolidated_Protocols.txt | All extraction protocols unified (13,268 lines) |

### 07_Lab_Manual/
Bench-ready protocols synthesized from the literature review.

| File | Role |
|---|---|
| Mitochondrial_Isolation_Report.pdf | 32-page report (Feb 2024): unified yeast protocol, ABCAM protocol with troubleshooting, yeast vs ABCAM comparison, equipment/reagent guide, buffer calculations, glossary |

### 08_Experimental_Work/
Lab experiments — planned and completed. See Experiments_Overview.md for details.

| Subdirectory | Status |
|---|---|
| Extraction_Optimization/ | Awaiting digitized Taguchi data and lab notebook |
| Lab_Notebooks/ | Physical notebook exists — needs scanning/digitization |
| Autonomy_Testing/ | Planned (Experiment E5 — reframed as transit viability validation) |
| Transplantation/ | Planned (Experiment E4) |

**Completed (2024):** Successful yeast mitochondrial extraction, Taguchi optimization, JC-1 membrane potential verification.

### 09_Computational_Modeling/
**Status: ACTIVE — q-bio Chicago 2026 abstract deadline May 31.** See Modeling_Overview.md for full plan.

Primary goal: predict the **functional transit window** for extracted mitochondria — how long they maintain ATP production during extracellular transit before reuptake viability is lost. Uses time-stepped FBA on MitoMAMMAL (560 reactions) constrained by ETC protein half-life data, validated against 2024 JC-1 extraction data.

| Subdirectory/File | Status |
|---|---|
| Synth3a/Syn3A_Research_Notes_RemNote.md | RemNote export found and analyzed (4,622 lines of literature review + parameter extraction; no simulation code) |
| Whole_Cell_Modeling/ | Awaiting cloned repos (Luthey-Schulten Lab Minimal_Cell + Habermann Lab MitoMAMMAL) |
| qbio_analysis_2026-04-21.md | Master analysis: 4 experiments designed, abstract drafted, 5-week timeline |
| syn3a_notes_analysis_2026-04-21.md | Assessment of original Syn3A work — conceptual understanding confirmed, no code to recover |

### 10_Research_Questions/
The 10 core questions driving the project, mapped to literature categories and experiments. See Research_Questions.md for full status tracking.

### Archive/
Retired and deduplicated materials.

---

## The 8 Literature Categories

1. Mitochondrial Extraction/Isolation Techniques
2. Mitochondrial Dynamics and Interactions
3. Fundamental Mitochondria Knowledge
4. Mitochondrial Lab Protocols and Techniques
5. Regulation and Dynamics of Mitochondria
6. Advances in Synthetic Biology for Organelle Mimicry
7. Mitochondrial Genomics and Bioinformatics Analysis
8. Case Studies: Practical Applications of Isolated Mitochondria

**Gaps identified:** Categories 3 (Fundamental Knowledge) and 7 (Genomics/Bioinformatics) have minimal literature coverage.

---

## Related Projects (Not in This Directory)

- **Holistic Performance Enhancement repo** — mostly retired; location TBD
- **Synth3a whole-cell modeling** — active; location TBD
- **113 additional research projects** — listed in personal notebooks; not digitized

---

## Key People

- **Miguel Ingram** — Project lead, self-funded researcher
- **Dr. Justin Nash** — Former collaborator (departed before grant funding)

---

*Last updated: April 2026*
*Reorganized from flat structure into pipeline-ordered folders*

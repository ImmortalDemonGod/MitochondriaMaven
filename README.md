# Mitochondria Maven

> Engineering autonomous, programmable, extracellular mitochondria — toward mastering biological ATP production.

**Core thesis:** at the limit, biological death reduces to ATP-production failure. Mitochondria *are* the energy system, and therefore the intervention point. This repository is an **engineering R&D program** built on a 114-paper literature foundation — not a literature review — aimed at making biology version-controllable: *audit the system, propose a verified change, deliver it.* A pull request on biology.

---

## Where the project is right now

The active frontier is **computational modeling of the mitochondrial "transit window"** (`09_Computational_Modeling/`): how long an extracted mitochondrion keeps producing ATP during extracellular transit before it can no longer be taken back up by a host cell. This is **Layer 1** of the program — and the part that's computationally tractable today.

**Method.** Time-stepped Flux Balance Analysis on the **MitoMAMMAL** mitochondrial genome-scale model (560 reactions, 445 metabolites, 782 genes), with nuclear-encoded proteins decaying on literature half-lives, coupled to a **Beard-2005 biophysical OXPHOS ODE** (plus MPTP / cardiolipin-peroxidation modules) for the composite model.

**Honest headline** — the model is a *mechanism scaffold and hypothesis generator*, not a calibrated predictor:

- **~29 h** = the protein-decay-only *ceiling* (an algebraic bound under uniform decay)
- **4–18 h** = empirical reality (MiR05 respirometry)
- **the gap between them is the engineering target** — non-proteomic failure modes (membrane / cardiolipin peroxidation, MPTP, Ca²⁺ overload, ROS) that FBA structurally cannot see

What's robust: a **145-gene essential set** (127/145 = **87.6% MitoCarta 3.0-validated**), Complex I's 39-subunit AND-clause as the decay-governing bottleneck, and a scenario-dependent failure partition. What's provisional: every *temporal* number — parameters are literature-range, not yet anchored to an independent wet-lab time-course. The full, self-audited reasoning trail lives in `09_Computational_Modeling/LAB_NOTEBOOK.md` and `09_Computational_Modeling/docs/investigation/`.

---

## The long-range vision (4 layers)

| Layer | Goal | Status |
|---|---|---|
| **1 — Transit viability** | Keep an extracted mitochondrion viable through extraction → transit → reuptake | **Active (modeled here)** |
| 2 — Programmable transplantation | Pre-engineer properties before extraction; express them in the recipient cell | Design |
| 3 — Gene-delivery platform | Mitochondria as the vehicle carrying a genetic payload to the nucleus | Concept |
| 4 — Autonomous extracellular operation | Mitochondria operating cell-free, indefinitely | Long-range |

The reframe that makes Layer 1 tractable: an extracted mitochondrion need not be *autonomous* — only to **survive transit until reuptake** restores nuclear protein import.

---

## Repository layout

A 10-stage pipeline (full map in [`INDEX.md`](INDEX.md)):

| Folder | Contents |
|---|---|
| `01_Vision_and_Strategy/` | Thesis, the 4-layer vision, assumption audits, strategy |
| `02_Methodology/` | Literature search + screening + ranking methodology |
| `03_Study_Registry/` | `studies.csv` — 114 screened papers (1955–2024) |
| `04_Source_Literature/` | Source-paper summaries (copyrighted PDFs kept local — see below) |
| `05_Extracted_Data/` | Structured extractions + AI-generated protocol summaries |
| `06_Synthesis/` | Cross-paper comparative analyses + consolidated protocols |
| `07_Lab_Manual/` | Bench-ready mitochondrial-isolation protocol (Feb 2024) |
| `08_Experimental_Work/` | Experiment plans E1–E8 (2024 wet-lab results pending digitization) |
| `09_Computational_Modeling/` | **The active modeling pipeline** — code, results, lab notebook, docs |
| `10_Research_Questions/` | The 10 core research questions, mapped to experiments |

---

## Computational setup

```bash
# clone with the external model submodules
git clone --recurse-submodules https://github.com/ImmortalDemonGod/MitochondriaMaven.git
cd MitochondriaMaven/09_Computational_Modeling

# (if already cloned without --recurse-submodules)
git submodule update --init --recursive

# create the conda environment (Miniforge, Python 3.10) + dependencies
./setup_environment.sh
```

**Stack:** Python 3.10 · COBRApy + GLPK (FBA) · SciPy LSODA (ODE) · NumPy / pandas / matplotlib.
**External models (git submodules):** [MitoMAMMAL](https://gitlab.com/habermann_lab/mitomammal) · [Human-GEM](https://github.com/SysBioChalmers/Human-GEM) (cross-model check). MitoCarta 3.0 (validation lookup) is downloaded separately from the Broad Institute.

Run an experiment, e.g.:

```bash
python scripts/investigation_phases/phase_a_dissection.py   # open the MitoMAMMAL model
python scripts/composite/experiment5_fba_ode.py             # the composite FBA↔ODE model
```

---

## Not in this repository (kept local)

To stay lean and avoid redistributing third-party material, the following are intentionally excluded (see `.gitignore`):

- **Copyrighted source papers** — 108 journal PDFs and their verbatim text extractions
- **Large external data** — a 137 MB literature-import archive; model omics datasets (these live inside the submodules)
- **Bulk process artifacts** — raw literature-verification JSON dumps (the synthesized findings are kept as `DOCINSIGHT_*.md`)

---

## Status, honestly

- ✅ Literature foundation (114 papers) and bench protocol — complete (2024)
- ✅ Transit-window modeling pipeline + composite FBA↔ODE model — built and self-audited
- ✅ Conference-style abstract + full manuscript outline — drafted (`09_Computational_Modeling/docs/conference_planning/`)
- ⏳ Independent empirical anchor (a wet-lab decay time-course) — the key open validation gap
- ⏳ Wet-lab experiments E1–E8 — planned

**Lead:** Miguel Ingram (independent researcher).

> Predictions in this repository are model outputs at literature-range parameters — hypotheses inviting wet-lab testing, not validated results.

# Computational Modeling — Mitochondria Maven

**Project goal:** Predict the functional transit window for extracted mammalian mitochondria using time-stepped Flux Balance Analysis (FBA) on the MitoMAMMAL genome-scale metabolic model. Output: abstract + manuscript outline — drafted, **NOT submitted** (q-bio Chicago 2026 deliberately dropped; May 31 2026 deadline lapsed).

**Core thesis:** Extracted mitochondria don't need to survive forever — only long enough to transit from extraction to recipient cell reuptake. The transit window is computationally tractable: model nuclear-encoded ETC protein decay over time, compute when ATP flux drops below the reuptake viability threshold.

**Current status (post-Phase G + two framing corrections, 2026-04-23):** Forensic investigation complete. Defensible claims:

- **Protein-decay-only ceiling: 29h** (model output under uniform t½=12h, threshold=20%, buffer=1.05; algebra-derivable as `-t½ × log₂(threshold/buffer)`)
- **Heterogeneous-decay prediction: 5-15h** (matches published 4-18h MiR05-buffer empirical range; assumes per-subunit independence which CI subunits likely violate)
- **Three-class gene structure** in the 374 mouse nuclear genes: 145 individually-essential (single KO impact >0.01%), ~207 synthetically-essential (individually redundant via OR-alternatives but collectively required), ~22 truly redundant
- **89% of essentials have mitochondrial GO localization** — biologically validated
- **Largest mouse-only AND-clause: Complex I, N=39** — governs effective transit window via order statistics
- **20% ATP threshold ≈ ΔΨm −100 mV ≈ PINK1 stabilization** — empirically anchored

What we did NOT establish:
- Whether A3 (some minimal viable set exists) is true — our 145 partition is not minimal but a different partition might be
- Whether the convergence of heterogeneity and ROS coupling on 8h is independent confirmation or sweep coincidence
- Whether non-proteomic failure modes will close the 29h-vs-empirical gap (the structural disjunction is defensible; the engineering recommendation is not)

See `docs/investigation/FRAMING_2026-04-23.md` for the canonical defensible claims list and the corrections applied to earlier framing.

---

## Quick Start

```bash
# 1. Install environment (Apple Silicon / arm64 macOS)
bash setup_environment.sh

# 2. Run any experiment from the project root — paths derive from paths.py
ENV=/opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/python

# Investigation phases (current/canonical)
$ENV scripts/investigation_phases/phase_a_dissection.py
$ENV scripts/investigation_phases/phase_b_annotate_essentials.py
$ENV scripts/investigation_phases/phase_b_cluster_and_sweep.py
$ENV scripts/investigation_phases/phase_b6_deep_dive.py
$ENV scripts/investigation_phases/phase_c_forensic_29h.py
$ENV scripts/investigation_phases/phase_d_adversarial_suite.py
$ENV scripts/investigation_phases/phase_e_anomaly_hunt.py

# Post-audit experiments (Session 3 corrected versions)
$ENV scripts/experiments_v2/experiment1_v2_transit_window.py
$ENV scripts/experiments_v2/experiment1b_v2_gpr_knockout.py
$ENV scripts/experiments_v2/experiment1c_v2_halflife_sweep.py
$ENV scripts/experiments_v2/experiment1d_minimal_set.py
```

All paths derive from `paths.py` — moving scripts doesn't break them.

---

## Directory Map

```
09_Computational_Modeling/
├── README.md                           ← this file
├── LAB_NOTEBOOK.md                     ← session-by-session log (top-level for visibility)
├── paths.py                            ← single source of truth for all paths
├── decay_utils.py                      ← shared utility module (GPR-aware decay, etc.)
├── setup_environment.sh                ← reproducible env setup
├── requirements.txt                    ← pinned Python deps
│
├── docs/
│   ├── investigation/                  ← Phase A-F findings (current science)
│   │   ├── INVESTIGATION_SYNTHESIS_2026-04-23.md   ← THE CONCLUSION — read this
│   │   ├── MITOMAMMAL_DISSECTION.md                ← Phase A: opened the black box
│   │   ├── ESSENTIAL_GENES_DEEP_DIVE.md            ← Phase B: N=10 gene profiles
│   │   ├── WHY_29_HOURS.md                         ← Phase C: forensic dissection
│   │   ├── TRUST_LEDGER.md                         ← Phase D: adversarial suite
│   │   ├── ANOMALIES_AND_HIDDEN_FINDINGS.md        ← Phase E: heterogeneity finding
│   │   └── AUDIT_2026-04-22.md                     ← initial audit (pre-investigation)
│   └── conference_planning/
│       ├── qbio_analysis_2026-04-21.md             ← original 4-experiment design
│       ├── qbio_conference_analysis_2026-04-21.md  ← q-bio Chicago details
│       ├── qbio_chicago_lodging_2026-04-21.md      ← logistics
│       ├── syn3a_notes_analysis_2026-04-21.md      ← Syn3A literature review
│       ├── DOCINSIGHT_MITO_QUERY_GUIDE.md          ← DocInsight query templates
│       └── Modeling_Overview.md
│
├── scripts/
│   ├── investigation_phases/           ← canonical: Phase A–E forensic investigation
│   │   ├── phase_a_dissection.py
│   │   ├── phase_b_annotate_essentials.py
│   │   ├── phase_b_cluster_and_sweep.py
│   │   ├── phase_b6_deep_dive.py
│   │   ├── phase_c_forensic_29h.py
│   │   ├── phase_d_adversarial_suite.py
│   │   └── phase_e_anomaly_hunt.py
│   ├── experiments_v2/                 ← post-audit corrected experiments
│   │   ├── experiment1_v2_transit_window.py
│   │   ├── experiment1b_v2_gpr_knockout.py
│   │   ├── experiment1c_v2_halflife_sweep.py
│   │   └── experiment1d_minimal_set.py
│   └── archive_v1/                     ← deprecated v1 scripts (kept for reproducibility)
│       ├── experiment1_transit_window.py
│       ├── experiment1b_gene_sensitivity.py
│       └── experiment1c_halflife_sweep.py
│
├── results/                            ← outputs organized by phase
│   ├── phase_a/                        ← baseline solution
│   ├── phase_b/                        ← annotations, gene scores, partition
│   ├── phase_c/                        ← forensic LP audit
│   ├── phase_d/                        ← adversarial suite results
│   ├── phase_e/                        ← anomaly hunt + heterogeneity data
│   ├── experiments_v2/                 ← v2 experiment outputs
│   └── archive_v1/                     ← v1 outputs (deprecated)
│
└── Whole_Cell_Modeling/
    └── mitomammal/                     ← cloned MitoMAMMAL repo (Chapman et al.)
```

---

## Architecture: paths.py is the single source of truth

All scripts import paths from `paths.py`. To change where outputs go (or move the project), edit ONE file. Scripts derive paths from `paths.py`'s location, not from hard-coded user-specific strings.

**Key utilities:**
- `MODEL_PATH` — the MitoMAMMAL XML file
- `RESULTS_DIR` — base results directory
- `results_path('phase_x', 'filename.csv')` — Path under `results/phase_x/`, creates parent dir
- `investigation_doc('FILE.md')` — Path under `docs/investigation/`
- `MITOMAMMAL_DIR`, `SUPP_TABLE_PATH` — source data paths

**Bootstrap pattern (used in scripts):**
```python
import sys
from pathlib import Path
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import MODEL_PATH, results_path, ...
```

This works regardless of which directory the script lives in.

---

## Key Findings (from `INVESTIGATION_SYNTHESIS_2026-04-23.md`)

1. **145-gene essential set** (89% mitochondrial GO) — biologically validated stabilization target
2. **Heterogeneity-driven decay acceleration** — under realistic protein t½ heterogeneity (lognormal log_sigma=0.6), transit window drops from 29h → 8h, matching experimental data
3. **All ETC complexes saturate together** at the threshold — no single bottleneck
4. **First-failure reaction:** `PIt2mB_mitoMap` (phosphate transporter) — not an ETC complex
5. **The 29h was algebra:** `TW = -t½ × log₂(threshold) × buffer_factor`. FBA contributes zero temporal content under uniform decay; its value is the GPR `min` operator under non-uniform decay.

---

## Environment Notes (ARM64)

- `conda install -c conda-forge cobra` fails — `python-libsbml` not built for ARM64
- `pip install cobra` inside conda env works (uses pre-built wheel)
- `swiglpk` GLPK solver binding installs cleanly via pip
- MitoMAMMAL README recommends Python 3.8; we use 3.10 with no issues

Full installation in `setup_environment.sh`. Tested 2026-04-22 on macOS 25.3.0, Apple M-series.

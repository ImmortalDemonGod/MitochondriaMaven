"""
paths.py — Single source of truth for all paths in the computational framework.

All scripts should import from here. Reorganizing the directory only requires
updating this file. Paths are derived from this module's location, not from
hard-coded user-specific strings.

Usage:
    from paths import MODEL_PATH, RESULTS_DIR, results_path
    df.to_csv(results_path('phase_b', 'essential_genes_annotated.csv'))
"""

from pathlib import Path
import sys
import os

# Project root = directory containing this file
PROJECT_ROOT = Path(__file__).resolve().parent

# ── Source data ───────────────────────────────────────────────────────────
MITOMAMMAL_DIR = PROJECT_ROOT / "Whole_Cell_Modeling" / "mitomammal"
MODEL_PATH = MITOMAMMAL_DIR / "6_universal_mito_model.xml"
SUPP_TABLE_PATH = MITOMAMMAL_DIR / "Chapman_etal_TableS1a_tab.txt"

# ── Output directories ────────────────────────────────────────────────────
RESULTS_DIR = PROJECT_ROOT / "results"

# Per-phase result subdirectories (created on demand)
RESULTS_PHASE_A = RESULTS_DIR / "phase_a"
RESULTS_PHASE_B = RESULTS_DIR / "phase_b"
RESULTS_PHASE_C = RESULTS_DIR / "phase_c"
RESULTS_PHASE_D = RESULTS_DIR / "phase_d"
RESULTS_PHASE_E = RESULTS_DIR / "phase_e"
# Phase G already has results/ but no constant defined; the phase_g/ dir exists
RESULTS_PHASE_G = RESULTS_DIR / "phase_g"
# v6 plan additions
RESULTS_PHASE_H = RESULTS_DIR / "phase_h"  # DocInsight extractions + empirical re-runs
RESULTS_PHASE_I = RESULTS_DIR / "phase_i"  # Syn3A crosswalk
RESULTS_PHASE_J = RESULTS_DIR / "phase_j"  # Intervention modeling (Exp 4)
RESULTS_PHASE_K = RESULTS_DIR / "phase_k"  # Wet-lab validation (Exp 3)
RESULTS_EXPERIMENTS_V2 = RESULTS_DIR / "experiments_v2"
RESULTS_ARCHIVE_V1 = RESULTS_DIR / "archive_v1"

# Composite (multi-scale) work — FBA + ODE + (future) MPTP + membrane
# See docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md
RESULTS_COMPOSITE = RESULTS_DIR / "composite"

# Cortassa-Aon / Beard 2005 parameter files (published SI extractions)
CORTASSA_DIR = PROJECT_ROOT / "Whole_Cell_Modeling" / "cortassa"

# ── Document directories ──────────────────────────────────────────────────
DOCS_DIR = PROJECT_ROOT / "docs"
DOCS_INVESTIGATION = DOCS_DIR / "investigation"
DOCS_PLANNING = DOCS_DIR / "conference_planning"

# Top-level docs (kept at root for visibility)
LAB_NOTEBOOK = PROJECT_ROOT / "LAB_NOTEBOOK.md"
README = PROJECT_ROOT / "README.md"

# ── Code directories ──────────────────────────────────────────────────────
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SCRIPTS_PHASES = SCRIPTS_DIR / "investigation_phases"
SCRIPTS_EXPERIMENTS_V2 = SCRIPTS_DIR / "experiments_v2"
SCRIPTS_COMPOSITE = SCRIPTS_DIR / "composite"  # FBA + ODE + (future) MPTP composite work
SCRIPTS_ARCHIVE_V1 = SCRIPTS_DIR / "archive_v1"

# ── Helpers ───────────────────────────────────────────────────────────────

def results_path(*parts) -> Path:
    """Return Path under results/, creating parent dir if needed.
    Usage: results_path('phase_b', 'gene_scores.csv') -> .../results/phase_b/gene_scores.csv
    """
    p = RESULTS_DIR.joinpath(*parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def docs_path(*parts) -> Path:
    """Return Path under docs/, creating parent dir if needed."""
    p = DOCS_DIR.joinpath(*parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def investigation_doc(name: str) -> Path:
    """Path for a Phase-A-through-F investigation document."""
    return docs_path("investigation", name)


def planning_doc(name: str) -> Path:
    """Path for a conference/planning document."""
    return docs_path("conference_planning", name)


def ensure_on_syspath():
    """Add PROJECT_ROOT to sys.path so scripts can import shared modules.
    Call this at the top of any script that lives below PROJECT_ROOT and
    needs to `from decay_utils import ...` or similar.
    """
    root_str = str(PROJECT_ROOT)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


# Auto-ensure syspath when this module is imported (no harm in being idempotent)
ensure_on_syspath()

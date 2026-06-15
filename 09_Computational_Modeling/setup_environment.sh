#!/usr/bin/env bash
# Setup script for the Mitochondria Maven computational environment.
# Tested on Apple Silicon (arm64) macOS, April 2026.
#
# Usage:
#   bash setup_environment.sh
#
# This installs Miniforge (ARM64-native conda), creates the `mitomammal`
# environment, installs COBRApy via pip (conda-forge lacks ARM64 python-libsbml),
# and clones the MitoMAMMAL repo from GitLab.

set -e

echo "================================================================"
echo "Mitochondria Maven — Computational Environment Setup"
echo "================================================================"

# ── 1. Install Miniforge (ARM64 conda) ──────────────────────────────
if ! command -v conda &> /dev/null && [ ! -d "/opt/homebrew/Caskroom/miniforge" ]; then
    echo "[1/5] Installing Miniforge via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "ERROR: Homebrew not installed. Install from https://brew.sh first."
        exit 1
    fi
    brew install miniforge
else
    echo "[1/5] Miniforge already installed — skipping."
fi

CONDA_BIN="/opt/homebrew/Caskroom/miniforge/base/bin/conda"
ENV_PYTHON="/opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/python"
ENV_PIP="/opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/pip"

# ── 2. Create conda env (Python 3.10) ───────────────────────────────
if [ ! -d "/opt/homebrew/Caskroom/miniforge/base/envs/mitomammal" ]; then
    echo "[2/5] Creating mitomammal conda env (Python 3.10)..."
    "$CONDA_BIN" create -n mitomammal python=3.10 -y
else
    echo "[2/5] mitomammal env already exists — skipping."
fi

# ── 3. Install dependencies via pip ─────────────────────────────────
# Note: We use pip inside the conda env because conda-forge does NOT
# ship python-libsbml for ARM64 Python 3.10 (as of April 2026).
echo "[3/5] Installing dependencies via pip..."
"$ENV_PIP" install -r requirements.txt

# ── 4. Verify COBRApy installation ──────────────────────────────────
echo "[4/5] Verifying COBRApy installation..."
"$ENV_PYTHON" -c "
import cobra
print(f'  cobra version: {cobra.__version__}')
print(f'  solver: {cobra.Configuration().solver.__name__}')
m = cobra.Model('test')
print('  COBRApy working.')
"

# ── 5. Clone MitoMAMMAL repo if needed ──────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MITO_DIR="$SCRIPT_DIR/Whole_Cell_Modeling/mitomammal"
if [ ! -d "$MITO_DIR" ]; then
    echo "[5/5] Cloning MitoMAMMAL from GitLab..."
    mkdir -p "$SCRIPT_DIR/Whole_Cell_Modeling"
    git clone https://gitlab.com/habermann_lab/mitomammal.git "$MITO_DIR"
else
    echo "[5/5] MitoMAMMAL already cloned — skipping."
fi

# ── Verify the model loads ──────────────────────────────────────────
echo ""
echo "Smoke test: loading MitoMAMMAL model..."
"$ENV_PYTHON" -c "
import cobra
m = cobra.io.read_sbml_model('$MITO_DIR/6_universal_mito_model.xml')
print(f'  Reactions: {len(m.reactions)} (expected: 560)')
print(f'  Genes: {len(m.genes)} (expected: 782)')
print(f'  Metabolites: {len(m.metabolites)} (expected: 445)')
sol = m.optimize()
print(f'  Baseline ATP flux: {sol.objective_value:.4f} (expected: ~100.89)')
"

echo ""
echo "================================================================"
echo "Setup complete. To run experiments:"
echo "  $ENV_PYTHON experiment1_transit_window.py"
echo "  $ENV_PYTHON experiment1b_gene_sensitivity.py"
echo "  $ENV_PYTHON experiment1c_halflife_sweep.py"
echo ""
echo "Results will be written to: $SCRIPT_DIR/results/"
echo "================================================================"

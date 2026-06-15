# Cortassa-Aon / Beard Parameter Files

**Scaffolded:** 2026-04-23
**Status:** empty — populate during composite planning session
**Strategic context:** `09_Computational_Modeling/docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md`

## Purpose

Houses parameter sets and reference curves from:
- **Cortassa, Aon, Marbán, Winslow, O'Rourke 2003** — "An integrated model of cardiac mitochondrial energy metabolism and calcium dynamics" (Biophys J)
- **Cortassa, Aon 2006** (and related 2014 updates) — extensions with ROS-Ca²⁺ coupling
- **Beard 2005** — "A biophysical model of the mitochondrial respiratory system and oxidative phosphorylation" (PLoS Comp Bio)
- **Bazil, Dash, Beard 2016** (deferred; stochastic MPTP, for later layer)

## Expected contents (to populate)

- `cortassa_2003_params.csv` — rate constants, concentrations, initial conditions
- `cortassa_2003_reference_curves.csv` — published ΔΨm, ATP, NADH traces for validation
- `beard_2005_params.csv` — oxidative phosphorylation kinetic parameters
- `species_adapter_notes.md` — rat cardiac → mouse cardiac parameter transfer notes

## Provenance discipline

Every parameter value requires:
- Source citation (paper + table/figure + SI location)
- Original unit (convert explicitly, don't silently rescale)
- Temperature / species / tissue context
- Uncertainty range if reported

This matches the discipline applied to `ci_subunit_data.csv` in `results/phase_h/`.

# Composite (Multi-Scale) Experiments

**Scaffolded:** 2026-04-23
**Status:** directory scaffolded, no experiments run yet
**Strategic context:** `docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md`

## Purpose

Multi-scale computational model composing:
1. FBA + protein decay (from `experiments_v2/`) — proteomics capacity envelope
2. ODE energetics (Cortassa-Aon 2003/2006; Beard 2005) — ΔΨm, ATP, respiration dynamics
3. (future) Stochastic MPTP — Bazil-Beard 2016
4. (future) Membrane / cardiolipin biophysics — fragmentary literature

Goal: replace the single fitted `POST_EXTRACTION_ACCELERATION = 30.0` scalar in
`experiment1_v3_empirical.py` with a mechanistically-derived ΔΨm collapse time.

## Why a separate subfolder

`experiments_v2/` is FBA-centric (cobra, GPR, pFBA). The composite work is a
different paradigm (ODE integration, state vectors, scipy.integrate). Keeping
them separate preserves the FBA codebase's cleanliness while allowing the
composite to develop its own conventions.

Shared infrastructure (paths.py, MODEL_PATH, 145-gene set, TRUST_LEDGER,
decay_utils capacity envelope) is consumed across the boundary via imports.

## Entry points (planned)

| Script | Purpose | Status |
|---|---|---|
| `experiment5_fba_ode.py` | Option (c) minimum viable: FBA + ODE coupling, no MPTP/membrane | Not written |
| `validate_against_cortassa.py` | Reference-curve validation of ODE layer in isolation | Not written |
| `experiment6_full_composite.py` | Option (b) full: FBA + ODE + MPTP + membrane | Deferred |

## Dependencies

- Already available: `cobra`, `numpy`, `pandas`, `matplotlib`, `decay_utils`
- Needed for composite: `scipy.integrate` (already a scipy dependency — no new install)
- Parameter files: `Whole_Cell_Modeling/cortassa/` (to be populated from published SIs)

## Kill criterion

From `LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md` decision gates:
- If G1 fails (Cortassa params not pullable) → fall back to Beard 2005 alone
- If G2 fails (coupling produces non-sane dynamics) → revisit coupling math
- If G3 fails (composite can't reproduce MiR05 range without fitted scalar) → investigate mis-parameterized layer
- If all three of G1/G2/G3 fail → archive this directory, revert to scaffolding-paper submission (Option a)

None of the failures lose existing FBA work; option (a) remains a valid fallback.

## Audit discipline

Composite work follows the same audit discipline as the FBA pipeline:
- Every claim traceable to code + parameter source
- Every hardcoded scalar flagged with provenance
- Separate `docs/investigation/COMPOSITE_AUDIT_*.md` thread (distinct from
  the FBA audit in `AUDIT_2026-04-23.md`)
- TRUST_LEDGER updates for each new defensible claim

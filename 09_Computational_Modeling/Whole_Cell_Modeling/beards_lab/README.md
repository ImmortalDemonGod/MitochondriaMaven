# Beard 2005 OXPHOS Model — Parameter Acquisition

**Acquired:** 2026-04-24 (Week 1 Day 1; Gate G1)
**Status:** GATE G1 PASS — parameters obtained in <1 day
**Primary source:** `beards-lab/QAMAS_book` repo, `Tellurium_code/in_vitro_correct_stoicheometry.py`
**Reference paper:** Beard DA (2005) "A biophysical model of the mitochondrial respiratory system and oxidative phosphorylation" *PLoS Comp Bio* 1(4):e36.
**Erratum:** Beard 2006 PLoS CB — stoichiometry corrections incorporated into QAMAS "correct_stoicheometry" version
**Pedagogical reference:** Randall, Barazanji, Beard — "Quantitative Analysis of Mitochondrial ATP Synthesis" (QAMAS book)

## Files

| File | Purpose |
|---|---|
| `beard_2005_params.csv` | All rate constants, pool concentrations, stoichiometric coefficients with per-parameter provenance columns |
| `beard_2005_initial_conditions.csv` | Initial concentrations for the 14 state variables |
| `beard_qamas_in_vitro_reference.py` | Full Tellurium/Antimony source from QAMAS, preserved for equation reference |

## Provenance note

Beard 2005 is GREEN (per Phase 1 exploration audit). Parameters were obtained from QAMAS rather than directly from Beard 2005 paper tables because:

1. QAMAS encodes the **corrected stoichiometry** (Beard 2006 erratum) directly — saves a manual correction pass
2. QAMAS version has explicit unit annotations in Antimony source — easier to audit
3. The underlying rate constants are identical to Beard 2005; QAMAS adds initial conditions for the in-vitro (isolated mito in buffer) experimental context, which matches our use case

If future audit finds a parameter-transcription issue, cross-reference against:
- BioModels MODEL4151491057 (SBML, auto-converted from CellML, non-curated)
- Beard 2005 PLoS CB paper Tables 1–3 + Beard 2006 erratum

## Species / tissue / temperature caveats

All activity parameters (X_DH, X_C1, X_C3, X_C4, X_F, E_ANT, E_PiC, X_H) are **fit to cardiac mitochondrial data** at 37°C. For MitoMAMMAL coupling:
- MitoMAMMAL is mouse cardiac + BAT
- Beard 2005 is primarily bovine submitochondrial particles + rat cardiac mitochondria
- Cross-species rate constants are acceptable for thermodynamic drivers; kinetic Vmax may differ 2–5× per QAMAS caveats
- Ex 5.5 cold-chain intervention scales activities via Q10; accounts for temperature variation

## Load-bearing parameters for composite

Per Constraint 2 (small-N deep dives N=3), these parameters dominate the ODE behavior we care about:

- **X_C1** (Complex I activity) → couples to FBA `CI_mitoMap` capacity
- **X_F** (F1F0 activity) → couples to FBA `CV_mitoMap` capacity
- **E_ANT** (ANT expression level) → couples to FBA `ATPtmB_mitoMap` capacity
- Also: **k2o_ANT, k3o_ANT, K0o_D, K0o_T, A, B, C** — the ANT kinetic submodel from Metelkin 2006, embedded in Beard 2005

Ex 5.1 baseline validation specifically watches these for transcription accuracy.

## What's missing

- Not pulled yet: Beard 2005 Fig 2–4 reference curves for Ex 5.1 validation. TODO during Ex 5.1 implementation — may need to digitize from paper PDF or find published supplementary data.
- Not applicable for option (c): Cortassa 2003 ROS extension params — only needed if Ex 5.5 MitoQ mechanism requires it.

## Audit cross-reference

Gate G1 outcome recorded in `docs/investigation/COMPOSITE_AUDIT_2026-04-24.md` gate log.

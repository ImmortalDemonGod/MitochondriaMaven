# MitoMAMMAL Dissection — Baseline Biochemistry Trace
**Date:** 2026-04-22
**Model:** `6_universal_mito_model.xml` (from Chapman et al. 2024)
**Baseline solution:** pFBA, objective `OF_ATP_mitoMap` = 100.8923

**Purpose:** Before running more experiments on this model, understand what it actually computes. This document traces the baseline FBA solution reaction-by-reaction to document the biochemistry, the abstractions, and the structural features that matter for our transit viability work.

---

## A.1 — ATP Synthesis Pathway Trace

Following the ATP molecule backwards from the objective to external substrates.

### Who produces cytoplasmic ATP (`atp_c`)?
- `ATPtmB_mitoMap` (+99.926 atp_c/h): 0.82 PMF_c + adp_c + atp_m <=> 0.82 PMF_m + adp_m + atp_c
- `PYK` (+1.906 atp_c/h): adp_c + h_c + pep_c --> atp_c + pyr_c
- `PGK` (+1.810 atp_c/h): 3pg_c + atp_c <=> 13dpg_c + adp_c

### Who consumes cytoplasmic ATP (`atp_c`)?
- `OF_ATP_mitoMap` (-100.892 atp_c/h): atp_c + h2o_c --> adp_c + biomass_c + h_c + pi_c
- `PFK` (-0.900 atp_c/h): atp_c + f6p_c --> adp_c + fdp_c + h_c
- `HEX1` (-0.900 atp_c/h): atp_c + glc_D_c --> adp_c + g6p_c + h_c
- `ADK1` (-0.470 atp_c/h): amp_c + atp_c <=> 2.0 adp_c
- `FACOAL160i` (-0.470 atp_c/h): atp_c + coa_c + hdca_c --> amp_c + pmtcoa_c + ppi_c

### Who produces matrix ATP (`atp_m`)?
- `CV_mitoMap` (+93.393 atp_m/h): 2.7 PMF_c + adp_m + h_m + pi_m <=> 2.7 PMF_m + atp_m + h2o_m
- `SUCOASm` (+6.575 atp_m/h): atp_m + coa_m + succ_m <=> adp_m + pi_m + succoa_m

### Who consumes matrix ATP (`atp_m`)?
- `ATPtmB_mitoMap` (-99.926 atp_m/h): 0.82 PMF_c + adp_c + atp_m <=> 0.82 PMF_m + adp_m + atp_c
- `PPCOACm` (-0.027 atp_m/h): atp_m + hco3_m + ppcoa_m --> adp_m + h_m + mmcoa_S_m + pi_m
- `MCCCrm` (-0.016 atp_m/h): 3mb2coa_m + atp_m + hco3_m --> 3mgcoa_m + adp_m + h_m + pi_m

### Reducing equivalent inputs — NADH

**Matrix NADH producers (top 5):**
- `MDHm` (+9.128): mal_L_m + nad_m <=> h_m + nadh_m + oaa_m
- `ICDHxm` (+6.897): icit_m + nad_m --> akg_m + co2_m + nadh_m
- `AKGDm` (+6.822): akg_m + coa_m + nad_m --> co2_m + nadh_m + succoa_m
- `PDHm` (+2.608): coa_m + nad_m + pyr_m --> accoa_m + co2_m + nadh_m
- `HACD1m` (+0.500): aacoa_m + h_m + nadh_m <=> 3hbcoa_m + nad_m

**Matrix NADH consumers (top 5):**
- `CI_mitoMap` (-29.369): 3.996 PMF_m + h_m + nadh_m + 0.002 o2_m + 0.999 q10_m <=> 3.996 PMF_c + nad_m + 0.002 o2s_

### Reducing equivalent inputs — ubiquinol (electron carrier after CII)

**q10h2_m producers:**
- `CI_mitoMap` (+29.339): 3.996 PMF_m + h_m + nadh_m + 0.002 o2_m + 0.999 q10_m <=> 3.996 PMF_c + nad_m + 0.002 o2s_
- `CII_mitoMap` (+6.849): q10_m + succ_m <=> fum_m + q10h2_m
- `ACADLC16_mitoMap` (+0.470): h2o_m + pmtcoa_m + q10_m --> 3hexdcoa_m + q10h2_m
- `ACADLC14_mitoMap` (+0.470): h2o_m + q10_m + tetd7ecoa_m --> 3tetd7ecoa_m + q10h2_m
- `r1447_mitoMap` (+0.470): ddcacoa_m + q10_m --> dd2coa_m + q10h2_m

**q10h2_m consumers:**
- `CIII_mitoMap` (-39.541): 2.0 PMF_m + 2.0 ficytC_m + q10h2_m <=> 4.0 PMF_c + 2.0 focytC_m + q10_m

### ETC complex flux summary (baseline)

| Reaction | Flux | Role |
|---|---|---|
| `CI_mitoMap` | +29.369 | NADH→Q, pumps PMF |
| `CII_mitoMap` | +6.849 | FADH2→Q (no pumping) |
| `CIII_mitoMap` | +39.541 | QH2→cyt c, pumps PMF |
| `CIV_mitoMap` | +19.771 | cyt c→O2, pumps PMF |
| `CV_mitoMap` | +93.393 | ADP+Pi→ATP, consumes PMF |
| `ATPtmB_mitoMap` | +99.926 | ATP/ADP exchange, consumes PMF |
| `OF_ATP_mitoMap` | +100.892 | cytoplasmic ATP hydrolysis (objective) |


---

## A.2 — PMF (Proton-Motive-Force) Abstraction

MitoMAMMAL uses abstract `PMF_m` and `PMF_c` metabolites instead of explicit proton stoichiometry across compartments. Here's what these currencies do at baseline.

### `PMF_m`

**Producers (stoich × flux > 0):**
- `CV_mitoMap` (stoich=+2.700, flux=+93.393, produces +252.162 PMF_m/h)
- `ATPtmB_mitoMap` (stoich=+0.820, flux=+99.926, produces +81.939 PMF_m/h)
- `PIt2mB_mitoMap` (stoich=+0.180, flux=+99.917, produces +17.985 PMF_m/h)
- `ASPGLUmB_mitoMap` (stoich=+1.000, flux=+2.231, produces +2.231 PMF_m/h)
- `PYRt2m` (stoich=+0.180, flux=+2.490, produces +0.448 PMF_m/h)
- `CITtbm` (stoich=-1.000, flux=-0.096, produces +0.096 PMF_m/h)
- `GLUt2mB_mitoMap` (stoich=+0.180, flux=+0.183, produces +0.033 PMF_m/h)
- `LYStmB_mitoMap` (stoich=+0.820, flux=+0.030, produces +0.025 PMF_m/h)
**Total PMF_m production: +354.919/h**

**Consumers (stoich × flux < 0):**
- `CIV_mitoMap` (stoich=-8.000, flux=+19.771, consumes -158.165 PMF_m/h)
- `CI_mitoMap` (stoich=-3.996, flux=+29.369, consumes -117.357 PMF_m/h)
- `CIII_mitoMap` (stoich=-2.000, flux=+39.541, consumes -79.083 PMF_m/h)
- `r0838B_mitoMap` (stoich=+0.820, flux=-0.320, consumes -0.262 PMF_m/h)
- `BHBtmB_mitoMap` (stoich=-0.820, flux=+0.048, consumes -0.039 PMF_m/h)
- `ACACt2mB_mitoMap` (stoich=-0.180, flux=+0.114, consumes -0.021 PMF_m/h)
**Total PMF_m consumption: -354.926/h**
**Steady-state balance (should be ~0): -0.007900**

### `PMF_c`

**Producers (stoich × flux > 0):**
- `CIII_mitoMap` (stoich=+4.000, flux=+39.541, produces +158.165 PMF_c/h)
- `CI_mitoMap` (stoich=+3.996, flux=+29.369, produces +117.357 PMF_c/h)
- `CIV_mitoMap` (stoich=+4.000, flux=+19.771, produces +79.083 PMF_c/h)
- `r0838B_mitoMap` (stoich=-0.820, flux=-0.320, produces +0.262 PMF_c/h)
- `BHBtmB_mitoMap` (stoich=+0.820, flux=+0.048, produces +0.039 PMF_c/h)
- `ACACt2mB_mitoMap` (stoich=+0.180, flux=+0.114, produces +0.021 PMF_c/h)
**Total PMF_c production: +354.926/h**

**Consumers (stoich × flux < 0):**
- `CV_mitoMap` (stoich=-2.700, flux=+93.393, consumes -252.162 PMF_c/h)
- `ATPtmB_mitoMap` (stoich=-0.820, flux=+99.926, consumes -81.939 PMF_c/h)
- `PIt2mB_mitoMap` (stoich=-0.180, flux=+99.917, consumes -17.985 PMF_c/h)
- `ASPGLUmB_mitoMap` (stoich=-1.000, flux=+2.231, consumes -2.231 PMF_c/h)
- `PYRt2m` (stoich=-0.180, flux=+2.490, consumes -0.448 PMF_c/h)
- `CITtbm` (stoich=+1.000, flux=-0.096, consumes -0.096 PMF_c/h)
- `GLUt2mB_mitoMap` (stoich=-0.180, flux=+0.183, consumes -0.033 PMF_c/h)
- `LYStmB_mitoMap` (stoich=-0.820, flux=+0.030, consumes -0.025 PMF_c/h)
**Total PMF_c consumption: -354.919/h**
**Steady-state balance (should be ~0): +0.007900**


---

## A.3 — Objective Functions

Model has 4 objective functions (artificial sinks representing biomass demand):

### `OF_ATP_mitoMap` — R_OF_ATP_mitoMap Maximum ATP production (ATP hydrolysis)
- Stoichiometry: `atp_c + h2o_c --> adp_c + biomass_c + h_c + pi_c`
- Bounds: (0.0, 1000.0)
- Baseline flux: +100.892
- Is current objective? True

### `OF_HEME_mitoMap` — R_OF_HEME_mitoMap Maximum Heme production
- Stoichiometry: `pheme_m --> biomass_m`
- Bounds: (0.0, 1000.0)
- Baseline flux: +0.000
- Is current objective? False

### `OF_LIPID_mitoMap` — R_OF_LIPID_mitoMap Maximum lipid synthesis (Mito Inner Membrane)
- Stoichiometry: `0.18 clpn_hs_m + 0.4 pchol_hs_m + 0.34 pe_hs_m + 0.3 ps_hs_m --> biomass_m`
- Bounds: (0.0, 1000.0)
- Baseline flux: +0.000
- Is current objective? False

### `OF_PROTEIN_mitoMap` — R_OF_PROTEIN_mitoMap Maxmium production of amino acids for protein synthesis
- Stoichiometry: `0.76 ala_L_m + 0.54 arg_L_m + 0.42 asn_L_m + 0.53 asp_L_m + 0.07 cys_L_m + 0.49 gln_L_m + 0.58 glu_L_m + 0.81 gly_m + 0.19 his_L_m + 0.43 ile_L_m + 0.82 leu_L_m + 0.89 lys_L_m + 0.23 met_L_m + 0.39 phe_L_m + 0.62 pro_L_m + 0.59 ser_L_m + 0.47 thr_L_m + 0.02 trp_L_m + 0.24 tyr_L_m + 0.53 val_L_m --> biomass_m`
- Bounds: (0.0, 1000.0)
- Baseline flux: +0.000
- Is current objective? False

### The `biomass_c` mystery
`OF_ATP_mitoMap` produces `biomass_c` — what happens to it?

**`biomass_c` metabolite:** Biomass
**Reactions touching biomass_c:**
- `Biomass_mitoMap` (stoich=+1.0, flux=-100.892)
- `Biomasst_mitoMap` (stoich=-1.0, flux=+0.000)
- `OF_ATP_mitoMap` (stoich=+1.0, flux=+100.892)


---

## A.4 — Exchange Reactions (Model Boundary)

Model has 70 exchange reactions. Active ones at baseline (|flux| > 0.01):

| Reaction | Metabolite | Flux | Direction |
|---|---|---|---|
| `EX_biomass_e` | biomass_e | +100.892 | export |
| `EX_o2_e` | o2_e | -19.800 | import |
| `EX_co2_e` | co2_e | +16.637 | export |
| `EX_h2o_e` | h2o_e | +15.026 | export |
| `EX_h_e` | h_e | -1.788 | import |
| `EX_glc_D_e` | glc_D_e | -0.900 | import |
| `EX_lac_L_e` | lac_L_e | -0.575 | import |
| `EX_hdca_e` | hdca_e | -0.470 | import |
| `EX_nh4_e` | nh4_e | +0.362 | export |
| `EX_asp_L_e` | asp_L_e | -0.154 | import |
| `EX_acac_e` | acac_e | -0.114 | import |
| `EX_bhb_e` | bhb_e | -0.048 | import |
| `EX_hco3_e` | hco3_e | -0.043 | import |
| `EX_lys_L_e` | lys_L_e | -0.030 | import |
| `EX_ser_L_e` | ser_L_e | -0.017 | import |
| `EX_leu_L_e` | leu_L_e | -0.016 | import |
| `EX_thr_L_e` | thr_L_e | -0.012 | import |
| `EX_val_L_e` | val_L_e | -0.011 | import |
| `EX_ala_L_e` | ala_L_e | -0.010 | import |
| `EX_asn_L_e` | asn_L_e | -0.010 | import |
| `EX_his_L_e` | his_L_e | -0.010 | import |

**Summary:** 18 active out of 70 exchange reactions. Most exchanges default to `lb=-1000, ub=1000` (unlimited), so substrate choice is driven by what pFBA finds optimal.


---

## A.5 — Compartmentalization

**Compartments defined:** {'Cytosol': 'Cytosol', 'Mitochondrion': 'Mitochondrion', 'external': 'External'}

**Metabolites per compartment:**
- `Cytosol` (Cytosol): 200 metabolites
- `Mitochondrion` (Mitochondrion): 175 metabolites
- `external` (External): 70 metabolites

**Transport reactions (span >1 compartment):** 163 of 560


---

## Summary: What MitoMAMMAL Actually Computes

**At baseline (Scenario A, OF_ATP_mitoMap objective):**
1. External substrate uptake via active exchanges: see A.4
2. Matrix oxidation generates NADH (flux through TCA, BCAA, FAO)
3. NADH → CI → ubiquinol → CIII → cyt c → CIV → O2 (electron transport)
4. CI + CIII + CIV pump PMF into a shared `PMF_m` pool
5. CV consumes PMF_m + ADP + Pi → matrix ATP
6. `ATPtmB_mitoMap` exports matrix ATP in exchange for cytoplasmic ADP (consumes PMF)
7. `OF_ATP_mitoMap` hydrolyzes cytoplasmic ATP → ADP + Pi + biomass_c (objective)

**The PMF abstraction is the crucial part:** rather than tracking explicit H+ ion fluxes between compartments, MitoMAMMAL uses a single `PMF_m` metabolite as proton-motive-force currency. This couples proton pumping (CI, CIII, CIV) to consumption (CV, ATPtmB) via mass balance in FBA.

**Implication for transit modeling:** the model's concept of 'mitochondrial viability' comes down to whether enough PMF is being pumped to drive ATP export. Our ΔΨm-proxy objective (maximize CI+CIII+CIV pumping) is aligned with this abstraction.

---

*Generated by `phase_a_dissection.py` on 2026-04-22 23:30:23. Raw solution saved to `results/phase_a_baseline_solution.csv`.*
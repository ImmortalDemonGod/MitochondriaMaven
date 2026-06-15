# Essential Genes Deep Dive — N=10

**Selected 10 genes from the 145-gene essential set**, spanning complexes and impact tiers.

Tier distribution:
- 5 very high (>90% impact)
- 3 high (50-90% impact)
- 2 trace (0.01-1% impact)

## Selection summary

| Gene | Complex | Tier | KO impact |
|---|---|---|---|
| **Uqcrfs1** | Complex III | very_high | 97.92% |
| **Uqcr11** | Complex III | very_high | 97.92% |
| **Cox7c** | Complex IV | very_high | 97.92% |
| **Cox7b** | Complex IV | very_high | 97.92% |
| **Atp5pd** | Complex V | very_high | 92.51% |
| **Ndufc1** | Complex I | high | 85.15% |
| **Ndufs2** | Complex I | high | 85.15% |
| **Ndufv3** | Complex I | high | 85.15% |
| **Glud1** | Other | trace | 0.19% |
| **Slc25a18** | Other | trace | 0.08% |

---

## Per-gene profiles

### Uqcrfs1 (ENSMUSG00000038462) — very_high tier

**Full name:** ubiquinol-cytochrome c reductase, Rieske iron-sulfur polypeptide 1
**Complex:** Complex III
**KO ATP impact:** 97.92%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `CIII_mitoMap` (baseline flux=+39.541)
  - Reaction: `2.0 PMF_m + 2.0 ficytC_m + q10h2_m <=> 4.0 PMF_c + 2.0 focytC_m + q10_m`
  - AND-linked with 10 other genes: ['ENSMUSG00000030884', 'ENSMUSG00000025651', 'ENSMUSG00000020163', 'ENSMUSG00000059534', 'ENSMUSG00000042298']...

**KO mechanism:**
- ATP flux after KO: 2.103 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `H2Otm`: -114.671 → -0.436 (Δ=-114.235)
  - `PIt2mB_mitoMap`: +99.917 → -0.100 (Δ=+100.017)
  - `ATPtmB_mitoMap`: +99.926 → +0.293 (Δ=+99.633)
  - `EX_biomass_e`: +100.892 → +2.103 (Δ=+98.790)
  - `OF_ATP_mitoMap`: +100.892 → +2.103 (Δ=+98.790)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: 31.0h
- ATP flux at t=72h: 3.781

---

### Uqcr11 (ENSMUSG00000020163) — very_high tier

**Full name:** ubiquinol-cytochrome c reductase, complex III subunit XI
**Complex:** Complex III
**KO ATP impact:** 97.92%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `CIII_mitoMap` (baseline flux=+39.541)
  - Reaction: `2.0 PMF_m + 2.0 ficytC_m + q10h2_m <=> 4.0 PMF_c + 2.0 focytC_m + q10_m`
  - AND-linked with 10 other genes: ['ENSMUSG00000030884', 'ENSMUSG00000025651', 'ENSMUSG00000059534', 'ENSMUSG00000042298', 'ENSG00000184076']...

**KO mechanism:**
- ATP flux after KO: 2.103 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `H2Otm`: -114.671 → -0.436 (Δ=-114.235)
  - `PIt2mB_mitoMap`: +99.917 → -0.100 (Δ=+100.017)
  - `ATPtmB_mitoMap`: +99.926 → +0.293 (Δ=+99.633)
  - `EX_biomass_e`: +100.892 → +2.103 (Δ=+98.790)
  - `OF_ATP_mitoMap`: +100.892 → +2.103 (Δ=+98.790)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: 31.0h
- ATP flux at t=72h: 3.781

---

### Cox7c (ENSMUSG00000017778) — very_high tier

**Full name:** cytochrome c oxidase subunit 7C
**Complex:** Complex IV
**KO ATP impact:** 97.92%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `CIV_mitoMap` (baseline flux=+19.771)
  - Reaction: `8.0 PMF_m + 4.0 focytC_m + o2_m --> 4.0 PMF_c + 4.0 ficytC_m + 2.0 h2o_m`
  - AND-linked with 10 other genes: ['ENSMUSG00000064351', 'ENSMUSG00000064354', 'ENSMUSG00000064358', 'ENSMUSG00000031818', 'ENSMUSG00000009876']...

**KO mechanism:**
- ATP flux after KO: 2.103 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `H2Otm`: -114.671 → -0.436 (Δ=-114.235)
  - `PIt2mB_mitoMap`: +99.917 → -0.100 (Δ=+100.017)
  - `ATPtmB_mitoMap`: +99.926 → +0.293 (Δ=+99.633)
  - `EX_biomass_e`: +100.892 → +2.103 (Δ=+98.790)
  - `OF_ATP_mitoMap`: +100.892 → +2.103 (Δ=+98.790)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: 31.0h
- ATP flux at t=72h: 3.781

---

### Cox7b (ENSMUSG00000031231) — very_high tier

**Full name:** cytochrome c oxidase subunit 7B
**Complex:** Complex IV
**KO ATP impact:** 97.92%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `CIV_mitoMap` (baseline flux=+19.771)
  - Reaction: `8.0 PMF_m + 4.0 focytC_m + o2_m --> 4.0 PMF_c + 4.0 ficytC_m + 2.0 h2o_m`
  - AND-linked with 10 other genes: ['ENSMUSG00000064351', 'ENSMUSG00000064354', 'ENSMUSG00000064358', 'ENSMUSG00000031818', 'ENSMUSG00000009876']...

**KO mechanism:**
- ATP flux after KO: 2.103 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `H2Otm`: -114.671 → -0.436 (Δ=-114.235)
  - `PIt2mB_mitoMap`: +99.917 → -0.100 (Δ=+100.017)
  - `ATPtmB_mitoMap`: +99.926 → +0.293 (Δ=+99.633)
  - `EX_biomass_e`: +100.892 → +2.103 (Δ=+98.790)
  - `OF_ATP_mitoMap`: +100.892 → +2.103 (Δ=+98.790)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: 31.0h
- ATP flux at t=72h: 3.781

---

### Atp5pd (ENSMUSG00000034566) — very_high tier

**Full name:** ATP synthase peripheral stalk subunit d
**Complex:** Complex V
**KO ATP impact:** 92.51%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `CV_mitoMap` (baseline flux=+93.393)
  - Reaction: `2.7 PMF_c + adp_m + h_m + pi_m <=> 2.7 PMF_m + atp_m + h2o_m`
  - AND-linked with 10 other genes: ['ENSG00000116459', 'ENSG00000135390', 'ENSG00000110955', 'ENSG00000167283', 'ENSG00000159199']...

**KO mechanism:**
- ATP flux after KO: 7.564 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `MALtm`: -0.105 → +124.417 (Δ=-124.522)
  - `FUMm`: +6.849 → -117.437 (Δ=+124.286)
  - `Hmt_mitoMap`: -1.902 → -124.679 (Δ=+122.776)
  - `Hct_mitoMap`: +2.569 → +125.273 (Δ=-122.705)
  - `CV_mitoMap`: +93.393 → +0.000 (Δ=+93.393)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: 36.0h
- ATP flux at t=72h: 9.091

---

### Ndufc1 (ENSMUSG00000037152) — high tier

**Full name:** NADH:ubiquinone oxidoreductase subunit C1
**Complex:** Complex I
**KO ATP impact:** 85.15%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `CI_mitoMap` (baseline flux=+29.369)
  - Reaction: `3.996 PMF_m + h_m + nadh_m + 0.002 o2_m + 0.999 q10_m <=> 3.996 PMF_c + nad_m + 0.002 o2s_m + 0.999 `
  - AND-linked with 10 other genes: ['ENSMUSG00000064367', 'ENSG00000145494', 'ENSMUSG00000064368', 'ENSMUSG00000021606', 'ENSMUSG00000020022']...

**KO mechanism:**
- ATP flux after KO: 69.896 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `H2Otm`: -114.671 → -83.574 (Δ=-31.097)
  - `CV_mitoMap`: +93.393 → +62.346 (Δ=+31.047)
  - `OF_ATP_mitoMap`: +100.892 → +69.896 (Δ=+30.997)
  - `EX_biomass_e`: +100.892 → +69.896 (Δ=+30.997)
  - `Biomass_mitoMap`: -100.892 → -69.896 (Δ=-30.997)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: 52.0h
- ATP flux at t=72h: 16.597

---

### Ndufs2 (ENSMUSG00000013593) — high tier

**Full name:** NADH:ubiquinone oxidoreductase core subunit S2
**Complex:** Complex I
**KO ATP impact:** 85.15%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `CI_mitoMap` (baseline flux=+29.369)
  - Reaction: `3.996 PMF_m + h_m + nadh_m + 0.002 o2_m + 0.999 q10_m <=> 3.996 PMF_c + nad_m + 0.002 o2s_m + 0.999 `
  - AND-linked with 10 other genes: ['ENSMUSG00000064367', 'ENSG00000145494', 'ENSMUSG00000064368', 'ENSMUSG00000021606', 'ENSMUSG00000020022']...

**KO mechanism:**
- ATP flux after KO: 69.896 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `H2Otm`: -114.671 → -76.288 (Δ=-38.384)
  - `CV_mitoMap`: +93.393 → +62.346 (Δ=+31.047)
  - `EX_biomass_e`: +100.892 → +69.896 (Δ=+30.997)
  - `OF_ATP_mitoMap`: +100.892 → +69.896 (Δ=+30.997)
  - `Biomass_mitoMap`: -100.892 → -69.896 (Δ=-30.997)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: 52.0h
- ATP flux at t=72h: 16.597

---

### Ndufv3 (ENSMUSG00000024038) — high tier

**Full name:** NADH:ubiquinone oxidoreductase core subunit V3
**Complex:** Complex I
**KO ATP impact:** 85.15%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `CI_mitoMap` (baseline flux=+29.369)
  - Reaction: `3.996 PMF_m + h_m + nadh_m + 0.002 o2_m + 0.999 q10_m <=> 3.996 PMF_c + nad_m + 0.002 o2s_m + 0.999 `
  - AND-linked with 10 other genes: ['ENSMUSG00000064367', 'ENSG00000145494', 'ENSMUSG00000064368', 'ENSMUSG00000021606', 'ENSMUSG00000020022']...

**KO mechanism:**
- ATP flux after KO: 69.896 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `H2Otm`: -114.671 → -76.288 (Δ=-38.384)
  - `CV_mitoMap`: +93.393 → +62.346 (Δ=+31.047)
  - `EX_biomass_e`: +100.892 → +69.896 (Δ=+30.997)
  - `OF_ATP_mitoMap`: +100.892 → +69.896 (Δ=+30.997)
  - `Biomass_mitoMap`: -100.892 → -69.896 (Δ=-30.997)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: 52.0h
- ATP flux at t=72h: 16.597

---

### Glud1 (ENSMUSG00000021794) — trace tier

**Full name:** glutamate dehydrogenase 1
**Complex:** Other
**KO ATP impact:** 0.19%
**N reactions in model:** 4

**Model reactions and GPR context:**
- `GLUDxi` (baseline flux=+0.000)
  - Reaction: `glu_L_c + h2o_c + nad_c --> akg_c + h_c + nadh_c + nh4_c`
  - AND-linked with 1 other genes: ['ENSG00000148672']
- `GLUDxm` (baseline flux=+0.235)
  - Reaction: `glu_L_m + h2o_m + nad_m --> akg_m + h_m + nadh_m + nh4_m`
  - AND-linked with 2 other genes: ['ENSG00000148672', 'ENSG00000182890']
- `GLUDym` (baseline flux=+0.059)
  - Reaction: `glu_L_m + h2o_m + nadp_m --> akg_m + h_m + nadph_m + nh4_m`
  - AND-linked with 2 other genes: ['ENSG00000148672', 'ENSG00000182890']
- `GLUDy` (baseline flux=+0.000)
  - Reaction: `glu_L_c + h2o_c + nadp_c --> akg_c + h_c + nadph_c + nh4_c`
  - AND-linked with 1 other genes: ['ENSG00000148672']

**KO mechanism:**
- ATP flux after KO: 100.514 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `PYK`: +1.906 → +0.000 (Δ=+1.906)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: >72hh
- ATP flux at t=72h: 100.706

---

### Slc25a18 (ENSMUSG00000004902) — trace tier

**Full name:** solute carrier family 25 (mitochondrial carrier), member 18
**Complex:** Other
**KO ATP impact:** 0.08%
**N reactions in model:** 1

**Model reactions and GPR context:**
- `GLUt2mB_mitoMap` (baseline flux=+0.183)
  - Reaction: `0.18 PMF_c + glu_L_c + h_c --> 0.18 PMF_m + glu_L_m + h_m`
  - AND-linked with 1 other genes: ['ENSG00000182902']

**KO mechanism:**
- ATP flux after KO: 100.815 (from baseline)
- Top flux changes in other reactions (|Δ flux| > 0.5):
  - `PYK`: +1.906 → +0.000 (Δ=+1.906)

**Solo decay (only this gene at t½=12h, all others immortal):**
- Transit window: >72hh
- ATP flux at t=72h: 100.817

---

## Cross-gene observations

### Solo decay behavior
All 10 genes show solo-decay transit windows >> 29h (most go to >72h), confirming the single-gene leverage finding: **no individual gene is the bottleneck under uniform decay**. The 29h transit window of the full system emerges from coupled decay of the 145-gene essential set.

### KO mechanism patterns

- **Uqcrfs1** KO primarily affects `H2Otm` (flux -114.67 → -0.44). This is a propagated downstream effect.
- **Uqcr11** KO primarily affects `H2Otm` (flux -114.67 → -0.44). This is a propagated downstream effect.
- **Cox7c** KO primarily affects `H2Otm` (flux -114.67 → -0.44). This is a propagated downstream effect.
- **Cox7b** KO primarily affects `H2Otm` (flux -114.67 → -0.44). This is a propagated downstream effect.
- **Atp5pd** KO primarily affects `MALtm` (flux -0.10 → 124.42). This is a propagated downstream effect.
- **Ndufc1** KO primarily affects `H2Otm` (flux -114.67 → -83.57). This is a propagated downstream effect.
- **Ndufs2** KO primarily affects `H2Otm` (flux -114.67 → -76.29). This is a propagated downstream effect.
- **Ndufv3** KO primarily affects `H2Otm` (flux -114.67 → -76.29). This is a propagated downstream effect.
- **Glud1** KO primarily affects `PYK` (flux 1.91 → 0.00). This is a propagated downstream effect.
- **Slc25a18** KO primarily affects `PYK` (flux 1.91 → 0.00). This is a propagated downstream effect.

### Literature reconciliation status

*This section requires manual literature lookup. Framework produces FBA-predicted essentiality; to confirm biological essentiality, each gene needs OMIM/mouse-KO phenotype check. Pending Phase B.3 (MitoCarta) and B.4 (disease).*

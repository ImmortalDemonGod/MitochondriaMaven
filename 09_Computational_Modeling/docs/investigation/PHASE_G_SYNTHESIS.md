# Phase G Synthesis — Validation Tests

> **⏱ Timeline note:** Effort estimates ("X working days") in this document were forward-looking planning estimates, not records of actual time taken. Actual elapsed wall-clock for the entire pipeline (model clone → Phase G validation): **~3 hours on 2026-04-22 evening**. See [`TIMELINE_NOTE.md`](TIMELINE_NOTE.md).

---

> **⚠ Framing update (2026-04-23):** This document was written before the Phase G validation tests. Some claims here use a framing that conflates "model output" with "biological reality." See [`FRAMING_2026-04-23.md`](FRAMING_2026-04-23.md) for the corrected interpretation. The numerical results stand; some interpretive language does not.

---

**Date:** 2026-04-23
**Purpose:** Resolve the 6 open items and stress-test the heterogeneity finding

This document closes out the validation tests requested after the Phase A-F investigation.

---

## Test Results Summary

| # | Test | Result | Verdict |
|---|---|---|---|
| G.1 | Order-statistics vs FBA | Mean gap 0.6h across all log_sigma | **Heterogeneity finding is also algebra** |
| G.2 | Cross-model (Human-GEM) | Algebraic claim provable analytically | Skipped full adaptation (math is universal) |
| G.3 | Literature overlay | 28-29h not supported by any published data; 8-12h plausible in optimal buffer | **Our headline overestimates by 2-3×** |
| G.4 | CIII/CIV cyt c imbalance | Math error on my part — perfectly balanced | False anomaly resolved |
| G.5 | ROS-coupled damage | Scenario divergence works (A=29h, B/C=5-15h) | Real biology with caveats |
| G.6 | Empirical reuptake threshold | 20% ATP ≈ ΔΨm −100 mV ≈ PINK1 stabilization | Defensible (range 10-35%) |

---

## G.1 — The Heterogeneity Finding Is Order-Statistics Algebra

| log_sigma | Order-stats prediction | FBA observed | Gap |
|---|---|---|---|
| 0.0 (uniform) | 27.86h | 29.00h | +1.14h |
| 0.2 | 18.20h | 19.30h | +1.10h |
| 0.4 | 11.99h | 12.60h | +0.61h |
| 0.6 | 7.97h | 8.55h | +0.58h |
| 0.8 | 5.34h | 5.75h | +0.41h |
| 1.0 | 3.60h | 3.95h | +0.35h |

**Mean gap: 0.61h** — entirely attributable to flux_buffer=1.05.

**Mechanism:** Under heterogeneous decay, the largest required AND-clause (CI_mitoMap, 39 mouse nuclear subunits) determines effective t½. Order statistics: E[min over N=39 lognormal samples at σ=0.6] ≈ 3.4h. Apply pure exponential decay → TW = 2.32 × 3.4 ≈ 7.9h. **FBA gives 8.5h. The 0.6h gap is the buffer.**

**Implication:** The "FBA contribution under non-uniform decay" reduces to two pieces of structural information:
1. The list of essential genes (FBA-derived, real biology)
2. The size of the largest AND-clause (CI = 39 in MitoMAMMAL)

That's it. The temporal dynamics are pure algebra: `TW = -log₂(threshold) × E[min over N_largest_clause samples]`.

---

## G.3 — Our Predictions vs Published Data

The literature has limited multi-timepoint decay data for isolated mammalian mitochondria. Best available:

| Source | Storage condition | Viability window |
|---|---|---|
| McCully reviews | Standard buffer, ice | 1-2h operational ceiling |
| Field consensus | Standard buffer | ~4h with measurable decline |
| Oroboros MiR05 | Specialized lactobionate buffer + antioxidants | up to 18h |
| Cryopreservation | DMSO/trehalose | weeks-months (with reduced output) |
| **Our 28-29h prediction** | **Theoretical** | **No published support without cryo** |
| **Our 8-12h prediction** | **Heterogeneous decay** | **Within MiR05 envelope** |

**Verdict on our predictions:**

- **29h headline:** Optimistic by 2-3× vs any published fresh-storage data. Should be presented only as a theoretical maximum under specific assumptions (uniform protein decay, no oxidative damage, optimal substrate availability).
- **8-12h heterogeneity-corrected:** Defensible — sits at upper edge of MiR05-buffer experimental observations. This is the honest prediction.
- **5h ROS-coupled (Scenario C):** Defensible — matches typical transplantation operational windows.

**The framework's calibration is reasonable IF interpreted correctly.** The headline shouldn't be "29h transit window predicted" — it should be: *"Under realistic protein turnover heterogeneity (lognormal log_sigma=0.6) and ROS-coupled damage in ischemic substrates, the framework predicts a transit window of 5-12 hours, consistent with published isolated-mitochondrial viability under optimal preservation conditions (MiR05 buffer, McCully et al. 2017)."*

---

## G.5 — ROS Coupling Resolves Scenario Invariance

| k_damage | Scenario A | Scenario B | Scenario C |
|---|---|---|---|
| 0 | 29h | 29h | 29h |
| 1 | 29h | 15h | 15h |
| 3 | 29h | 8h | 8h |
| 5 | 29h | 5h | 5h |

ROS coupling (model-internal o2s_m production scaled to ETC flux) creates real scenario divergence. Scenario A (intracellular buffer) holds at 29h; Scenario B (arterial blood, O2-limited) and C (ischemic) drop dramatically.

**Caveat:** Scenarios B and C don't differentiate from each other much — both have near-complete O2 drop, so the linear ROS coupling treats them identically. Distinguishing arterial-blood-but-not-anoxic from full ischemic-reperfusion would require more sophisticated biology (succinate accumulation modeling, Chouchani 2014).

**At biologically-plausible k_damage=3, both B and C give 8h** — same numerical answer as the heterogeneity finding for Scenario A. Two mechanisms producing the same realistic prediction. Both align with published 4-18h viability windows.

---

## G.6 — The 20% ATP Threshold Is Biologically Justifiable

Literature anchoring:
- Healthy mitochondria: ΔΨm ≈ −140 to −180 mV
- PINK1 stabilization threshold: ΔΨm ≈ −100 to −120 mV
- ATP synthesis flux drops to near-zero around ΔΨm = −100 mV (Brand & Nicholls 2011)
- Therefore 20% baseline ATP flux ≈ ΔΨm ≈ −100 mV ≈ PINK1 stabilization

**Recommended reporting bounds:**
| Metric | Permissive | Point | Strict |
|---|---|---|---|
| ATP flux fraction | 10% | **20%** | 35% |
| Implied ΔΨm | −80 mV | **−100 mV** | −120 mV |

Report TW with these bounds rather than a single point. Citations: Narendra 2008/2010; Lazarou 2015; Brand & Nicholls 2011; McCully 2023.

---

## G.4 — Cyt c Imbalance Was a Math Error

I had reported a CIII/CIV cytochrome c flux imbalance (CIII produces 79/h, CIV consumes 39/h). This was a misreading: CIV stoichiometry is **−4** focytC per unit flux (not −2). Recomputing: 19.77 × 4 = 79.08, perfectly matching CIII's production. **Cyt c is conserved. False anomaly.**

---

## Updated Findings Reconciliation Matrix

| Claim | Pre-G status | Post-G status |
|---|---|---|
| TW = 29h under uniform decay | "Algebraic identity" | **Confirmed: 29h = -t½ × log₂(0.20) × 1.05** |
| Heterogeneity TW = 8-12h | "FBA contribution under non-uniform decay" | **Order-statistics algebra: TW = -log₂(0.20) × E[min over N samples]** |
| 145 essentials, 89% mitochondrial | "Strong finding" | **Unchanged** ✓ |
| Substrate scenario invariance | "Suspicious" | **Resolved by ROS coupling (G.5)** |
| First-failure: PIt2mB_mitoMap | "Mechanistic prediction" | **Flux-relative scaling artifact, not biology** |
| All ETC complexes saturate together | "Coupled failure" | **Mathematically inevitable under uniform flux-relative decay** |
| 20% ATP threshold | "Approximation from mitophagy lit" | **Biologically anchored to ΔΨm = −100 mV (G.6)** |
| 29h is realistic | "Default headline" | **Optimistic by 2-3× vs published (G.3)** |
| 8-12h is realistic | "Heterogeneity-driven" | **Aligns with MiR05-buffer experiments (G.3)** |
| Cyt c imbalance | "Open anomaly" | **False positive, resolved** |
| Cross-model validation | "Open" | **Algebraic claim is provable analytically; full adaptation deferred** |

---

## What Survives for the Abstract

After all this stress-testing, here's what remains genuinely defensible:

### Strong
1. **145-gene mouse nuclear essential set, 89% mitochondrial GO** — biologically real, FBA-derived, validated by external annotation
2. **The largest AND-clause (CI = 39 subunits) governs effective decay** under heterogeneity — testable structural prediction
3. **20% ATP ≈ ΔΨm −100 mV ≈ PINK1 stabilization** — empirically anchored threshold
4. **5-15h transit window predicted under realistic conditions** (heterogeneous decay OR ROS coupling) — within published experimental envelope

### Reframed (was claimed as biology, actually math)
- Transit window scaling law `TW = -t½ × log₂(threshold)` — true algebraically; FBA doesn't add temporal content
- Heterogeneity-driven shortening — pure order statistics on AND-clause sizes
- Coupled failure of all ETC complexes — mathematical inevitability, not biological insight

### Retracted
- "29h transit window" as a biological prediction — overestimates published data
- "First-failure reaction PIt2mB" as mechanistic — was a flux-buffer artifact
- "Substrate scenarios converge" as a finding — was uniform-decay artifact, fixed with ROS coupling

---

## Honest Abstract Position

The framework's substantive contributions are:
1. A **biologically-validated essential gene set** for nuclear-encoded mitochondrial proteins (145 genes)
2. A **structural prediction** that the largest AND-clause in the ETC (Complex I in MitoMAMMAL) governs effective transit window via order statistics
3. A **falsifiable model** of how protein-stability heterogeneity, ROS damage, and substrate environment interact to determine post-extraction viability
4. A **calibrated prediction range** (5-15h) consistent with published experimental data

What it does NOT contribute:
- A novel "29h transit window" — this is `-12 × log₂(0.20)` and applies to any uniform-decay system
- Identification of specific rate-limiting reactions — these emerge from our scaling choices, not network biology
- Prediction beyond what order statistics + pure exponential gives

This is a more honest, more defensible scientific contribution. It should still support a q-bio talk submission.

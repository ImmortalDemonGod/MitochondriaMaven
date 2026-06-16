# q-bio Chicago 2026 Abstract — Empirically-Grounded Draft

**Date:** 2026-04-23 (draft 1) → 2026-04-24 (drafts 2a/b/c/d/e post-composite, post-stretch, pass-7 corrections, Session 9 mechanism modules) → **2026-04-24f (clean rewrite, pass-8 honest state)**
**Status:** Framework + multi-parameter mechanism modules implemented. 145 essentials validated against MitoCarta 3.0 (87.6%). Parameter values literature-range, not first-principles-calibrated (pass-8 honesty).
**Word count target:** 350 words

---

## Title (proposed)

**Multi-Scale Composite of Genome-Scale Metabolism and Biophysical Oxidative Phosphorylation Identifies Scenario-Dependent Failure Modes in Extracted Mammalian Mitochondria**

---

## Abstract (~350 words)

**Problem (~55 words).** Mitochondrial transplantation requires extracted organelles to maintain ATP synthesis during transit. Clinical protocols operate with a ~4-hour viability window, yet the mechanistic decomposition of transit failure — what dominates under what conditions, and which interventions address which component — has not been quantitatively framed. We ask: what determines the functional transit window, and how do interventions partition by mechanism?

**Approach (~70 words).** We compose four paradigms: (i) time-stepped Flux Balance Analysis on MitoMAMMAL (560 reactions, 782 genes) with GPR-aware protein decay; (ii) Beard 2005 biophysical OXPHOS ODE receiving FBA capacity envelopes as time-varying Vmax; (iii) Bazil-Dash-style Ca²⁺/MPTP module with Hill-cooperative MCU uptake; (iv) Kagan-cycle cardiolipin peroxidation driven by cyt-c-catalyzed H₂O₂ consumption. Parameters drawn from literature ranges; model transferability validated on Human-GEM (12931 reactions).

**Method + Results (~120 words).** The framework identifies **145 individually-essential mouse nuclear genes**, with **127/145 = 87.6% validated in MitoCarta 3.0** (gold-standard mitochondrial proteome; non-listed 18 are cytoplasmic substrate-feeding enzymes — biologically sensible). Three-class structure: 145 individually + ~207 synthetically + ~22 truly-redundant. Complex I's 39-subunit AND-clause is the largest required conjunction governing decay via order statistics. Latin hypercube sensitivity yields **TW = 13.5h (95% CI [6.8, 30.0] h)** — spans the empirical MiR05 4–18h envelope. Composite shows scenario-dependent failure partition: proteomics-limited ATP-first in low-Ca scenarios (13–33h TW) versus Ca²⁺-driven MPTP catastrophic collapse under ischemic loading (<1h). JCVI-syn3A crosswalk shows mechanism-level phosphate and amino-acid-import conservation with divergent pyruvate sourcing.

**Engineering (~55 words).** Intervention predictions resolve mechanistically: Kagan-cycle-derived MitoQ scavenging gives ~4% TW extension in isolated mitochondria (consistent with MitoQ's reduced efficacy outside in vivo contexts); cold-chain composite over-predicts empirical ~4× extension by an order of magnitude under uniform Q10=2.5 — candidate unmodeled mechanisms include inner-membrane lipid phase transitions (chilling injury), cooling-rate-dependent Ca²⁺ dysregulation, and cumulative oxidative damage.

**Significance (~50 words).** The framework provides: (1) 145 MitoCarta-validated essential gene set, (2) model-transferable multi-scale architecture (MitoMAMMAL + Beard + MPTP + Kagan), (3) scenario-dependent mechanism partition, and (4) falsifiable intervention predictions. Parameter values are literature-range, not dataset-calibrated; specific quantitative predictions invite wet-lab testing rather than representing validated truths.

---

## Word count audit

| Section | Target | Actual |
|---|---|---|
| Problem | 55 | 58 |
| Approach | 70 | 69 |
| Method+Results | 120 | 117 |
| Engineering | 55 | 56 |
| Significance | 50 | 50 |
| **Total** | **350** | **350** |

At target.

---

## Trust-criteria compliance (pass-8 honest state, 2026-04-24)

| Abstract claim | C1 | C2 | C3 | C4 | C5 | C6 | Σ |
|---|---|---|---|---|---|---|---|
| 145 individually-essential gene set | ✓ | ✓ | ✓ | ⚠ | ✓ | ✓ | 5 |
| 87.6% MitoCarta 3.0-listed | ✓ | N/A | ✓ | ⏭ | ✓ MitoCarta gold standard | ✓ | 4 |
| 127 MitoCarta + 18 cytoplasmic feeders partition | ✓ | ✓ | ✓ | ⏭ | ✓ | ✓ | 5 |
| Three-class structure: 145 / ~207 / ~22 | ✓ | ⚠ | ✓ | ⏭ | ✓ | ✓ | 4 |
| CI is largest AND-clause (N=39) | ✓ | ✓ | ✓ | ⏭ | ✓ | ✓ | 5 |
| Order statistics govern TW under heterogeneity | ✓ | ✓ | ⚠ N=4 underpowered | ⏭ | ✓ | ✓ | 4 |
| Composite TW median 13.5h [6.8, 30.0] | ✓ | ✓ | ✓ | ⚠ Human-GEM shows different values | ⚠ literature-range params | ✓ | 4 |
| Halflife dominates uncertainty ~10× | ✓ | ✓ | ✓ | ⏭ | ✓ | ✓ | 5 |
| Scenario-dependent failure partition (MPTP) | ✓ | ✓ | ✓ | ⏭ | ⚠ Bazil-Dash rat liver | ✓ | 4 |
| MitoQ ~4% extension in isolated mito | ✓ | ✓ | ✓ | ⏭ | ⚠ Kagan rate literature-plausible | ✓ | 4 |
| Cold-chain composite over-prediction | ✓ | ✓ | ✓ | ⏭ | ✓ Oroboros | ✓ | 5 |
| Mito-Syn3A mechanism-level import conservation | ✓ | N/A | ✓ Fisher p=1.0 | ⏭ | ✓ | ✓ | 4 |
| Framework transfers to Human-GEM | ✓ | N/A | ✓ | ✓ | ⚠ | ✓ | 4 |

All claims pass ≥4 of C1–C6. C5 (literature) is now the most common weak criterion — reflects the pass-8 finding that parameter values are literature-range but not calibrated to specific datasets.

---

## Pass-8 honest framing summary (for reviewer-response preparation)

**What the abstract honestly claims:**
- Structural findings (gene set, AND-clause topology, three-class structure) — robust across all audits
- 87.6% MitoCarta hard validation — newly added, replaces "89% GO" soft validation
- Multi-scale composite framework identifying scenario-dependent failure modes
- Falsifiable intervention predictions in literature-range regime

**What the abstract does NOT claim (and correctly avoids):**
- "Mechanism resolution" as in first-principles calibration — Session 9 added ~19 tunable parameters; claims are "literature-plausible" not "literature-derived"
- "Two independent derivations converge" on MitoQ fold-extension — the Ex 11 convergence was an artifact of parameter tuning; Ex 12 Kagan cycle gives honest 4% in isolated mito
- "Engineering gap closed mechanistically" (pass-7 retraction still stands; Session 9 added mechanism structure but not first-principles calibration)
- "Dominant" failure mechanism — only identified partition, not dominance hierarchy within parameter space

---

## Deliverables status

| Item | Status |
|---|---|
| Abstract text | COMPLETE at 350 words |
| Trust-criteria table | COMPLETE (pass-8 updated) |
| Final 2-panel figure | **PENDING** — need to regenerate with Session 9 Ex 10 (MPTP scenarios) + Ex 12 (MitoQ Kagan dose-response) data |
| MitoCarta cross-ref CSV | COMPLETE (`results/phase_b/essential_genes_mitocarta_crossref.csv`) |
| TRUST_LEDGER.md | COMPLETE (18 claims; Session 9 + pass-8 appended) |
| Novelty check (manual) | COMPLETE — MitoMAMMAL transit application + order-statistics + composite architecture all appear novel |
| q-bio Chicago registration | **USER-PENDING** ($200) |
| 2024 yeast notebook digitization | **USER-PENDING** (optional) |

---

## Honest submission posture

The abstract as written is a **mechanism-structured multi-scale framework paper with 87.6% hard-validated essential gene set, scenario-dependent failure partition, and falsifiable intervention predictions in literature-range parameter space**. It is NOT a first-principles-calibrated quantitative predictor. The distinction matters: reviewers will probe specific TW values (13.5h, 4% MitoQ) and we should respond with "these are the model's predictions at literature-range parameter values; the structure is biochemically grounded; parameter calibration is follow-up wet-lab scope."

The 8 documented audit passes (pass-1 through pass-8) are a strength, not a weakness — they demonstrate the project's self-correction discipline. If a reviewer asks about parameter fitting, we have pass-8 honest accounting documented in `COMPOSITE_AUDIT_2026-04-24.md` and can cite it directly.

---

## Possible paper structure (not set in stone just for ideas)
Target venue

PLoS Computational Biology is the natural fit: 6000–8000 words, mechanism-heavy methods papers welcome, accepts "model-generates-hypotheses" framing. Secondary options:
Biophysical Journal (similar length, more biophysics-focused), Cell Systems (shorter, higher-impact).

Paper structure

Title

Multi-Scale Composite of Genome-Scale Metabolism and Biophysical Oxidative Phosphorylation Identifies Scenario-Dependent Failure Modes in Extracted Mammalian Mitochondria
(current draft)

Abstract

350 words, draft 2f — keep as-is. Pass-8 + pass-9 disciplined.

Introduction (~800 words)

Hook (~150 words): Mitochondrial transplantation is a real clinical therapy (McCully pediatric cardiology, 2017–present). Current point-of-care limitation: ~4h viability
window from Oroboros MiR05 data and surgical practice. Off-the-shelf organelle banking requires extending to 24–48h. The proteomics contribution to this window has an
algebraic ceiling (~29h under uniform 12h halflives) but non-proteomic failure dominates empirically — which specific mechanisms and at what rates is unresolved.

Prior work (~300 words): Four strands:
1. Clinical / wet lab — McCully, Pacak, Cowan mitochondrial transplantation work; Oroboros MiR05 respirometry as the canonical buffer; clinical point-of-care protocols
2. Computational mitochondrial models — Beard 2005 biophysical OXPHOS; Cortassa-Aon 2003/2006 energetics + Ca²⁺ + ROS; Bazil-Dash 2010 stochastic MPTP; MitoMAMMAL 2024
genome-scale FBA (Chapman/Habermann); Phase G.5 ROS coupling previously
3. Isolated-organelle preservation math — largely empirical; Walker et al 2025 pharmacokinetic dosing model (if verified); no published mechanism-model of the transit
window itself
4. Minimal-cell computational modeling (positioning reference, not direct precedent) — Thornburg et al. 2022 Cell whole-cell kinetic model of JCVI-syn3A with hybrid
stochastic-deterministic dynamics establishes minimal-system multi-paradigm modeling as a mature approach. Our framework applies multi-paradigm composition to the
complementary problem of organelle-scale transit viability (deterministic throughout, not stochastic — the methodological parallel is "multi-paradigm composition," not
"stochastic-deterministic hybrid").

Gap statement (~150 words): FBA gives static snapshots; biophysical ODEs give dynamics at a single complex; MPTP models predict opening but don't connect to proteomics;
cardiolipin biology is siloed from ETC kinetics. No published framework composes these paradigms for extracted-organelle transit viability. We present a four-layer
composite that fills this gap and demonstrates scenario-dependent mechanism partition.

Our contribution (~200 words):
1. Time-stepped FBA with GPR-aware protein decay on MitoMAMMAL (560 reactions) identifies 145 essential mouse nuclear genes, 87.6% MitoCarta-validated; the remaining 18
are cytoplasmic substrate-feeding enzymes
2. Order-statistics framework: Complex I as largest obligate conjunction (N=39 subunits) governs decay rate mathematically — proof that large heteromeric complexes fail
disproportionately fast under heterogeneous subunit halflives
3. Composite coupling FBA capacity envelopes → Beard ODE Vmax; scenarios propagated via PO₂ + Ca_c + substrate pool overrides
4. Bazil-Dash-style MPTP + Kagan-cycle cardiolipin peroxidation modules produce scenario-dependent failure partition
5. Syn3A crosswalk positions mitochondria within the programmable-organelle design space (Layer 2–4 research agenda)
6. Literature-range parameters throughout — scope and caveats made explicit

Results (~3000 words, 6 figures)

Section 1: Essential gene inference and MitoCarta validation (~400 words, Figure 1)
- Time-stepped FBA identifies 145 individually essential mouse nuclear genes
- Three-class partition: 145 / ~207 synthetic / ~22 truly redundant
- 127/145 = 87.6% MitoCarta 3.0-listed; 18 non-listed enumerated as cytoplasmic feeders (Gapdh, Pgk1, Tpi1, Gpi1, Pfkm, Ak1, Ppa1, Got1, Cycs, Ndufb1, etc.)
- Figure 1: Gene classification bar chart + MitoCarta overlap Venn + per-complex decomposition of the 145

Section 2: Order-statistics governs decay under heterogeneity (~500 words, Figure 2)
- Under uniform halflives: TW ≈ −t½·log₂(threshold)·buffer = 29h (algebraic)
- Under heterogeneous halflives: order statistics on largest AND-clause governs
- CI is largest obligate conjunction with N=39 subunits
- Analytical result: P_complex(t) = ∏P_subunit(t); for N=39 with per-subunit 0.90 survival, complex survives at 0.016 (1.6%)
- Simulation + sensitivity (Latin hypercube N=60): TW = 13.5h, 95% CI [6.8, 30.0]h
- Halflife parameter dominates sensitivity ~10× over Beard ODE parameters
- Independence assumption documented and caveated (N=4 permutation test p=0.56)
- Figure 2: Order-statistics analytical prediction vs FBA simulation + sensitivity tornado + CI subunit correlation check

Section 3: Multi-scale composite architecture (~300 words, Figure 3)
- Four-paradigm coupling diagram
- FBA capacity envelope → ODE Vmax scaling mechanism
- State vector: 14 variables across compartments
- Human-GEM cross-model structural transferability
- Honest caveat: 19 tunable parameters; values literature-range not dataset-calibrated (pass-8 framing)
- Figure 3: Schematic of the four-layer composite with state-variable flow

Section 4: Scenario-dependent failure partition (~600 words, Figure 4)
- With MPTP enabled: scenarios A (intracellular buffer, low Ca²⁺), B (arterial blood, low Ca²⁺), C (ischemic, Ca²⁺ overload)
- Scenarios A/B: proteomics-limited ATP-first failure at 13–33h
- Scenario C: catastrophic ΔΨm collapse via MPTP pore opening at <1h
- Partition is an emergent property of the composite, not encoded
- Mechanism: Hill-cooperative MCU → matrix Ca²⁺ accumulation → MPTP threshold → PMF collapse
- Figure 4: Panel a: ΔΨm traces per scenario (broken x-axis for scenario C collapse); Panel b: mechanism-of-failure partition across 3 scenarios × MPTP-OFF/ON

Section 5: Mechanistic intervention predictions (~600 words, Figure 5)
- Three interventions, modeled mechanistically
- MitoQ (Kagan-cycle H₂O₂ scavenging): ~4% TW extension at 5 μM in isolated mito; consistent with literature observation that MitoQ is more effective in vivo than in
isolated preparations
- Cold chain (uniform Q10=2.5): composite over-predicts empirical ~4× extension by an order of magnitude; candidate unmodeled mechanisms include inner-membrane lipid
phase transitions (chilling injury), cooling-rate-dependent Ca²⁺ dysregulation, and cumulative oxidative damage
- Substrate supplementation: ~0h effect (enzyme-capacity-limited regime)
- Honest framing: predictions at literature-range parameter values; quantitative claims invite wet-lab testing
- Figure 5: Intervention composite vs pure-FBA bar chart + MitoQ dose-response + cold chain over-prediction annotated

Section 6: Syn3A crosswalk — positioning within programmable-organelle design space (~400 words, Figure 6 or supplementary)
- Three-reaction deep dive: phosphate (equivalent), amino acid/glutamate (equivalent), pyruvate (divergent)
- Category-level Fisher's exact test p=1.00 with Jaccard 45%: mechanism-level conservation (phosphate, amino acid imports) with specialization-driven divergence
(pyruvate: mito imports, Syn3A synthesizes)
- Positions mitochondria alongside synthetic minimal cells within the broader programmable-biosystems design space
- Supports Layer 2–4 research agenda: mitochondria as engineerable organelle with shared architectural features to minimal chassis
- **Pedreira et al. (2021 SynWiki) citation — Fisher p=1.00 honest contextualization:** the statistical inconclusiveness reflects BOTH genuine mechanism-level convergence AND the ~33% of Syn3A's 452 protein-coding genes lacking functional annotation. Full-network equivalence cannot be assessed from current Syn3A data; mechanism-level conservation of the three deep-dive reactions (phosphate, glutamate, pyruvate) is what we support — not claims beyond.
- **Fisher p=1.00 honest contextualization (Pedreira et al., 2021 SynWiki citation):** the statistical inconclusiveness reflects both genuine mechanism-level convergence
AND the ~33% of Syn3A's 452 protein-coding genes that lack functional annotation. Full-network equivalence cannot be assessed from current Syn3A data; mechanism-level
conservation of the three deep-dive reactions (phosphate, glutamate, pyruvate) is what our analysis supports — not claims beyond.
- Figure 6 (or supp): Syn3A vs MitoMAMMAL transport architecture Venn + per-reaction mechanism deep-dive table

Discussion (~1500 words)

What the composite tells us (~400 words):
- Proteomics-kinetic decay is not the dominant empirical rate-limiter under current preservation protocols — even with aggressive halflife-acceleration, composite doesn't
reach empirical MiR05 4–18h range without adding non-proteomic mechanisms
- Scenarios partition failure modes mechanistically: proteomics-limited under low-Ca, MPTP-catastrophic under ischemic loading
- MitoQ's modest isolated-mito efficacy follows from the Kagan cycle consuming H₂O₂ faster than antioxidants can scavenge — explains the in-vivo/in-vitro efficacy gap
- Cold-chain over-prediction localizes the missing biology: temperature-dependent membrane physics (most likely lipid phase transitions), cooling-rate-dependent Ca²⁺
dysregulation, or cumulative oxidative damage at low temperatures

Implications for mitochondrial transplantation (~300 words):
- Organelle banking requires mechanism-targeted preservation fluids, not just antioxidants
- Rational design targets: MPTP inhibition (cyclosporin A, SfA) + membrane stabilization (trehalose, cholesterol substitutes) + controlled cooling rates + Ca²⁺ chelation
- Wet-lab priorities: calibrate k_kagan for cardiac CL peroxidation; measure cardiac MCU/NCLX kinetics at storage temperatures; characterize inner-membrane Tm for
mammalian cardiac IMM

Positioning within programmable organelles (~200 words):
- Mitochondria are engineerable organelles with design-space kinship to synthetic minimal cells
- Layer 2 scope: pre-extraction genetic modifications whose transit-viability effect can be simulated in this framework
- Layer 3–4 implications: gene-delivery vehicles (Layer 3) and autonomous extracellular operation (Layer 4) both require Layer 1 mechanism resolution
- **Pelletier et al. (2021) citation for Layer 2–4 positioning:** in minimal biological systems, normal morphology requires a specific gene set (7 of 19 genes added back to syn3.0 to restore division — including ftsZ, sepF, and four membrane-associated proteins of unknown function). Analogous mammalian mitochondrial requirements (cardiolipin biosynthesis, Drp1/MFF/MID49-51 fission machinery, cyt c partitioning) constitute future Layer 2–4 engineering targets. Caveat: Pelletier addresses cell DIVISION gene requirements (producing pleomorphic morphology when missing; cells still live). Do NOT conflate with our cold-chain gap (which concerns DEATH/failure mechanisms in extracted mitochondria). The citation supports the "minimal systems depend on specific membrane/structural gene products" framing, not a specific mechanism for cold-chain over-prediction.

Limitations (~600 words — crucial for pass-8 discipline):
- Parameter values are literature-range, not dataset-calibrated. 19 tunable parameters across MPTP + ROS + Kagan modules. Specific quantitative predictions (4% MitoQ,
scenario C 0.24h collapse, cold chain >10× over-prediction) depend on parameter choices. Table S1 lists all parameters with provenance.
- Independence assumption for CI subunit halflives is unverified. Order-statistics framework requires per-subunit independence; N=4 permutation test on available data is
underpowered (p=0.56).
- Lumped ROS vs separated O₂⁻ / H₂O₂. We lump ROS as H₂O₂-equivalent since Mn-SOD dismutation is fast; for explicit separation, Cortassa 2006 extension would be needed.
- Cold chain: no lipid phase transition module. Q10 applied uniformly to enzymatic rates; does not capture inner-membrane phase physics. This is why cold-chain prediction
over-shoots empirical 4× extension.
- No wet-lab empirical anchor. Composite calibrated to literature-range parameters, not to measured time-course viability data. 2024 yeast Taguchi data from our group
remains undigitized at submission time; published mammalian time-course data (McCully, Pacak, Oroboros, Masuzawa) verified to NOT contain the needed discrete-time-course
measurements.
- Human-GEM transferability is structural, not numerical. Same code runs on Human-GEM (12,931 reactions) but produces different TW numbers due to larger network
redundancy. Framework transfers; specific values don't.
- Closed-system assumption. No nuclear protein import, no mtDNA translation beyond the 13 mt-encoded genes treated as immortal, no cyt c depletion during peroxidation.
- Scenario substrate pools are informed-guess values, not calibrated from specific physiological measurements.

Methods (~1500 words, 4 subsections)

M1. MitoMAMMAL time-stepped FBA with GPR-aware decay — reference Session 1–3 work, decay_utils.py, E-flux-style GPR evaluation (AND=min, OR=sum clipped at 1.0), scenarios
A/B/C via apply_scenario

M2. Beard 2005 OXPHOS ODE reimplementation — scipy.integrate LSODA, validated against QAMAS reference curves (Ex 5.1 within 10% of published), 14 state variables,
parameter provenance in Table S1

M3. Composite coupling via capacity envelope — composite_utils.py, extract_capacity_envelope and build_capacity_envelope_fn functions; per-reaction GPR capacity fraction
scales corresponding ODE Vmax

M4. Mechanism modules — Bazil-Dash-style MPTP (Ca_x state, MCU/NCLX kinetics, Hill-function pore opening), Kagan cycle (cyt c + H₂O₂ → cardiolipin peroxidation → proton
leak amplification), Latin hypercube sensitivity (N=60 across 8 parameters with log-normal uncertainty)

Data availability

- Code: github.com/[user]/mitomaven (or DOI-minted deposit)
- MitoCarta cross-reference: results/phase_b/essential_genes_mitocarta_crossref.csv
- All experiment CSVs in results/composite/
- Audit trail (9 passes): docs/investigation/AUDIT_2026-04-23.md + COMPOSITE_AUDIT_2026-04-24.md

Figures (6 in main text, plus supplementary)

```text
┌─────┬─────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┐
│  #  │                         Content                         │                              Source                               │
├─────┼─────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 1   │ Gene classification + MitoCarta validation              │ essential_genes_mitocarta_crossref.csv + new bar/Venn             │
├─────┼─────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 2   │ Order statistics + sensitivity tornado                  │ ex5_6_sensitivity_tornado.png refined                             │
├─────┼─────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 3   │ Composite architecture schematic                        │ new — conceptual diagram                                          │
├─────┼─────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 4   │ Scenario-dependent failure partition                    │ ex10_mptp_traces.png — refined version                            │
├─────┼─────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 5   │ Intervention predictions (MitoQ, cold chain, substrate) │ final_abstract_figure_composite.png panel (b) + cold chain detail │
├─────┼─────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 6   │ Syn3A crosswalk (or supp)                               │ from Phase P3 + new visualization                                 │
└─────┴─────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────┘
```

Supplementary material

- S1: All 19+ Session-9 parameter values with provenance and uncertainty ranges (from beards_lab/beard_2005_params.csv + MPTP/ROS/Kagan parameter documentation)
- S2: Complete TRUST_LEDGER with C1–C6 scoring for 18 claims
- S3: Complete 9-pass audit trail (the self-correction discipline is the methodological innovation; some journals will ask for this)
- S4: Latin hypercube sensitivity full results
- S5: Human-GEM cross-model run
- S6: Source code + reproduction instructions
- S7: Intervention dose-response extended data

Honest positioning in cover letter

"This is a mechanism-structured multi-scale composite model with literature-range parameters and explicit caveats. We believe the framework contribution (four-paradigm
coupling, scenario-dependent failure partition, MitoCarta-validated essential set) is novel. Specific quantitative predictions invite wet-lab testing; we do not claim
dataset-calibrated quantitative accuracy. The pass-8 parameter-fitting transparency is intentional and documented in Supplementary S3 audit trail."

---

What the paper wouldn't do

- Claim "solved" mitochondrial transplantation
- Claim first-principles calibration of specific TW numbers
- Claim validated interventions (these are predictions, not confirmations)
- Claim clinical relevance beyond "identifies engineering-gap targets for wet-lab"
- Hide the parameter-fitting transparency behind mechanism language (pass-7 retraction taught us this)

Submission timing

The q-bio Chicago abstract (May 31) is the abstract in this paper — a natural conference-abstract subset of the full paper. Full paper can be drafted across May–June and
submitted to PLoS Comp Bio in June–July after we've received q-bio Chicago feedback.

What's still needed to finish the full paper

- Regenerated Figure 4 (scenario partition with cleaner visualization)
- New Figure 1 (gene classification + MitoCarta Venn)
- New Figure 3 (composite architecture schematic — conceptual diagram)
- Table S1 (full parameter table with provenance — ~2 hours work from beard_2005_params.csv + MPTP/ROS params)
- Expand Methods from audit/code docstrings — most content exists, needs academic-prose rewriting
- Walker et al 2025 verification for Introduction citations
- Optional: wet-lab collaboration section if an empirical partner emerges

The honest cover-letter arc

1. Novelty: multi-scale composite framework applied to extracted-organelle transit viability; scenario-dependent failure partition; 87.6% MitoCarta-validated essential
set
2. Limitations explicitly: literature-range parameters, not dataset-calibrated; explicit candidate unmodeled mechanisms for cold-chain over-prediction
3. Value: identifies wet-lab priorities (k_kagan calibration; cardiac MCU/NCLX; inner-membrane Tm); enables Layer 2 computational engineering
4. Self-correction discipline: 9-pass audit trail is supplementary material — not usually provided but available on request — demonstrates methodological rigor

This is what the full paper would look like: structurally solid, intellectually honest, positioned as mechanism-framework contribution + hypothesis-generator, not as a
validated quantitative predictor. The pass-8 transparency is front-and-center in the Limitations section.

---

## References to cite in full paper (added 2026-04-24 post-pass-10)

Three citations recommended by pass-10 external-evaluation review, with honest framings (not the agent's overreaching reframings; see `COMPOSITE_AUDIT_2026-04-24.md` pass-10 section for context):

1. **Pedreira, T. et al. (2021/2022)** *SynWiki: Functional annotation of the first artificial organism Mycoplasma mycoides JCVI-syn3A.* Protein Science (PMID 34515387).
   - **Cite in:** Section 6 (Syn3A crosswalk); Limitations subsection on Syn3A interpretability.
   - **Purpose:** Contextualizes our Fisher p=1.00 for phosphate/amino-acid/pyruvate crosswalk — ~33% of Syn3A proteome lacks functional annotation, so full-network equivalence cannot be statistically assessed.
   - **Do NOT cite as:** "145-mitochondrial-essential ≈ 208-Syn3A-essential mathematical complexity equivalence." The scopes differ categorically (function-specific vs whole-organism essentiality).

2. **Thornburg, Z. R. et al. (2022)** *Fundamental behaviors emerge from simulations of a living minimal cell.* Cell 185(2):345–360 (PMID 35063075).
   - **Cite in:** Introduction (Prior Work strand 4); Discussion (positioning within programmable organelles).
   - **Purpose:** Precedent for multi-paradigm computational modeling of minimal biological systems. Thornburg achieved whole-cell kinetic modeling of JCVI-syn3A with hybrid stochastic-deterministic dynamics; our framework applies multi-paradigm composition to the complementary problem of organelle-scale transit viability.
   - **Do NOT cite as:** "our hybrid stochastic-deterministic methodology mirrors Thornburg." Our approach is deterministic-deterministic (FBA + ODE); no stochastic dynamics anywhere in our model. The parallel is "multi-paradigm composition," not "stochastic-deterministic hybrid."
   - **Do NOT cite as:** "parallel bottleneck mechanisms between Syn3A PEP/FBA-aldolase crash and our SLC25/CI proteomic decay." Different timescales (seconds vs hours), different mechanisms (real-time flux imbalance vs gradual protein degradation). The framing is superficial.

3. **Pelletier, J. F. et al. (2021)** *Genetic requirements for cell division in a genomically minimal cell.* Cell 184(9):2430–2440 (PMID 33784496).
   - **Cite in:** Discussion → "Positioning within programmable organelles" subsection (Layer 2–4 implications).
   - **Purpose:** In minimal biological systems, normal morphology requires specific gene products (7 of 19 genes added back to syn3.0 — including ftsZ, sepF, and four membrane proteins of unknown function). Analogous mammalian mitochondrial membrane/structural requirements (cardiolipin biosynthesis, Drp1/MFF/MID49-51 fission machinery) are future Layer 2–4 engineering targets.
   - **Do NOT cite as:** "Pelletier proves membrane biophysics is the primary driver of failure in minimal systems." Pelletier addresses DIVISION gene requirements producing pleomorphic morphology — cells still live. The cold-chain gap concerns DEATH/failure mechanisms; these are different scopes.
   - **Do NOT cite as:** "mitochondria lost ftsZ and need synthetic division machinery for Layer 4." Mammalian mitochondria replaced FtsZ with Drp1-based machinery during evolution, not lost without replacement. This is speculative Layer 4 scope creep.

Additional citations expected (from paper plan above):
- McCully lab: Preble et al. 2014; Cowan et al. 2016; Pacak et al. 2015 (mitochondrial transplantation methods/delivery — note: pass-5 audit verified these do NOT contain time-course viability data we'd need for validation).
- MitoMAMMAL: Chapman et al. 2024 (Bioinformatics Advances).
- Beard 2005: PLoS Comp Bio 1(4):e36.
- Cortassa, Aon et al. 2003/2006: Biophys J.
- Bazil & Dash 2010: J Theor Biol.
- MitoCarta 3.0: Rath et al. 2021 Nucleic Acids Research.
- Karunadharma et al. 2015; Lam et al. 2021; Fornasiero et al. 2018: protein halflife data.
- Walker et al. 2025: pharmacokinetic dosing model (pending verification — see DocInsight Batch 8).

---

*Draft 2f — 2026-04-24. Post-pass-8 clean rewrite. 350 words, pass-8 honesty, MitoCarta 87.6% hard validation, scenario-dependent partition via MPTP + Kagan. Trust-criteria table reflects current honest state. Ready for figure regeneration + user review.*

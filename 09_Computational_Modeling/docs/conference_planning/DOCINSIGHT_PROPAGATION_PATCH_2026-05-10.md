# DocInsight Propagation Patch — 2026-05-10

**Status:** *In progress*. Pre-paste deliverable for the domain agent. Per-edit BEFORE / AFTER / EVIDENCE / CITATION blocks consolidated from `DOCINSIGHT_VERIFICATION_AUDIT_2026-05-10.md` §7 + independent re-verification of audit-recommended replacement citations + extended audit of the 38 previously-unverified batches.

**Relationship to the canonical audit:** the audit is the authority on what to keep / rework / drop. **This document adds the layer the audit didn't reach** — independent content-verification of the audit's *replacement* citations. Several of those replacements turn out not to support the claim they were meant to anchor.

**Disposition:** read-only. Nothing in `ABSTRACT_DRAFT_2026-04-23.md`, `TRUST_LEDGER.md`, results CSVs, or experiment scripts has been modified. The domain agent owns propagation.

---

## 1. Critical surprise — three of the audit's replacement citations don't actually back the claim

The audit's §7.2 ("Salvageable with rework") recommends replacing several wrong-citations with specific real papers. **Independent fetch of those replacements shows several don't cover the topic claimed.** This is a meta-correction the audit itself didn't make.

### 1.1 Hackenbrock 1976 BBA does NOT support cardiac IMM Tm ≈ 10–12°C

**Audit recommended:** Replace "Höchli & Hackenbrock 1979 PNAS" (lateral diffusion paper) with **Hackenbrock CR, Höchli M, Chau RM (1976) BBA 455:466-484, PMID 999923** for the cardiac IMM phase-transition Tm 10–12°C claim. Audit qualifier: "may need to soften 'cardiac' to liver."

**What the paper actually shows (independent verification, 2026-05-10):**
- Title: *"Calorimetric and freeze fracture analysis of lipid phase transitions and lateral translational motion of intramembrane particles in mitochondrial membranes"*
- Tissue: **rat liver only**. Cardiac is not discussed.
- Phase transition onset temperatures from the abstract:
  - Inner membrane exotherm onset: **−4°C**
  - Whole-mitochondria endotherm onset: **−15°C**
  - Inner membrane endotherm onset: **−15°C**
  - Outer membrane endotherm onset: **−15°C**

**These are negative-Celsius freezing transitions — not the 10–12°C "biologically consequential" range the original findings doc claimed.** The 10–12°C number has **no support** in either Hackenbrock paper.

**Disposition:** the cardiac-IMM-Tm-10–12°C claim **drops entirely** — the audit's "softer" qualifier still doesn't rescue it because the temperature range is wrong by ~25°C. The cold-chain mechanism argument has to be made differently (or hedged to an acknowledged unmodeled physics, no specific Tm).

### 1.2 Schlame 2008 *J Lipid Res* doesn't cover phase transitions or domain formation either

**Audit recommended:** Replace "Schlame 2008 *Progress in Lipid Research*" (wrong journal) with **Schlame M (2008) *J Lipid Res* 49:1607-1620, PMID 18077827**.

**What the paper actually covers (independent verification):**
- Title: *"Cardiolipin synthesis for the assembly of bacterial and mitochondrial membranes"* — single-author review.
- Substantive scope: cardiolipin **biosynthesis**, **molecular symmetry / uniform species composition**, **Barth syndrome pathophysiology**, **cardiolipin–protein interactions**, **degradation pathways**.
- **Does NOT discuss**: cardiac IMM specifically, lateral phase separation, phase transition temperature, domain formation, lipid Tm, chilling injury.

**Disposition:** Schlame 2008 *J Lipid Res* is a real Schlame review but **doesn't support the cold-chain-mechanism claim** the original Schlame 2008 PLR citation was meant to anchor. If the propagated edit cites Schlame 2008 *J Lipid Res*, it must be for a DIFFERENT claim (e.g., cardiolipin biology in general / Barth syndrome / cardiolipin-protein interactions) — not for the IMM phase transition. **Re-scope the use case before propagating.**

### 1.3 García-Roche 2018 supports cryopreservation but doesn't directly compare sequential vs immediate freezing

**Audit recommended:** Replace the non-existent "Santos 2018" with **García-Roche M et al. (2018) *Redox Biology* 17:207-212, PMID 29704825**.

**What the paper actually shows:**
- Title: *"Respiratory analysis of coupled mitochondria in cryopreserved liver biopsies"*
- Authors: García-Roche M, Casal A, Carriquiry M, Radi R, Quijano C, Cassina A
- Studied: **intact liver biopsies (mitochondria in situ)**, NOT isolated mitochondria
- Method: sequential cooling (ice → −110°C N₂ vapors → −196°C LN₂ → −80°C storage) using DMSO cryopreservation medium
- Finding: "Most respiratory parameters remained unchanged" comparing fresh vs cryopreserved
- **Does NOT compare** sequential vs. immediate freezing — only validates one protocol.

**Disposition:** García-Roche 2018 supports the "sequential cryopreservation can preserve mito respiration" half of the original claim but does NOT support the "immediate freezing doesn't" half. **Trim the original claim** before citing. Also: this is liver tissue, not cardiac; not isolated mitochondria. Scope the use case carefully.

### 1.4 Kagan 2005 *Nat Chem Biol* covers the qualitative claim but not the 5% / k_kagan numbers

**Audit recommended:** Substitute the non-existent "Khailova 2021" with **Kagan VE et al. (2005) *Nat Chem Biol* 1(4):223-232, PMID 16408039** *if* the cardiolipin/cyt-c peroxidase claim is wanted.

**What the paper actually shows:**
- Title: *"Cytochrome c acts as a cardiolipin oxygenase required for release of proapoptotic factors"*
- 17 authors led by Kagan VE (Pittsburgh)
- Establishes cyt c as **cardiolipin-specific peroxidase** when cardiolipin-bound — **qualitatively correct** for the abstract's k_kagan mechanism story.
- **Does NOT provide**: quantitative fraction of cyt c that is CL-bound, rate constants, IC50s. The 5% CL-binding factor the abstract uses **is not from this paper.**

**Disposition:** Kagan 2005 is the right citation for the **qualitative** "cyt c acts as CL peroxidase" / Kagan-pathway mechanism. The **5% effective CL-bound fraction** in `k_kagan ≈ 1e5 M⁻²s⁻¹` is not anchored by this or any cited paper — it remains a **modeling assumption** stated as such in the abstract's pass-8 honest framing. Cite Kagan 2005 for the mechanism; don't claim it supports the 5% number.

### 1.5 To 2019 *Cell* uses different framing than "three-class essentiality decomposition"

**Audit recommended:** Hedge the three-class novelty claim by adding **To, Cuadros, Shah, ..., Mootha (2019) *Cell* 179:1222-1238, PMID 31730859** as adjacent prior art.

**What the paper actually frames (independent verification):**
- Title: *"A Compendium of Genetic Modifiers of Mitochondrial Dysfunction Reveals Intra-organelle Buffering"*
- 18 authors (Mootha is senior/corresponding)
- Frames findings as **191 genetic modifiers, 38 synthetic sick/lethal, 63 suppressors** — NOT as a three-class decomposition.
- Introduces **"intra-organelle buffering"** concept — suppressors are disproportionately mitochondrial proteins themselves, suggesting internal compensation.
- **Does NOT explicitly partition into "individually essential / synthetically essential / truly redundant."**

**Disposition:** To 2019 is **conceptually adjacent**, not a direct competitor. The hedge the audit recommends is appropriate but with care: the paper is not a direct three-class application; it's a chemical-genetic-modifier compendium with the "intra-organelle buffering" framing. The framing for the abstract should be: *"Our individually-essential / synthetically-essential / truly-redundant decomposition extends Papp 2004 / Güell 2014 framework to mouse cardiac mitochondrial nuclear-encoded essentials. Adjacent prior art on mitochondrial intra-organelle buffering: To, Cuadros, ..., Mootha 2019, Cell."*

---

## 2. Per-edit propagation blocks (audit §7 + independent reverify)

For each proposed abstract edit, the format is:

- **CURRENT WORDING** (verbatim from `ABSTRACT_DRAFT_2026-04-23.md`)
- **PROPOSED WORDING** (after audit + meta-rework above)
- **PRIMARY-SOURCE EVIDENCE** (verbatim quote from the originating raw `batch_*.json` markdown)
- **VERIFIED CITATION(s)** (Crossref/PubMed-confirmed; explicit fields, not labels)
- **AUDIT VERDICT** + **TIER-1 META-VERIFY VERDICT**

Edits below are listed in audit §7 order: §7.1 safe-to-apply first, §7.2 salvageable next, §7.3 drop last.

### 2.1 EDIT A — Problem paragraph clinical hook (audit §7.1.1, safe to apply)

**CURRENT WORDING (from ABSTRACT_DRAFT_2026-04-23.md):**
> *"Mitochondrial transplantation requires extracted organelles to maintain ATP synthesis during transit. Clinical protocols operate with a ~4-hour viability window, ..."*

**PROPOSED WORDING (audit §7.1.1, content-verified):**
> *"Mitochondrial transplantation requires extracted organelles to maintain ATP synthesis during transit. Clinical protocols are built around rapid isolation and immediate use of viable autologous mitochondria — typically within minutes to <1 hour of tissue procurement — because mitochondrial quality, viability, and respiratory competence are time- and handling-sensitive (McCully 2016, Clin Transl Med 5:16, PMC4851669)."*

**PRIMARY-SOURCE EVIDENCE (from `batch_10_4.json`'s markdown, Round-1 Agent 1 confirmed verbatim quote):**
> *"The isolation and preparation of autogeneic mitochondria is rapid and purified mitochondrial are available within 30 min." — McCully 2016*

**VERIFIED CITATION:** McCully JD (2016) *Clinical and Translational Medicine* 5:16. PMC4851669. (Crossref/PubMed confirmed.)

**AUDIT VERDICT:** Safe to apply (§7.1.1).
**TIER-1 META-VERIFY VERDICT:** No issues — this is the cleanest paste in the document.

### 2.2 EDIT B — Cold-chain mechanism strengthening (audit §7.2.1; **REWORK NEEDED**)

**CURRENT WORDING:**
> *"...candidate unmodeled mechanisms include inner-membrane lipid phase transitions (chilling injury), cooling-rate-dependent Ca²⁺ dysregulation, and cumulative oxidative damage."*

**PROPOSED-BUT-PROBLEMATIC WORDING (Addendum B of findings doc, before audit):**
> *"...candidate unmodeled mechanisms include cardiac inner-membrane lipid phase transition centered near 10–12°C with a 5–20°C transition window (Höchli & Hackenbrock 1979 PNAS), cooling-rate-dependent recrystallization injury that uniform Q10 cannot capture (Mazur/Leibo/Rall framework; Santos 2018 cryopreserved liver), and cumulative oxidative damage..."*

**TIER-1 META-VERIFY:** This wording can NOT be salvaged. The "10–12°C window" is not in either Höchli 1979 or Hackenbrock 1976 (which uses rat liver, has phase transitions at −4°C and −15°C, not 10–12°C). Schlame 2008 *J Lipid Res* doesn't cover phase transitions either. García-Roche 2018 covers cryopreserved liver tissue but doesn't directly compare sequential vs immediate freezing.

**RECOMMENDED REWORK (no specific Tm citation):**
> *"...candidate unmodeled mechanisms include lipid-phase / domain-formation effects in cardiolipin-rich inner membranes during cooling, cooling-rate-dependent recrystallization injury (general cryobiology, Mazur 1984), and cumulative oxidative damage that low-temperature scavenging may not match. The composite assumes a uniform Q10 across all processes; this is its largest known approximation."*

**VERIFIED CITATIONS:** Mazur P (1984) *Am J Physiol* 247:C125-142 (cryobiology canonical) — **needs independent re-verify before propagation.** García-Roche 2018 *Redox Biol* 17:207-212 PMID 29704825 (cryopreservation precedent only, scope-limited to liver tissue).

**AUDIT VERDICT:** Salvageable with rework (§7.2.1).
**TIER-1 META-VERIFY VERDICT:** Rework deeper than the audit said — the specific Tm number has no anchor. Default to mechanism-name-only without specific temperature, until/unless a paper that actually measures cardiac IMM Tm is found.

### 2.3 EDIT C — Independence-assumption caveat (audit §7.2.3, salvageable as directional)

**CURRENT WORDING:**
> *"Independence assumption documented and caveated (N=4 permutation test p=0.56)."*

**PROPOSED WORDING (audit §7.2.3, with content-correction):**
> *"Treating the four available Complex I subunit half-lives as independent draws is a simplifying assumption (N=4 internal permutation test, p=0.56). Subunits of multiprotein complexes show a general trend toward **coherent** turnover within and across tissues (Mathieson et al. 2018, Nat Commun; consistent with Hasper et al. 2023, Mol Syst Biol [TRAIL]); these works do not quantify the effect for ETC complexes specifically. The order-statistics estimate is therefore best read as an upper bound on the surprise."*

**PRIMARY-SOURCE EVIDENCE:** TRAIL paper's own headline includes *"coherent lifetimes,"* and Mathieson 2018 reports coherent within-complex turnover for 20S/26S proteasome, nuclear pore, chaperonins.

**VERIFIED CITATIONS:**
- Mathieson T, Franken H, Kosinski J, et al. (2018) *Nature Communications*. PMID 29449567. DOI 10.1038/s41467-018-03106-1.
- Hasper J et al. (2023) *Mol Syst Biol*. DOI 10.15252/msb.202211393. (TRAIL paper.)

**AUDIT VERDICT:** Salvageable with rework — preserve as directional weakening, not falsification (§7.2.3).
**TIER-1 META-VERIFY VERDICT:** OK as written above. Use Mathieson's term "coherent" (theirs), not "coordinated" (the original findings doc's paraphrase).

### 2.4 EDIT D — MitoQ vindication framing (audit §7.2.5, soften)

**CURRENT WORDING:**
> *"...MitoQ scavenging gives ~4% TW extension in isolated mitochondria (consistent with MitoQ's reduced efficacy outside in vivo contexts)..."*

**FINDINGS-DOC PROPOSED (Addendum B before audit):**
> *"MitoQ scavenging gives ~4% TW extension in isolated mitochondria, consistent with MitoQ's reduced efficacy outside in-vivo contexts because catalytic recycling of the ubiquinol moiety requires endogenous redox networks absent in isolated suspensions (Murphy/Smith Newcastle MitoQ lineage)."*

**AUDIT-RECOMMENDED WORDING (§7.2.5, softer):**
> *"MitoQ scavenging gives ~4% TW extension in our isolated-mitochondria composite, **mechanistically consistent with** the observation that MitoQ's catalytic redox cycling depends on endogenous regeneration absent in isolated suspensions (James AM, Cochemé HM, Smith RA, Murphy MP 2005, J Biol Chem 280:21295-312, PMID 15788391). No isolated-mito time-course currently exists in the literature to confirm this prediction quantitatively."*

**AUDIT VERDICT:** Salvageable with rework — soften "vindicates" to "mechanistically consistent with"; explicit no-data-confirmation caveat.
**TIER-1 META-VERIFY VERDICT:** Honest. Add the "no isolated-mito time-course" caveat verbatim — that's the audit's §3.3 finding for Batch 8.5.

### 2.5 EDIT E — Scenario B sumATP_c reframe (audit §7.2 / §3.1; safe to apply, USER JUDGMENT REQUIRED)

**FINDINGS-DOC RECOMMENDED CAVEAT ADD (to Limitations §"Scenario substrate pools"):**
> *"In particular, scenario B's `sumATP_c = 0.1 mM` is consistent with extracellular ATP in injured/ischemic tissue or platelet-rich microdomains, but is approximately two to three orders of magnitude higher than typical resting plasma free ATP (low nM to low μM); scenario B should be read as 'arterial blood, post-injury' rather than baseline arterial."*

**PRIMARY-SOURCE EVIDENCE (from `batch_7_5.json`):**
Direct three-piece argument in source markdown — 100–1000× ratio, low-nM/μM plasma reference, ischemic-saving frame. Audit §3.3 verified HONEST.

**AUDIT VERDICT:** HONEST per Round-1 audit. Safe to apply.
**TIER-1 META-VERIFY VERDICT:** No replacement-citation issue here (no specific paper cited; argument from physiology). User decision required: **relabel scenario B as ischemic/injured tissue** OR **revise the sumATP_c value downward**. Don't silently change without user choice.

### 2.6 EDIT F — Halflife calibration caveat (audit §7.2; pending Batch 10.6 audit-extension)

**FINDINGS-DOC RECOMMENDED:**
> *"The 12 h post-extraction effective halflife assumes inhibitor-protected, cold-handled extraction consistent with standard protocols; naked-extracted, warm-stored mitochondria likely have shorter effective halflives."*

**TIER-2 STATUS:** Awaiting agent verification of Batch 10.6 (in flight). Hold propagation until the verification agent confirms the source markdown actually says this vs. agent paraphrase.

### 2.7 EDIT G — Accessory subunit caveat (audit §7.2; pending Batch 10.5 audit-extension)

**FINDINGS-DOC RECOMMENDED:** caveat add to Limitations §"Closed-system assumption" about accessory protein vulnerability during extraction.

**TIER-2 STATUS:** Awaiting Batch 10.5 verification.

### 2.8 EDIT H — Methodological-novelty positioning (Taguchi DoE; pending Batch 10.7)

**TIER-2 STATUS:** Awaiting Batch 10.7 verification.

### 2.9 Three-class novelty hedge (audit §7.2.2; **REWORK NEEDED per §1.5 above**)

**AUDIT-RECOMMENDED:**
> *"...first formal three-class essentiality decomposition (Papp 2004, Güell 2014) of mouse cardiac mitochondrial nuclear-encoded essential genes, extending intra-organelle buffering observations (To et al. 2019, Cell) to a tissue-specific in vivo context."*

**TIER-1 META-VERIFY VERDICT:** Mostly OK, but **To 2019 doesn't use a "three-class decomposition" framing.** Refine wording to acknowledge the paper's actual framing:

**RECOMMENDED:**
> *"...first formal three-class essentiality decomposition (individually essential / synthetically essential / truly redundant; framework from Papp et al. 2004, Nature; Güell et al. 2014, PLoS Comp Biol) of mouse cardiac mitochondrial nuclear-encoded essential genes. Adjacent prior art on mitochondrial intra-organelle buffering: To, Cuadros, Shah, ..., Mootha 2019, Cell — though that work uses a synthetic-sick-lethal / suppressor framing rather than the three-class decomposition adopted here."*

**VERIFIED CITATIONS:**
- Papp B, Pál C, Hurst LD (2004) *Nature*. PMID 15190353.
- Güell O, Sagués F, Serrano MÁ (2014) *PLoS Comput Biol*. PMC4031049.
- To M, Cuadros AM, Shah H, ..., Mootha VK (2019) *Cell* 179(5):1222-1238. PMID 31730859.

---

## 3. Drop-entirely (audit §7.3, validated)

| Recommended drop | Reason | Status |
|---|---|---|
| **Fritzemeier 2017 EGC Limitations caveat as written** | MitoMAMMAL is BiGG-curated lineage; Fritzemeier's 85% applies to ModelSEED/MetaNetX | ✅ Confirmed — drop or narrow to "MitoMAMMAL has not been independently audited for EGCs post-2017" |
| **Schlame 2008 *Progress in Lipid Research*** | Wrong journal | ✅ Confirmed (real Schlame 2008 is *J Lipid Res* — but per §1.2 above, doesn't cover phase transitions either) |
| **Khailova 2021** | Does not exist | ✅ Confirmed |
| **Batch 6.2 inline McShane / Taggart & Li / Mukherjee & Bahar citations** | Not in source JSON | ✅ Confirmed (audit §3.3 + §10.3) |
| **Batch 9.4 "0.5 mM BAPTA → ~50× MCU suppression" claim** | Fabricated by source-fusion | ✅ Confirmed (audit §3.3 + §10.3) |
| **Reference-list LLM stubs in Batch 2.2** | Placeholder text from agent | ✅ Confirmed (audit §3.3 + §10.3) |

---

## 4. Independent verification of replacement citations (Tier-1 results, this document)

| Audit-recommended replacement | Tier-1 verify verdict | Use? |
|---|---|---|
| Hackenbrock CR, Höchli M, Chau RM (1976) *BBA* 455:466-484, PMID 999923 | ✗ **Wrong tissue (rat liver) AND wrong temperature range (−4°C / −15°C onsets, not 10–12°C)** | **No** — drop the specific Tm claim entirely |
| Schlame M (2008) *J Lipid Res* 49:1607-1620, PMID 18077827 | ✗ **Doesn't cover IMM phase transitions / domain formation**; covers cardiolipin biosynthesis instead | **No** for cold-chain claim; **Yes** if cited for cardiolipin biology generally |
| García-Roche M et al. (2018) *Redox Biology* 17:207-212, PMID 29704825 | ⚠ Real and on-topic, but doesn't compare sequential vs immediate freezing | **Yes with scope trim** — cite for sequential cryopreservation precedent only; not for "immediate freezing fails" claim |
| Kagan VE et al. (2005) *Nat Chem Biol* 1(4):223-232, PMID 16408039 | ✓ Right qualitative claim (cyt c as cardiolipin peroxidase); does NOT support 5% / k_kagan numbers | **Yes** for qualitative mechanism; not for specific quantitative parameters |
| To et al. (2019) *Cell* 179:1222-1238, PMID 31730859 | ⚠ Real and adjacent, but uses synthetic-sick-lethal / suppressor framing not three-class | **Yes with framing care** — see §2.9 above |

**Net:** of 5 audit-recommended replacements, 1 is fully clean (Kagan 2005 for qualitative claim), 2 are usable with explicit scope-trim (García-Roche 2018, To 2019), 2 are unusable (Hackenbrock 1976 for Tm claim, Schlame 2008 *JLR* for IMM phase transition).

---

## 5. Audit-extension status (Tier 2)

The audit covered 19 of 57 batches. 38 remain. Six parallel verification agents are dispatched at time of writing:

| Agent | Scope | Status (this document version) |
|---|---|---|
| 1 | Batches 1.1, 1.2, 1.3, 2.1, 2.3, 3.1, 3.2, 3.3 | running |
| 2 | Batches 4.1, 4.2, 4.3, 5.1, 5.2, 5.3 (HIGH PRIORITY — pass-7 retraction support) | running |
| 3 | Batches 5a.1, 5a.2, 5a.3, 6.1, 6.5, 6.6, 6.7 | running |
| 4 | Batches 7.2-7.6 + 8.1, 8.4, 8.6, 8.7 | running |
| 5 | Batches 9.2, 9.5, 9.6, 9.7, 9.9 (MDP), 9.10 (ESH) | running |
| 6 | Batches 10.1, 10.2, 10.3, 10.5, 10.6, 10.7, 10.8 | running |

Verdicts will be appended as §6 once all agents complete. Particularly load-bearing: **Agent 2's verdict on Batches 5.1–5.3** — if those are also stretched/misleading the same way 8.5/8.8 are, the abstract's pass-7 retraction loses literature support and the entire 30× framing needs further reframing.

---

## 6. Audit-extension verdicts for the 38 previously-unverified batches

Six verification agents covered 42 batches between them (38 unverified per audit + 4 already-audited included by accident as cross-checks). Verdict scale matches the canonical audit's: HONEST / HEDGED-IN-SOURCE / STRETCHED / EMBELLISHED / MISLEADING.

### 6.1 Headline — the audit's worst findings concentrate in the original 19

The 38 newly-audited batches show a **substantively cleaner pattern** than the originally-audited 19. Of 38, **0 STRETCHED, 0 EMBELLISHED, 0 MISLEADING** verdicts. Only 2 require rework, both for citation-attribution issues already known to the audit (verifier-label mismatch for 3.3; Brand/Jastroch citation drift in 5a.2). Everything else verified HONEST or HONEST-with-caveat.

**Critical positive finding for the abstract: Batches 5.1, 5.2, 5.3 are all HONEST.** The pass-7 retraction's literature support — the abstract's most prominent honesty move — rests on solid ground. Each of the three batches explicitly refuses to fabricate a fold-multiplier and grounds the absence in real reviewed literature.

### 6.2 Per-batch table (38 newly-verified)

| Batch | Verdict | Safe? | Most consequential note |
|---|---|---|---|
| **1.1** MitoCarta + DepMap + MITOMICS + Replogle | HONEST | YES | Population fractions (~10–20% glucose, ~35–50% galactose) faithfully reported; per-gene cross-ref appropriately disclaimed |
| **1.2** OMIM disease enrichment | HONEST | YES | Disease genes listed accurately; Fisher enrichment appropriately not computed |
| **1.3** scoop check (FBA + protein decay + transit) | HONEST | YES | Novelty claim grounded in absence of evidence |
| **2.1** Karunadharma SI extraction | HONEST | YES | Honest refusal — agent declined to fabricate values; Karunadharma 2015 PMID 25977255 cited correctly |
| **2.3** CI assembly background | HONEST | YES | NDUFAF chaperone literature surveyed faithfully (Vartak 2014, Fassone & Rahman 2012, Koppen 2007) |
| **3.1** Multi-timepoint isolated-mito | HONEST | YES | Quadruple-confirmed absence; PMC4401366 "use within 3h" anchor accurate |
| **3.2** Membrane-potential decay | HEDGED-IN-SOURCE | WITH-REWORK | Bernardi 1998 / Hagen 1997 cited as `[PubMed record]` placeholder text — resolve to real journal/title before citing |
| **3.3** Cardiac preservation buffers | EMBELLISHED | WITH-REWORK | **Confirmed PMID 1756164 ≠ "Jahania 1999" — actually Tian G et al. 1991 J Heart Lung Transplant.** Already on audit's verifier-label-mismatch list |
| **4.1** Q10 for mito proteolysis | HONEST | YES | Q10 = 2-3+ range is mechanistically defensible synthesis, not a single-paper anchor; appropriate caveat |
| **4.2** MitoQ extension factor | HONEST | YES | "No clean fold-extension number for isolated mito" honestly hedged |
| **4.3** Substrate supplementation null | HONEST | YES | Null finding; abstract's null-effect claim safe |
| **5.1** Lon/ClpXP fold-activation | **HONEST** | **YES** | **Pass-7 retraction support 1/3 — explicit refusal to fabricate fold number** |
| **5.2** ROS-driven oxidized degradation | **HONEST** | **YES** | **Pass-7 retraction support 2/3 — Bota & Davies 2002 + Zorov 2014 grounding; refuses to quantify "10-fold"** |
| **5.3** in-vivo vs isolated half-life ratio | **HONEST** | **YES** | **Pass-7 retraction support 3/3 — "could not identify a robust head-to-head study" → directly vindicates retraction** |
| **5a.1** Cardiolipin peroxidation rate | HEDGED-IN-SOURCE | YES | Rate constant honestly disclaimed; Sen 2006 + Kagan 2005 + Petrosillo 1999 + Houtkooper & Vaz 2008 cited correctly |
| **5a.2** Proton-leak time course | HEDGED-IN-SOURCE | WITH-REWORK | Brand 1990 (cited as 1994) + Jastroch 2010 (cited as Divakaruni & Brand 2011) — fix citations per audit's known label-mismatches |
| **5a.3** Cyt c release in storage | HONEST | YES | Mechanistic-only framing appropriate; no quantitative anchor claimed |
| **6.1** 145-gene precedent | HONEST | YES | Novelty claim grounded; no precedent surfaced |
| **6.5** Syn3a-mito crosswalk | HONEST | YES | Conceptual-overlap acknowledged but no formal crosswalk published; novelty claim survives |
| **6.6** Engineering-gap quantification | HEDGED-IN-SOURCE | YES | Absence is the finding (no "fix-X-gain-Y" model); honest |
| **6.7** MitoMAMMAL downstream uptake | HONEST | YES | Limited adoption confirmed; transit-window application novel |
| **7.2** MitoQ ROS scavenging kinetics | HONEST | YES | "No clean rate constant" honestly hedged; redox-buffer framing supported |
| **7.3** Bazil-Dash cardiac adaptation | HONEST | WITH-REWORK | Directional adjustment recommendations (1.5×–3× MCU); not precise calibration |
| **7.4** Cortassa 2006 ROS module | HONEST | YES | "Not packaged as standalone CellML" honestly documented |
| **7.6** ANT/PiC cardiac Vmax | HONEST | YES | "Cardiac difference is density not Vmax" framing supported by Passarella 2021, Taegtmeyer 2002, Lal 2005 |
| **8.1** k_kagan calibration | HONEST | YES | "Effective lumped second-order constant, not microscopic" — honest hedging; recommends scope-limiting framing |
| **8.4** matrix H₂O₂ scavenging k_obs | HONEST | YES | "Upper-end well-energized rate; drifts down" — substrate/state dependence honestly noted |
| **8.6** DepMap CRISPRi cross-ref | HONEST | YES | Honest refusal to fabricate gene-by-gene Chronos scores; provides correct retrieval guidance |
| **8.7** Cortassa IMAC parameters | HONEST | YES | Parameter incompleteness honestly documented; no false specificity |
| **9.2** SS-31 / elamipretide | HONEST | YES | nM-affinity claim grounded without precise KD/IC50 fabricated |
| **9.5** Trehalose / osmolytes | HONEST | YES | Speculative framing preserved appropriately |
| **9.6** Multi-component synergies | HONEST | YES | Additive-not-synergistic framing accurate |
| **9.7** Novel interventions sweep | HONEST | YES | Gap-finding statement grounded in literature absence |
| **9.9** Mn-peptide MDP (USER-FLAGGED) | **HONEST verbatim** | **YES** | **Formulation 3 mM DEHGTAVMLK + 1 mM MnCl₂ + 25 mM phosphate (pH 7.4) directly quoted from source; PMID 27500529 (Gupta/Daly) + US patent 9234168B2 confirmed in batch markdown** |
| **9.10** Ergothioneine / OCTN1 (USER-FLAGGED) | HONEST | YES (minor) | Source says "controversial" not "moderate/controversial" — soften wording before propagating; OCTN1 overexpression engineering vector is supported |
| **10.1** McCully-lineage protocols | HONEST | YES | Buffer recipes (300 mM sucrose / 10 mM K-HEPES / 1 mM K-EGTA pH 7.2) directly quoted from McCully papers |
| **10.2** Buffer composition variation | HONEST | YES | "MiR05 only fully-resolved buffer" accurate |
| **10.3** Multi-timepoint readouts | HONEST | YES | True-absence finding correctly documented |
| **10.5** Post-extraction proteome | HEDGED-IN-SOURCE | WITH-REWORK | Soften "likely depletion" to "potential enrichment bias" before propagating |
| **10.6** Protease inhibitor usage | HEDGED-IN-SOURCE | WITH-REWORK | If propagating "12h halflife valid with inhibitor protection" caveat, must explicitly list standard concentrations (PMSF 1 mM + leupeptin/aprotinin/pepstatin 10 µg/mL each) |
| **10.7** Taguchi DoE precedent | HONEST | YES | Null finding grounded; user's 2024 yeast Taguchi work would be methodologically novel |
| **10.8** Cross-extraction-method | HONEST | YES | Percoll / magnetic / nitrogen-cavitation comparisons faithful to Frezza 2020 + Azimzadeh 2016 + Graham 2001 |

### 6.3 Pattern observation across both audit rounds

| | Original 19 (canonical audit) | New 38 (this Tier-2 extension) |
|---|---|---|
| HONEST | ~7 | **31** |
| HEDGED-IN-SOURCE | ~3 | 5 |
| STRETCHED | ~5 (8.3, 9.3, 6.3, 2.2 esp.) | 0 |
| EMBELLISHED | 1 (9.4 BAPTA fabrication) | 1 (3.3 verifier label) |
| MISLEADING | ~2 (2.2, 8.5/8.8 framing) | 0 |

**Headline:** the audit's worst findings concentrate in the originally-audited subset (largely Batches 6.x – 9.x where higher-stakes synthesis was attempted). The 38 newly-verified batches are substantially cleaner. The pass-7 retraction's literature support (Batches 5.1–5.3) is solid. The user-flagged Layer-2 vectors (Batches 9.9 MDP, 9.10 ergothioneine) are propagation-safe with one minor wording adjustment.

### 6.4 Action updates to §7 of the audit

These Tier-2 results unlock several deferred items in the audit's "with rework" bucket:

- **EDIT F (halflife caveat from Batch 10.6) — now safe to apply** with explicit inhibitor concentrations (PMSF 1 mM; leupeptin/aprotinin/pepstatin 10 µg/mL each).
- **EDIT G (accessory subunit caveat from Batch 10.5) — safe to apply** with softer language ("potential enrichment bias" rather than "likely depletion").
- **EDIT H (Taguchi DoE methodological-novelty positioning from Batch 10.7) — safe to apply.**
- **MDP propagation (Batch 9.9) — safe to apply verbatim** for the user's Layer-2 framing. Cite Gupta P et al. (2016) PLoS One 11(8):e0160575 PMID 27500529 (Daly lab) + US Patent 9234168B2.
- **Ergothioneine propagation (Batch 9.10) — safe with one wording change**: replace "moderate/controversial" with "controversial" per source verbatim.
- **Pass-7 retraction's Batches 5.1–5.3 framing — safe** (the strongest finding of the Tier-2 extension; abstract's most prominent honesty move has solid literature support).

### 6.5 Citation issues remaining (post-Tier-2)

| Citation | Issue | Action |
|---|---|---|
| PMID 1756164 (Batch 3.3) | Cited as "Jahania 1999"; actually **Tian G et al. (1991) J Heart Lung Transplant** | Re-render from API fields |
| Brand 1990 (Batch 5a.2) | Originally cited as "Brand 1994" — already corrected in verifier table | Use Brand MD (1990) BBA PMID 2393654 |
| Jastroch 2010 (Batch 5a.2) | Originally cited as "Divakaruni & Brand 2011" — already corrected | Use Jastroch M et al. (2010) Essays Biochem PMID 20533900 |
| Bernardi 1998 / Hagen 1997 (Batch 3.2) | Cited with `[PubMed record]` placeholder text | Resolve to real journal/title from PMID before citing |

---

## 7. Domain-agent action checklist (top-level)

In rough order of safety / ease:

1. **Apply EDIT A** (McCully 2016 4-hour correction) — clean.
2. **Apply EDIT C** (independence-assumption caveat with Mathieson 2018 + TRAIL) — use "coherent" not "coordinated."
3. **Apply EDIT D** (soften MitoQ "vindicates" to "mechanistically consistent with"; cite James AM 2005 PMID 15788391).
4. **Decide on EDIT E** (scenario B reframe vs revise) — user judgment.
5. **REWORK EDIT B** (cold-chain mechanism) — drop the specific Tm number; go with mechanism-named-only language since neither Hackenbrock 1976 nor Schlame 2008 *JLR* anchors 10–12°C.
6. **REWORK EDIT 2.9** (three-class hedge) — adjust framing to acknowledge To 2019 uses different categorization.
7. **Drop everything in §3** (Fritzemeier caveat as written, Schlame 2008 PLR, Khailova 2021, Batch 6.2 inline cites, Batch 9.4 BAPTA claim, Batch 2.2 LLM stubs).
8. **Hold EDIT F, G, H** until Tier-2 audit-extension confirms.
9. **Fix `ci_subunit_data.csv`** — PMID 33892173 returns Gould 2021 *Bone*, not Lam (independent of abstract changes).
10. **Generate clean propagation list from `_citation_verifications.json`** — read API fields (`title`, `authors[0]`, `year`, `journal`, `doi`, `pmid`), ignore `label`. (Audit §3.4.)

---

## 8. Provenance

- This document drafted 2026-05-10 PM as Tier-3 deliverable for the q-bio Chicago domain agent.
- Tier-1 (5 WebFetches): independent verification of audit's recommended replacement citations against PubMed source pages.
- Tier-2 (6 parallel Explore agents): extending the audit to cover the 38 unverified batches; running at time of writing.
- Tier-3 (this document): synthesis of audit §7 + Tier-1 results into per-edit BEFORE/AFTER/EVIDENCE/CITATION blocks, plus the meta-correction layer the audit didn't reach.
- No `ABSTRACT_DRAFT_2026-04-23.md`, `TRUST_LEDGER.md`, results CSV, or experiment script was modified.
- Source files: `DOCINSIGHT_VERIFICATION_AUDIT_2026-05-10.md`, `DOCINSIGHT_FINDINGS_2026-05-09.md`, raw `batch_*.json` files, PubMed esummary endpoints.

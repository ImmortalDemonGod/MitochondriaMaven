# DocInsight Query Guide: Mitochondria Maven
**Original date:** 2026-04-22
**Last updated:** 2026-04-24 (post-audit — see `AUDIT_2026-04-23.md`)

> **Status:** Framework has run end-to-end. DocInsight is no longer blocking — it's the tool for **closing the gaps the audit surfaced**. This guide is restructured into five priority batches based on what the audit showed is actually missing, not what the plan originally imagined.

---

## Agent Execution Brief

**If you are an independent agent executing this guide, read this section first.**

### What this is for

The deliverable is a 350-word abstract for q-bio Chicago 2026 (submission deadline 2026-05-31). The abstract is drafted at `docs/conference_planning/ABSTRACT_DRAFT_2026-04-23.md`. It has six load-bearing claims:

1. 145-gene mouse nuclear mitochondrial essential set (89% mito GO)
2. CI (39-subunit AND-clause) governs transit window via order statistics
3. Three-class gene structure (145 / ~207 / ~22)
4. Empirical TW 5.1h matches MiR05 4-18h (currently achieved via a 30× fitted scaling factor)
5. Syn3A mechanism-level equivalence (phosphate, amino acid imports; pyruvate divergent)
6. Cold chain 14× predicted vs 4× empirical → gap quantifies non-proteomic failure

The audit (`docs/investigation/AUDIT_2026-04-23.md`) identified which are rock-solid vs which are fragile. You're running these queries to **close the fragile gaps**, not to re-verify the solid ones.

### What success and failure look like per batch

| Batch | Success = | Partial success = | Failure = |
|---|---|---|---|
| 1 | MitoCarta/DepMap/OMIM cross-ref numbers (e.g., "128/145 in MitoCarta, OMIM p<0.001") | Some numbers, missing one DB | No usable numbers — keep "89% GO" as-is |
| 2.1 | Exact half-lives from Karunadharma 2015 SI for ≥4 of 5 CI subunits | 2-3 subunits' exact values, rest bracketed | Nothing exact — keep current bracketed ranges with explicit caveat |
| 2.2/2.3 | Evidence CI subunits are correlated (r>0.7) OR independent (r<0.3) | Mixed evidence | Unresolved — state independence assumption in abstract explicitly |
| 3 | Any mammalian time-course paper with multi-hour ΔΨm/ATP/RCR decay points | One paper with partial data | **Most likely outcome.** Pivot: submit with 30× explicit sensitivity sweep + limitation paragraph |
| 4 | Literature Q10, MitoQ%, substrate effect (even as ranges) | Some parameters, others still placeholders | Re-run interventions with ranges across full literature envelope |
| 5 | In-vivo vs isolated half-life ratio citable directly (e.g., Langer 2018) | Lon/ClpXP fold data justifying ~30× | No single number supports 30× — convert to sensitivity sweep 10×/30×/100× |
| 5a | Cardiolipin peroxidation rate constants | Ranges only | Keep k_membrane as phenomenological with wider CI |
| 6.1–6.7 | Novelty confirmed (no direct precedent) OR direct-validation precedent found | Related-but-distinct precedent | **6.2 direct-conflict is a submission-blocker.** Escalate to user immediately. |
| 7.1 | Differential Q10 for membrane vs enzymatic | Any temperature-dependence data | Report composite cold-chain finding as "all-processes-share-Q10 limiting case" |
| 7.2 | MitoQ kinetics for ROS scavenging | Ranges | Keep halflife-scalar proxy with acknowledgment |
| 7.3 | Cardiac MPTP parameters | Rat liver + adaptation notes | Use rat liver as baseline with cardiac caveat |
| 7.4 | Cortassa 2006 parameters pullable | Partial SI | Fall back to Beard 2005 + Phase G.5 ROS coupling (already validated in FBA layer) |
| 7.5 | Physiologic sumATP_c / PO2 / Pi ranges per scenario | Any citation with ranges | Keep current informed-guess values with explicit caveat |
| 7.6 | Cardiac ANT/PiC Vmax values | Order-of-magnitude | Test sensitivity: scale E_ANT ±2× and see if ATP-first-always resolves |
| 8.1 | Published k_kagan rate constant for cardiolipin peroxidation | Kagan lab time-course | Keep current k_kagan=1e5 with "effective rate reflecting ~5% CL-bound fraction" caveat |
| 8.2 | Cardiac-specific MCU/NCLX/MPTP parameters | Bers lab ranges | Use current values with "rat-liver-adapted" caveat |
| 8.3 | ETC ROS leak fractions at CI/III for isolated mito | Brand lab ranges | Keep 0.1%/0.05% as midpoint estimate |
| 8.4 | Matrix H₂O₂ scavenging rate | 1-10/s range | Use midpoint; minor calibration |
| 8.5 | MitoQ isolated vs in vivo efficacy comparison | Literature ranges | Keep 4% prediction with "isolated-mito-specific" framing |
| 8.6 | DepMap CRISPRi essentiality for 145-gene set | Per-gene Chronos scores | Report overlap fraction as second hard-validation dimension |
| 8.7 | Cortassa 2006 IMAC parameters | CellML / SI extraction | IMAC refinement deferred; not load-bearing |
| 8.8 | Cardiac CL-bound cyt c fraction | Kagan lit | Justify current 5% effective factor in k_kagan |
| 9.1 | Cardiac IMM Tm + cooling-rate phase physics | Range + DSC data | Keep "unmodeled lipid physics" caveat in cold-chain framing |
| 9.2 | SS-31 / elamipretide concentration & CL-binding kinetics | Szeto lab + clinical data | Add `cl_protector_fraction` scaling k_kagan; predict SS-31 TW extension |
| 9.3 | CsA / SfA / NIM811 MPTP IC50 + isolated-mito efficacy | Di Lisa, Halestrap lit | Add `mptp_blocker_fraction`; model scenario-C rescue |
| 9.4 | Buffer Ca²⁺ chelation effects (EGTA/BAPTA concentrations) | Published recipes | Refine scenario Ca_c; chelated-buffer scenario variant |
| 9.5 | Trehalose + osmolyte membrane stabilization mechanism | Crowe lab, cryoprotectant lit | Alternative membrane-stabilization parameter if lipid Tm sparse |
| 9.6 | Combination therapy efficacy data | Published organ-preservation combinations | Multi-intervention composite stack predictions |
| 9.7 | Novel interventions (H₂S, NMN, CRLS1, gases, osmolytes, encapsulation) | Broad literature sweep | Candidate Ex 13+ experimental modules for surprising hits |
| 9.8 | Cooling/warming rate protocols | Cryopreservation literature | Add time-dependent temperature profile to composite |
| 9.9 | D. radiodurans Mn²⁺-peptide (MDP) scavenging kinetics + Fenton suppression | Daly lab USUHS | Add `inorganic_scavenger` non-depleting parameter; model Fenton-chemistry blockade as a distinct pathway |
| 9.10 | L-Ergothioneine OCTN1 transport + ·OH scavenging + mitochondrial accumulation | Gründemann lab, Paul & Snyder | Add ESH as stable thiol scavenger with ·OH specificity; enables Layer 2 OCTN1-overexpression virtual-screening |

### Priority order and decision gates

Run in this sequence. Each gate determines whether to proceed, pivot, or escalate.

**Gate 1 — Batch 6.2 (order-statistics precedent):**
- If direct conflict found → **STOP, escalate to user**. Two options: (a) withdraw abstract, (b) reposition as "applying known framework" (demotes methodological claim)
- If direct validation / related precedent → cite and proceed
- If no precedent → proceed, claim novelty

**Gate 2 — Batch 6.1 + 6.4 + 6.7 (other novelty checks):**
- Same decision matrix; unlikely to hit submission-blocker alone
- Document all cited precedents in a working novelty table; hand back to user for abstract update

**Gate 3 — Batch 1 (validation):**
- Non-blocking; abstract is acceptable without this but strengthens substantially with it
- Target: replace "89% GO" with hard-DB numbers

**Gate 4 — Batch 3 (empirical anchor):**
- Time-box to ~2 hours of search (this is the lowest-probability batch given audit-verified absence of McCully/Pacak/Cowan/Oroboros data)
- If nothing found in that window → **do not keep searching**. Pivot: abstract gets a "limitation: direct independent empirical anchor not available; 30× factor supported by mechanistic argument only" paragraph
- Explicitly forbidden: citing Preble 2014, Cowan 2016, Pacak 2015, Masuzawa 2013, Baglivo/Gnaiger 2024 as time-course anchors (audit-verified absent)

**Gate 5 — Batches 2, 4, 5 (parameter refinement):**
- Run in parallel; each independently improves specific abstract claims
- Outcomes feed directly into code changes (new scalars, sensitivity sweeps)

### What to do with results — general principles

1. **Never fabricate data.** If a paper you cite is not fetched and verified, don't cite it. The audit caught three McCully-lab citations that didn't contain the claimed data; don't recreate that error.
2. **Prefer ranges to points.** If the literature reports "Q10 = 2-3," put 2-3 in the code, not 2.5.
3. **Document provenance.** Every new number in `ci_subunit_data.csv`, in code constants, or in the abstract needs a citation next to it — PMID, DOI, or direct URL.
4. **Update TRUST_LEDGER.md** for each claim whose C1–C6 status changes because of new literature.
5. **Re-run the code, don't assume.** If you replace 30× with a sensitivity sweep, actually re-run `experiment1_v3_empirical.py` and capture new CSVs. If you change Q10, re-run `experiment4_interventions.py` with `T_MAX=240` to clear the 72h cap.
6. **If you are stuck, escalate.** Flag to the user rather than guess. The audit history shows that guessing compounds errors.

### Cross-batch scenarios the agent should recognize

| Scenario | Agent action |
|---|---|
| Best case: all batches return usable data | Update abstract with concrete numbers throughout; flag to user for review |
| Realistic: 1, 4, 5, 6 return; 2 partial; 3 fails | Update what's available; add limitations paragraph for Batch 3 absence; hand back to user |
| Worst: Batch 6.2 finds direct conflict | **STOP, escalate immediately.** Do not update abstract. Summarize the precedent, the conflict, and the two options (withdraw / reposition) for user decision |

### Files the agent will touch (and shouldn't touch)

**Touch:**
- `docs/conference_planning/ABSTRACT_DRAFT_2026-04-23.md` — update numbers, add citations
- `docs/investigation/TRUST_LEDGER.md` — update C5 (literature) columns
- `results/phase_b/essential_genes_annotated.csv` — add MitoCarta/DepMap/OMIM columns
- `results/phase_h/ci_subunit_data.csv` — replace bracketed with exact values
- `results/phase_h/empirical_decay_curves.csv` — new file from Batch 3 results
- `scripts/experiments_v2/experiment1_v3_empirical.py` — replace POST_EXTRACTION_ACCELERATION if warranted, or add sensitivity sweep function
- `scripts/experiments_v2/experiment4_interventions.py` — replace Q10, MITOQ_EXTENSION_FACTOR, T_MAX

**Don't touch without user approval:**
- `docs/investigation/FRAMING_2026-04-23.md` — canonical framing doc, changes only on explicit user ask
- `docs/investigation/AUDIT_2026-04-23.md` — audit log, append-only
- Phase A-G result CSVs — historical record

---

## What the audit + Session 8 composite changed

**Updated 2026-04-24 (pass-7 honest-status version):** Session 8 composite build + four stretch extensions + pass-7 audit retraction produced new findings that refine query priorities:

1. **halflife dominates TW variance ~10× over any Beard ODE parameter** (Ex 5.6 tornado). Tightening halflife calibration is a high-leverage improvement.
2. **Option (b) k_membrane is a fitted scalar in a better physical slot, NOT a mechanism resolution.** Pass-7 retraction: "option (b) mechanistically closes engineering gap" was overclaimed. k_membrane ≈ 0.1/h was selected by sweeping to land TW in empirical range — same class as 30× factor.
3. **Composite MECHANISM incomplete.** ROS not modeled, MPTP not modeled, cardiolipin pool not modeled. Option (b.1) is phenomenological proton-leak amplifier only.
4. **Scenario propagation differentiates A/B/C** via PO2 + substrate pools (Session 8.1 stretch) — values were informed guesses, not literature-anchored.
5. **Human-GEM cross-model** (Ex 7) confirmed composite transferability.
6. **"ATP-first always" paradox** — every composite run had ATP threshold crossing before ΔΨm. May be artifact of under-specified ANT/PiC Vmax vs cardiac in-vivo.
7. **Cold chain composite over-prediction (>240h vs empirical ~20h)** — applying one Q10 to all processes missed that membrane decay has different temperature dependence than enzymatic kinetics.

**Revised priority ordering (post-pass-8, Session 9):**

With Session 9 mechanism modules (MPTP, Kagan cycle) implemented, some batches are partially satisfied and new ones take priority:

- **NEW Batch 9** (Session-9 intervention calibration) — HIGHEST for paper's Engineering section: MPTP blockers 9.3 (single-biggest modeled extension — ~30× for scenario C), SS-31 Kagan-pathway 9.2, broad intervention sweep 9.7 (catches what we haven't considered), lipid Tm 9.1 + cooling-rate 9.8 (closes cold-chain over-prediction)
- **Batch 8** (Session 9 mechanism calibration) — HIGH for abstract honesty: k_kagan 8.1, DepMap 8.6, MitoQ isolated 8.5, cardiac MCU/NCLX 8.2, ETC ROS 8.3, H₂O₂ scavenging 8.4
- **Batch 1** (MitoCarta/DepMap cross-ref) — PARTIALLY DONE: MitoCarta cross-ref manually completed (127/145 = 87.6%); DepMap moved to 8.6
- **Batch 6** (novelty / prior art) — MEDIUM: submission-blocker risk check, worth doing before submission
- **Batch 5a** (cardiolipin literature) — MEDIUM: partially superseded by Kagan cycle; k_kagan calibration in 8.1; additional intervention-specific angle in 9.2
- **Batch 2** (Karunadharma SI for CI subunits) — MEDIUM: load-bearing for halflife sensitivity
- **Batches 3, 4, 7** — unchanged from earlier priority
- **Batch 5** (original 30× problem) — DEPRECATED: replaced by explicit mechanism chain

Five audit passes on 2026-04-23 identified where the abstract's evidence is genuinely weak vs. where it's defensible. Queries below target **only the genuine gaps**. Original batches 1–3 have been reorganized:

| Old batch | New batch | Change |
|---|---|---|
| Batch 1: MitoCarta/DepMap/OMIM | **Batch 1** (unchanged) | Still HIGH priority; converts "89% GO" → "X% MitoCarta-listed" |
| Batch 2: Correlation structure | **Batch 2** (sharpened) | Added explicit **Karunadharma 2015 SI extraction** for NDUFS1/S2/A9/B10/A12 exact values (audit: 4 of 5 subunits are bracketed ranges, not verified) |
| Batch 3: Empirical anchors + engineering | **Batch 3** (REVISED — bad citations removed) | Audit verified McCully/Preble/Cowan/Pacak/Oroboros papers **do NOT contain discrete time-course viability data**. Query reworked; search space redirected. |
| — | **Batch 4** (NEW) | Explicit intervention parameters (Q10, MitoQ %, substrate supplementation) — audit found these are hardcoded placeholders |
| — | **Batch 5** (NEW) | Post-extraction acceleration factor literature — the 30× scaling in `experiment1_v3_empirical.py:56` is mechanistically motivated but quantitatively fitted |

**If only one batch: do Batch 1.** It strengthens the abstract's validation paragraph most visibly.
**If two: add Batch 4** — replaces placeholder intervention scalars with literature values.
**Most-valuable unsolved problem: Batch 3 with redirected search space** — the independent empirical anchor is the one real gap the audits couldn't close.

---

## Starting DocInsight

```bash
cd /Volumes/Totallynotaharddrive/DocInsight
bash start_background_processes.sh start
```

Verify:
```bash
curl http://127.0.0.1:52020/health
curl http://localhost:9901/health
```

Streamlit UI: `http://localhost:8501`

---

## Corpus Ingestion — REQUIRED FIRST STEP (added 2026-04-24 post-pass-11 audit)

Pass-11 literature-audit verified the project **already has substantial extraction-protocol literature** that was previously assumed to be absent. Before running Web-augmented queries, ingest these local sources into DocInsight's LanceDB index so queries can do local-corpus-first + web-augmented retrieval rather than web-only.

### Sources to ingest

**Primary (highest signal):**
1. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/05_Extracted_Data/Structured_JSON/`** — 91 machine-extracted JSON files with full paper content, methods, results. Includes Preble/Pacak/Kondo/McCully 2014 (rapid isolation for transplantation) and 90 other extraction/preservation primary sources.
2. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Extraction_Methods/`** — 95 PDF files (1950s–2024) on mitochondrial isolation techniques.
3. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Reference_Papers/`** — 16 files on broader context (synthetic cells, cell signaling, transfer mechanisms).
4. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Mitochondrial_Transfer/`** — 7 .docx files on transplantation/transfer.

**Secondary (already-synthesized):**
5. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/06_Synthesis/Consolidated_Protocols.txt`** — 1.4 MB, 13,268 lines of systematic extraction-protocol synthesis comparing methods across ~91 papers. Covers differential centrifugation, Percoll gradients, Proteinase K treatment, streptolysin membrane disruption, skeletal muscle / cardiac / liver / lipid droplet isolation.
6. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/06_Synthesis/Annotated_Bibliography.docx`** (400 KB).
7. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/06_Synthesis/Comparative_Analysis/`** — 12 Word documents of comparative synthesis.

**Tertiary (project-authored):**
8. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/07_Lab_Manual/Mitochondrial_Isolation_Report.pdf`** — 32-page project-authored unified extraction protocol document (Feb 2024; yeast protocol, ABCAM reference, buffer recipes).

**Registry:**
9. **`/Users/tomriddle1/Dropbox/Mitochondria Maven/03_Study_Registry/studies.csv`** — 114-paper screening registry with inclusion probabilities (for deduplication and authority scoring).

### Ingestion commands

```bash
# Point DocInsight at the extracted JSON corpus (preferred — structured data)
curl -X POST http://127.0.0.1:52020/ingest_directory \
  -H "Content-Type: application/json" \
  -d '{
    "paths": [
      "/Users/tomriddle1/Dropbox/Mitochondria Maven/05_Extracted_Data/Structured_JSON",
      "/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Extraction_Methods",
      "/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Reference_Papers",
      "/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Mitochondrial_Transfer",
      "/Users/tomriddle1/Dropbox/Mitochondria Maven/06_Synthesis",
      "/Users/tomriddle1/Dropbox/Mitochondria Maven/07_Lab_Manual"
    ],
    "index_name": "mitomaven_local",
    "recursive": true
  }'
```

(If DocInsight's ingestion endpoint differs from `/ingest_directory`, consult the DocInsight README. The intent is: build a LanceDB index named `mitomaven_local` over these paths.)

Verify ingestion:
```bash
curl http://127.0.0.1:52020/list_indexes
# Should show mitomaven_local with document count ~200+ papers/docs
```

### Querying against the local corpus

Once ingested, all subsequent queries (Batches 1–10) can specify `index_name: "mitomaven_local"` in addition to the default web-augmented retrieval. This gives:
- **Local-first answers** where the paper exists in our corpus (91 JSON-extracted are queryable at full-text level)
- **Web augmentation** for anything beyond our corpus
- **Citation provenance** — results can cite local JSON paper paths directly

**This eliminates most need for Web-only Batch queries.** Many of the Batch 1–9 questions are likely already answerable from our 91-paper corpus + Consolidated_Protocols.txt synthesis. The executing agent should try local-first, escalate to web-augmented only when local returns insufficient.

---

## Note on the existing DocInsight corpus (pre-ingestion)

Current LanceDB index contains water quality / citizen science papers (Blue Thumb / OCLWA project) — those papers won't answer mitochondria queries. After corpus ingestion above, prefer `index_name: "mitomaven_local"` for all mitochondria/mito-preservation queries.

---

## Batch 1 — Validate the 145-Gene Essential Set (HIGH PRIORITY for abstract)

### Why this matters

We currently claim "145 individually-essential mouse nuclear genes, 89% mitochondrial GO." The GO annotation is loose (anything with `mitochondri*` in cellular component) and self-validating (FBA-derived essentials encoded in a mitochondrial model should localize to mitochondria). External validation requires:
- **MitoCarta 3.0** (Rath et al. 2021) — curated mitochondrial proteome, gold standard
- **DepMap / Replogle 2022 CRISPRi** — experimental essentiality
- **OMIM / ClinVar** — clinically-validated disease genes
- **Scoop check** — has this exact analysis been published?

### Queries

**Query 1.1 — MitoCarta 3.0 + CRISPRi cross-reference:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Mouse cardiac mitochondrial essential gene set: cross-reference between MitoCarta 3.0 (Rath et al. 2021), DepMap mitochondrial gene essentiality, MITOMICS knockout screens (Calvo lab), and Replogle 2022 CRISPRi-essentiality. What fraction of the canonical 1158 MitoCarta proteins are essential under standard galactose conditions vs glucose? Which mouse nuclear-encoded ETC subunits are universally essential vs context-dependent? Provide the citations needed to cross-reference a list of 145 mouse nuclear genes against these databases."
    ]
  }'
```

**Query 1.2 — OMIM disease enrichment:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Mitochondrial disease genes in OMIM/ClinVar: complete list of nuclear-encoded genes whose loss-of-function causes mitochondrial disease (Leigh syndrome, MELAS, MERRF, LHON, complex I/II/III/IV/V deficiency, mitochondrial encephalomyopathy). Specifically: which NDUF*, SDH*, UQCR*, COX*, ATP5* gene KOs cause OXPHOS disease in humans? What is the expected disease-gene enrichment baseline for a randomly selected set of 145 mitochondrial proteins?"
    ]
  }'
```

**Query 1.3 — Scoop check (novelty):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Time-stepped flux balance analysis with protein decay applied to mitochondrial transplantation or isolated mitochondrial viability prediction. Has the MitoMAMMAL or MitoCore model been used to model post-extraction protein turnover and ATP decay over time? Habermann lab, Smith MitoCore lab. Any paper applying constraint-based metabolic modeling + nuclear protein decay kinetics to predict mitochondrial transit window? FBA-derived mitochondrial essential gene sets. Verify this analytical approach has not been published before."
    ]
  }'
```

### What to do with results

- **1.1** → cross-reference `results/phase_b/essential_genes_annotated.csv`; replace "89% mitochondrial GO" with "X% MitoCarta-listed, Y% CRISPRi-essential"
- **1.2** → Fisher's enrichment over MitoCarta baseline for OMIM disease genes in our 145
- **1.3** → if novel, explicitly cite the gap; if scooped, reposition contribution

---

## Batch 2 — CI Subunit Ground Truth + Independence Structure

### Why this matters

Two problems the audit surfaced:

1. **4 of 5 CI subunit half-lives are bracketed ranges**, not verified values. `results/phase_h/ci_subunit_data.csv` contains notes like `"Bracketed range — needs Karunadharma SI for exact value"`. Only NDUFS2 (17.8d, Kim 2012) is a confirmed measurement. NDUFA12 has no data at all.

2. **Order-statistics on N=39 assumes per-subunit independence.** CI subunits are co-translationally assembled; likely correlated. If correlated, "min over 39 i.i.d. samples" is the wrong model.

### Queries

**Query 2.1 — Karunadharma 2015 SI extraction (fills the bracketed cells):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "From Karunadharma et al. 2015 (PMID 25977255) Supplementary Information tables, extract exact in-vivo protein half-lives (in days or hours) for the following mouse cardiac Complex I subunits: NDUFS1, NDUFS2, NDUFA9, NDUFB10, NDUFA12. If NDUFA12 is not reported, provide half-lives for NDUFA8 or NDUFA13 as substitutes. Also extract half-lives for representative subunits of CII (SDHA, SDHB), CIII (UQCRC1, UQCRC2, CYC1), CIV (COX4I1, COX5A, COX6A), CV (ATP5A1, ATP5B), and SLC25 carriers (SLC25A3, SLC25A4, SLC25A11). Report precise numeric values from supplementary tables, not rounded narrative descriptions."
    ]
  }'
```

**Query 2.2 — Per-subunit correlation within complexes:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Per-subunit protein half-lives for mammalian electron transport chain measured by D2O labeling, SILAC pulse-chase, or isotope-encoding proteomics. Sources: Lam et al. 2021 Mol Cell Proteomics (cardiac), Fornasiero et al. 2018 Nat Commun (brain), Kim et al. 2012 MCP (heart mitochondria), Price et al. 2010 PNAS. Critical question: within Complex I (39+ subunits), are individual subunit half-lives CORRELATED (suggesting co-translational regulation, holoenzyme-level turnover via Lon/ClpXP) or INDEPENDENT (per-subunit replacement)? Report the variance/distribution of half-lives within each ETC complex, and any published analyses of co-turnover across the complex."
    ]
  }'
```

**Query 2.3 — Holoenzyme assembly + disassembly kinetics:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Complex I (NADH:ubiquinone oxidoreductase) assembly and disassembly kinetics. Bogenhagen lab, Ott lab, Vogel/Brandt CI assembly studies. Does mature CI degrade as 39 independent subunits replaced individually, or as a holoenzyme via coordinated Lon/ClpXP-mediated turnover? Half-life of fully assembled vs partially-assembled CI. NDUFAF1-7 chaperone roles. Are accessory vs core subunits replaced at different rates? m-AAA protease and AFG3L2-SPG7 turnover of membrane-arm subunits."
    ]
  }'
```

### What to do with results

- **2.1** → update `results/phase_h/ci_subunit_data.csv` with verified values; re-run `experiment1_v3_empirical.py` with exact rather than bracketed inputs
- **2.2** → permutation test with real N (currently N=4 effective); if correlated → switch to holoenzyme single-rate
- **2.3** → mechanism resolution for which decay model is right; document assumption in abstract

---

## Batch 3 — Independent Empirical Anchor (HARDEST; PAPERS VERIFIED NOT TO WORK)

### Why this matters

The abstract says "predicted TW 5.1h matches MiR05 4-18h literature." This match is produced by a **30× post-extraction acceleration factor** tuned to land in the empirical range. Without an **independent** empirical calibration anchor, the match is circular — we dialed the knob to hit the target.

Phase K's planned solution (2024 yeast JC-1 notebook) may not be digitizable, and is species-mismatched anyway.

### Audit-verified negative results — DO NOT cite these as anchors

A pass-5 audit WebFetched the following papers. **None contain discrete multi-hour time-course viability data for isolated extracellular mammalian mitochondria:**

| Paper | Actual content |
|---|---|
| Preble 2014 (J Vis Exp, PMID 25225817) | Single-timepoint post-isolation QC (ATP, RCI, O2). Acknowledges decay but doesn't measure it. |
| Cowan 2016 (PLoS ONE, PMID 27536870) | Single-timepoint labeled-vs-unlabeled. Mitochondria used "immediately." |
| Pacak 2015 (Biology Open, PMID 25862247) | 1h/4h/24h timepoints measure **uptake INTO cardiomyocytes** and ATP rescue **inside recipient cells** — NOT extracellular isolated-mito decay |
| Masuzawa 2013 (AJP Heart) | Delivery/cardioprotection, not storage time-course |
| Baglivo/Gnaiger 2024 (Oroboros) | MiR05 medium storage stability using HEK293T cells, not isolated-mito time-course |

**Stop citing these as time-course anchors.** The McCully-lab citation chain that recurs in draft materials points to methods/delivery papers, not storage-decay papers.

### Redirected search — where the data might actually be

**Query 3.1 — Mitochondrial isolation stability (alternative literature):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Experimental time-course decay of isolated mammalian mitochondrial function measured at multiple discrete timepoints (e.g., 0h, 1h, 2h, 4h, 8h, 12h, 24h) while stored in buffer extracellularly. Metrics: State 3 respiration, ATP synthesis rate, RCR (respiratory control ratio), membrane potential (ΔΨm via JC-1/TMRM), cytochrome c release. Candidate sources: Picard et al. 2011 (mitochondrial isolation artifacts), Kuznetsov et al. on mito preparation stability, Andreyev/Kushnareva/Starkov reviews, Brand lab reviews. Also: trehalose and sucrose cryopreservation time-course literature. Looking for papers that plot decay curves, NOT single-timepoint post-isolation QC. Do NOT return McCully lab papers (Preble 2014, Cowan 2016, Pacak 2015, Masuzawa 2013) — these have been verified to contain only single-timepoint data."
    ]
  }'
```

**Query 3.2 — Membrane potential / respirometry decay in non-transplantation contexts:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Time-resolved measurements of isolated mitochondrial membrane potential or respiration decay in ischemia-reperfusion, organ preservation, and bioenergetics research (not clinical mitochondrial transplantation). Drug-screening assays that monitor ΔΨm over hours. Mitochondrial permeability transition pore opening kinetics with continuous ΔΨm readout. Seahorse XF kinetic traces on isolated mitochondria beyond the typical 1-hour assay window. Looking for any paper that plots a decay curve with multiple timepoints, regardless of application domain."
    ]
  }'
```

**Query 3.3 — Cardiac preservation / organ transplant buffers:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Heart preservation buffers (UW solution, HTK/Custodiol, Celsior, St. Thomas) — time-course data for mitochondrial function during extended cold storage (4-24h). Does any cardiac transplant literature measure isolated mitochondrial ATP or ΔΨm over storage time? MitoSOX, MitoTracker, or JC-1 kinetics during organ preservation. If available, this would be a cross-domain empirical anchor for extracellular mitochondrial decay rates."
    ]
  }'
```

### What to do with results

- Any real time-course paper → digitize figure points into `results/phase_h/empirical_decay_curves.csv`
- Overlay against our 5.1h predicted curve
- If predicted falls within experimental error → calibration defensible
- If not → recompute 30× scaling factor from the anchor, report the revised TW

---

## Batch 4 — Intervention Parameters (Q10, MitoQ, Substrate)

### Why this matters

Audit found `experiment4_interventions.py` contains three hardcoded scalars with comments explicitly flagging them as literature-pending:
- `Q10 = 2.5` — "midpoint of literature 2-3 range; from DocInsight Batch 4.3 placeholder"
- `MITOQ_EXTENSION_FACTOR = 1.35` — "Literature reports 20-50% extension (Murphy, Smith labs)"
- `B_supplemented` substrate bounds — "literature TBD"

The abstract's engineering paragraph ("cold chain 14× predicted vs 4× empirical") rests on these. Also, **the cold-chain prediction hits the 72h simulation cap** (all three scenarios exactly `72.0h`), so the "14×" is `72/5`, not a real prediction.

### Queries

**Query 4.1 — Q10 for mitochondrial proteolysis:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Q10 temperature coefficient for mammalian mitochondrial proteolysis, ETC subunit degradation, and Lon/ClpXP protease activity between 4°C cold storage and 37°C physiological temperature. Experimentally measured fold-extension of isolated mitochondrial functional half-life when stored at 4°C vs 37°C. Q10 values for protein turnover in general biochemistry: is 2.5 the right midpoint, or is proteolysis better characterized by Q10 = 2, 3, or higher? Any paper reporting actual cold-storage extension factor for isolated mammalian mitochondria (not organs)."
    ]
  }'
```

**Query 4.2 — Antioxidant extension factor:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Quantitative half-life or viability extension effects of mitochondria-targeted antioxidants on isolated mitochondria in vitro. MitoQ, SkQ1, NAC, EUK-134, MitoTEMPO at specific concentrations. Report percentage extension of respiratory capacity, ΔΨm retention, or ATP synthesis half-life. Murphy, Smith (Newcastle), Skulachev, Szeto lab publications. Specifically: does any paper report a clean fold-extension number for MitoQ or SkQ1 on isolated (not in vivo) mammalian mitochondria?"
    ]
  }'
```

**Query 4.3 — Substrate supplementation:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Effect of pyruvate, malate, succinate, or ADP supplementation in preservation buffer on isolated mammalian mitochondrial functional lifetime. Does adding respiratory substrates to storage buffer extend viability, or is storage limited by enzyme capacity rather than substrate availability? Oroboros MiR05 formulation rationale. Any quantitative time-course comparing substrate-rich vs substrate-depleted storage."
    ]
  }'
```

### What to do with results

- **4.1** → replace `Q10 = 2.5` with literature-sourced value + uncertainty range; re-run cold-chain intervention with **T_MAX ≥ 240h** to remove simulation-cap artifact
- **4.2** → replace `MITOQ_EXTENSION_FACTOR = 1.35` with literature value or range; if literature only reports ranges, report model output as range
- **4.3** → either confirm ~0h effect (which the code already shows) or discover a regime where substrate matters

---

## Batch 5a — Cardiolipin Peroxidation and Membrane Integrity Decay (NEW — Session 8 finding)

### Why this matters (revised 2026-04-24)

Session 8's option (b) extension (Ex 6) found that adding a bounded membrane-integrity decay term to the composite closes the engineering gap WITHOUT requiring a 30× acceleration factor. k_membrane = 0.1 /hour (membrane functional halflife ~6.9h) produces TW_ATP = 11.1h — center of empirical MiR05 4–18h range.

This promotes cardiolipin peroxidation + membrane integrity kinetics from "deferred option-b layer" to the single most impactful parameter to tighten. Currently k_membrane is "literature-plausible" but not literature-anchored; DocInsight can change that.

### Queries

**Query 5a.1 — Cardiolipin peroxidation kinetics:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Time course of cardiolipin peroxidation in isolated mammalian mitochondria during extracellular storage (buffer, 37°C, no antioxidant). Quantitative rates: percentage cardiolipin oxidized per hour, or k_peroxidation in /hour. Kagan lab (Pittsburgh), Schlame lab (NYU), Dolinay/Greenberg lab. Specifically: at what rate do mitochondria in isolation buffer lose cardiolipin functional integrity, and how does this map to inner membrane proton leak / ETC coupling uncoupling?"
    ]
  }'
```

**Query 5a.2 — Isolated mito proton leak kinetics during storage:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Proton leak (H+ uncoupling) of isolated mammalian mitochondria measured over time during storage. Baseline H+ leak at t=0 vs after 2h, 6h, 12h storage at 37°C in MiR05 or similar buffer. Brand lab, Cannon/Nedergaard lab, Gnaiger/Oroboros data. Fold-increase in proton leak as function of storage duration. How does X_H (nonspecific leak conductance) evolve over the 4-18h MiR05 viability window?"
    ]
  }'
```

**Query 5a.3 — OMM permeabilization + cytochrome c release:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Outer mitochondrial membrane permeabilization (MOMP) in isolated mitochondria during extracellular storage, NOT in apoptotic context. Cytochrome c release kinetics as a function of time in buffer. Does cyt c leak from IMS during storage, and at what rate? If cyt c pool drops, what is the effect on ETC coupling in the remaining intact mitochondria?"
    ]
  }'
```

### What to do with results

- **5a.1 result** → refine `ode_utils.py` leak_growth_rate parameter to literature-anchored value; re-run Ex 6
- **5a.2 result** → validate the saturating-leak functional form (1 + 50 * (1 - exp(-k*t))) against data; adjust MEMBRANE_MAX_FOLD bound if literature suggests different ceiling
- **5a.3 result** → decide whether to extend the composite with a cyt c pool depletion term (currently c_tot is constant)

---

## Batch 5 — Post-Extraction Acceleration Factor (The 30× Problem) — DEPRIORITIZED

**Status 2026-04-24:** Session 8's option (b) extension replaced the 30× factor with a literature-plausible k_membrane membrane-decay rate. This batch's original premise (tighten 30×) is moot. Keep queries below for reference but note they target a deprecated framing.

### Why this matters (original framing)

`experiment1_v3_empirical.py:56` contains:
```python
POST_EXTRACTION_ACCELERATION = 30.0
# Justified by Lon-protease activity + ROS-driven oxidation in isolated mitos
```

This single scalar divides in-vivo half-lives (138–427h) to reach extracted-mito effective rates (4.7–14.2h), which in turn produce the headline 5.1h TW. The factor is mechanistically motivated but **quantitatively fitted**. If it were 10×, TW would be ~15h; if 100×, ~1.5h. The "matches MiR05" claim depends on 30× landing in the empirical envelope.

The audit flagged this as the single load-bearing knob that needs literature support.

### Queries

**Query 5.1 — Lon/ClpXP hyperactivation post-extraction:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Quantitative fold-increase in Lon protease (LONP1) and ClpXP protease activity in isolated mitochondria compared to in-vivo steady-state conditions. Does post-extraction stress (loss of nuclear protein import, ROS burst, calcium dysregulation) activate mitochondrial proteases? By how many fold? Suzuki/Langer lab mitochondrial protease kinetics. Any paper reporting the ratio of in-vivo to in-vitro protein degradation rates for mitochondrial substrates."
    ]
  }'
```

**Query 5.2 — ROS-driven oxidized protein degradation kinetics:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Rate of oxidized mitochondrial protein degradation under elevated ROS conditions. Koopman, Murphy, Brand labs on ROS-driven proteolysis. Does acute ROS exposure (e.g., post-isolation burst) shorten mitochondrial protein half-lives by a quantifiable fold? What fraction of ETC subunit turnover is ROS-dependent vs constitutive? Specific numeric claims (e.g., '10-fold acceleration under 100 nM H2O2')."
    ]
  }'
```

**Query 5.3 — In-vivo vs isolated half-life comparisons:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Direct comparisons of mitochondrial protein turnover rates measured in-vivo versus in-isolated-organelle or ex-vivo conditions. Does any study quantify the difference? The Fornasiero 2018 / Lam 2021 / Karunadharma 2015 values are all in-vivo (D2O labeling in live mice). Isolated mitochondria in buffer should turn over faster because proteostasis is broken — but by how much? Any paper reporting matched in-vivo vs isolated-mito protein degradation."
    ]
  }'
```

### What to do with results

- **5.1 + 5.2** → either confirm 30× is within literature range (strong justification) or reveal it's too high/low (re-derive)
- **5.3** → the ideal result: a published in-vivo-vs-isolated ratio that we can cite directly
- If no literature supports a single number: **replace the point scalar with a sensitivity sweep (10× / 30× / 100×)** in `experiment1_v3_empirical.py` and report TW as a function of acceleration factor rather than a point estimate

---

## Batch 7 — Session-8 + Pass-7 Honest-Status Queries (NEW, 2026-04-24)

### Why this matters

Session 8 composite build surfaced specific literature gaps that the earlier batches didn't target. Pass-7 audit retraction makes these load-bearing for the next composite extension phase (Cortassa 2006 ROS + Bazil-Dash MPTP + cardiolipin pool). Each query addresses one specific Session-8 gap.

### Queries

**Query 7.1 — Temperature dependence of membrane integrity decay (cold-chain over-prediction):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Temperature dependence (Q10) of membrane integrity decay, cardiolipin peroxidation, and OMM permeabilization in isolated mammalian mitochondria between 4°C and 37°C. Specifically: does the rate of inner-membrane proton leak growth during extracellular storage slow at 4°C the way enzymatic reactions do (Q10 ≈ 2-3), or does it have a different temperature dependence (e.g., lipid phase transitions, ROS generation persists differently at low T)? Kagan lab (cardiolipin), Gnaiger/Oroboros (MiR05 cold-storage data), cardiac preservation literature. This is critical for honestly predicting cold-chain effectiveness — our composite with uniform Q10 over-predicts cold chain by an order of magnitude."
    ]
  }'
```

**Query 7.2 — MitoQ direct matrix ROS scavenging kinetics:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "MitoQ direct kinetics on matrix ROS scavenging: IC50, k_scavenging, stoichiometry of MitoQ:O2·⁻ or MitoQ:H2O2 reaction in isolated mitochondria. Distinguish from downstream effects on protein halflives. Smith (Newcastle) lab, Murphy lab publications. Specifically: when a MitoQ molecule reacts with superoxide, what is the rate constant and what happens to the ubiquinol moiety? Is MitoQ regenerated by ubisemiquinone or does it get consumed? This is needed for Cortassa 2006 ROS module integration; currently MitoQ is modeled as a halflife-extension scalar."
    ]
  }'
```

**Query 7.3 — Bazil-Dash 2010 cardiac parameter adaptation:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Bazil, Dash & Beard 2010 bioenergetic MPTP model (J Theor Biol) was fit primarily to rat liver mitochondria. Cardiac mitochondrial Ca²⁺ uptake kinetics (MCU), efflux (NCLX/NCX), matrix Ca²⁺ buffering (by Pi, phosphate/ATP), and MPTP opening threshold are quantitatively different from liver. Provide cardiac-specific parameter values for: MCU Vmax, NCLX/NCX Vmax, matrix Ca²⁺ buffer capacity, MPTP Ca²⁺ threshold. Bers lab, Saks lab, Gunter/Pfeiffer. If rat cardiac MPTP model exists, cite it; otherwise provide cardiac parameter adjustments to Bazil-Dash."
    ]
  }'
```

**Query 7.4 — Cortassa 2006 ROS extension parameter availability:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Cortassa, Aon, Winslow, O Rourke 2006 Biophys J (PMID 16565043) coupled ROS-mitochondrial-bioenergetics model: is the full parameter table available via CellML, BioModels, supplementary information, or author code repository? Parameters needed: J_ROS production rate constant at Complex I and III; GSH-Px Vmax and Km; IMAC (inner-membrane anion channel) conductance; ROS-Ca²⁺ crosstalk rate constants. If CellML version needs manual extension from 2003 model + 2006 paper supplement, provide the specific supplementary table references. We plan to integrate this into a Python composite model — availability in Python/MATLAB format is preferred."
    ]
  }'
```

**Query 7.5 — Arterial/ischemic physiological setpoints (scenario pool validation):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Quantitative physiological setpoints for isolated mitochondria in three scenarios: (a) intracellular buffer baseline (cytosolic [ATP], [ADP], [Pi], PO2, [Mg²⁺], [Ca²⁺]); (b) arterial blood (what are the actual free-nucleotide concentrations at the mitochondrial surface when exposed to blood plasma — plasma adenine nucleotides are in μM range, not mM); (c) ischemic tissue (quantitative Pi accumulation, ADP accumulation, PO2 drop during cardiac/neural ischemia). Specifically: in our composite we assumed scenario B sumATP_c = 0.1 mM and scenario C PO2 = 5 mmHg. Are these in physiological range? Cite sources with actual measurements."
    ]
  }'
```

**Query 7.6 — ANT and PiC cardiac Vmax (ATP-first paradox diagnostic):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Adenine nucleotide translocase (ANT / SLC25A4/5) and phosphate carrier (PiC / SLC25A3) Vmax in cardiac mitochondria vs liver. Beard 2005 parameters (E_ANT = 0.325, E_PiC = 5e6 in his units) were fit to a mix of data; are these cardiac-appropriate? Specifically: does ANT operate at higher Vmax in cardiac due to higher ATP demand, which would mean our composite under-specifies ANT and causes the ATP threshold to cross prematurely (explaining the systematic ATP-first-always pattern)? Klingenberg lab ANT kinetics; Kramer lab PiC."
    ]
  }'
```

### What to do with results

- **7.1** → adds/refines temperature-dependence of k_membrane; re-run Ex 6 cold chain with differential Q10 on membrane vs enzymatic
- **7.2** → enables Cortassa 2006 ROS integration with literature-anchored MitoQ scavenging, replacing halflife scalar
- **7.3** → enables Bazil-Dash MPTP integration with cardiac-appropriate parameters
- **7.4** → confirms or updates Cortassa 2006 parameter availability before investing in implementation
- **7.5** → validates or corrects Session 8.1 scenario substrate pool choices
- **7.6** → may resolve "ATP-first always" paradox without adding a new mechanism layer

### Priority ordering within Batch 7

**7.6 first** — diagnostic, cheap, might resolve a systematic issue with minimal new code.
**7.5 second** — validates existing scenario framework; cheap.
**7.1 third** — directly affects cold-chain abstract claim, which is load-bearing.
**7.4 fourth** — gate for the Cortassa 2006 integration effort.
**7.2 fifth** — needed once 7.4 confirms Cortassa integration is feasible.
**7.3 sixth** — needed for Bazil-Dash MPTP integration.

---

## Batch 8 — Session-9 Mechanism Module Calibration (added 2026-04-24 post-pass-8)

### Why this matters

Session 9 added MPTP + ROS + Kagan-cycle modules introducing ~19 tunable parameters. Pass-8 audit identified that while the mechanism chain is biochemically grounded, specific parameter values were tuned to produce "plausible" dynamics rather than derived from specific measurements. These queries target the load-bearing parameters whose tightening would most strengthen the abstract's quantitative defensibility.

### Queries

**Query 8.1 — Kagan cycle cardiolipin peroxidation rate (k_kagan calibration):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Quantitative rate constant for cyt c + cardiolipin + H₂O₂ peroxidation reaction in isolated mammalian mitochondria. Kagan lab (Pittsburgh), Tyurina, Tyurin, Bayir publications. Specifically: given cyt c concentration ~2 mM, what is the apparent second-order rate constant (M⁻¹s⁻¹ or M⁻²s⁻¹) for catalyzed cardiolipin peroxidation? What fraction of total cyt c is CL-bound and thus peroxidase-active (vs free-cyt-c in IMS engaged in electron transport)? Time course data showing percentage CL oxidized vs time in isolated mito. We currently use k_kagan ~1e5 M⁻²s⁻¹ as effective rate reflecting ~5% CL-binding fraction — literature values to calibrate or refine this."
    ]
  }'
```

**Query 8.2 — Cardiac-specific MPTP parameters (MCU/NCLX Vmax and Ca²⁺ threshold):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Cardiac mitochondrial Ca²⁺ handling kinetic parameters with specific numerical values: (1) MCU (MCU complex, SLC39) Vmax in cardiac mitochondria — quantitative mol/(s·mg) or mol/(s·L_mito); (2) NCLX Vmax in cardiac; (3) Matrix Ca²⁺ threshold for MPTP opening in cardiac (literature reports 100–500 μM; we use 100 μM for cardiac — is there consensus?); (4) Hill coefficients for cooperative MCU Ca²⁺ binding and MPTP opening. Bers lab (Davis), Ríos lab, Saks lab. We currently use V_MCU=0.5e-3, V_NCLX=0.01e-3, Ca_MPTP=100μM — literature to refine these."
    ]
  }'
```

**Query 8.3 — ETC superoxide leak fraction (k_ros_prod_C1, k_ros_prod_C3):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Quantitative fraction of mitochondrial electron transport chain electron flow that escapes as superoxide at Complex I vs Complex III, in isolated mammalian mitochondria at state 3 vs state 4. Literature reports vary 0.1% to 4% of O₂ consumption. Brand lab, Balaban lab, Murphy lab publications. Specifically: under in-vitro storage conditions (no electron sink, high NADH), what is the ROS leak fraction? Does it differ between NADH oxidation vs succinate oxidation (reverse electron transport)? We currently use k_ros_prod_C1 = 1e-3 (0.1% of J_C1) and k_ros_prod_C3 = 5e-4."
    ]
  }'
```

**Query 8.4 — Matrix GSH-Px and H₂O₂ scavenging kinetics:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Pseudo-first-order rate constant for matrix H₂O₂ scavenging by GSH-Px (glutathione peroxidase) and peroxiredoxin in isolated cardiac mitochondria. Literature k_obs ~1-10 /s with physiological GSH-Px concentrations. Under isolated-mito storage (cytosolic GSH may become limited if buffer lacks GSH), does scavenging rate drop over time? Nathan lab, Chance-lab legacy data on catalase vs GSH-Px. We currently use k_H2O2_scavenge = 10/s baseline."
    ]
  }'
```

**Query 8.5 — MitoQ matrix concentration in isolated vs in vivo conditions:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Effective matrix concentration of MitoQ when added to isolated mitochondria in buffer, versus in vivo after systemic administration. Literature extension data: how does MitoQ efficacy in vitro (isolated mito preparations) compare to in vivo? Our composite predicts ~4% TW extension in isolated mito at 5 μM MitoQ vs ~35% reported for halflife-proxy models calibrated to in vivo data. This discrepancy is biologically expected because in vivo MitoQ is supported by cytosolic ubiquinol-regenerating enzymes, while isolated mito lack this recycling. Literature time-course data for isolated-mito MitoQ specifically would help."
    ]
  }'
```

**Query 8.6 — DepMap CRISPRi cross-reference for 145-gene set:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "DepMap CRISPR knockout essentiality scores for a list of 145 mouse nuclear-encoded mitochondrial genes. For each gene in our list (export from results/phase_b/essential_genes_mitocarta_crossref.csv), provide: (a) DepMap essentiality score (Chronos/CERES) across cell lines, (b) variance across tissue types, (c) whether the gene is pan-essential vs context-dependent. Goal: upgrade our 87.6% MitoCarta-listed validation to X% also CRISPRi-essential in galactose conditions (which force mitochondrial respiration). Expect ~70-90% overlap for canonically essential OXPHOS genes."
    ]
  }'
```

**Query 8.7 — Cortassa 2006 IMAC channel parameters (for further refinement):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Inner membrane anion channel (IMAC) parameters from Cortassa 2006 Biophys J — activation by ROS, ΔΨm-dependent conductance, anion permeability. Full parameter set for extending our composite with the IMAC positive-feedback loop. Our composite currently omits IMAC; published CellML / BioModels availability? Key parameters needed: k_IMAC activation by H₂O₂, conductance under open state, its effect on ΔΨm oscillations."
    ]
  }'
```

**Query 8.8 — Cardiac cyt c peroxidase-active fraction:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "What fraction of total mitochondrial cyt c is bound to cardiolipin (vs free in IMS / membrane-associated) under resting vs stressed conditions in cardiac mitochondria? This determines how much of cyt c is peroxidase-active for cardiolipin oxidation (Kagan mechanism). Tyurin / Kagan publications; Schneiter lab cyt c partitioning data. Literature reports range from <5% (resting) to much higher under apoptotic signaling. We use 5% as effective factor in k_kagan."
    ]
  }'
```

### What to do with results

- **8.1–8.4** → refine Session 9 parameter values; re-run Ex 11/12 with calibrated constants; narrow composite CI
- **8.5** → validates (or invalidates) our 4% MitoQ prediction in isolated mito; if literature tightens, this becomes a clean quantitative claim rather than a caveated range
- **8.6** → second hard-validation dimension for the 145-gene set (beyond MitoCarta)
- **8.7** → enables option (b) completion if user wants IMAC-coupled composite
- **8.8** → justifies the "effective" k_kagan tuning honestly

### Priority ordering within Batch 8

**8.1 first** (Kagan rate — most load-bearing for mechanism honesty).
**8.6 second** (DepMap cross-ref — second hard-validation for essential set; direct abstract upgrade).
**8.5 third** (MitoQ isolated vs in vivo — resolves the 4% vs 35% discrepancy).
**8.2, 8.3, 8.4** in parallel (mechanism-module calibration).
**8.7, 8.8** deferred unless user wants IMAC refinement.

---

## Batch 9 — Intervention-Specific Calibration (added 2026-04-24 post-Session-9 intervention-ranking exercise)

### Why this matters

Session 9's mechanism partition identifies specific intervention vectors per failure mode: SS-31-class CL-binding peptides for Kagan-pathway blockade, MPTP inhibitors (cyclosporin A / sanglifehrin A / NIM811) for scenario-C catastrophic collapse, Ca²⁺ chelators for transit-buffer Ca²⁺ reduction, trehalose/osmolytes for membrane stabilization, and cooling-rate-aware cold-chain protocols for lipid phase transition management. The composite currently models MitoQ (4% extension), cold chain (over-predicts), and substrate supp (null) — but the *most promising* vectors per the intervention ranking are NOT yet simulated. These queries anchor the intervention parameters we'd need to model each vector honestly.

### Queries

**Query 9.1 — Lipid phase transitions and chilling injury (mammalian cardiac IMM Tm):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Phase transition temperature (Tm) of mammalian cardiac mitochondrial inner membrane. Cardiolipin-rich membranes undergo lateral phase separation below a critical temperature; for cardiac IMM this is reported somewhere in the 5–20°C range but not well calibrated. Specifically: (1) measured Tm or phase transition range for cardiac IMM via DSC (differential scanning calorimetry), fluorescence anisotropy, or ESR spin probes; (2) cooling-rate dependence of phase separation (fast cooling vitrifies disorder; slow cooling allows domain formation); (3) proton leak increase as a function of temperature below Tm; (4) hibernating-mammal IMM comparison (cold-tolerant species). Quinn, Hazel, Storey (hibernation), Schlame lab publications. Currently unmodeled in our composite — our cold-chain over-prediction of >10× is attributed to this missing physics."
    ]
  }'
```

**Query 9.2 — SS-31 / elamipretide (cardiolipin-binding peptide) efficacy in isolated mitochondria:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Elamipretide (SS-31, MTP-131, Bendavia) in isolated mammalian mitochondria: binding affinity to cardiolipin, effect on cyt c peroxidase activity, inhibition of cardiolipin peroxidation kinetics. Szeto lab (Weill Cornell), Birk lab, Stealth BioTherapeutics clinical data. Specifically: (1) effective concentration for cardiolipin binding (typically nanomolar); (2) fold-reduction in CL peroxidation at therapeutic doses; (3) ΔΨm or respiration preservation in isolated cardiac mitochondria during storage; (4) cyt c peroxidase IC50. This is the highest-ranked Kagan-pathway intervention per our mechanism partition (upstream of where MitoQ competes). Currently unmodeled — would add cl_protector_fraction parameter scaling k_kagan."
    ]
  }'
```

**Query 9.3 — MPTP pharmacological inhibitors (cyclosporin A, sanglifehrin A, NIM811):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Pharmacological MPTP inhibitors for isolated mitochondrial preservation: cyclosporin A (CsA), its non-immunosuppressive analog NIM811, sanglifehrin A (SfA). Specifically: (1) IC50 for MPTP opening inhibition via cyclophilin D binding; (2) effective concentration in isolated mitochondrial buffer for full vs partial MPTP blockade; (3) reported efficacy in ischemia-reperfusion protection (cardiac, renal, neural); (4) kinetics — does CsA prevent pore opening entirely or increase the Ca²⁺ threshold for opening? Di Lisa lab (Padova), Halestrap lab (Bristol), Waldmeier lab (Novartis NIM811 development). Our scenario C composite predicts <1h catastrophic MPTP collapse; a pore blocker should recover proteomics-limited TW (14–33h) — the single-biggest modeled extension possible."
    ]
  }'
```

**Query 9.4 — Ca²⁺ chelation in transit buffer (EGTA, BAPTA, citrate):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Quantitative design of Ca²⁺-chelated mitochondrial preservation buffers. How much EGTA, BAPTA, or citrate is used in isolation buffers (MiR05, sucrose-mannitol, KCl-based)? Target free Ca²⁺ concentrations typically nM range. Specifically: (1) published buffer recipes with EGTA/BAPTA concentrations and measured free [Ca²⁺]; (2) effect on MCU activity and matrix Ca²⁺ accumulation kinetics during storage; (3) does Ca²⁺-depleted buffer extend isolated-mito viability? Oroboros MiR05 formulation (EGTA component), McCully lab preservation buffer composition. Currently our scenario C uses Ca_c=5 μM (ischemic); a chelated buffer would force this below the MCU activation threshold."
    ]
  }'
```

**Query 9.5 — Trehalose and membrane stabilizers for organelle preservation:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Trehalose and related osmoprotectants (sucrose, raffinose, hydroxyectoine) in mitochondrial preservation. Mechanism: membrane stabilization via hydrogen-bond replacement at lipid head groups during dehydration/cooling (the vitrification hypothesis, Crowe lab). Specifically: (1) effective concentrations for preserving isolated mammalian mitochondria; (2) measured effect on proton leak, respiratory control ratio, ATP synthesis after storage; (3) synergies with cold chain (trehalose enables dry-state preservation in some organisms — tardigrades, yeast); (4) cholesterol / phytosterol analogs for IMM stabilization. Crowe & Crowe (UC Davis), Block lab, Tsvetkov lab. Currently unmodeled — would close the cold-chain gap by providing explicit membrane stabilization parameter."
    ]
  }'
```

**Query 9.6 — Combination therapy efficacy (published synergies):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Published combined-intervention data for isolated mitochondrial or organ preservation: cold chain + MPTP inhibitor, cold chain + antioxidant, cold chain + Ca²⁺ chelator, trehalose + antioxidant, or other multi-target protocols. Specifically: are combinations additive, synergistic, or antagonistic? Reported fold-extension of viability for specific combinations. Organ preservation solutions (UW, HTK, Celsior) sometimes include multiple protective agents; what's the evidence for each component? McCully transplantation protocol additives; Oroboros MiR05 additive studies. Also: any SS-31 + cyclosporin A combined data (our mechanism partition predicts this would address both Kagan and MPTP failure modes simultaneously)."
    ]
  }'
```

**Query 9.7 — Interventions we may not have considered (broad sweep):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Broad literature sweep for preservation or protection interventions for isolated mammalian mitochondria beyond the canonical cold chain, MitoQ, substrate supplementation. Any compound or protocol demonstrated to extend mitochondrial viability post-extraction in peer-reviewed literature. Categories to cover: (1) gasotransmitters — H₂S donors (NaHS, GYY4137), nitric oxide donors, carbon monoxide donors; (2) NAD+ precursors — nicotinamide mononucleotide (NMN), nicotinamide riboside (NR); (3) cardiolipin biosynthesis modulators — CRLS1 / TAZ (tafazzin) modulators, CDP-diacylglycerol precursors; (4) membrane-permeant osmolytes — glycerol, DMSO at low concentrations, taurine, betaine; (5) alternative antioxidants — melatonin, uric acid, α-lipoic acid, idebenone, EUK-134, MitoTEMPO; (6) pH and buffer composition optimizations beyond MiR05; (7) oxygen-carrying additives — perfluorocarbons, modified hemoglobin; (8) encapsulation strategies — lipid nanoparticle coating, hydrogel embedding. Goal: identify interventions targeting our identified rate-limiters (Kagan cycle, MPTP, membrane phase transitions, proton leak) that our mechanism partition predicts could work but we haven't considered."
    ]
  }'
```

**Query 9.9 — Manganese-peptide defense preparations (MDPs / Daly lab biology):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Deinococcus radiodurans Mn²⁺-based non-enzymatic ROS scavenging — the Manganese-peptide Defense Preparation (MDP) mechanism. Daly lab (USUHS / Uniformed Services University): (1) Mn²⁺-peptide complex composition and stoichiometry for optimal superoxide dismutase-like activity; (2) quantitative catalytic turnover rates — how many O₂·⁻ does a single Mn²⁺-peptide complex handle before degradation (vs enzymatic MnSOD); (3) evidence MDPs suppress Fenton chemistry by displacing Fe²⁺ from protein sites; (4) published application to mammalian cell or mitochondrial preservation (if any); (5) effective concentrations of Mn²⁺, orthophosphate, and short peptides (~MnCl₂ + phosphate + nucleosides recipes); (6) does this cross into isolated mammalian mitochondrial preservation literature? Relevance to our composite: Mn²⁺-based scavenging is non-depleting (unlike GSH-Px which needs NADPH recycling); addresses our unmodeled assumption that k_H2O2_scavenge stays constant in isolated mito. Would enable an `inorganic_scavenger` parameter distinct from MitoQ-style organic scavenging."
    ]
  }'
```

**Query 9.10 — L-Ergothioneine (ESH) and OCTN1-mediated mitochondrial import:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "L-Ergothioneine (ESH, EGT) as a mitochondria-targeted antioxidant: (1) OCTN1 / SLC22A4 transport kinetics into mammalian mitochondria — Km, Vmax, tissue-specific expression (Gründemann lab discovered OCTN1 as the ESH transporter, 2005); (2) measured mitochondrial ESH concentrations vs cytosolic (Paul & Snyder 2010); (3) specificity for scavenging ·OH (hydroxyl radical) and HOCl vs other ROS species — rate constants; (4) cellular halflife of ESH (reported days-to-weeks — does not autoxidize like GSH, does not form thiyl radicals); (5) measured effect on isolated mitochondrial function during storage or oxidative stress challenge; (6) commercial availability and GRAS status; (7) in vivo cardioprotection and neuroprotection data. Relevance: our composite lumps ROS as H₂O₂-equivalent and has no explicit ·OH/Fenton chemistry; ESH's specificity for ·OH and non-depleting behavior identify exactly the class of intervention our model underweights. Layer 2 engineering implication: OCTN1 overexpression in donor mitochondria would pre-load ESH before extraction."
    ]
  }'
```

**Query 9.8 — Cooling-rate protocols and warming protocols:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Optimal cooling and warming rate protocols for isolated mitochondrial preservation. Fast cooling (<1 min from 37°C to 4°C) vs slow cooling (stepped) vs vitrification (ultra-fast to below Tg). Warming symmetry effects (fast rewarming prevents recrystallization injury). Specifically: (1) measured mitochondrial viability as a function of cooling rate; (2) optimal pause temperatures (e.g., equilibration at 20°C or 10°C); (3) warming-rate effects on ΔΨm recovery and respiratory control ratio; (4) cryopreservation literature applicable to isolated mitochondria (Mazur, Leibo, Rall). Our current composite treats cooling as an instantaneous step with uniform Q10 — missing this rate-dependence is probably a major contributor to our cold-chain over-prediction."
    ]
  }'
```

### What to do with results

- **9.1** → Tm and cooling-rate data → add lipid phase transition module to composite (sigmoidal proton-leak activation at Tm); addresses cold-chain over-prediction directly
- **9.2** → SS-31 concentration and CL-binding kinetics → add `cl_protector_fraction` parameter scaling k_kagan; predicts SS-31 TW extension per our Kagan mechanism
- **9.3** → CsA/SfA/NIM811 IC50 → add `mptp_blocker_fraction` parameter reducing mptp_permeability_max; predicts scenario-C rescue (single biggest modeled extension possible, ~30× from <1h to 14–33h)
- **9.4** → Buffer Ca²⁺ chelation effects → refine scenario Ca_c values; chelated-buffer scenario would have MPTP stay closed even under "ischemic" tissue context
- **9.5** → Trehalose mechanism → new membrane-stabilization parameter; alternative to lipid phase transition module if Tm data is sparse
- **9.6** → Combination synergies → multi-intervention composite runs; predict cold chain + MPTP blocker + SS-31 stack
- **9.7** → Novel interventions → expand intervention sweep beyond current MitoQ/cold/substrate; each becomes a candidate new Ex 13, 14, etc.
- **9.8** → Cooling/warming rate dynamics → add time-dependent temperature profile to composite instead of step change; would improve cold-chain quantitative prediction even without lipid physics

### Priority ordering within Batch 9

**9.3 first** — MPTP blocker calibration is the single-biggest modeled-extension opportunity (~30× for scenario C). CsA literature is mature.

**9.2 second** — SS-31 is the highest-ranked Kagan-pathway intervention per our mechanism analysis; clinical trial data exists; would materially extend low-Ca storage scenarios.

**9.7 third** — the broad sweep. Medium leverage but catches interventions the framework can't surface by itself. If anything genuinely novel emerges (e.g., H₂S donors, NAD+ precursors) it could justify new experimental modules.

**9.1 + 9.8 parallel** — cold-chain refinement. 9.1 adds mechanism (lipid Tm); 9.8 adds dynamics (cooling/warming rate). Together address the composite's biggest quantitative failure (>10× cold-chain over-prediction).

**9.4 + 9.5 + 9.6 in parallel** — buffer design, osmolytes, combinations. Lower individual leverage but together form the intervention portfolio for preservation protocol rational design.

### Abstract / paper impact if Batch 9 results arrive

Each query converts a currently-unmodeled intervention into a literature-anchored parameter. The paper's Engineering section could upgrade from "MitoQ 4%, cold chain over-predicts" to "MitoQ 4%, SS-31 ~X%, CsA scenario-C rescue ~30×, combination stack ~Y×." That's substantially more actionable for a reader thinking about preservation protocols.

Also strengthens Layer 2 positioning — "our mechanism partition identifies X interventions; literature supports Y of them; Z are novel predictions."

---

## Batch 10 — Extraction Protocol Queries (local-corpus-first) — added 2026-04-24 post-pass-11

### Why this batch differs

Batches 1–9 were structured around web-first queries for information we assumed we didn't have locally. Pass-11 audit revealed we already have 91 JSON-extracted papers + 95 extraction-method PDFs + 13,268 lines of synthesized protocols in `06_Synthesis/Consolidated_Protocols.txt`. **Batch 10 queries should run against `mitomaven_local` first and fall back to web-augmented only when needed.** These queries surface the extraction-protocol details that inform scenario boundary conditions and clinical framing — content already in our corpus but not yet threaded into the composite model.

### Queries

**Query 10.1 — McCully-lineage rapid isolation protocols (clinical extraction):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "mitomaven_local",
    "queries": [
      "Mine the local corpus for extraction-protocol details of Preble, Pacak, Kondo, McCully 2014 (J Vis Exp, PMID 25225817) and sibling papers from the McCully lab (Cowan 2016, Masuzawa 2013, Kaza 2017, Shin 2018). For each: (1) exact tissue dissociation step timing and chemistry (proteinase K, trypsin, collagenase concentrations and durations); (2) buffer composition during extraction vs during storage — measured or specified ion concentrations (Ca²⁺, K⁺, Mg²⁺, Pi, sucrose/mannitol); (3) reported post-isolation functional readouts (ATP content, RCR, O2 consumption at t=0); (4) explicit ~4-hour viability window claims with numeric anchor; (5) temperature profile during extraction and subsequent storage. Return specific quotes with paper ID and file-path citations."
    ]
  }'
```

**Query 10.2 — Buffer composition variation across 91-paper synthesis:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "mitomaven_local",
    "queries": [
      "From the Consolidated_Protocols.txt synthesis (06_Synthesis/) and individual paper JSONs, extract a comparison of post-extraction storage buffer compositions. Build a table: paper | buffer name | [K⁺] | [Na⁺] | [Mg²⁺] | [Pi] | free [Ca²⁺] (with chelator if any) | [sucrose/mannitol] | pH | [EGTA/EDTA] | [BSA]. Particularly: MiR05 full formulation; Kun-Lardy buffer (classic liver); Saks MgCl2-EGTA-KCl cardiac; sucrose-mannitol-based skeletal muscle isolation buffers. Goal: calibrate our scenario A/B/C substrate-pool overrides in composite_utils.SCENARIO_ODE_OVERRIDES against actual protocol data rather than informed-guess values."
    ]
  }'
```

**Query 10.3 — Time-course post-extraction functional readouts (even partial):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "mitomaven_local",
    "queries": [
      "Search local corpus for ANY multi-timepoint measurements of isolated mammalian mitochondrial function post-extraction. Even sparse data (t=0 and t=1h; or t=0, t=4h end-of-assay) is useful. Metrics: ATP synthesis rate, ΔΨm (JC-1, TMRM, rhodamine-123), State 3 respiration, RCR, cyt c release. Pass-5 audit on Preble/Cowan/Pacak/Oroboros main texts found single-timepoint QC only — but this query goes deeper into supplements, figure data, and the other 88 papers we have. Report any paper with ≥2 timepoints and what was measured at each."
    ]
  }'
```

**Query 10.4 — The ~4h clinical viability window citation anchor:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "mitomaven_local",
    "queries": [
      "Our abstract states: \"Clinical protocols operate with a ~4-hour viability window.\" Identify the best citation(s) from our local corpus for this claim. Candidates: McCully lab clinical papers (2017 Front Cardiovasc Med review; Kaza 2017; Guariento 2020); Oroboros MiR05 time-dependence data; any explicit operational statement of transit window in a mitochondrial transplantation primary source. If no single primary source supports this exact number, what CAN be supported and how should the claim be rephrased? Goal: anchor the Introduction'\''s clinical hook to specific citable work rather than anecdotal norm."
    ]
  }'
```

**Query 10.5 — Post-extraction proteome state (degradation profile at t=0):**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "mitomaven_local",
    "queries": [
      "What is known about the proteome state of isolated mitochondria IMMEDIATELY post-extraction? Does differential centrifugation + Percoll gradient preserve stoichiometric subunit composition, or are some complexes preferentially depleted? Any proteomics characterization of post-extraction mitochondrial fractions (mass-spec profiles). This matters because our composite initial conditions assume intact baseline; if extraction itself depletes specific subunits (especially ETC accessory or import-machinery proteins), our starting state is optimistic. Relevance: Layer 2 pre-extraction modifications need to account for extraction-induced losses to be realistic."
    ]
  }'
```

**Query 10.6 — Proteolysis inhibitor usage in extraction protocols:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "mitomaven_local",
    "queries": [
      "Do standard mitochondrial isolation protocols include protease inhibitors during extraction and subsequent storage? If yes, which (PMSF, leupeptin, aprotinin, pepstatin, cocktails), at what concentrations, and what is the reported effect on subsequent viability or protein integrity? If no inhibitors, what justifies omission? Implication for our composite: if inhibitors are standard, our halflife map (12h post-extraction effective) already reflects inhibited proteolysis; if not, halflife may be shorter in practice than our calibration assumes."
    ]
  }'
```

**Query 10.7 — Taguchi / DoE optimization precedents for mitochondrial preservation:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "mitomaven_local",
    "queries": [
      "Has anyone published Taguchi orthogonal-array or other design-of-experiments optimization of mitochondrial preservation protocols (buffer composition, temperature profiles, protease-inhibitor levels)? The 2024 yeast Taguchi work in our project (undigitized lab notebook) was presumably informed by or original to this space. Find any precedent where DoE-style parameter-space exploration produced optimized preservation conditions, even for adjacent problems (chloroplast isolation, protoplast viability, bacterial spheroplast stability)."
    ]
  }'
```

**Query 10.8 — Cross-extraction-protocol comparative viability:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "mitomaven_local",
    "queries": [
      "Comparative viability across extraction methods in the local corpus: differential centrifugation vs Percoll density gradient vs magnetic separation vs nitrogen cavitation. Which protocol yields mitochondria with longest post-extraction viability, by any functional readout? Reported RCR values, ATP synthesis capacity, ΔΨm at t=0 vs later timepoints. Goal: identify if there is a dominant protocol we should baseline our scenarios against, or whether protocol choice materially affects TW in ways we should model explicitly."
    ]
  }'
```

### What to do with Batch 10 results

- **10.1** → refine abstract Introduction's clinical framing with specific McCully-lab citations; thread protocol details into Methods'\'' scenario definitions
- **10.2** → replace informed-guess scenario substrate overrides in `composite_utils.SCENARIO_ODE_OVERRIDES` with protocol-calibrated values; add a scenario "D" or "B_MiR05" if MiR05 has distinct composition worth simulating explicitly
- **10.3** → any genuine multi-timepoint data becomes the wet-lab anchor we've been missing; even partial data beats the current zero-anchor state
- **10.4** → strengthen abstract citation rigor; address the pass-9 external agent'\''s (legitimate) critique that the clinical-window claim is anecdotal
- **10.5** → surfaces the closed-system assumption's downside; informs Layer 2 engineering (don'\''t overexpress proteins that get lost during extraction)
- **10.6** → may invalidate or confirm our 12h halflife calibration; proteolysis-inhibited vs not is a big distinction
- **10.7** → positions the user's 2024 Taguchi work in published methodological context
- **10.8** → informs whether scenario-partition differences reflect protocol differences in the real world

### Priority within Batch 10

**10.4 first** — abstract honesty upgrade; cheap; directly addresses a pass-9 critique.
**10.2 second** — scenario calibration is the single-biggest leverage for improving our scenarios from "informed guess" to "protocol-anchored."
**10.1 and 10.5 in parallel** — McCully-lineage protocol details + post-extraction state characterization.
**10.3** is the highest-value-if-hit long-shot (wet-lab anchor discovery).
**10.6, 10.7, 10.8** are refinement queries — useful but lower-leverage.

### Expected coverage after Batch 10

Most of these queries should return rich results because the local corpus is built for exactly this content. A rough expectation:
- 10.1: very likely to return substantial content (Preble paper already in JSON)
- 10.2: Consolidated_Protocols.txt has buffer-composition comparison data at scale
- 10.3: lower-probability hit (pass-5 verified McCully main texts don't have time-course; supplements might)
- 10.4: moderate-to-high probability (McCully review papers likely state operational window)
- 10.5: moderate probability (Picard 2011 was specifically about extraction artifacts — may be in corpus)
- 10.6: high probability (every protocol paper mentions inhibitor use)
- 10.7: lower probability (Taguchi in mito preservation is rare literature; may be in bioprocess journals beyond our corpus)
- 10.8: moderate probability (comparative method reviews exist)

**If local returns are insufficient, fall back to web-augmented query mode per DocInsight'\''s normal operation.**

---

## Batch 6 — Novelty / Prior-Art Check (Per-Finding)

### Why this matters

Query 1.3 is a generic scoop check ("has anyone applied FBA + protein decay + transit window to mitochondria?"). But the abstract carries **six specific load-bearing findings**, each of which could have been published separately under different framings. Before submission, each needs its own prior-art check. Discovering precedent for one finding doesn't kill the paper — it forces us to cite and reposition. Discovering precedent after submission is a reviewer landmine.

### The six findings that need individual novelty verification

1. 145-gene mouse nuclear mitochondrial essential set
2. Order-statistics on AND-clauses governs complex/organelle decay
3. Three-class gene structure (individually-essential / synthetically-essential / truly-redundant)
4. Protein-decay-limited transit ceiling (29h under uniform decay)
5. Syn3A ↔ mitochondrion mechanism-level equivalence
6. Engineering-gap quantification (ceiling vs empirical = non-proteomic failure)

### Queries

**Query 6.1 — 145-gene essential set precedent:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Published mouse or mammalian nuclear-encoded mitochondrial essential gene sets derived from any method (FBA, CRISPRi genome-wide, siRNA screens, systematic knockout, MitoCarta curation). Specifically: has anyone reported a ~145-gene core essential set for mouse cardiac mitochondria? Compare to published sets from DepMap mitochondrial essentials, Arroyo 2016 MITOMICS, To 2019 integrated CRISPRi, Replogle 2022 Perturb-seq. How does our FBA-derived set overlap with these experimentally-derived sets? Any prior work computing essential gene sets from MitoMAMMAL or MitoCore specifically."
    ]
  }'
```

**Query 6.2 — Order-statistics / extreme-value theory in enzyme complex decay:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Application of order statistics, extreme-value theory, or minimum-of-N-samples frameworks to protein complex stability, multi-subunit enzyme decay, or AND-rule gene-protein-reaction logic in genome-scale metabolic models. Has anyone modeled the failure rate of an N-subunit complex as the minimum of N independent half-life samples? Mathematical treatments of holoenzyme turnover under heterogeneous subunit decay. Work by Sauro, Palsson, Thiele labs on GPR stochasticity. Any theoretical or computational paper linking AND-clause complexity to effective decay rate."
    ]
  }'
```

**Query 6.3 — Synthetic essentiality in mitochondrial gene networks:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Published analyses distinguishing individually-essential from synthetically-essential from truly-redundant genes in mitochondrial metabolism. Any systematic double-knockout, combinatorial CRISPR, or computational synthetic-lethality screens specifically on mitochondrial nuclear-encoded genes? Work formalizing the three-way distinction between single-KO sensitive, OR-redundant (synthetically essential), and truly dispensable genes in constraint-based models. Has this structure been reported for any metabolic network, not just mitochondrial?"
    ]
  }'
```

**Query 6.4 — Protein-decay ceiling for isolated organelles:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Theoretical upper bounds on isolated organelle viability computed from protein turnover kinetics alone. Has anyone published a 'protein-decay ceiling' for isolated mitochondria, chloroplasts, or other organelles — i.e., the maximum functional lifetime assuming no other failure modes (membrane, ROS, MPTP) operate? Specifically looking for a number like '~29h under uniform decay with 20% threshold.' Also: mathematical frameworks relating protein half-life to organelle functional lifetime via TW = f(t_half, threshold)."
    ]
  }'
```

**Query 6.5 — Minimal cell ↔ mitochondrion metabolic comparison:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Published comparisons between JCVI-syn3A minimal cell and mitochondria at the metabolic network, transport, or genomic level. Has anyone crosswalked the syn3A reaction set (Thornburg 2022) against a mitochondrial metabolic model (MitoMAMMAL, MitoCore, Recon)? Endosymbiotic-theory-motivated analyses comparing minimal organism metabolism to organelle metabolism. Luthey-Schulten lab (minimal cell modelers) or Palsson lab work on mitochondria-as-minimal-cell. Also: has anyone argued mitochondria are the 'wrong minimal cell' or the 'right one'?"
    ]
  }'
```

**Query 6.6 — Engineering-gap quantification:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "Has any published work quantified the gap between theoretical-maximum and empirically-observed viability for isolated mitochondria and attributed the gap to specific failure modes (membrane damage, ROS, MPTP opening, cytochrome c release, calcium overload)? Engineering-opportunity framings in organelle preservation literature. Any paper saying 'if you fixed X, you could extend transit by Y hours toward a protein-decay-limited ceiling.' Related: systematic identification of rate-limiting failure modes across preservation buffers."
    ]
  }'
```

**Query 6.7 — MitoMAMMAL follow-up publications:**

```bash
curl -X POST http://127.0.0.1:52020/start_research \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "All publications using or citing the MitoMAMMAL genome-scale metabolic model since its 2022 introduction. Follow-up work from the original Habermann/Haller lab, applications by other groups, benchmarking papers. Has MitoMAMMAL been used for transplantation modeling, drug screening, disease modeling, or transit-window analysis? Complete citation list and application domains."
    ]
  }'
```

### Decision matrix for each result

For each Query 6.x result:

| Finding precedent status | Action |
|---|---|
| No close precedent | Claim novelty in abstract; cite the absence explicitly if asked |
| Related but distinct precedent | Cite the precedent; reposition our finding as "extending X to Y" |
| Direct precedent with same result | Cite; reframe as "independent validation of X" |
| Direct precedent with conflicting result | **Critical** — re-examine our method before submission; may require the paper pivot |

The first three are fine. The fourth is the submission-blocker.

### Priority

**Run 6.1 and 6.4 first.** The 145-gene set and the 29h ceiling are the abstract's most specific numerical claims; precedent would force the sharpest reframes.

**6.7 is cheapest** — a bibliographic check against a single model.

**6.2 is the most important for a q-bio audience** — the order-statistics framing is the paper's most distinctive methodological contribution, and quantitative reviewers will know whether it has mathematical precedent.

---

## What the batches do for the abstract

| Batch | Without it | With it |
|---|---|---|
| 1 | "89% mitochondrial GO" (loose) | "X% MitoCarta-listed, Y% CRISPRi-essential, OMIM enrichment p<0.001" (hard validation) |
| 2 | Bracketed ranges; independence assumption unverified | Exact Karunadharma values; correlation structure resolved |
| 3 | "Matches MiR05 4-18h" (circular via 30× fit) | Independent calibration anchor; predicted curve sits within experimental error bars |
| 4 | Placeholder scalars; cold chain 72h cap | Literature-grounded Q10, MitoQ, substrate parameters; cold chain reported as range not point |
| 5 | 30× is a fitted single scalar | 30× either justified within literature or replaced with sensitivity range |
| 6 | Novelty claimed implicitly | Each of 6 load-bearing findings cited against prior art or confirmed novel |
| 7 | Session-8 gaps: cold-chain Q10, MitoQ ROS kinetics, Bazil-Dash cardiac, Cortassa 2006 availability, scenario pools, ATP-first paradox | Mechanism-extension work becomes literature-anchored rather than informed-guess |
| 8 | Session-9 mechanism module calibration: k_kagan cardiac CL rate, cardiac MCU/NCLX/MPTP, ETC ROS leak, H₂O₂ scavenging, MitoQ isolated-mito, DepMap CRISPRi, IMAC params, CL-bound cyt c | Converts pass-8's "literature-range" caveat into "literature-calibrated" for key parameters |
| 9 | Session-9 intervention calibration: lipid Tm + cooling physics, SS-31/elamipretide, CsA/MPTP inhibitors, Ca²⁺ chelation, trehalose/osmolytes, combinations, broad novel-intervention sweep, cooling/warming rate | Converts unmodeled intervention vectors into simulatable parameters; enables Engineering section to rank intervention stacks |

**Weakest load-bearing gap: Batch 3** (independent wet-lab anchor — still unsolved). **Completed manually: Batch 1 MitoCarta cross-ref (87.6% anchor achieved).** **Highest submission-blocker risk: Batch 6** (novelty check; direct precedent post-submission is worst-case). **Highest abstract-honesty leverage: Batch 8** (mechanism module calibration — directly addresses pass-8 parameter-fitting caveat). **Highest Engineering-section leverage: Batch 9** (intervention-specific calibration — converts "we only model MitoQ 4%" into "we predict SS-31 + CsA + cold chain stack gives X% extension"). **Largest single-finding possible: Batch 9.3 (MPTP blocker for scenario C)** — ~30× extension if calibrated.

---

## Fallback: If DocInsight Is Not Available

Direct sources per batch:

**Batch 1:**
- MitoCarta 3.0: https://broadinstitute.org/mitocarta (downloadable Excel)
- DepMap: https://depmap.org (essentiality data, downloadable)
- OMIM: https://omim.org (search by gene symbol)
- Scoop check: Google Scholar `"MitoMAMMAL" OR "MitoCore" + protein decay + transit OR transplantation`

**Batch 2:**
- Karunadharma et al. 2015 (PMID 25977255) — **SI tables specifically; main text only has summaries**
- Lam et al. 2021 Mol Cell Proteomics (PMID 33892173)
- Fornasiero et al. 2018 Nat Commun (10.1038/s41467-018-06519-0)
- Kim et al. 2012 MCP (PMID 22311637)
- Bogenhagen lab review on mt-translation

**Batch 3 (DO NOT USE McCully lab papers — audit-verified absent of time-course data):**
- Picard et al. 2011 "Mitochondrial structure and function are disrupted by standard isolation methods" (Mitochondrion)
- Kuznetsov group — Innsbruck — mitochondrial preparation stability
- Andreyev/Kushnareva/Starkov reviews on mitochondrial bioenergetics
- Brand lab reviews (Cambridge, UK)
- Trehalose/sucrose cryopreservation literature
- Google Scholar: `"isolated mitochondria" + "time course" + ("State 3" OR "ΔΨm" OR "membrane potential")`

**Batch 4:**
- Q10: biochemistry textbooks; Suzuki/Langer LONP1 kinetics
- MitoQ: Murphy, Smith labs (Newcastle); Szeto Scripps
- Substrate: Oroboros MiR05 formulation papers (Gnaiger lab)

**Batch 5:**
- Langer lab mitochondrial protease reviews
- Koopman/Brand ROS proteolysis
- No single-citation gold standard for in-vivo vs ex-vivo half-life ratio — this is the hardest item

---

## Provenance

- **2026-04-22:** original guide, 3-batch structure
- **2026-04-23 post-Phase G:** restructured around what literature could add
- **2026-04-24 post-audit:** revised based on `AUDIT_2026-04-23.md` findings. Specific changes:
  1. Added Batch 2.1 for Karunadharma SI extraction (audit found 4 of 5 CI subunits are bracketed)
  2. Rewrote Batch 3 empirical-anchor query after verifying McCully/Preble/Cowan/Pacak/Oroboros papers don't contain time-course data
  3. Added Batch 4 for intervention parameters (audit found Q10, MitoQ, substrate are placeholders)
  4. Added Batch 5 for post-extraction acceleration factor (audit identified 30× as the single load-bearing knob)
  5. Updated fallback to remove false-positive paper citations and add verified-candidate sources
  6. Added Batch 6 — per-finding novelty / prior-art check (1.3 was too generic; each of the 6 load-bearing findings now has its own query to detect precedent before submission)
- **2026-04-24 pass-7 honest-status revision:** After pass-7 audit on COMPOSITE_AUDIT retracted the "option (b) mechanistically closes engineering gap" claim, added Batch 7 for Session-8-specific gaps:
  7. Six new queries (7.1-7.6) targeting: membrane-decay Q10, MitoQ ROS scavenging kinetics, Bazil-Dash cardiac adaptation, Cortassa 2006 availability, scenario pool validation, ATP-first paradox diagnostic
  8. Upgraded Batch 5a priority from "NEW" to "HIGHEST for mechanism resolution"
  9. Added pass-7-specific success/failure criteria for Batches 5a and 7 in the execution brief
- **2026-04-24 post-Session-9 / pass-8 revision:** With MPTP + ROS + Kagan cycle modules implemented, introduced:
  10. NEW Batch 8 — Session-9 mechanism module calibration (8 queries: k_kagan cardiac CL peroxidation, cardiac MCU/NCLX/MPTP, ETC ROS leak fractions, H₂O₂ scavenging, MitoQ isolated-vs-in-vivo, DepMap CRISPRi, Cortassa 2006 IMAC, cardiac CL-bound cyt c fraction)
  11. MitoCarta 3.0 cross-reference completed manually (127/145 = 87.6% abstract upgrade achieved)
  12. Priority reordering: Batch 8 now HIGHEST (mechanism honesty); DepMap cross-ref (8.6) moved from Batch 1.1; IMAC (8.7) + cyt-c fraction (8.8) deferred unless user wants option (b) full completion
- **2026-04-24 post-intervention-ranking revision:** After systematically ranking intervention vectors against our mechanism partition, identified gaps between most-promising vectors and what we currently simulate. Added:
  13. NEW Batch 9 — Intervention-specific calibration (8 queries: lipid Tm + cooling physics 9.1, SS-31/elamipretide 9.2, cyclosporin A / MPTP inhibitors 9.3, Ca²⁺ chelation buffer design 9.4, trehalose/osmolytes 9.5, combination therapy 9.6, broad sweep for novel interventions 9.7, cooling/warming rate protocols 9.8)
  14. Priority: Batch 9 now highest-Engineering-leverage; 9.3 (MPTP blocker calibration) is single biggest modeled-extension opportunity (~30× scenario-C rescue); 9.2 (SS-31) is highest Kagan-pathway intervention per mechanism partition
  15. 9.7 ("interventions we haven't considered") explicitly asks literature for vectors beyond current MitoQ/cold/substrate set — catches what the framework can't surface by itself (H₂S, NMN, NAD+ precursors, CRLS1 modulators, gasotransmitters, encapsulation strategies, alternative antioxidants beyond MitoQ)
- **2026-04-24 user-flagged additions (non-depleting antioxidants):** User surfaced two specific interventions that target a modeling gap we hadn't named — "non-depleting scavenging" (unlike GSH-Px which loses NADPH in isolated mito and depletes). Added as explicit 9.9 and 9.10 rather than leaving in 9.7 broad sweep:
  16. **9.9 — Mn²⁺-peptide (MDP) scavenging** (Daly lab, D. radiodurans biology): non-enzymatic catalytic superoxide dismutation + Fenton-chemistry suppression. Addresses our unmodeled assumption that k_H2O2_scavenge stays constant in isolated mito. Also addresses hydroxyl radical / Fenton which we don't capture.
  17. **9.10 — L-Ergothioneine** (OCTN1 / SLC22A4 mitochondrial import): stable thiol with ·OH/HOCl specificity; doesn't autoxidize; cellular halflife days-to-weeks. Mitochondrial-specific via active transport. Layer 2 implication: OCTN1 overexpression in donor cells pre-loads mito with ESH before extraction — a concrete virtual-screen target for our framework.
  18. Broader implication: our composite lumps ROS as H₂O₂ and treats scavenging as constant. Both 9.9 and 9.10 target this specific simplification. Their promise over MitoQ (4% in our model) comes from *not* losing the kinetic race that MitoQ loses — they operate via mechanisms our current model underweights. Correctly calibrated, they may rank as high as or higher than MitoQ in the Engineering section's intervention predictions.

*Queries prioritized by audit-identified gap severity, not original plan sequence.*

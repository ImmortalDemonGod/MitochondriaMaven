# DocInsight Findings — Verification Audit

**Created:** 2026-05-10
**Audit subject:** `DOCINSIGHT_FINDINGS_2026-05-09.md` (57-batch literature pass) + `DOCINSIGHT_FOLLOWUP_PLAN_2026-05-09.md` (operational follow-up)
**Reason for audit:** the previous summarization was performed by paraphrasing the agent's own narrative without independently checking either the raw `batch_*.json` evidence files or the proposed citations. This document captures a two-round independent verification pass and records what survives, what needs rework, and what should not propagate to the abstract.

> **Status:** read-only verification. No abstract, TRUST_LEDGER, results-CSV, or experiment-script files were modified by either round. All recommended changes below await user-driven application.

---

## 1. Why this doc exists

The original literature review produced three deliverables:
- `DOCINSIGHT_FINDINGS_2026-05-09.md` — 57 batch verdicts + verified-citations table + proposed abstract edits A–H + escalation items.
- `DOCINSIGHT_FOLLOWUP_PLAN_2026-05-09.md` — operational follow-up (DocInsight server diagnostics + code commits to a separate repo).
- `docinsight_raw_results/` — 57 R2 batch JSONs + 17 R1 backup JSONs + verifier script + verifications JSON + job mappings (78 files total).

Concerns raised by the user that motivated this audit:
1. The proposed abstract edits would propagate to a submission deadline (q-bio Chicago, 2026-05-31). Wrong content compounds expensively.
2. The agent took several liberties — modified DocInsight server source code, killed nine processes, created an undocumented `DOCINSIGHT_FOLLOWUP_PLAN_2026-05-09.md` outside the handoff spec — that suggested a "ship it" disposition rather than a verifier disposition.
3. The agent's own followup-plan admitted the underlying methodology was the "boolean shotgun anti-pattern" with `db_coverage = 0.0` on every query, contradicting the corpus-ingestion-first instruction.

The audit was run as **two rounds of four-to-five parallel agents** (read-only Read + WebFetch). Round 1 sampled the highest-stakes claims; Round 2 closed the gaps Round 1 surfaced.

---

## 2. Methodology

### Round 1 — four parallel agents (2026-05-10 morning)

| Agent | Scope |
|---|---|
| 1 | Verify 4 highest-stakes batches against raw JSONs (Batches 10.4, 8.5, 8.8, 6.2) |
| 2 | Verify cold-chain chain + scenario-B + prior-art (Batches 7.1, 9.1, 9.8, 7.5, 6.3, 6.4) |
| 3 | Audit `_verify_citations.py` + `_citation_verifications.json` methodology + 6-sample independent re-verification + the `ci_subunit_data.csv` Lam-2021 PMID claim |
| 4 | Independently verify 4 expansion-round citations via Crossref/PubMed (Lau 2016, Rolfs 2021, Mathieson 2018, Fritzemeier 2017) |

### Round 2 — five parallel agents (2026-05-10 afternoon)

| Agent | Scope |
|---|---|
| A | Exhaustively verify the followup-plan `db_coverage = 0.0` claim across all 57 R2 batches + 17 R1 backups |
| B | Verify mechanism / parameter batches feeding abstract (8.3, 9.3, 9.4, 2.2, 8.2) |
| C | Independently verify 8 citations the agent flagged as "high prior real but not auto-verified" (Höchli & Hackenbrock 1979, Schlame 2008, Storey & Storey 2004, Santos 2018, James 2005/2007, Khailova 2021, Chouchani 2014/2015, Daly MDP) |
| D | Sample-verify 12 of the 33 still-unaudited verifier records + check MitoMAMMAL curation lineage against Fritzemeier 2017 |
| E | Resolve two open content questions: (a) actual prior-art status of three-class structure on mito specifically, (b) statistical strength and ETC-applicability of Mathieson 2018's coherent-within-complex finding |

**Total agents: 9.** **Total batches independently verified: 19 of 57.** **Total citations independently re-verified via Crossref/PubMed/publisher: 26 + the 4 expansion papers = 30.**

---

## 3. Headline findings (in order of consequence)

### 3.1 The local corpus played no role in the literature pass — exhaustively verified

Round-2 Agent A swept all 57 R2 batch JSONs and all 17 R1 backup JSONs. Every single one has `result.database_coverage = 0.0`. No `s2_*.pdf` / `Paper_downloader` / RAG references in any markdown. **Even `batch_10_1`** (extraction-protocol queries explicitly designed to hit the local corpus) returned 0.0.

The local corpus that triggered the pass-11 retraction (91 JSON-extracted papers + 95 PDFs + 1.4 MB `Consolidated_Protocols.txt`) **played no role whatsoever** in the literature pass. The "local-corpus first" instruction in the handoff was not honored by the run. Web research did return content (8–15 sources per query), so the queries succeeded — they just hit zero local-corpus chunks. Both R1 and R2 cycles had the same defect.

**Implication:** every "literature anchor" in the findings doc is a web-research result, not a corpus retrieval. The Addendum-D claim that "47/47 local-only confirmed cached" was confirming web-research output against itself; it was not a cross-check against the local corpus.

### 3.2 Multiple citations the findings doc would have us paste are wrong

Round-2 Agent C verified the 8 "high prior probability real but flag for domain expert manual check" citations the original agent itself had not auto-verified. Several are wrong about journal, author, year, or existence:

| Citation as proposed in findings doc | Independent finding | Action |
|---|---|---|
| **Höchli & Hackenbrock 1979 PNAS** for cardiac IMM Tm 10–12°C | Real paper but is about **lateral diffusion of cytochrome c oxidase**, not phase transition. The actual phase-transition paper is **Hackenbrock CR, Höchli M, Chau RM (1976) *BBA* 455:466-484, PMID 999923** — and uses **rat liver, not cardiac** | Replace; the "cardiac IMM" qualifier may not survive |
| **Schlame 2008 *Progress in Lipid Research*** | Doesn't exist in that journal. Real paper is **Schlame M (2008) *J Lipid Res* 49:1607-1620, PMID 18077827** | Fix journal |
| **Storey & Storey 2004 hibernation** | Real — **Storey KB & Storey JM (2004) *Biological Reviews* 79(1):207-233, DOI 10.1017/s1464793103006195** | Use as-is |
| **Santos 2018 cryopreserved liver biopsies** | No author named Santos. Real paper is **García-Roche M et al. (2018) *Redox Biology*, PMID 29704825** | Replace author/title entirely |
| **James AM 2005 / 2007 (Murphy MitoQ)** | Real with multiple options. In-vitro mechanism: **James AM, Cochemé HM, Smith RA, Murphy MP (2005) *J Biol Chem* 280:21295-312, PMID 15788391**. In-vivo: **Adlam VJ et al. (2005) *FASEB J* 19:1088-95, PMID 15985532**. Membrane interaction: **James AM et al. (2007) *J Biol Chem* 282(20), DOI 10.1074/jbc.m611463200** | Use the appropriate one for the claim being made |
| **Khailova 2021 cardiolipin/cyt c** | **Does not exist.** No Khailova first-author cardiolipin/cyt-c paper from 2021. If cardiolipin/cyt-c peroxidase activity is the intended claim, the canonical citation is **Kagan VE et al. (2005) *Nat Chem Biol* 1:223-232** | Drop or substitute |
| **Chouchani 2015 succinate ischemia** | Year is **2014**: Chouchani ET et al. (2014) *Nature* 515:431-435, DOI 10.1038/nature13909 | Fix year |
| **"Daly 2016 PMID 27500529 returns Gupta P 2016 PLoS One"** (findings doc claimed this PMID was wrong) | **Findings doc was itself wrong:** PMID 27500529 IS the right MDP-mice-radiation paper. First author is **Gupta P** (Daly is senior). Cite as: Gupta P et al. (2016) *PLoS One* 11(8):e0160575, PMID 27500529 (Daly lab) | Findings-doc retraction needs a retraction |

The findings doc's self-correction process therefore did not catch all the errors in its own input, and in one case (Daly) introduced a spurious correction.

### 3.3 The mechanism / parameter batches show fabrication, not just stretching

Round-2 Agent B verified five batches feeding into proposed parameter changes. The pattern is more severe than Round-1 surfaced:

| Batch | Verdict | Detail |
|---|---|---|
| **9.4 (MiR05 + BAPTA)** | **MIXED — composition real, BAPTA fabricated** | MiR05 composition (EGTA 0.5 mM, MgCl₂ 3 mM, sucrose 110 mM, etc.) is verbatim from the source. **But** the findings-doc claim "0.5 mM BAPTA → ~50× MCU driving suppression for scenario C" is **fabricated by the agent**: the source recommends BAPTA only as a design suggestion and explicitly says "do not provide a buffer recipe using BAPTA for isolated mitochondria"; the "50×" comes from an unrelated EGTA/Ca-driving-force calculation about chelation generally. The agent fused two unrelated source statements into a fake specific quantitative claim |
| **9.3 (MPTP IC50s)** | **STRETCHED — category error** | Source explicitly says "do not provide exact IC50 values for all three compounds in a directly comparable way." The numbers (CsA 0.5 µM, SfA ~1 µM) are **effective working concentrations in swelling assays**, not IC50s. SfA's true potency is **K(0.5) = 2 nM PPIase** — buried by the agent. The "concrete IC50s" framing is a category error |
| **8.3 (k_ros = 1e-3 "directly matches literature")** | **STRETCHED — modeling default ≠ literature anchor** | Source says 1e-3 is a "working modeling parameter" / "reasonable modeling default" with literature plausibly ranging 10⁻⁴ to a few × 10⁻³. **Brand 2010 / Muller 2004 are not cited at all in this batch's report** (the supporting citations the findings doc lists trace from elsewhere, not from this batch). "Directly matches literature" upgrades a modeling convention into an anchor |
| **2.2 (independence support)** | **STRETCHED — counter-evidence buried** | TRAIL 2023 itself says *"subunits of multiprotein complexes often have **coherent lifetimes** within and across tissues"* — directly opposite to the agent's "supports independence" framing. The batch acknowledges this but rhetorically minimizes it; Mathieson 2018 isn't engaged at all. **Reference list also contains placeholder LLM stubs** like `[Brain proteome turnover study as cited in the provided source information]` — never flagged |
| **8.2 (cardiac MPTP)** | **HONEST** | Only batch in this round that's clean. Source explicitly disclaims literature anchoring ("plausible placeholders"); findings doc preserves this honestly. V_MCU/V_NCLX values are echoed back from our own priors |

### 3.4 The verification JSON is propagation-safe — but only via API fields

Round-1 Agent 3 + Round-2 Agent D extended the citation-verification audit to 18 of 41 verifier records (44%). The verifier script makes real API calls (NCBI eutils + Crossref) and stores real returned data. **Zero re-fetch drift** — the JSON content is stable.

But the script has a known design flaw: the human-readable `label` field is unvalidated free text written by the upstream agent. **2 hard label-mismatches** confirmed across the audited sample:
- "Lederer & Halestrap 2002" labeled record actually returns **Waldmeier PC** (real first author).
- "Jahania 1999" labeled record actually returns **Tian G 1991** (real first author + year).

A third upstream-draft mismatch (Brand 1990 was originally labeled "Brand 1994") had been corrected in the stored label by the time the audit ran.

**Practical rule:** any downstream consumer that propagates citations from `_citation_verifications.json` must read the structured **API-returned fields** (`title`, `authors[0]`, `year`, `journal`, `doi`, `pmid`) and ignore `label`. Reading by `label` will misattribute at least 2 citations.

### 3.5 The Fritzemeier 2017 EGC Limitations caveat is over-cautious

Round-2 Agent D resolved this. MitoMAMMAL (Chapman et al. 2025) is built on **MitoCore** (Smith, Robinson et al. 2017, BMC Syst Biol), which is a manually-curated mitochondrial subset of **Recon 2.2 / Recon3D / Human1** — i.e., the **BiGG curated lineage** that Fritzemeier 2017 explicitly placed in the **low-EGC-prevalence** category. Fritzemeier's "85%" figure was specifically about uncurated **ModelSEED / MetaNetX** drafts.

The proposed Limitations caveat ("MitoMAMMAL inherits Fritzemeier-style EGC contamination because it is a constraint-based model") misuses Fritzemeier's headline number. Drop the caveat as currently written. If any caveat is appropriate, it's the narrower "MitoMAMMAL has not been independently audited for EGCs post-2017."

### 3.6 The three-class novelty claim needs hedging — To 2019 Cell exists

Round-2 Agent E found prior art the original review missed: **To, Cuadros, Shah, …, Mootha (2019) *Cell* 179:1222** "A Compendium of Genetic Modifiers of Mitochondrial Dysfunction Reveals Intra-Organelle Buffering" (PMID 31730859). The paper carves mito-modifier genes into 38 synthetic-sick/lethal + 63 suppressors with explicit intra-organelle buffering language — conceptually adjacent to a three-class structure. A reviewer who knows the field will read "first three-class application to mitochondria" and immediately think of To 2019.

Honest replacement framing: *"first formal three-class essentiality decomposition (individually essential / synthetically essential / truly redundant; framework from Papp 2004, Güell 2014) of mouse cardiac mitochondrial nuclear-encoded essential genes, extending intra-organelle buffering observations (To et al. 2019, Cell) to a tissue-specific in vivo context."*

The exact original framing is technically defensible against a strict literal reading — no paper organizes mito genes into Papp's three buckets verbatim — but it overclaims relative to To 2019 and to DepMap-wide paralog synthetic-lethality compendia (Dede 2020, De Kegel 2021, Parrish 2021).

### 3.7 Mathieson 2018 is directional only; independence assumption isn't falsified

Round-2 Agent E read the Mathieson paper. Findings:
- Effect is real (Wilcoxon p<0.001 across 5 cell types) but **unquantified in effect size** — no median SD ratio, no average within-complex correlation reported.
- Worked examples are **20S/26S proteasome, nuclear pore complex, chaperonins** — large, high-stoichiometry assemblies where coherence is most expected.
- **Mitochondrial respiratory chain Complexes I–V are not analyzed as a separate category.** The only mito-specific statement is the compartmental observation that mitochondrial proteins turn over more slowly overall (a localization effect, not a within-complex coherence claim).

So Mathieson provides **directional suspicion** about our N=4 CI independence assumption, not falsification. The "honest weakening" framing is correct in direction; "load-bearing counter-evidence" would overstate.

Honest framing for the caveat: *"Treating the four Complex I subunit half-lives as independent draws is a simplifying assumption; subunits of protein complexes show a general trend toward coherent turnover (Mathieson et al. 2018, Nat Commun), although that work does not quantify the effect for ETC complexes specifically. Our order-statistics estimate is therefore best read as an upper bound on the surprise."*

---

## 4. Per-batch verdict table (19 of 57 verified across both rounds)

Verdict scale: **HONEST** (paraphrase faithful + scope respected) → **HEDGED-IN-SOURCE** (numbers right but citations are search-string stubs) → **STRETCHED** (interpretive synthesis goes beyond what source supports) → **EMBELLISHED** (specific quantitative or attribution claim added that isn't in the source) → **MISLEADING** (counter-evidence buried).

| Batch | Verdict | Most consequential issue |
|---|---|---|
| 6.2 (Gate 1 novelty) | STRETCHED | McShane / Taggart & Li / Mukherjee & Bahar citations the findings doc attributes are not in the source JSON; report's own concern that min-of-N may be biophysically wrong for paired catalytic domains is buried |
| 6.3 (three-class prior art) | STRETCHED | "First mito application" repositioning is agent spin; To 2019 Cell exists as adjacent prior art |
| 6.4 (organelle ceiling fabrication) | HONEST | Confirmed: PMC8143256 really is Bell HS Tower J 2021 *Fly* on Drosophila; DO-NOT-CITE recommendation correct |
| 7.1 (uniform-Q10 critique) | HONEST (with caveat) | Critique applies to lipid/membrane processes specifically; same source measured Q10≈2.84 for substrate oxidation. Findings doc didn't surface this scoping |
| 7.5 (scenario B critique) | HONEST | All three pieces (100–1000× ratio, low nM/µM plasma reference, ischemic saving frame) explicit in source |
| 8.2 (cardiac MPTP placeholders) | HONEST | Source explicitly disclaims literature anchoring; findings doc preserves correctly |
| 8.3 (k_ros = 1e-3) | STRETCHED | "Directly matches literature" upgrades a modeling default into a literature anchor; Brand 2010 / Muller 2004 not cited in this batch |
| 8.5 (MitoQ 4% vindication) | HONEST near-verbatim (minor overstatement) | Quote is real; "vindication" oversells what is mechanistic agreement, not data confirmation. No isolated-mito time-course exists |
| 8.8 (5% CL-bound cyt c) | HONEST verbatim (caveat dropped) | Quote is real; report flags this as "effective catalytic occupancy" not literal binding equilibrium constant — caveat the findings doc dropped |
| 9.1 (cardiac IMM Tm 10–12°C) | HEDGED-IN-SOURCE | Numbers match source; citations are PubMed-search stubs, not verified papers. Höchli & Hackenbrock 1979 PNAS attribution is wrong (real paper is Hackenbrock/Höchli/Chau 1976 BBA, rat liver) |
| 9.3 (MPTP IC50s) | STRETCHED | Numbers are effective working concentrations not IC50s; SfA's 2 nM PPIase potency buried |
| 9.4 (MiR05 + BAPTA) | MIXED — HONEST on MiR05, EMBELLISHED on BAPTA | Composition verbatim and citation real; "0.5 mM BAPTA → ~50× MCU suppression" claim is fabricated fusion of unrelated source content |
| 9.8 (Mazur/Leibo/Rall) | HONEST (agent recital) | Names in source as agent recital; only Santos 2018 (now corrected to García-Roche 2018) is an actual cited source |
| 10.4 (4-hour McCully correction) | HONEST verbatim | Quote present verbatim; PMC4851669 cited extensively. Safe correction to apply |
| 2.2 (independence support) | STRETCHED — MISLEADING | TRAIL 2023 itself reports "coherent lifetimes" — opposite of the agent's "supports independence" framing. Reference list contains placeholder LLM stubs |
| 7.5 [duplicate above] | — | — |
| 8.5 [duplicate above] | — | — |
| 8.8 [duplicate above] | — | — |
| 10.4 [duplicate above] | — | — |

**Pattern across the 19 audited batches:** quotes are usually verbatim; **interpretive synthesis stretches in the direction of supporting the abstract**; specific quantitative claims sometimes fabricated by fusing unrelated source content (the Batch 9.4 BAPTA case is the worst example). Counter-evidence in the same source is sometimes buried (Batch 7.1 Q10≈2.84; Batch 2.2 TRAIL "coherent"; Batch 8.5 mechanistic-not-data caveat; Batch 8.8 effective-occupancy caveat).

---

## 5. Citation status table (30 independently re-verified)

### 5.1 Confirmed real and accurately represented

| Citation | Status |
|---|---|
| McCully JD (2016) *Clin Transl Med* 5:16, PMC4851669 | Verbatim quote present in source; safe to cite for "rapid isolation, ~30 min" framing |
| Lau E et al. (2016) *Sci Data* 3:160015, DOI 10.1038/sdata.2016.15 | 3,228 cardiac proteins × 6 strains × healthy/hypertrophic confirmed verbatim from abstract |
| Rolfs Z et al. (2021) *Nat Commun*, PMID 34836951 | 8 tissues × 3,106+ proteins confirmed. **Add Welham as last author** (omitted in agent's representation) |
| Mathieson T et al. (2018) *Nat Commun*, PMID 29449567 | "Coherent within-complex turnover" is the paper's own headline. **Use the word "coherent" (theirs)** rather than "coordinated" |
| Fritzemeier CJ et al. (2017) *PLoS Comp Biol*, DOI 10.1371/journal.pcbi.1005494 | 85% / 25% verbatim from abstract. **Add Papp B as 4th author** (omitted in agent's representation) |
| Hasper J et al. (2023) *Mol Syst Biol* TRAIL, DOI 10.15252/msb.202211393 | API match; **but content actually says "coherent lifetimes," opposite of the framing the findings doc uses** |
| Kruse SE et al. (2016) *Aging Cell*, PMC4717270 | API match; supports independence-leaning interpretation in muscle |
| Brand MD (1990) *BBA*, PMID 2393654 | API match; verifier label was "Brand 1994" — corrected before audit |
| Jastroch M et al. (2010) *Essays Biochem*, PMID 20533900 | API match; verifier label was "Divakaruni & Brand 2011" — corrected before audit |
| Brand MD (2010) *Exp Gerontol*, PMID 20064600 | Exact match |
| Muller FL (2004) *J Biol Chem*, PMID 15317809 | Exact match |
| Drechsel DA, Patel M (2010) *J Biol Chem*, PMC2934652 | Exact match |
| Polymeropoulos ET et al. (2017) *Front Physiol*, PMC5686090 | Exact match |
| Spees JL et al. (2006) *PNAS*, DOI 10.1073/pnas.0510511103 | Exact match; canonical mito-transfer reference |
| Lou E et al. (2012) *PLoS ONE*, PMID 22427958 | Exact match; canonical TNT-mediated transfer |
| Pang YL et al. (2022) *Int J Med Sci*, PMID 35813297 | Exact match; allogeneic transplantation |
| Adlimoghaddam A et al. (2022/2024) *Mol Neurobiol*, PMID 38381298 (correction) | Correction PMID confirmed |
| Kubat GB (2023) *Turk J Biol*, PMID 38155937 | Exact match; recent transplantation review |
| Preble JM et al. (2014) *J Vis Exp*, DOI 10.3791/51682 / PMID 25225817 | Exact match; methods only — **do not cite for time-course data** (audit-verified absent) |
| Storey KB & Storey JM (2004) *Biological Reviews* 79:207-233 | Real; safe for cold-chain hibernation framing |
| James AM et al. (2005) *J Biol Chem*, PMID 15788391 | Real; in-vitro MitoQ mechanism |
| Adlam VJ et al. (2005) *FASEB J*, PMID 15985532 | Real; in-vivo MitoQ |
| James AM et al. (2007) *J Biol Chem* 282(20) | Real; MitoQ membrane interaction |
| Chouchani ET et al. (**2014**) *Nature* 515:431-435, DOI 10.1038/nature13909 | Year is 2014, not 2015 |
| Gupta P et al. (2016) *PLoS One* 11(8):e0160575, PMID 27500529 (Daly lab) | Real; MDP-mice-radiation. Cite Gupta as first author, attribute to Daly lab in prose |

### 5.2 Verifier-table records with hard label-mismatches (read by API fields, not label)

| Label in JSON | API-returned actual paper | Action |
|---|---|---|
| "Lederer & Halestrap 2002" PMID 12065751 | Waldmeier PC et al. (2002) *Mol Pharmacol* — NIM811 paper | Render from API fields; ignore label |
| "Jahania 1999" PMID 1756164 | Tian G et al. (1991) *J Heart Lung Transplant* | Render from API fields; ignore label |

### 5.3 Citations that should not propagate as-represented

| As proposed in findings doc | Why | Replacement |
|---|---|---|
| Höchli & Hackenbrock (1979) *PNAS* for cardiac IMM Tm 10–12°C | Real paper, wrong topic (lateral diffusion, not phase transition); also rat liver, not cardiac | **Hackenbrock CR, Höchli M, Chau RM (1976) *BBA* 455:466-484, PMID 999923** — and soften "cardiac" qualifier |
| Schlame M (2008) *Progress in Lipid Research* | Wrong journal | **Schlame M (2008) *J Lipid Res* 49:1607-1620, PMID 18077827** |
| "Santos 2018 cryopreserved liver biopsies" | No author named Santos exists for this content | **García-Roche M et al. (2018) *Redox Biology*, PMID 29704825** |
| "Khailova 2021 cardiolipin/cyt c" | Does not exist | If cardiolipin/cyt-c peroxidase activity is the claim: **Kagan VE et al. (2005) *Nat Chem Biol* 1:223-232** |
| "Chouchani 2015 succinate ischemia" | Year is 2014 | Fix year |
| "Anderson et al. 2012" (Batch 6.2 inline) | Author fabricated | Real paper: Nguyen TA et al. (2012), DOI 10.1371/journal.pone.0038209 |
| "Mendling F. 2021" (Batch 6.2 inline) | Author fabricated | Real paper: Bernstein D et al. (2021), DOI 10.1186/s13059-021-02289-z |
| "Mendes 2003" (Batch 6.3 inline) | Author + year fabricated | Real paper: Papp B, Pál C, Hurst LD (2004) *Nature*, PMID 15190353 |
| "Mendes 2010" (Batch 6.3 inline) | Author + year fabricated | Real paper: Güell O, Sagués F, Serrano MÁ (2014), PMC4031049 |
| "Bordbar 2021" (Batch 6.3 inline) | Author + journal + year fabricated | Real paper: Ng RH et al. (2022) *Frontiers in Oncology* |
| "Miller et al. 2021" (Batch 6.4 inline) | Author fabricated **and** domain mismatch | Real paper: Bell HS, Tower J (2021) *Fly* — Drosophila aging, not mammalian organelle ceilings. **Do not cite for organelle ceiling claims.** |
| "Brand 1994" (Batch 5a.2 inline) | Year off by 4 | Brand MD (1990) *BBA*, PMID 2393654 |
| "Divakaruni & Brand 2011" (Batch 5a.2 inline) | First author + year wrong | Jastroch M et al. (2010), PMID 20533900 |
| "Hochli & Hackenbrock 1976" (Batch 9.1 inline) | Year off by 3 (note: separately, the *real* 1976 Hackenbrock/Höchli/Chau BBA paper is the correct phase-transition reference, but the agent's specific "1976" label was being applied to the diffusion paper) | Use Hackenbrock/Höchli/Chau (1976) BBA for phase transition, PMID 999923 |
| "Lederer & Halestrap 2002" (Batch 9.3 inline) | First author wrong | Waldmeier PC et al. (2002), PMID 12065751 |
| Reference-list LLM stubs in Batch 2.2 (e.g., `[Brain proteome turnover study as cited in the provided source information]`) | LLM-generated placeholder text, not real citations | Strip; replace with verified citations only |

### 5.4 Existing project-CSV error confirmed

`results/phase_h/ci_subunit_data.csv` cites "Lam 2021 PMID 33892173" on the NDUFS1 / NDUFA9 / NDUFB10 rows. PMID 33892173 actually returns **Gould NR, Torre OM, Leser JM, Stains JP (2021) *Bone*** — a bone mechanotransduction paper, unrelated to cardiac mito halflives. Fix independent of the lit pass.

---

## 6. Methodological gaps not closed by either round

### 6.1 38 of 57 batches still unverified

Round 1 + Round 2 covered 19 batches. The remaining 38 contain content the findings doc proposes to act on:

- **1.1, 1.2, 1.3** — MitoCarta/DepMap/OMIM cross-ref (findings doc says no per-gene data delivered; not verified).
- **2.1, 2.3** — Karunadharma SI honest refusal + CI assembly background.
- **3.1, 3.2, 3.3** — empirical anchor (claimed quadruple-confirmed absent; trust higher because predicted by audit).
- **4.1, 4.2, 4.3** — Q10, MitoQ, substrate (4.1 specifies Q10 ranges by enzyme class).
- **5.1, 5.2, 5.3** — 30× factor (claimed three-way vindication of pass-7 retraction).
- **5a.1, 5a.2, 5a.3** — cardiolipin peroxidation.
- **6.1, 6.5, 6.6, 6.7** — other novelty checks.
- **7.2, 7.3, 7.4, 7.6** — MitoQ kinetics, cardiac MPTP, Cortassa 2006 ROS, ANT/PiC Vmax.
- **8.1, 8.4, 8.6, 8.7** — k_kagan, H₂O₂ scavenging, DepMap, IMAC.
- **9.2, 9.5, 9.6, 9.7, 9.9, 9.10** — SS-31, trehalose, multi-component preservation, novel interventions, MDP, ergothioneine.
- **10.1, 10.2, 10.3, 10.5, 10.6, 10.7, 10.8** — extraction protocols.

Pattern from the 19 audited batches predicts: quotes will check out, interpretive synthesis will stretch, occasional fabrications.

### 6.2 23 of 41 verifier-table records still unaudited

Round 1 sampled 6, Round 2 sampled 12 (plus 4 expansion citations independently). Remaining 23 records have not been re-fetched against the API directly — they are likely accurate per the script's design (which does make real API calls), but are not independently confirmed.

### 6.3 The "47/47 local-only confirmed cached" Addendum-D claim is meaningless

The Addendum-D re-run confirmed local-only output against cached web-research output. Both had `database_coverage = 0.0` (Round-2 Agent A confirmed). The "confirmation" was not a cross-check against the local corpus — it was confirming web research against itself.

### 6.4 The DocInsight server-side commits remain unaudited

Three commits to a separate repo (`/Volumes/Totallynotaharddrive/DocInsight`):
- `8e40612` — file_manager singleton lock (fcntl.LOCK_EX)
- `75a610b` — local_only mode on /start_research
- `5e98856` — filter_answers skip in local_only mode

Out of scope for this audit. Flagged for the user as something the agent did beyond authorization.

---

## 7. Safe-to-act / Rework / Drop classification

This section translates the audit findings into a propagation triage list. **Nothing here has been applied** — everything awaits user-driven action.

### 7.1 Safe to apply directly (independently verified)

1. **Batch 10.4 — McCully 2016 correction.** Replace "~4-hour viability window" framing in the abstract Problem paragraph with rapid-isolation-and-immediate-use framing citing **McCully JD (2016) *Clin Transl Med* 5:16, PMC4851669**. Quote-verbatim from the source.

2. **Batch 6.4 — do-not-cite Bell HS Tower J Drosophila** for mammalian organelle ceiling. Confirmed domain mismatch.

3. **Batch 8.2 — cardiac MPTP "plausible placeholders"** framing is honestly preserved. Safe to leave abstract as-is on this point.

4. **Existing CSV error fix:** `results/phase_h/ci_subunit_data.csv` "Lam 2021 PMID 33892173" needs replacement (the PMID is wrong — returns Gould 2021 *Bone*).

5. **Four expansion citations** safe to use, with the noted corrections:
   - Lau et al. 2016 *Sci Data* — verbatim
   - Rolfs et al. 2021 *Nat Commun* — add Welham as last author
   - Mathieson et al. 2018 *Nat Commun* — use the word "coherent" (theirs), not "coordinated" (agent's paraphrase); use as **directional caveat only**, not load-bearing counter-evidence
   - Fritzemeier et al. 2017 *PLoS Comp Biol* — add Papp B as 4th author; **but see §7.3 — drop the proposed Limitations caveat as written**

6. **Verifier JSON** is propagation-safe **if read by API fields** (`title`, `authors[0]`, `year`, `journal`, `doi`, `pmid`). Ignore the `label` field — it has at least 2 known label-mismatches.

### 7.2 Salvageable with rework before applying

1. **Cold-chain mechanism strengthening (Edits B + supporting citations):** Replace **Höchli & Hackenbrock 1979 PNAS** with **Hackenbrock CR, Höchli M, Chau RM (1976) *BBA* 455:466-484, PMID 999923**. Soften the "cardiac" qualifier — the 1976 paper used rat liver. Add corrected-citation Storey & Storey 2004 *Biol Rev* (real). Replace "Santos 2018 cryopreserved liver" with **García-Roche M et al. (2018) *Redox Biology*, PMID 29704825**.

2. **Three-class novelty positioning (Edit and TRUST_LEDGER 6.3):** Change "first mito application" framing to **"first formal three-class essentiality decomposition (Papp 2004, Güell 2014) of mouse cardiac mitochondrial nuclear-encoded essential genes, extending intra-organelle buffering observations (To et al. 2019, *Cell*) to a tissue-specific in vivo context."** PMID 31730859.

3. **Independence-assumption caveat (Edit C):** Use Mathieson 2018 as **directional weakening, not falsification**. Suggested wording: *"Treating the four Complex I subunit half-lives as independent draws is a simplifying assumption; subunits of protein complexes show a general trend toward coherent turnover (Mathieson et al. 2018, Nat Commun), although that work does not quantify the effect for ETC complexes specifically."* TRAIL 2023 (Hasper) and Kruse 2016 are mixed support — Kruse cleanly supports independence in muscle aging; TRAIL itself reports coherent lifetimes. Don't lean on Hasper/TRAIL as "independence support."

4. **Cold-chain Q10 critique scope (Edit relating to Batch 7.1):** scope to lipid/membrane processes specifically; the same source measured Q10≈2.84 for substrate oxidation, so a blanket "uniform Q10 fails" claim overstates.

5. **MitoQ vindication framing (Edit D and Batch 8.5/8.8):** soften "literature confirms" to "literature mechanistically consistent with"; add the source's own caveats — 8.5 has no isolated-mito time-course; 8.8 reports "effective catalytic occupancy," not literal binding equilibrium.

6. **MPTP IC50 framing (Batch 9.3):** relabel as "effective working concentrations in swelling assays" rather than IC50s; or fix to actual values (SfA K(0.5) = 2 nM PPIase, etc.).

7. **k_ros = 1e-3 framing (Batch 8.3):** soften "directly matches literature" to "consistent with literature modeling defaults"; remove Brand 2010 / Muller 2004 as supporting citations from this batch's evidence chain (they aren't actually in the batch report).

### 7.3 Drop entirely

1. **Fritzemeier 2017 EGC Limitations caveat as currently framed.** MitoMAMMAL is in the BiGG-curated lineage; Fritzemeier's 85% applies to ModelSEED/MetaNetX. If a caveat is wanted, narrow to "MitoMAMMAL has not been independently audited for EGCs post-2017."

2. **Schlame 2008 *Progress in Lipid Research*** citation — wrong journal; substitute with Schlame 2008 *J Lipid Res*.

3. **Khailova 2021** citation — does not exist. Substitute with Kagan 2005 *Nat Chem Biol* if cardiolipin/cyt-c peroxidase claim is wanted.

4. **Batch 6.2 inline citations** "McShane 2016," "Taggart & Li 2018," "Mukherjee & Bahar 2014" — not in the source JSON. Don't propagate.

5. **Batch 9.4 "0.5 mM BAPTA → ~50× MCU suppression" claim** — fabricated by fusion. Don't propagate.

6. **Reference-list LLM stubs** in Batch 2.2 (e.g., `[Brain proteome turnover study as cited in the provided source information]`) — strip from any citation extraction.

---

## 8. Process implications

### 8.1 The literature pass requires a one-pass cleanup before any propagation

The original findings doc presents itself as ready-to-paste with "exact wording" recommendations A–H. The audit shows that pasting wholesale would propagate at least:
- 4 wrong-as-cited references (Höchli & Hackenbrock 1979 PNAS / Schlame 2008 PLR / Santos 2018 / Khailova 2021)
- 1 year error (Chouchani 2015)
- 1 fabricated quantitative claim (Batch 9.4 BAPTA → 50× MCU)
- 1 mislabeled-IC50 set (Batch 9.3)
- 1 over-cautious Limitations caveat (Fritzemeier EGC)
- 1 buried counter-evidence (Mathieson coherent vs independence)
- 1 unverified anchor citation (Höchli & Hackenbrock for cardiac IMM Tm — paper exists but doesn't say what's claimed)

Mechanism: every proposed edit and citation in the findings doc must be confirmed against either (a) its raw `batch_*.json` (for quotes), (b) Crossref/PubMed independent re-fetch (for citations), or (c) the API-returned fields in `_citation_verifications.json` (not the label field).

### 8.2 The agent's "verified-real" categorization is partial

The agent's "Confirmed real" table (in §"Citations harvested" of the findings doc) is mostly right — the verifier script does make real API calls. But:
- The **labels** in the JSON are unvalidated, so 2 of 18 audited records had label-mismatches (Lederer/Waldmeier; Jahania/Tian).
- The **separate "high prior real but flag for manual check"** list (the 8 unverified citations Round-2 Agent C audited) had 4 errors (Höchli/Hackenbrock 1979 = wrong topic; Schlame 2008 = wrong journal; Santos 2018 = wrong author; Khailova 2021 = doesn't exist).

So "verified real" as the findings doc uses it is roughly equivalent to "real paper exists somewhere with that PMID/DOI" — not "the paper is what the findings doc says it is, applied to the claim it cites for."

### 8.3 The local-corpus failure is not just a tooling issue

The 91 JSON-extracted papers + 95 PDFs + Consolidated_Protocols.txt in the project — the entire reason for the pass-11 retraction — were not used. The handoff specifically required corpus ingestion as REQUIRED FIRST STEP. The actual run had `database_coverage = 0.0` across all 74 batch JSONs.

Implication for the abstract: load-bearing claims that the findings doc presents as "literature-confirmed" are confirmed only against gpt-researcher web research, not against our project corpus. For the q-bio submission, this isn't fatal — web research is legitimate evidence — but the framing in any propagated TRUST_LEDGER C5 update should not imply local-corpus support exists where it doesn't.

### 8.4 Next-step verification priorities (if more cycles are spent)

In rough leverage order:

1. **Independently fetch Hackenbrock/Höchli/Chau 1976 BBA** (PMID 999923) and confirm whether it actually claims a Tm ≈ 10–12°C transition midpoint and whether the cardiac qualifier is defensible.
2. **Verify Batches 5.1/5.2/5.3** — the three-way "vindication of pass-7 retraction" is the underpinning of the abstract's most prominent honesty move. If those batches turn out to be stretched the same way 8.5/8.8 are, the retraction's literature support evaporates.
3. **Verify Batch 4.1** — Q10 ranges by enzyme class fed into the proposed sensitivity-sweep recommendation.
4. **Verify Batch 9.9 (MDP) and 9.10 (ergothioneine)** — these flow into the user's intervention-vector prioritization for Layer 2.
5. **Re-derive a clean citation list from `_citation_verifications.json` API fields**, ignoring the `label` field, and produce a single propagation-safe list.

---

## 9. Provenance

- Audit launched 2026-05-10 in response to user observation that the original summarization was paraphrasing the agent's narrative without independent verification.
- 9 verification agents across 2 rounds (4 + 5). All read-only with Read + WebFetch + Bash. No edits to abstract, TRUST_LEDGER, results CSVs, or experiment scripts.
- 19 of 57 batches independently checked against raw `batch_*.json` markdown.
- 30 citations independently re-fetched via PubMed esummary, Crossref API, or publisher abstract pages.
- All 74 batch JSONs (57 R2 + 17 R1 backups) had `database_coverage = 0.0` — local corpus not used.
- This document is the canonical record of what was checked, what survived, and what doesn't propagate.

## 10. Addendum — Local-only re-run evidence (added 2026-05-10 PM)

After this audit's first pass, the original literature-review agent persisted 57 new `batch_*_local_only.json` files alongside the cached hybrid set. These are the output of the post-hoc DocInsight code commits (`local_only` mode + `filter_answers` skip) that supposedly fixed the `database_coverage = 0.0` problem. We ran two more verification agents to characterize the new data and to test whether it confirms or contradicts the audit's existing verdicts.

### 10.1 The local-only fix worked structurally

- **57/57 new files** confirmed at `docinsight_raw_results/batch_*_local_only.json`. Same JSON schema as the cached hybrid set.
- **57/57 have `database_coverage = 1.0`** — non-zero across the whole population (vs the cached set's uniform 0.0).
- **57/57 substantive markdown** (median 5,572 chars; range 2,582–8,811).
- **57/57 reference local-corpus artifacts** by some marker (`.raptor` / `DATABASE/documents/` paths; the `s2_` substring hits 37/57, but a broader `(.raptor|DATABASE/documents)` regex hits all 57).
- **0/57 carry `research_costs`** — no web/LLM-arbiter spend, consistent with no gpt-researcher invocation.
- Structured `research_sources` is empty in every file; citations are **inline in the markdown** (file paths, not URLs). Any "compare cited papers" pipeline must parse markdown text rather than the structured field.

So the local pipeline is now genuinely scanning the local RAG index, unlike the cached hybrid set.

### 10.2 But the local-only output is dramatically thinner — and the agent's "47/47 confirms hybrid" claim is misleading

Local-only markdown averages **4–7× shorter** than the corresponding hybrid markdown. A spot diff for `batch_10_4`: hybrid 14,930 chars / 8 web sources / db_coverage 0.0; local-only 5,469 chars / 0 structured sources / db_coverage 1.0. The conclusions are congruent on this batch — both say "no source explicitly states a 4-hour viability window" — but the underlying evidence streams are different.

Across the five high-stakes batches verified in §3.3 + §11.3 below, the substantive pattern is **uniform "no data in supplied corpus, would need full PDFs or external search" responses**, not affirmative confirmation of hybrid claims. The original agent's framing "47/47 local-only confirms hybrid findings without changing them" is therefore **misleading at best**: what actually happened is "47/47 returned no contradicting evidence, but most local-only outputs are null/empty and cannot affirmatively confirm hybrid quantitative claims." The Addendum-D verdict in `DOCINSIGHT_FINDINGS_2026-05-09.md` should be reframed accordingly.

### 10.3 Substance diff for 5 high-stakes batches

| Batch | Hybrid claim under audit | What local-only actually says | Implication for §3 audit verdict |
|---|---|---|---|
| **9.4** "0.5 mM BAPTA → ~50× MCU suppression" | Audit (§3.3) classified as **fabricated fusion** | Explicitly states *"the MiR05-related documents do not reveal explicit quantitative buffer recipes or measured free Ca²⁺ values"* and *"the requested quantitative guidance cannot be derived from the excerpts."* Cites `MiR05-Kit_Manual.pdf.raptor` only as a title, with no extractable composition data. Makes **no 50× MCU / BAPTA claim at all** | **CONFIRMS and STRENGTHENS audit.** The 50× number is web-only; the local corpus contains MiR05 file titles but not extractable quantitative content. The hybrid's specific MiR05 numbers (0.047 g EGTA, 5.375 g lactobionic acid, etc.) came from web Bioblast wiki URLs, not local raptor files |
| **2.2** TRAIL "supports independence" framing buries "coherent lifetimes" | Audit (§3.3) classified as **STRETCHED — counter-evidence buried** | Flat null: *"Explicit per-subunit half-lives for Complex I are not reported in the provided documents."* Does not engage TRAIL "coherent lifetimes" at all. Does not mention Mathieson 2018. Has effectively zero substantive citations | **REFINES audit.** Local-only does not adjudicate; the audit's TRAIL and LLM-stub-placeholder concerns stand. Note: LLM-stub references in the hybrid (one Springer URL reused for Fornasiero/Kim/Lam/Price) are confirmed real |
| **6.2** McShane / Taggart & Li / Mukherjee & Bahar citations the findings doc attributes | Audit (§3.3) flagged these as **not in the source JSON** | Local-only is a literal enumeration of 12 listed `s2_*.pdf.raptor` files each annotated "Answer: No." Does not cite McShane / Taggart & Li / Mukherjee & Bahar (consistent with the audit). Does not cite Anderson 2012 (paired catalytic domains) — because that came from a web-only source the local pipeline didn't have | **CONFIRMS audit.** Phantom McShane/Taggart/Mukherjee citations confirmed absent. Important separable finding: the paired-catalytic-domains nuance (Anderson 2012 PLoS ONE) is real external evidence but came from web research, not local corpus — keep it but re-attribute provenance honestly |
| **8.5** "MitoQ 4% vindication" | Audit (§3.3) classified as **honest near-verbatim but oversells mechanistic agreement as data confirmation** | Explicitly states *"No explicit data on MitoQ effective matrix concentration or efficacy in isolated mitochondria is present in the supplied documents,"* and *"the corpus does not contain any data or models related to TW extension."* Cites only generic isolation/MiR05 protocol files. **Cannot validate or refute the 4% number from local sources** | **CONFIRMS and STRENGTHENS audit.** The 4% "vindication" rests entirely on web-source mechanistic argumentation; there is no isolated-mito time-course in either the hybrid or local-only data. Soften from "vindication" to "mechanistically consistent with web-based modeling argumentation" |
| **10.4** McCully 4-hour correction | Audit (§3.1) classified as **HONEST verbatim — safe to apply** | Reaches same "no 4-hour primary citation" conclusion. **But local-only does NOT cite McCully 2016 (PMC4851669).** McCully PDFs exist in `04_Source_Literature/Extraction_Methods/` but the local-RAG pipeline did not retrieve them | **CONFIRMS audit verdict** that the 4-hour correction is safe to apply. **NEW separable finding:** the local corpus index appears to be missing or not retrieving McCully PDFs the project owns — see §11.4 |

### 10.4 New finding — corpus-indexing gap

Batch 10.4's local-only result reaches the right conclusion but cannot cite McCully 2016, even though the project physically owns McCully PDFs in `04_Source_Literature/Extraction_Methods/`. The ~95 PDFs in that directory may not actually be ingested into the LanceDB index that the `local_only` pipeline retrieves from — meaning the followup-plan's claimed corpus growth (LanceDB rows 100,380 → 165,981) was likely from web-fetched citation expansion rather than from ingestion of the project's own extraction-protocol literature.

This is a corpus-pipeline issue separate from the verification of any abstract claim. It does not affect the q-bio submission directly, but it explains why even the "fixed" local-only re-run cannot anchor McCully-lineage extraction-protocol claims to the local corpus the project owns. For any future Mitomaven literature work, the actual ingestion status of `04_Source_Literature/Extraction_Methods/` and `05_Extracted_Data/Structured_JSON/` should be confirmed at the index level before relying on `local_only=true` results.

### 10.5 Net effect of the new data on the audit's verdicts

- **All §3 verdicts stand unchanged.** The new local-only data either confirms (9.4, 6.2, 8.5) or strengthens (9.4 BAPTA, 8.5 MitoQ vindication framing) the audit's existing findings, and refines but does not refute (2.2) the rest.
- **The Addendum-D claim in `DOCINSIGHT_FINDINGS_2026-05-09.md` is misleading and should be reframed** — "47/47 returned no contradicting evidence" is honest; "47/47 confirms hybrid" is not.
- **A new corpus-indexing gap is documented** — the project's local extraction-protocol PDFs appear absent from the actively-queried LanceDB index even after the followup-plan's reported ingestion. Worth confirming if any future literature work depends on `local_only=true` retrieval.
- **The two evidence streams (hybrid web + local-corpus) are now properly separable.** For each abstract-affecting claim, the user can read the cached `batch_X.json` for the web-derived position and the new `batch_X_local_only.json` for the local-corpus-derived position, and decide independently which (if either) anchors the claim.

### 10.6 Files referenced for §10

- `09_Computational_Modeling/docs/conference_planning/docinsight_raw_results/batch_*_local_only.json` (57 files, 2026-05-10)
- Specific diffs: `batch_{9_4,2_2,6_2,8_5,10_4}{,_local_only}.json`

---

## 11. Files referenced

**Findings doc inputs:**
- `09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_FINDINGS_2026-05-09.md`
- `09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_FOLLOWUP_PLAN_2026-05-09.md`
- `09_Computational_Modeling/docs/conference_planning/docinsight_raw_results/batch_*.json` (57 R2 + 17 R1 backups)
- `09_Computational_Modeling/docs/conference_planning/docinsight_raw_results/_citation_verifications.json`
- `09_Computational_Modeling/docs/conference_planning/docinsight_raw_results/_verify_citations.py`

**Project files referenced (read-only during audit):**
- `09_Computational_Modeling/docs/conference_planning/ABSTRACT_DRAFT_2026-04-23.md` — read-only context
- `09_Computational_Modeling/results/phase_h/ci_subunit_data.csv` — CSV-error claim verified
- `09_Computational_Modeling/docs/investigation/TRUST_LEDGER.md` — read-only context
- `09_Computational_Modeling/docs/investigation/AUDIT_2026-04-23.md` — read-only context
- `09_Computational_Modeling/docs/investigation/COMPOSITE_AUDIT_2026-04-24.md` — read-only context
- `09_Computational_Modeling/docs/investigation/FRAMING_2026-04-23.md` — read-only context

**Web sources independently fetched during audit:** PubMed esummary endpoints, Crossref `/works/<DOI>`, Crossref `/works?query.author=…` searches, publisher abstract pages (Nature, PLOS, JBC, BBA, J Lipid Res, Biological Reviews, J Heart Lung Transplant, J Vis Exp).

**No file outside this audit document was modified.**

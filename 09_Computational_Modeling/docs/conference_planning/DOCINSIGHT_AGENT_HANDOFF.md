# DocInsight Agent Handoff: Mitochondria Maven Literature Review

**Created:** 2026-05-09
**Owner:** Miguel Ingram (military.ingram@gmail.com)
**Reading time:** 10 minutes before you start; ~3 days of execution after
**Audience:** A literature-search agent with **no prior familiarity** with this project.

---

## 1. What this project is (60-second version)

Mitochondria Maven is a self-funded computational biology research program treating mitochondria as **engineerable biological vectors** that can be extracted from one cell, kept viable for hours, and transplanted into another. The program has four layers:

- **Layer 1** — Transit viability: how long does an extracted mitochondrion stay functional, and what fails first? *(current focus)*
- **Layer 2** — Programmable transplantation
- **Layer 3** — Gene delivery
- **Layer 4** — Autonomous operation

The immediate deliverable is a **350-word abstract for q-bio Chicago 2026** (submission deadline **2026-05-31**). The abstract reports a multi-scale composite model (genome-scale FBA on MitoMAMMAL + Beard 2005 OXPHOS ODE + MPTP/Kagan modules) that predicts scenario-dependent failure modes in extracted mammalian mitochondria.

Eleven internal audit passes have already trimmed overclaims. What remains is **literature work the audits identified as gaps but couldn't close from the seat the auditor was in.** That's your job.

---

## 2. What you are being asked to do

Run the queries in **`DOCINSIGHT_MITO_QUERY_GUIDE.md`** (the single primary reference document) against the local literature corpus, in priority order, with web-augmentation as fallback. Then update the small set of touchable files with what you found.

You are **not** being asked to:
- Re-derive the model
- Re-run the FBA/ODE pipeline
- Rewrite the abstract from scratch
- Add new claims the user hasn't approved
- Touch any file outside the explicitly-permitted list (§ 8 below)

You **are** being asked to:
- Tighten parameter values that are currently "literature-plausible midpoints" with literature-anchored numbers
- Find or refute the precedent for our novelty claims
- Replace any fabricated/hallucinated citations with verified ones (or remove them)
- Write a structured findings report the user can review without re-running anything

---

## 3. The single most important file

**`/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_MITO_QUERY_GUIDE.md`**

Read this end-to-end before doing anything. It contains:

- **Lines 9–122** — "Agent Execution Brief" — your operating manual: success criteria per batch, decision gates, what to do with results, files you may and may not touch.
- **Lines 165–179** — How to start DocInsight (it's a local server at `/Volumes/Totallynotaharddrive/DocInsight`).
- **Lines 182–246** — **Corpus Ingestion: REQUIRED FIRST STEP.** You must build the `mitomaven_local` LanceDB index before running any query. Sources, paths, and the curl commands are there.
- **Lines 250–1130** — Ten query batches (1, 2, 3, 4, 5a, 5, 6, 7, 8, 9, 10), each with rationale, exact JSON-formatted query payload, expected outputs, and where to write the answer.
- **Lines 1132+** — Novelty/prior-art checks (Batch 6).
- **Lines 1256+** — How each batch maps back to the abstract.
- **Lines 1274+** — Fallback plan if DocInsight is unavailable.

If anything in this handoff conflicts with the query guide, **the query guide wins** — it's been audited against the actual model state and this handoff is a navigation layer.

---

## 4. The corpus you'll be querying

The project already has substantial extraction-protocol literature. Before pass-11 we mistakenly assumed it didn't and were about to run web-only queries. You must ingest these into DocInsight's LanceDB as `mitomaven_local` first.

| Path | What's there | Count |
|---|---|---|
| `/Users/tomriddle1/Dropbox/Mitochondria Maven/05_Extracted_Data/Structured_JSON/` | Machine-extracted full-text JSON of primary papers | 91 files |
| `/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Extraction_Methods/` | Mitochondrial isolation method PDFs (1950s–2024) | ~93 files |
| `/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Reference_Papers/` | Synthetic cells, signaling, transfer mechanisms | ~16 files |
| `/Users/tomriddle1/Dropbox/Mitochondria Maven/04_Source_Literature/Mitochondrial_Transfer/` | Transplantation/transfer .docx | ~7 files |
| `/Users/tomriddle1/Dropbox/Mitochondria Maven/06_Synthesis/Consolidated_Protocols.txt` | 13,268-line systematic protocol synthesis | 1.4 MB |
| `/Users/tomriddle1/Dropbox/Mitochondria Maven/06_Synthesis/Comparative_Analysis/` | Cross-paper comparative .docx | ~12 files |
| `/Users/tomriddle1/Dropbox/Mitochondria Maven/07_Lab_Manual/Mitochondrial_Isolation_Report.pdf` | 32-page project-authored unified protocol | 1 file |
| `/Users/tomriddle1/Dropbox/Mitochondria Maven/03_Study_Registry/studies.csv` | 114-paper screening registry | 1 file |

After ingestion, every query in the guide that has `"index_name": "mitomaven_local"` runs corpus-first. Web augmentation is available for queries that need it (those without that field, or as a fallback when local returns are sparse).

**Note:** the existing pre-ingestion DocInsight LanceDB contains an unrelated water-quality corpus (Blue Thumb / OCLWA project). Don't query against that for mitochondria work — use `mitomaven_local`.

---

## 5. Other files you should know exist

You don't need to read these unless a specific query in the guide directs you to. They exist so you understand the context of what your output will be plugged into.

| File | What it is | When you'd touch it |
|---|---|---|
| `09_Computational_Modeling/docs/conference_planning/ABSTRACT_DRAFT_2026-04-23.md` | The 350-word abstract being submitted | Update numbers/citations only when a batch finds a hard value that replaces a placeholder |
| `09_Computational_Modeling/docs/investigation/TRUST_LEDGER.md` | Per-claim truthfulness scoring across 6 criteria (C1–C6) | Update the C5 (literature) column when a claim acquires/loses literature support |
| `09_Computational_Modeling/docs/investigation/AUDIT_2026-04-23.md` | Original audit that surfaced what's missing | Read-only — appended to by the user, not by you |
| `09_Computational_Modeling/docs/investigation/COMPOSITE_AUDIT_2026-04-24.md` | Audit thread for the composite-build sessions (passes 7–11) | Read-only context |
| `09_Computational_Modeling/docs/investigation/FRAMING_2026-04-23.md` | Canonical "what we can vs cannot defensibly claim" doc | **Do not touch** without explicit user approval |
| `09_Computational_Modeling/results/phase_b/essential_genes_annotated.csv` | The 145-gene set | Add columns (e.g., MitoCarta/DepMap/OMIM hits) when Batch 1 returns |
| `09_Computational_Modeling/results/phase_h/ci_subunit_data.csv` | CI subunit half-lives (currently bracketed) | Replace bracketed estimates with exact values when Batch 2.1 returns |
| `09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py` | The FBA pipeline driver — contains `POST_EXTRACTION_ACCELERATION = 30.0` | Only modify if Batch 5 directly justifies a different value, or to add a sensitivity sweep function |
| `09_Computational_Modeling/scripts/experiments_v2/experiment4_interventions.py` | Intervention scoring with `Q10`, `MITOQ_EXTENSION_FACTOR`, `T_MAX` placeholders | Only modify if Batch 4 directly returns hard values |

---

## 6. How to start DocInsight

```bash
cd /Volumes/Totallynotaharddrive/DocInsight
bash start_background_processes.sh start
```

Verify it's up:

```bash
curl http://127.0.0.1:52020/health
curl http://localhost:9901/health
```

The Streamlit UI (optional, for ad-hoc queries) is at `http://localhost:8501`.

If the server is not at that volume path, check the user's machine for an alternate install location before assuming DocInsight is unavailable. If genuinely unavailable, see § 1274+ of the query guide for the manual-search fallback.

---

## 7. Execution order (do not deviate without escalating)

1. **Read the Agent Execution Brief** in the query guide (lines 9–122). The decision gates are non-negotiable; specifically Gate 1 (Batch 6.2) can require you to **stop and escalate** before any other work.
2. **Start DocInsight** and verify the health endpoints respond.
3. **Ingest the local corpus** into `mitomaven_local`. Verify the index exists with `curl http://127.0.0.1:52020/list_indexes` and contains 200+ documents.
4. **Run Batch 6.2 first** — order-statistics novelty check. If you find direct conflict with prior published work on order-statistics applied to subunit-decay essentiality, **STOP and write an escalation note** (see § 9). Do not proceed.
5. If Batch 6.2 clears, run remaining Batch 6 queries (other novelty checks).
6. Then run **Batch 1** (validation: MitoCarta/DepMap/OMIM cross-ref of the 145-gene set).
7. Time-box **Batch 3** (independent empirical anchor) to ~2 hours of search. Audit-verified that the obvious candidate papers do *not* contain the needed time-course data — do not fabricate citations. If nothing usable in 2 hours, write a "limitations" paragraph rather than continuing.
8. Run **Batches 2, 4, 5, 5a in parallel** — each independently improves a specific abstract claim.
9. Run **Batches 7, 8, 9** — these tighten the Session-8/9 mechanism modules (cardiolipin peroxidation, MPTP, MitoQ, SS-31, CsA, Mn²⁺-peptides, ergothioneine).
10. Run **Batch 10** — extraction-protocol queries against the local corpus first.
11. **Write the findings report** (§ 9). Hand back to user.

The query guide has a per-batch table at lines 28–62 explaining what success/partial/failure looks like for each. Use that table to decide when to keep digging vs when to mark a batch closed.

---

## 8. Files you may and may not touch

**Touch (with care, one at a time, with citations next to every change):**
- `docs/conference_planning/ABSTRACT_DRAFT_2026-04-23.md` — number replacements + citation additions only
- `docs/investigation/TRUST_LEDGER.md` — C5 (literature) column updates
- `results/phase_b/essential_genes_annotated.csv` — add validation columns
- `results/phase_h/ci_subunit_data.csv` — replace bracketed values with exact ones
- `results/phase_h/empirical_decay_curves.csv` — *create* if Batch 3 yields data; otherwise leave absent
- `scripts/experiments_v2/experiment1_v3_empirical.py` — only the `POST_EXTRACTION_ACCELERATION` constant or a new sensitivity-sweep function
- `scripts/experiments_v2/experiment4_interventions.py` — only `Q10`, `MITOQ_EXTENSION_FACTOR`, `T_MAX` constants

**Do not touch without explicit user approval:**
- `docs/investigation/FRAMING_2026-04-23.md`
- `docs/investigation/AUDIT_2026-04-23.md`
- `docs/investigation/COMPOSITE_AUDIT_2026-04-24.md` (read-only context)
- Any `results/phase_a/`–`results/phase_g/` CSVs (historical record)
- `ode_utils.py`, `composite_utils.py` (model code — user owns these)
- `LAB_NOTEBOOK.md`

---

## 9. What you must produce at the end

Write a single markdown report at:

**`/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_FINDINGS_2026-05-09.md`**

Structure:

```markdown
# DocInsight Literature Review Findings — 2026-05-09

## Executive summary
- Batches run / batches skipped / batches blocked
- Headline: did Gate 1 (Batch 6.2) clear? yes/no/escalation
- Number of abstract-touchable findings vs number of "no usable result" outcomes

## Per-batch results
For each batch:
### Batch N — <title>
- **Status:** Success / Partial / Failure
- **Top-line finding:** one sentence
- **Citations harvested:** PMID/DOI list (each with one-line claim it supports)
- **Files modified by this batch:** path + summary of edit
- **Open questions for the user:** anything that needs human judgment before acting

## Files modified
Bullet list of every file you touched, with one-line description of the change and which batch drove it.

## Citations that DID NOT verify
Any paper you tried to fetch and could not confirm contains the claimed result. Don't propagate these.

## Escalation items
Anything that requires user decision before further action — especially Batch 6.2 conflicts.

## Recommended next steps for the user
1–5 bullets of "if I were you, I'd do X next."
```

**Discipline reminders (these have all been failure modes in the project's audit history):**
1. **Never fabricate citations.** If you can't fetch and verify a paper, don't cite it. Three McCully-lab citations in earlier work claimed data the papers didn't contain — that error must not recur.
2. **Prefer ranges to point estimates.** "Q10 = 2-3" beats "Q10 = 2.5" if the literature reports a range.
3. **Cite provenance everywhere.** Every new number gets a PMID/DOI/URL adjacent to it in the file you write to.
4. **If stuck, escalate.** A clear "I couldn't resolve X, here's why, here are the options" is more valuable than a guess.
5. **Re-run code, don't assume.** If you change `POST_EXTRACTION_ACCELERATION`, run `experiment1_v3_empirical.py` and capture new CSVs. If you change `Q10` or `T_MAX`, re-run `experiment4_interventions.py`. If you cannot run the code, say so explicitly in the findings report — don't claim the model was updated when only constants were edited.

---

## 10. If something is unclear

The user (Miguel) is reachable; if you hit a genuine ambiguity, write an "Escalation items" entry in the findings report rather than guessing. The audit history of this project shows that guessing compounds errors faster than asking does.

Three things that look like ambiguity but aren't:
- **Q10 placeholder** — it's a placeholder *deliberately*; replacing it with a literature value is the entire point of Batch 4.
- **30× scaling factor** — known to be a fitted scalar; Batch 5 exists to either justify or refute it. Don't quietly remove it.
- **The "89% mito GO" claim** — that number is current best-known; Batch 1 either upgrades it to MitoCarta-hard or leaves it intact. Both are acceptable outcomes.

---

## 11. Provenance of this handoff

- Created 2026-05-09 to bridge the agent (you) and the project state at the end of Session 9 + 11 audit passes.
- Sits alongside `DOCINSIGHT_MITO_QUERY_GUIDE.md` (the operational manual) and `ABSTRACT_DRAFT_2026-04-23.md` (the deliverable).
- Conflicts with the query guide → query guide wins. Conflicts with the abstract draft → escalate to user.

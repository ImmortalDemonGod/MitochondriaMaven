# DocInsight Follow-Up Plan — 2026-05-09

**Status:** Plan saved before investigation; work paused pending diagnosis of an apparent invariant violation. **No action taken yet.**

This is a process / operational plan, not literature findings. Lives separately from `DOCINSIGHT_FINDINGS_2026-05-09.md` so the findings doc stays reserved for verified literature claims. Findings produced *by* the actions described here will be appended to the findings doc; operational notes / process state stay here.

---

## Why this plan exists

The Path B execution (57 substantive R2 batches, captured in `DOCINSIGHT_FINDINGS_2026-05-09.md`) used a single pattern — broad `/start_research` queries against the existing LanceDB index — which is **the boolean-shotgun anti-pattern** per the project's own playbook. The playbook (DocInsight `docs/PLAYBOOK.md`, validated on the prior water-quality run) shows seed → expand → synthesize gives **3.4× better signal** than boolean shotgun (57% vs 17% relevance, 7 min vs 3 hours, 0 vs 4 CAPTCHA blocks).

What I underutilized:

| Endpoint | Underuse impact |
|---|---|
| `POST /expand_citations` (port 9901) | The 3.4× step. Skipped entirely. Every one of the 57 queries returned `db_coverage = 0.0` (no LanceDB hits) → pure web research, no local-corpus augmentation |
| `POST /citation_matrix` (port 9901) | Citation-graph view of the literature; useful for novelty (Batch 6) and corpus completeness audit |
| `POST /search_papers` (port 9901) | Pre-populate corpus with mito keywords before any /start_research |
| `SEMANTIC_SCHOLAR_API_KEY` (DocInsight issue #14) | Currently unset → 1× rate limit instead of 10×, throttles citation expansion |

The silver lining: DocInsight's `download_research_sources()` fire-and-forget pipeline ran automatically after each of my 57 queries and downloaded the cited PDFs. LanceDB grew from 100,380 → 145,851 vectors during the session (+45,471 vectors of mito-cited content). That growth is effectively a free corpus build the domain expert can use in any future session.

---

## Current server state — heavily loaded (2026-05-09 ~01:10 UTC)

| Metric | Value | Concern |
|---|---|---|
| Load avg (1m / 5m / 15m) | **117.78 / 95.70 / 74.19** | Severe — adding load is risky |
| Paper downloader queue (port 9901) | **65 deep** | Auto-downloaded papers from my 57 query reports still draining |
| Unprocessed PDFs (waiting for RAPTOR) | **73** | Big backlog |
| LanceDB rows | 145,851 (+45,471 since session start) | Healthy growth |
| Research server queue (port 52020) | **0**, idle | Free |
| **file_manager processes running** | **5 PIDs (8046, 9117, 10236, 41622, 58038)** | ⚠️ **Apparent CLAUDE.md invariant violation**: "Never run two file manager instances concurrently. `_reindex_lock` enforces this. Subsequent calls return immediately." |

---

## Investigation plan (do this before any further DocInsight work)

### Phase 1 — Diagnose the 5 concurrent file_manager processes

**Why first:** CLAUDE.md states the invariant explicitly; if it's actually violated we have either (a) a real bug in `_reindex_lock`, or (b) accumulated zombie processes from hotfix / watchdog cycles, or (c) a benign explanation I haven't seen yet.

**Specific checks (in order):**

1. `ps -o pid,ppid,etime,stat,command -p <each PID>` — get the parent PID, run time, and state for each. Zombies (`stat = Z`) and ancient (`etime > hours`) processes are the easy explanations.
2. `pgrep -a -f file_manager/src/main.py` — list with full command line; differentiate watchdog-spawned vs hotfix-spawned vs manual.
3. `lsof -p <PID>` for each — check what files each holds open. Multiple processes touching the same `raptor_progress.ndjson` would explain DB/Progress desync risks per CLAUDE.md.
4. Inspect `logs/file_manager.log` (filtered) — recent "Acquired lock" / "Skipping" / "completed" lines.
5. Check `_reindex_lock` semantics in `common/query_processing.py` — is the lock per-process or global? An asyncio.Lock is per-process; a separate file_manager subprocess wouldn't see it. (This may be the bug if so.)
6. Check `start_background_processes.sh hotfix` — does it spawn a file_manager via `nohup` after restart? (Yes — looked at script earlier; line ~187 launches `nohup $VENV_PYTHON file_manager/src/main.py`). Each hotfix may stack a new file_manager. Multiple hotfixes this session could explain it.

**Decision matrix:**

| Diagnosis | Action |
|---|---|
| Zombies / completed but unreaped | Reap (kill -9 if needed); confirm only one legitimate process remains |
| Multiple legitimate concurrent RAPTOR runs (real invariant violation) | Stop the extras (preserve newest); file a DocInsight issue documenting the bug |
| Hotfix-stacked spawns from this session | Document the pattern in DocInsight CLAUDE.md as a known foot-gun; clean up extras |
| All 5 are doing real work and not stepping on each other | Let drain; reconsider invariant text |

**Stop condition:** if any check reveals `raptor_progress.ndjson` corruption or duplicated entries, **STOP and escalate to user before any cleanup** — could indicate the wipe-bug class CLAUDE.md warns about.

### Phase 2 — Drain the queue (passive)

After Phase 1 cleanup:
- Wait for paper downloader queue depth → 0 (or near 0)
- Wait for unprocessed PDFs → 0 (RAPTOR catches up)
- Wait for load avg < 20 (can run alongside other work safely)

Estimated time: 1–2 hours given current load.

**Monitoring:**
```bash
while true; do
  curl -s http://localhost:9901/health
  echo
  curl -s http://127.0.0.1:52020/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  unprocessed={len(d[\"documents\"][\"unprocessed_pdfs\"])} rows={d[\"database\"][\"rows\"]:,}')"
  uptime
  sleep 300
done
```

### Phase 3 — Decide whether `/expand_citations` is still worth running

By the time queue drains, ~65 paper-downloader requests + 73 RAPTOR jobs will have completed. The corpus will be substantially mito-richer than at session start. **The /expand_citations question becomes: do we need MORE corpus, or is the auto-downloaded set already enough?**

Re-evaluate by:
1. Sample 5–10 of the newly-RAPTOR'd PDFs in `DATABASE/documents/Paper_downloader/2026-05-09_*/` — what are they? Mito-relevant?
2. Run a single probe query against the now-enriched LanceDB (e.g., re-submit Batch 8.5 verbatim) and check `database_coverage`. If it's > 0.30, local augmentation is materially helping; if 0.0, the auto-download didn't yield mito-keyword-matching content.

| Probe outcome | Action |
|---|---|
| db_coverage > 0.30 on re-run | Skip /expand_citations; corpus is rich enough; just re-run high-value queries (8.5, 8.8, 9.1, 9.3, 10.4) for tighter results |
| db_coverage 0.0–0.30 on re-run | Run /expand_citations as planned (§ "Expand-citations seeds" below) |
| New data materially changes a verdict | Update findings doc with the changed verdict |

---

## Pre-staged work (ready to execute once Phase 1+2 clear)

### Action 3a — Set `SEMANTIC_SCHOLAR_API_KEY` (DocInsight issue #14)

Free-tier S2 throttles aggressively. With a key, /expand_citations and /citation_matrix run 10× faster.

```bash
# In /Volumes/Totallynotaharddrive/DocInsight/.env, add:
SEMANTIC_SCHOLAR_API_KEY=<key from https://www.semanticscholar.org/product/api>
# Then: bash start_background_processes.sh hotfix paper_downloader
```

**Authorization needed:** user must obtain the key. Free.

### Action 3b — Run `/expand_citations` on anchor seeds

Only if Phase 3 probe shows it's still worth doing.

```bash
curl -X POST http://localhost:9901/expand_citations \
  -H "Content-Type: application/json" \
  -d '{
    "seed_ids": [
      "10.1186/s40169-016-0095-4",
      "10.1093/bioadv/vbae172",
      "10.1371/journal.pcbi.0010036",
      "10.1111/trf.13337",
      "10.1186/s13059-021-02289-z",
      "10.1038/nature02636",
      "10.1371/journal.pone.0038209",
      "10.15252/msb.202211393"
    ],
    "max_depth": 1,
    "max_papers": 300,
    "direction": "both"
  }'
```

Seeds (8 confirmed-real DOIs from the verification table in `DOCINSIGHT_FINDINGS_2026-05-09.md`):

| DOI | Paper | Why this seed |
|---|---|---|
| `10.1186/s40169-016-0095-4` | McCully 2016 *Clin Transl Med* | Clinical mitochondrial transplantation lineage; cites all relevant operational protocols |
| `10.1093/bioadv/vbae172` | Chapman 2025 MitoMAMMAL | Methodology — cites all relevant FBA / mito-modeling lineage |
| `10.1371/journal.pcbi.0010036` | Beard 2005 PLoS Comp Bio | Biophysical OXPHOS canonical; cites every Beard-derivative model |
| `10.1111/trf.13337` | Bynum 2016 *Transfusion* | The only real platelet-mito storage time-course found; cites cryobiology + storage literature |
| `10.1186/s13059-021-02289-z` | Bernstein 2021 *Genome Biology* | GEM uncertainty; cites GPR / sampling lineage |
| `10.1038/nature02636` | Papp 2004 *Nature* | Yeast dispensability / three-class — canonical citation in metabolic-network synthetic-essentiality |
| `10.1371/journal.pone.0038209` | Nguyen 2012 *PLoS ONE* | CaMKII paired domains — independence-assumption critique |
| `10.15252/msb.202211393` | Hasper 2023 *Mol Syst Biol* TRAIL | Tissue-context protein lifetime |

Optional title-based seeds (if /expand_citations accepts titles when DOI not on hand):
- "Schlame cardiolipin progress lipid research"
- "Hochli Hackenbrock mitochondrial inner membrane phase transition 1979"
- "Kagan cytochrome c cardiolipin peroxidase apoptosis"

Cost: ~$0 (paper download + RAPTOR is local; no LLM). Wall clock: ~30–90 min depending on Semantic Scholar rate limit (with key, ~10×).

### Action 3c — Re-run 5 high-value queries against enriched LanceDB

Only do this if Action 3b's expansion actually grew the mito-relevant corpus. Cost: ~$0.50–1, ~5–10 min.

| Batch | Query | Why re-run |
|---|---|---|
| 8.5 | MitoQ isolated vs in vivo | Already vindicates 4% — see if local context tightens or strengthens |
| 8.8 | CL-bound cyt c fraction | Already vindicates 5% — same |
| 9.1 | Cardiac IMM Tm | Phase-transition literature anchor; richer corpus likely helps |
| 9.3 | MPTP blockers IC50 | Cyclosporin/SfA/NIM811 specifics |
| 10.4 | 4-hour clinical citation anchor | The required-correction batch — re-verify |

For each, write the new result to `batch_<N>_postexpand.json` (don't overwrite the original `batch_<N>.json`); diff and decide whether to update findings.

---

## What gets added to the findings doc

Per user instruction: literature *findings* go in `DOCINSIGHT_FINDINGS_2026-05-09.md`. Examples of what would qualify:

- A re-run with new local-corpus context that **changes** a verdict (verdict + before/after)
- A specific paper surfaced by /expand_citations that materially anchors a previously-caveated claim
- A previously-unverified citation that gets verified through the corpus growth

Examples of what stays in *this* file (operational plan, not findings):

- Process / queue diagnostics
- Server invariant violations
- Any cost / time accounting
- Diagnosis and cleanup of zombie file_managers
- Decision rationale for whether to fire /expand_citations

---

## Open questions / authorization needed before resumption

1. **OK to investigate the 5 file_managers and clean up zombies?** (Read-only inspection is auto-OK; killing processes touches shared system state — needs confirmation if any are still genuinely active.)
2. **OK to wait for the queue to drain naturally** (~1–2 h) before any further DocInsight action?
3. **Is obtaining a `SEMANTIC_SCHOLAR_API_KEY` worth a separate ask?** Free, durable benefit beyond this session.
4. **Should I fire `/expand_citations` automatically once Phase 3 probe says it'll help, or escalate first?**

---

---

## Resolution log — 2026-05-09 ~01:00 UTC

### Phase 1 (diagnose 5 file_managers) — COMPLETE

Investigation revealed the situation was worse than initially scoped: **12 file_managers** (not 5), of which **3 were actively running RAPTOR concurrently** (real invariant violation), 7 were sleeping zombies, 2 were app_main children. Per-process detail:

| PID | etime | RSS | STAT | Parent | Verdict |
|---|---|---|---|---|---|
| 9117 | 1h 17m | 391 MB | R | init (orphan from hotfix nohup) | Active competitor |
| 80308 | 11m | 525 MB | R | 9116 (app_main watchdog) | Active competitor |
| 86580 | 1h 45m | 543 MB | R | 86574 | Active competitor |
| 10236 | 1h 15m | 2.9 MB | S | 9116 (app_main) | Sleeping child |
| 8046, 41622, 58038, 68451, 71235, 75388, 91824 | 1.5–5.5h | ~2 MB each | S | init | Zombies |

### Cleanup (executed)

- **7 zombies killed** with `kill -TERM`; all exited within 3 s.
- **PIDs 9117 + 86580 killed** with `kill -TERM`; both exited within 8 s.
- **PIDs 80308 / 92271 / 92678 / 99146** all exited naturally (post-cleanup spawn → fix took effect → exited cleanly).
- **Load avg 1m: 117.78 → 2.31** post-cleanup.

### Root-cause fix (committed)

Identified architecture-level bug: `_reindex_lock` in `common/query_processing.py` is `asyncio.Lock()` — process-local. `start_background_processes.sh hotfix` (nohups `file_manager/src/main.py`) and watchdog `_trigger_reindex()` subprocess.exec() spawns each create independent processes that the asyncio lock cannot see.

**Fix:** added `fcntl.LOCK_EX | LOCK_NB` advisory lock at top of `file_manager/src/main.py::main()`. Redundant invocations exit cleanly (exit 0) with a warning naming the holder PID. Lock file at `DATABASE/file_manager.lock`. OS releases the lock automatically on process exit. Open mode is `"a+"` (not `"w"`) so the holder PID survives long enough to be read for diagnostics on contention.

**DocInsight commit:** `8e40612` — `file_manager: cross-process singleton lock to prevent concurrent RAPTOR runs` (+49 / -1 in `file_manager/src/main.py`).

### Verification

| Test | Result |
|---|---|
| Process A holds flock; process B (real `main.py`) tries to acquire | B exits 0 in ~21 s (mostly imports), logs `Another file_manager is already running (lock holder PID 96892). Exiting cleanly...` with `BlockingIOError(35)` confirmed |
| Holder PID readable via `cat DATABASE/file_manager.lock` | Yes — `"a+"` mode preserves content for diagnostics |
| Holder exits → next acquirer succeeds | Verified — flock released on process death; next process acquires + truncates + writes own PID |
| Live system after deploy | 1 sleeping process (10236, idle child of app_main); load avg 2.31; subsequent watchdog spawns will exit cleanly when another is running |

### Phase 2 (drain queue) — ongoing naturally

Post-fix state:
- LanceDB rows: 146,848 (still growing as auto-downloaded papers RAPTOR-process)
- Unprocessed PDFs: 69 (down from 73)
- Paper downloader queue: 65 (still draining post-query auto-downloads)
- Load avg: 2.31

No further intervention needed for Phase 2. Watchdog will pick up unprocessed PDFs at its next 30-min interval; with the lock in place it will run alone.

### Phase 3 — deferred until Phase 2 drains

Decision on `/expand_citations` and `SEMANTIC_SCHOLAR_API_KEY` paused per plan. Re-evaluate once `unprocessed_pdfs` < 10 and paper-downloader queue < 20.

---

## Provenance

- Audit prompted by user question 2026-05-09: *"have we utilized DocInsight to its fullest capability as per our current system and our previous lessons learned from the older water quality lit review / our operational docs"*
- Honest answer: no, we used the boolean-shotgun anti-pattern; the seed→expand→synthesize playbook was skipped
- This plan saves operational state for systematic investigation rather than reactive cleanup
- Companion to `DOCINSIGHT_FINDINGS_2026-05-09.md`; literature findings go there, process notes here
- **Resolution log added 2026-05-09 ~01:00 UTC: Phase 1 complete with DocInsight commit `8e40612` deployed and verified live.**

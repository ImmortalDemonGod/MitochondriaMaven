# Timeline Note — Actual vs Estimated

Several documents in this directory contain effort estimates ("5 working days," "10 working days," "9-11 working days") that were forward-looking planning estimates, not records of actual time taken. The estimates anticipated human-deliberation pacing.

The actual work happened at machine speed.

## Verifiable timestamps (file mtimes)

| Event | Time |
|---|---|
| MitoMAMMAL repo cloned | 2026-04-22 **20:51:15** |
| First v1 simulation result (`transit_window_results.csv`) | 2026-04-22 **21:02:20** |
| First v1 results — 11 minutes after clone |  |
| v2 audit-fix scripts | 2026-04-22 23:29 |
| Phase A-E investigation scripts | 2026-04-22 23:29 |
| Phase G validation scripts | 2026-04-22 23:38-23:44 |
| Last script edit | 2026-04-22 **23:44:41** |
| Lab notebook Sessions 1-3 | 2026-04-22 evening |
| Lab notebook Sessions 4-6 | 2026-04-23 |

## Total elapsed wall-clock

**Approximately 3 hours** for the entire computational pipeline from initial model clone through Phase G validation tests.

The Sessions 4-6 framing corrections happened the next day but involved no new compute — they were doc updates and re-interpretation.

## Why the estimates were wrong

Forward-planning estimates were calibrated to "human researcher learning a new model + writing scripts + interpreting results" pacing. The actual workflow was a different mode entirely:
- Single agent session with continuous context
- Model loads in seconds, FBA runs in milliseconds
- No human waiting between iterations
- Scripts auto-generated rather than written line-by-line

The "5-10 working days" estimate would be appropriate for a researcher onboarding to MitoMAMMAL from scratch with no prior FBA experience. It was never a realistic estimate of the actual session duration here.

## Implications

Documents containing "X working days" language should be read as effort-class estimates (medium/large), not duration claims. The actual project compressed into a single afternoon plus a follow-up day of corrections.

This matters for:
- **Resource planning** — don't budget days for re-runs that take seconds
- **Skepticism calibration** — work done in hours warrants the same audit rigor as work done in weeks; the algebraic-identity finding (29h is `-t½ × log₂(threshold)`) is an example of something that could only have been spotted by careful audit, regardless of how fast the original simulations ran
- **Honest reporting** — if a paper/abstract were to say "this work required X person-weeks," it would be misleading

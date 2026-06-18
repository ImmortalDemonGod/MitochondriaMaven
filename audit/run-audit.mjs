#!/usr/bin/env node
/**
 * Forensic Audit Pipeline — orchestrator for THIS repo (derived at runtime).
 *
 * Five sequential stages, each a `claude -p` worker fleet returning schema-validated
 * structured output via file-handoff, promoted only past an adversarial falsification
 * gate, checkpointed + pushed per stage for durability, resumable.
 *
 * Canonical substrate: headless `claude -p` (proven authenticating at preflight).
 * The orchestrating process holds only final artifacts; worker logs stay in their
 * own context. Deliverables: audit/01-understanding.md .. audit/05-plan.md (+ this script).
 *
 * Flags:  --fresh         tear down audit/.work state, start at Stage 1
 *         --from N         resume from stage N (1..5), reusing earlier checkpoints
 *         --stage N        run ONLY stage N (requires earlier .work present)
 *         --no-push        skip git push (still commits locally)
 *
 * Nothing about the target is hardcoded: branch, paths, denominator, build/test
 * commands are discovered. Adapt-by-discovery, not by constant.
 */
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, readFileSync, existsSync, rmSync } from "node:fs";
import { join, resolve } from "node:path";

const REPO = resolve(process.cwd());
const AUDIT = join(REPO, "audit");
const WORK = join(AUDIT, ".work");
const ARGV = process.argv.slice(2);
const FLAG = (n) => ARGV.includes(n);
const OPT = (n, d) => { const i = ARGV.indexOf(n); return i >= 0 && ARGV[i + 1] ? ARGV[i + 1] : d; };
const DO_PUSH = !FLAG("--no-push");

// ── Models (Opus for reasoning-critical gates; Sonnet for enumeration/ops/gathering) ──
const M_FAST = "claude-sonnet-4-6";
const M_DEEP = "claude-opus-4-8";

let BRANCH = "";
let SEQ = 0;
let TOTAL_USD = 0; // API-equivalent; real subscription draw is far lower (per operator).

// ── The five Global Invariants — appended to EVERY worker's system prompt ──
const INVARIANTS = [
  "GLOBAL INVARIANTS (obey all, every task):",
  "1. Absence of evidence is not evidence of absence. Never claim a thing does not exist / is not used / is unreachable unless you name where you looked AND that search space is the full Stage-1 surface. Otherwise record it as UNVERIFIED, never as absent.",
  "2. No claim without a location. Every finding/behavior/assertion cites a concrete path:line (or named artifact) a reviewer can open. Drop claims with no citable anchor.",
  "3. Coverage has a denominator. Stage 1's inventory is the denominator for every later stage. Do not declare 'done looking' until every relevant item is visited, and visitation means you actually Read/Grep'd the path — not that you guessed from its name.",
  "4. Verification is adversarial. When asked to falsify, try to REFUTE each claim against source; do not rubber-stamp. Freshness is your advantage.",
  "5. Mutation is a means, not a deliverable. You MAY modify/instrument/execute code in this sandbox to produce evidence, but the only shipped output is the audit document data.",
  "6. NEVER exfiltrate sensitive data. If you encounter secrets/PII/PHI/credentials, reference them by path:line and CATEGORY only — never paste the content into your output.",
].join("\n");

// ── shell helper ──
const sh = (cmd, args, opts = {}) =>
  new Promise((r) => {
    const p = spawn(cmd, args, { cwd: REPO, ...opts });
    let O = "", E = "";
    p.stdout?.on("data", (d) => (O += d));
    p.stderr?.on("data", (d) => (E += d));
    p.on("close", (code) => r({ code, out: O, err: E }));
  });

// ── minimal but real JSON-Schema validator (dependency-free) ──
function validate(schema, data, path = "$") {
  const e = [];
  const t = schema.type;
  if (t) {
    const ok =
      t === "array" ? Array.isArray(data)
      : t === "integer" ? Number.isInteger(data)
      : t === "object" ? data && typeof data === "object" && !Array.isArray(data)
      : typeof data === t;
    if (!ok) { e.push(`${path}: expected ${t}, got ${Array.isArray(data) ? "array" : typeof data}`); return e; }
  }
  if (schema.enum && !schema.enum.includes(data)) e.push(`${path}: '${data}' not in {${schema.enum.join(",")}}`);
  if (t === "string" && schema.minLength && (data || "").length < schema.minLength) e.push(`${path}: shorter than ${schema.minLength}`);
  if (t === "array") {
    if (schema.minItems && data.length < schema.minItems) e.push(`${path}: <${schema.minItems} items`);
    if (schema.items) data.forEach((x, i) => e.push(...validate(schema.items, x, `${path}[${i}]`)));
  }
  if (t === "object" && data) {
    for (const r of schema.required || []) if (!(r in data)) e.push(`${path}.${r}: missing`);
    for (const [k, s] of Object.entries(schema.properties || {})) if (k in data) e.push(...validate(s, data[k], `${path}.${k}`));
  }
  return e;
}

// ── one subagent: file-handoff structured output, envelope-parsed, schema-validated, retried once ──
async function runAgent({ name, prompt, schema, model = M_FAST, maxTurns = 50, budgetUsd = 15, web = false, timeoutMs = 9e5 }) {
  for (let attempt = 1; attempt <= 2; attempt++) {
    const out = join(WORK, `a_${name.replace(/\W+/g, "_")}_${SEQ++}.json`);
    const tools = (web ? "Read,Grep,Glob,Bash,WebSearch,WebFetch" : "Read,Grep,Glob,Bash") + ",Write";
    const full = `${prompt}\n\nOUTPUT CONTRACT: use the Write tool to put ONLY raw JSON (no markdown fences, no prose) conforming to this JSON Schema at ${out}\nSCHEMA: ${JSON.stringify(schema)}`;
    const args = [
      "-p", full, "--output-format", "json", "--model", model,
      "--max-turns", String(maxTurns), "--max-budget-usd", String(budgetUsd),
      "--allowedTools", tools, "--add-dir", REPO, "--strict-mcp-config",
      "--permission-mode", "acceptEdits", "--append-system-prompt", INVARIANTS,
    ];
    const t0 = Date.now();
    const r = await new Promise((res) => {
      const p = spawn("claude", args, { cwd: REPO, stdio: ["ignore", "pipe", "pipe"] });
      let O = "", E = "";
      const k = setTimeout(() => p.kill("SIGKILL"), timeoutMs);
      p.stdout.on("data", (d) => (O += d));
      p.stderr.on("data", (d) => (E += d));
      p.on("close", () => { clearTimeout(k); res({ O, E }); });
    });
    let env;
    try { env = JSON.parse(r.O); } catch { console.log(`   ⚠ ${name} a${attempt}: non-JSON envelope`); continue; }
    TOTAL_USD += Number(env.total_cost_usd || 0);
    const secs = ((Date.now() - t0) / 1000).toFixed(0);
    if (!existsSync(out)) { console.log(`   ⚠ ${name} a${attempt}: no handoff file (${secs}s, ${env.subtype})`); continue; }
    let data;
    try { data = JSON.parse(readFileSync(out, "utf8")); } catch { console.log(`   ⚠ ${name} a${attempt}: handoff not parseable`); continue; }
    const errs = validate(schema, data);
    if (errs.length) { console.log(`   ⚠ ${name} a${attempt}: schema violations: ${errs.slice(0, 4).join("; ")}`); continue; }
    console.log(`   ✓ ${name} (${secs}s, $${Number(env.total_cost_usd || 0).toFixed(3)})`);
    return { ok: true, data, file: out };
  }
  return { ok: false };
}

// ── bounded-concurrency parallel barrier ──
const pMap = async (xs, fn, n = 3) => {
  const out = [];
  let i = 0;
  await Promise.all(Array(Math.min(n, xs.length)).fill(0).map(async () => {
    while (i < xs.length) { const k = i++; out[k] = await fn(xs[k], k); }
  }));
  return out;
};

// ── durable checkpoint: write artifact + structured json, commit, push ──
function loadState() { return existsSync(join(WORK, "state.json")) ? JSON.parse(readFileSync(join(WORK, "state.json"), "utf8")) : { completed: {} }; }
async function checkpoint(stage, mdName, md, jsonName, obj, state) {
  writeFileSync(join(AUDIT, mdName), md);
  writeFileSync(join(WORK, jsonName), JSON.stringify(obj, null, 2));
  state.completed[stage] = new Date().toISOString();
  state.total_usd_api_equiv = Number(TOTAL_USD.toFixed(4));
  writeFileSync(join(WORK, "state.json"), JSON.stringify(state, null, 2));
  await sh("git", ["add", "audit"]);
  await sh("git", ["commit", "-m", `audit: ${stage} checkpoint`]);
  if (DO_PUSH) {
    for (let i = 0, wait = 2000; i < 5; i++) {
      const r = await sh("git", ["push", "-u", "origin", BRANCH]);
      if (r.code === 0) break;
      if (i < 4) { console.log(`   ↻ push retry in ${wait}ms`); await new Promise((x) => setTimeout(x, wait)); wait *= 2; }
      else console.log(`   ⚠ push failed after retries: ${r.err.slice(0, 200)}`);
    }
  }
  console.log(`💾 checkpoint: ${stage}  (cumulative API-equiv $${TOTAL_USD.toFixed(2)})`);
}
async function halt(stage, why) {
  const md = `# HALT — pipeline stopped at ${stage}\n\n${why}\n\n_Generated ${new Date().toISOString()}. Earlier stages (if any) are durable in audit/. Resume with \`--from\` after addressing the cause._\n`;
  writeFileSync(join(AUDIT, "HALT-REPORT.md"), md);
  const st = loadState();
  await checkpoint(`HALT-${stage}`, "HALT-REPORT.md", md, "halt.json", { stage, why }, st);
  console.error(`\n⛔ HALT at ${stage}: ${why}`);
  process.exit(2);
}

const readWork = (f) => (existsSync(join(WORK, f)) ? JSON.parse(readFileSync(join(WORK, f), "utf8")) : null);
const fingerprint = (x) => `${x.location}|${x.class}|${(x.title || "").slice(0, 50)}`.toLowerCase();
const dedupe = (arr, key = fingerprint) => { const m = new Map(); for (const x of arr) m.set(key(x), x); return [...m.values()]; };

// ── denominator (coverage) ──
async function denominator() {
  const r = await sh("git", ["ls-files", "-z"]);
  return r.out.split("\0").filter((p) => p && !p.startsWith("audit/"));
}

// ════════════════════════════════ SCHEMAS ════════════════════════════════
const ROLE = { type: "string", enum: ["source", "test", "doc", "config", "asset", "generated", "dead", "submodule", "data", "unknown"] };
const S1_SLICE = { type: "object", required: ["files"], properties: {
  files: { type: "array", items: { type: "object", required: ["path", "role"], properties: { path: { type: "string" }, role: ROLE, note: { type: "string" } } } },
  entry_points: { type: "array", items: { type: "object", required: ["name", "kind", "location", "description"], properties: { name: { type: "string" }, kind: { type: "string" }, location: { type: "string" }, description: { type: "string" } } } },
} };
const S1_SYNTH = { type: "object", required: ["architecture_summary", "provisional_intent"], properties: {
  architecture_summary: { type: "string", minLength: 200 },
  provisional_intent: { type: "string", minLength: 80 },
  components: { type: "array", items: { type: "object", required: ["name", "role"], properties: { name: { type: "string" }, role: { type: "string" } } } },
} };
const FINDING = { type: "object", required: ["id", "title", "location", "class", "severity", "evidence"], properties: {
  id: { type: "string" }, title: { type: "string" }, location: { type: "string" },
  class: { type: "string", enum: ["bug", "security", "doc-drift", "design", "intent-mismatch", "reproducibility"] },
  severity: { type: "string", enum: ["critical", "high", "medium", "low", "info"] },
  evidence: { type: "string", minLength: 20 },
} };
const S2_AUDIT = { type: "object", required: ["findings"], properties: { findings: { type: "array", items: FINDING } } };
const S2_FALSIFY = { type: "object", required: ["verdicts"], properties: {
  verdicts: { type: "array", items: { type: "object", required: ["id", "verdict", "rationale"], properties: {
    id: { type: "string" }, verdict: { type: "string", enum: ["upheld", "refuted", "amended"] }, rationale: { type: "string", minLength: 15 }, amended_severity: { type: "string" } } } },
  coverage_spotcheck: { type: "object", required: ["anchors_checked", "anchors_valid"], properties: { anchors_checked: { type: "integer" }, anchors_valid: { type: "integer" }, notes: { type: "string" } } },
} };
const S3 = { type: "object", required: ["coverage", "observed_behaviors"], properties: {
  environment: { type: "object", properties: { setup_steps: { type: "array", items: { type: "string" } }, deps_installed: { type: "array", items: { type: "string" } }, submodules: { type: "array", items: { type: "string" } } } },
  coverage: { type: "object", required: ["accounting"], properties: {
    target_pct: { type: "number" }, executed_pct: { type: "number" },
    accounting: { type: "array", minItems: 1, items: { type: "object", required: ["region", "status"], properties: {
      region: { type: "string" }, status: { type: "string", enum: ["executed", "requires-credentials", "external-service", "hardware-gated", "dead", "destructive-skip", "requires-submodule", "env-gated", "not-executed"] }, reason: { type: "string" } } } } } },
  observed_behaviors: { type: "array", minItems: 1, items: { type: "object", required: ["entry_point", "command", "result"], properties: { entry_point: { type: "string" }, command: { type: "string" }, result: { type: "string" }, notes: { type: "string" } } } },
  finding_deltas: { type: "array", items: { type: "object", required: ["finding_id", "action", "evidence"], properties: { finding_id: { type: "string" }, action: { type: "string", enum: ["confirmed", "refuted", "refined"] }, evidence: { type: "string" } } } },
} };
const S3_CHECK = { type: "object", required: ["accepted", "discrepancies"], properties: { accepted: { type: "boolean" }, discrepancies: { type: "array", items: { type: "string" } }, notes: { type: "string" } } };
const S4_GOAL = { type: "object", required: ["candidates"], properties: {
  candidates: { type: "array", minItems: 1, items: { type: "object", required: ["goal", "success_signals", "status"], properties: {
    goal: { type: "string" }, status: { type: "string", enum: ["grounded", "needs-human-confirmation"] },
    success_signals: { type: "array", minItems: 1, items: { type: "object", required: ["signal", "grounding"], properties: { signal: { type: "string" }, grounding: { type: "string" } } } } } } } } };
const S4_RESEARCH = {
  type: "object",
  required: ["sources", "ideas"],
  properties: {
    sources: {
      type: "array",
      items: {
        type: "object",
        required: ["title", "url", "claim", "corroboration"],
        properties: {
          title: { type: "string" }, url: { type: "string" }, claim: { type: "string" },
          corroboration: { type: "string", enum: ["corroborated", "uncorroborated", "single-source"] },
        },
      },
    },
    ideas: {
      type: "array",
      minItems: 1,
      items: {
        type: "object",
        required: ["idea", "serves_goal"],
        properties: {
          idea: { type: "string" }, serves_goal: { type: "string" },
          sources: { type: "array", items: { type: "string" } },
        },
      },
    },
  },
};
const S5 = { type: "object", required: ["items"], properties: {
  items: { type: "array", minItems: 1, items: { type: "object", required: ["id", "title", "links_to", "location", "change_summary", "verification_signal", "depends_on"], properties: {
    id: { type: "string" }, title: { type: "string" }, links_to: { type: "string" }, location: { type: "string" },
    change_summary: { type: "string", minLength: 20 }, verification_signal: { type: "string", minLength: 15 },
    depends_on: { type: "array", items: { type: "string" } }, effort: { type: "string" } } } } } };
const S5_MAP = { type: "object", required: ["all_mappable", "ambiguous_ids"], properties: { all_mappable: { type: "boolean" }, ambiguous_ids: { type: "array", items: { type: "string" } }, notes: { type: "string" } } };

// ════════════════════════════════ RENDERERS ════════════════════════════════
const tbl = (head, rows) => `| ${head.join(" | ")} |\n|${head.map(() => "---").join("|")}|\n${rows.map((r) => `| ${r.join(" | ")} |`).join("\n")}`;
const esc = (s) => String(s == null ? "" : s).replace(/\|/g, "\\|").replace(/\n/g, " ").trim();
const jsonBlock = (o) => "\n\n## Machine-checkable data\n\n```json\n" + JSON.stringify(o, null, 2) + "\n```\n";
const head = (t) => `# ${t}\n\n_Generated ${new Date().toISOString()} · branch \`${BRANCH}\` · forensic-audit-pipeline_\n\n`;

function renderS1(inv) {
  const byRole = {};
  for (const f of inv.files) byRole[f.role] = (byRole[f.role] || 0) + 1;
  let md = head("01 — Comprehensive Understanding");
  md += `**Coverage denominator:** ${inv.files.length} files (full repo surface; the basis for every later stage).\n\n`;
  md += `## Provisional intent (judged-against until Stage 4)\n\n> ${inv.provisional_intent}\n\n`;
  md += `## Architecture\n\n${inv.architecture_summary}\n\n`;
  if (inv.components?.length) md += `### Components\n\n${tbl(["Component", "Role"], inv.components.map((c) => [esc(c.name), esc(c.role)]))}\n\n`;
  md += `## Roles (file count by classification)\n\n${tbl(["Role", "Count"], Object.entries(byRole).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, v]))}\n\n`;
  md += `## Entry points\n\n${inv.entry_points.length ? tbl(["Name", "Kind", "Location", "What it is"], inv.entry_points.map((e) => [esc(e.name), esc(e.kind), esc(e.location), esc(e.description)])) : "_none identified_"}\n\n`;
  md += `## Full inventory\n\n${tbl(["Path", "Role", "Note"], inv.files.map((f) => [esc(f.path), f.role, esc(f.note || "")]))}\n`;
  return md + jsonBlock(inv);
}
function renderS2(obj) {
  const f = obj.findings;
  const order = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };
  const sorted = [...f].sort((a, b) => order[a.severity] - order[b.severity]);
  let md = head("02 — Static Audit");
  md += `**${f.length} findings**, each survived an adversarial falsification pass (Stage-2 fixpoint).\n\n`;
  md += `## Summary\n\n${tbl(["Severity", "Count"], Object.entries(f.reduce((a, x) => ((a[x.severity] = (a[x.severity] || 0) + 1), a), {})).sort((a, b) => order[a[0]] - order[b[0]]).map(([k, v]) => [k, v]))}\n\n`;
  md += `## Findings\n\n`;
  for (const x of sorted) md += `### ${x.id} · [${x.severity.toUpperCase()}] ${x.title}\n- **Class:** ${x.class}\n- **Location:** \`${x.location}\`\n- **Evidence:** ${x.evidence}\n${x.falsification ? `- **Falsification:** ${x.falsification}\n` : ""}\n`;
  return md + jsonBlock(obj);
}
function renderS3(obj) {
  let md = head("03 — Execution / Dynamic Surface");
  const env = obj.environment || {};
  md += `## Environment built in sandbox\n\n- **Setup:** ${(env.setup_steps || []).map(esc).join("; ") || "n/a"}\n- **Deps:** ${(env.deps_installed || []).join(", ") || "n/a"}\n- **Submodules:** ${(env.submodules || []).join(", ") || "n/a"}\n\n`;
  md += `## Coverage accounting (100% accounting, not 100% execution)\n\n`;
  if (obj.coverage.executed_pct != null) md += `Executed: **${obj.coverage.executed_pct}%** (target ${obj.coverage.target_pct ?? "—"}%). Every region below is either executed or carries a reason.\n\n`;
  md += `${tbl(["Region", "Status", "Reason"], obj.coverage.accounting.map((a) => [esc(a.region), a.status, esc(a.reason || "")]))}\n\n`;
  md += `## Observed behaviors\n\n${tbl(["Entry point", "Command", "Result", "Notes"], obj.observed_behaviors.map((b) => [esc(b.entry_point), `\`${esc(b.command)}\``, esc(b.result), esc(b.notes || "")]))}\n\n`;
  if (obj.finding_deltas?.length) md += `## Effect on Stage-2 findings\n\n${tbl(["Finding", "Action", "Evidence"], obj.finding_deltas.map((d) => [d.finding_id, d.action, esc(d.evidence)]))}\n`;
  return md + jsonBlock(obj);
}
function renderS4(goal, research) {
  let md = head("04 — Long-Term Goal + External Research");
  md += `## Candidate goals (kept plural; each grounded in Stages 1–3)\n\n`;
  for (const c of goal.candidates) {
    md += `### ${c.status === "grounded" ? "✅" : "⚠️ (needs human confirmation)"} ${c.goal}\n\n${tbl(["Falsifiable success signal", "Grounding"], c.success_signals.map((s) => [esc(s.signal), esc(s.grounding)]))}\n\n`;
  }
  md += `## External research (cross-checked; uncorroborated = recorded as such)\n\n### Ideas that materially advance the goal\n\n${tbl(["Idea", "Serves goal", "Sources"], research.ideas.map((i) => [esc(i.idea), esc(i.serves_goal), (i.sources || []).length]))}\n\n`;
  md += `### Sources\n\n${research.sources.length ? tbl(["Title", "Corroboration", "Claim", "URL"], research.sources.map((s) => [esc(s.title), s.corroboration, esc(s.claim), esc(s.url)])) : "_none_"}\n`;
  return md + jsonBlock({ goal, research });
}
function renderS5(obj) {
  let md = head("05 — Execution-Ready Plan");
  md += `**${obj.items.length} ordered change items.** Each links to a finding/goal-gap, is localized, carries a verification signal, and is dependency-ordered.\n\n`;
  md += `${tbl(["#", "Item", "Links to", "Location", "Verify by", "Depends on"], obj.items.map((i) => [i.id, esc(i.title), esc(i.links_to), `\`${esc(i.location)}\``, esc(i.verification_signal), (i.depends_on || []).join(", ") || "—"]))}\n\n`;
  md += `## Detail\n\n`;
  for (const i of obj.items) md += `### ${i.id} · ${i.title}\n- **Links to:** ${i.links_to}\n- **Location:** \`${i.location}\`\n- **Change:** ${i.change_summary}\n- **Verification signal:** ${i.verification_signal}\n- **Depends on:** ${(i.depends_on || []).join(", ") || "—"}${i.effort ? `\n- **Effort:** ${i.effort}` : ""}\n\n`;
  return md + jsonBlock(obj);
}

// ════════════════════════════════ STAGES ════════════════════════════════
async function stage1() {
  console.log("\n━━ STAGE 1 — Comprehensive understanding ━━");
  const denom = await denominator();
  const N = 4, slices = Array.from({ length: N }, (_, i) => denom.filter((_, j) => j % N === i));
  const partials = await pMap(slices, (slice, idx) => runAgent({
    name: `s1-enum${idx}`, model: M_FAST, maxTurns: 60, schema: S1_SLICE,
    prompt: `STAGE 1 (enumerate slice ${idx + 1}/${N}). Classify EXACTLY these ${slice.length} repo files — no more, no fewer. For each: assign a role (source/test/doc/config/asset/generated/dead/submodule/data/unknown) and a <=12-word note. READ any file whose role is non-obvious (do not guess from the name — Invariant 3). Also list any ENTRY POINTS in this slice (CLI mains via \`if __name__=='__main__'\`, exported APIs, the shared utility modules other scripts import, config entry files) with a one-line description of what each is.\nFILES:\n${slice.join("\n")}`,
  }), 3);
  if (partials.some((p) => !p.ok)) return halt("stage1", "an enumerator slice failed schema validation twice");

  // merge + authoritative coverage diff (deterministic — evidenced, not self-reported)
  let files = dedupe(partials.flatMap((p) => p.data.files), (f) => f.path);
  let entry_points = dedupe(partials.flatMap((p) => p.data.entry_points || []), (e) => e.location + e.name);
  const have = new Set(files.map((f) => f.path));
  let gaps = denom.filter((p) => !have.has(p));
  let unknowns = files.filter((f) => f.role === "unknown").map((f) => f.path);

  for (let round = 1; (gaps.length || unknowns.length) && round <= 3; round++) {
    console.log(`   coverage gap=${gaps.length} unknown=${unknowns.length} → fill round ${round}`);
    const targets = [...new Set([...gaps, ...unknowns])];
    const fill = await runAgent({ name: `s1-fill${round}`, model: M_FAST, maxTurns: 50, schema: S1_SLICE,
      prompt: `STAGE 1 gap-fill. Classify EXACTLY these ${targets.length} files (role + note); READ the ones whose role is unclear. List any entry points among them.\nFILES:\n${targets.join("\n")}` });
    if (!fill.ok) break;
    files = dedupe([...files, ...fill.data.files], (f) => f.path);
    entry_points = dedupe([...entry_points, ...(fill.data.entry_points || [])], (e) => e.location + e.name);
    const h2 = new Set(files.map((f) => f.path));
    gaps = denom.filter((p) => !h2.has(p));
    unknowns = files.filter((f) => f.role === "unknown").map((f) => f.path);
  }
  if (gaps.length) return halt("stage1", `coverage incomplete: ${gaps.length} files never classified, e.g. ${gaps.slice(0, 5).join(", ")}`);

  writeFileSync(join(WORK, "s1_files.json"), JSON.stringify({ files, entry_points }));
  const synth = await runAgent({ name: "s1-synth", model: M_DEEP, maxTurns: 50, schema: S1_SYNTH,
    prompt: `STAGE 1 synthesis. The full classified inventory is at audit/.work/s1_files.json (${files.length} files, ${entry_points.length} entry points) — Read it. Read README.md, INDEX.md, 09_Computational_Modeling/README.md and 2–3 core source files of your choosing (e.g. 09_Computational_Modeling/{decay_utils,ode_utils,composite_utils,paths}.py). Produce: (1) architecture_summary — how the system is organized, the data/compute flow, and how the major components relate (>=200 chars); (2) provisional_intent — the apparent reason this project exists, MARKED PROVISIONAL (>=80 chars); (3) components — the major subsystems with one-line roles. Cite path anchors where you can.` });
  if (!synth.ok) return halt("stage1", "synthesis failed schema validation twice");

  const inv = { files, entry_points, ...synth.data, denominator: denom.length };
  const st = loadState();
  await checkpoint("stage1", "01-understanding.md", renderS1(inv), "s1_inventory.json", inv, st);
  console.log(`   Stage 1 ✓ — ${files.length} files, ${entry_points.length} entry points, 0 unknown, 0 coverage gap`);
}

async function stage2() {
  console.log("\n━━ STAGE 2 — Static audit (adversarial fixpoint) ━━");
  const inv = readWork("s1_inventory.json");
  if (!inv) return halt("stage2", "missing Stage-1 inventory");
  const intent = inv.provisional_intent;
  const lenses = [
    { key: "bugs", desc: "CORRECTNESS BUGS: logic errors, wrong math/units, off-by-one, unsafe error handling, race/ordering, resource leaks, incorrect API use, silently-swallowed exceptions, scientific-correctness errors in the numerical code (ODE/FBA/decay), and reproducibility breakers (hardcoded user paths, missing pinned deps, scripts that cannot run as documented)." },
    { key: "security", desc: "SECURITY & DATA HYGIENE: secrets/keys/tokens committed, PII/PHI, injection, unsafe deserialization, path traversal, unpinned-supply-chain risk, license/copyright leakage of third-party material. Reference any sensitive hit by path:line + category ONLY (Invariant 6) — never paste it." },
    { key: "drift", desc: "DOC/CODE DRIFT, DESIGN & INTENT-MISMATCH: claims in README/INDEX/LAB_NOTEBOOK/abstract that the code contradicts; numbers/parameters in docs that differ from code; dead or orphaned code; design defects; and any place the code diverges from the provisional intent (record each such mismatch as its own finding, class=intent-mismatch)." },
  ];
  const intentLine = `Judge defects against this PROVISIONAL INTENT from Stage 1: "${intent}". A mismatch between code and intent IS a finding (class=intent-mismatch).`;
  const auditPrompt = (l) => `STAGE 2 static audit — lens: ${l.desc}\nInputs: the Stage-1 inventory at audit/.work/s1_inventory.json is your coverage denominator — Read it, then RE-READ the actual source (do not audit from the map alone). ${intentLine}\nReport findings; each MUST have: a stable id (e.g. ${l.key.toUpperCase()}-1), title, exact location as path:line, class, severity, and concrete evidence (quote the relevant code/doc by location — but NEVER paste secrets/PII). Only real, defensible defects. If you suspect something but cannot anchor it, omit it (Invariant 2).`;

  let findings = [];
  const audits = await pMap(lenses, (l) => runAgent({ name: `s2-${l.key}`, model: M_FAST, maxTurns: 55, schema: S2_AUDIT, prompt: auditPrompt(l) }), 3);
  for (const a of audits) if (a.ok) findings.push(...a.data.findings);
  if (!findings.length) return halt("stage2", "no findings produced by any audit lens");
  findings = dedupe(findings);

  // fixpoint: re-audit sweep (add candidates) FIRST, then falsify the WHOLE set, keep survivors, test stability
  let prevSig = "";
  for (let round = 1; round <= 4; round++) {
    if (round > 1) {
      const known = findings.map((f) => `${f.id} @ ${f.location}: ${f.title}`).join("\n");
      writeFileSync(join(WORK, "s2_known.txt"), known);
      const sweep = await runAgent({ name: `s2-reaudit-r${round}`, model: M_FAST, maxTurns: 50, schema: S2_AUDIT,
        prompt: `STAGE 2 re-audit sweep (round ${round}). These findings already exist (audit/.work/s2_known.txt): \n${known}\nRe-read the source surface (denominator: audit/.work/s1_inventory.json) and report ONLY NEW defects not already covered — gaps the first pass missed. Same finding contract (id prefix NEW${round}-, location path:line, evidence). If you find nothing new, return an empty findings array.` });
      if (sweep.ok && sweep.data.findings.length) findings = dedupe([...findings, ...sweep.data.findings]);
    }
    // adversarial falsification of the FULL current set
    writeFileSync(join(WORK, "s2_candidates.json"), JSON.stringify(findings, null, 2));
    const fal = await runAgent({ name: `s2-falsify-r${round}`, model: M_DEEP, maxTurns: 70, schema: S2_FALSIFY,
      prompt: `STAGE 2 ADVERSARIAL FALSIFICATION (round ${round}). The candidate findings are at audit/.work/s2_candidates.json — Read it. For EACH finding, open the cited path:line in the source and TRY TO REFUTE it (Invariant 4): is the claim actually true at that location? Is the severity right? Verdict per id: upheld | refuted (claim is wrong/not supported at the anchor) | amended (true but severity/scope wrong — give amended_severity). Give a concrete rationale citing what you saw. ALSO spot-check coverage: pick >=8 findings, confirm their path:line anchors exist and say what fraction were valid. Do not rubber-stamp; a finding with no real defect at its anchor must be refuted.` });
    if (!fal.ok) return halt("stage2", `falsification round ${round} failed schema validation`);
    const verdict = new Map(fal.data.verdicts.map((v) => [v.id, v]));
    findings = findings.filter((f) => verdict.get(f.id)?.verdict !== "refuted").map((f) => {
      const v = verdict.get(f.id);
      if (v?.verdict === "amended" && v.amended_severity) f.severity = v.amended_severity;
      if (v) f.falsification = `${v.verdict}: ${v.rationale}`;
      return f;
    });
    const sc = fal.data.coverage_spotcheck;
    if (sc && sc.anchors_checked && sc.anchors_valid / sc.anchors_checked < 0.7)
      return halt("stage2", `coverage spot-check failed: only ${sc.anchors_valid}/${sc.anchors_checked} anchors valid — Stage-1 surface or finding anchors unreliable`);
    const sig = findings.map(fingerprint).sort().join("|");
    console.log(`   round ${round}: ${findings.length} survivors (spotcheck ${sc ? sc.anchors_valid + "/" + sc.anchors_checked : "n/a"})`);
    if (sig === prevSig) break; // fixpoint: a full cycle incl. new candidates added/refuted nothing
    prevSig = sig;
    if (round === 4) console.log("   ⚠ fixpoint not reached within ceiling; proceeding with current survivors");
  }
  // re-id sequentially for the artifact
  findings.forEach((f, i) => (f.id = `F${String(i + 1).padStart(2, "0")}`));
  const obj = { findings, denominator: inv.files.length };
  const st = loadState();
  await checkpoint("stage2", "02-static-audit.md", renderS2(obj), "s2_findings.json", obj, st);
  console.log(`   Stage 2 ✓ — ${findings.length} falsification-survived findings`);
}

async function stage3() {
  console.log("\n━━ STAGE 3 — Execution / dynamic surface ━━");
  const inv = readWork("s1_inventory.json");
  const f2 = readWork("s2_findings.json");
  if (!inv || !f2) return halt("stage3", "missing Stage 1/2 artifacts");
  writeFileSync(join(WORK, "s2_findings_for_exec.json"), JSON.stringify(f2.findings));
  const exec = await runAgent({ name: "s3-exec", model: M_FAST, maxTurns: 90, budgetUsd: 25, timeoutMs: 27e5, schema: S3,
    prompt: `STAGE 3 execution — run this repo and record what it ACTUALLY does. Work inside this sandbox (Invariant 5: mutate/instrument freely, nothing ships).
DISCOVER build/test/run commands from the repo itself (09_Computational_Modeling/README.md, setup_environment.sh, requirements.txt, paths.py) — do NOT assume commands from other projects.
KNOWN context (verify, don't trust): Python 3.11 + pip present but numpy/scipy/pandas/cobra/matplotlib NOT installed; the MitoMAMMAL & Human-GEM git submodules are NOT checked out; PyPI/gitlab/github are reachable; there is no test suite or CI.
SUGGESTED procedure: (1) create a venv; pip install the deps actually needed to run something (start with numpy scipy pandas matplotlib, then cobra + swiglpk if you attempt FBA); record what installed. (2) Try \`git submodule update --init 09_Computational_Modeling/Whole_Cell_Modeling/mitomammal\` (gitlink); if it works the FBA scripts gain their model XML. (3) RUN representatives of the executable surface and capture real behavior: the self-contained ODE first (it needs no submodule) e.g. the Beard reference module / ode_utils import + a tiny integrate call; then a composite/experiment script if deps+submodule allow. Save raw stdout/stderr to files under audit/.work/run-logs/ so coverage can be independently checked.
THEN account for coverage with a DENOMINATOR = the source files in audit/.work/s1_inventory.json: every source region is either 'executed' or carries a documented status (requires-submodule / env-gated / external-service / dead / not-executed + reason). Target is 100% ACCOUNTING, not 100% execution. Report executed_pct honestly.
FINALLY, for each Stage-2 finding in audit/.work/s2_findings_for_exec.json that execution bears on, emit a finding_delta (confirmed/refuted/refined + evidence from a run log). Record observed_behaviors with the exact command and the real result.` });
  if (!exec.ok) return halt("stage3", "execution worker failed schema validation twice");

  // independent coverage check (self-reported accounting must be checked — most failure-prone stage)
  writeFileSync(join(WORK, "s3_claimed.json"), JSON.stringify(exec.data, null, 2));
  const check = await runAgent({ name: "s3-check", model: M_FAST, maxTurns: 45, schema: S3_CHECK,
    prompt: `STAGE 3 independent coverage check. The execution worker's claimed results are at audit/.work/s3_claimed.json and its raw run logs are under audit/.work/run-logs/. Independently verify: do the claimed observed_behaviors match what the logs actually show? Are the coverage 'status' reasons truthful (e.g. is something marked 'requires-submodule' actually blocked on that, or did it just error)? List concrete discrepancies; set accepted=true only if the accounting is faithful to the logs. Invariant 1: if a log is missing you cannot confirm that behavior — say so.` });
  if (check.ok && !check.data.accepted)
    console.log(`   ⚠ coverage discrepancies: ${(check.data.discrepancies || []).slice(0, 3).join(" | ")}`);
  const obj = { ...exec.data, independent_check: check.ok ? check.data : { accepted: null, discrepancies: ["checker failed"] } };
  const st = loadState();
  await checkpoint("stage3", "03-execution.md", renderS3(obj), "s3_execution.json", obj, st);
  console.log(`   Stage 3 ✓ — executed ${obj.coverage.executed_pct ?? "?"}%, ${obj.observed_behaviors.length} behaviors, check.accepted=${obj.independent_check.accepted}`);
}

async function stage4() {
  console.log("\n━━ STAGE 4 — Goal + external research (parallel halves) ━━");
  const inv = readWork("s1_inventory.json");
  if (!inv) return halt("stage4", "missing Stage-1 inventory");
  // GOAL ‖ RESEARCH-GATHER run concurrently
  const goalP = runAgent({ name: "s4-goal", model: M_DEEP, maxTurns: 50, schema: S4_GOAL,
    prompt: `STAGE 4 (goal half). Infer the repo's long-term GOAL(s). Read the Stage 1–3 artifacts: audit/01-understanding.md, audit/02-static-audit.md, audit/03-execution.md (and audit/.work/*.json). Also read 01_Vision_and_Strategy/Programmable_Mitochondria_Vision_2026-04-21.md and README.md. Output candidate goals — keep them PLURAL, do not collapse to one. Each candidate = a set of FALSIFIABLE success_signals, and EVERY signal must trace to evidence in Stages 1–3 (cite the artifact/path). A candidate with no grounding is speculation: either drop it or mark status=needs-human-confirmation. The surviving set is carried into the plan, so keep the assumptions visible.` });
  const angles = [
    "genome-scale metabolic modeling (FBA/COBRA) of mitochondria & organelles, GPR-aware constraint methods, MitoMAMMAL/Human-GEM tooling, and validation against MitoCarta",
    "biophysical OXPHOS / mitochondrial bioenergetics ODE models (Beard 2005, QAMAS, MPTP & cardiolipin-peroxidation models) and multi-scale FBA↔ODE coupling methods",
    "mitochondrial transplantation & isolated-organelle viability: empirical transit/preservation windows, ΔΨm decay time-courses, protein half-life datasets, and reproducible scientific-software practices (testing, packaging) for this kind of repo",
  ];
  const researchG = await pMap(angles, (a, i) => runAgent({ name: `s4-research${i}`, model: M_FAST, web: true, maxTurns: 35, schema: S4_RESEARCH,
    prompt: `STAGE 4 (research half, angle ${i + 1}). Deep external web search for ideas/technologies/projects/papers that MATERIALLY advance this project's goal, focused on: ${a}. Gather independently and cite EVERY source (title + url). Mark each source corroboration as corroborated (>=2 independent sources agree) / single-source / uncorroborated. Output sources[] and ideas[] (each idea: what it is, how it serves the goal, which sources). Prefer primary literature & official docs. Be honest about uncertainty (Invariant 1).` }), 3);
  const goal = await goalP;
  if (!goal.ok) return halt("stage4", "goal worker failed schema validation");
  let sources = [], ideas = [];
  for (const g of researchG) if (g.ok) { sources.push(...g.data.sources); ideas.push(...g.data.ideas); }
  sources = dedupe(sources, (s) => (s.url || s.title).toLowerCase());
  ideas = dedupe(ideas, (i) => i.idea.toLowerCase().slice(0, 60));
  // synthesis: weigh sources against each other (deep-research shape)
  writeFileSync(join(WORK, "s4_research_raw.json"), JSON.stringify({ sources, ideas }, null, 2));
  const synth = await runAgent({ name: "s4-research-synth", model: M_DEEP, web: true, maxTurns: 30, schema: S4_RESEARCH,
    prompt: `STAGE 4 research synthesis. Raw multi-agent gather is at audit/.work/s4_research_raw.json. Cross-check the claims against each other and against the candidate goals in audit/.work/*goal* / audit/01-understanding.md. Promote only ideas that are relevant AND supported; re-mark corroboration honestly (downgrade anything resting on a single weak source to single-source/uncorroborated). Return the consolidated, de-duplicated sources[] and the ranked ideas[] that best advance the goal.` });
  const research = synth.ok ? synth.data : { sources, ideas };
  const st = loadState();
  await checkpoint("stage4", "04-goal.md", renderS4(goal.data, research), "s4_goal_research.json", { goal: goal.data, research }, st);
  console.log(`   Stage 4 ✓ — ${goal.data.candidates.length} goal candidates, ${research.ideas.length} ideas, ${research.sources.length} sources`);
}

async function stage5() {
  console.log("\n━━ STAGE 5 — Execution-ready plan ━━");
  for (const f of ["s1_inventory.json", "s2_findings.json", "s3_execution.json", "s4_goal_research.json"])
    if (!readWork(f)) return halt("stage5", `missing prior artifact ${f}`);
  let obj = null;
  for (let round = 1; round <= 2; round++) {
    const extra = round > 1 ? `\nThe prior plan had AMBIGUOUS items a fresh agent could not map to a concrete diff target: ${readWork("s5_ambig.json")?.ambiguous_ids?.join(", ")}. Rewrite those to be unambiguous (precise location + concrete change + concrete verification).` : "";
    const plan = await runAgent({ name: `s5-plan-r${round}`, model: M_DEEP, maxTurns: 60, schema: S5,
      prompt: `STAGE 5. Produce an EXECUTION-READY change plan closing the gap between current state (Stages 1–3) and goal (Stage 4). Read audit/01-understanding.md, audit/02-static-audit.md, audit/03-execution.md, audit/04-goal.md (and audit/.work/*.json). Every plan item MUST have: id; title; links_to (a specific Stage-2 finding id OR a Stage-4 goal-gap); location (file/module to change); change_summary (what to do); verification_signal (the concrete observation/test/command that proves it worked); depends_on (ids of prerequisite items — dependency order). Order items so dependencies come first. Prioritize: reproducibility/correctness blockers and high-severity findings before enhancements; goal-advancing items after the foundation is sound. Do NOT invent work unmoored from a finding or goal-gap.${extra}` });
    if (!plan.ok) return halt("stage5", `planner round ${round} failed schema validation`);
    // completeness gate
    const incomplete = plan.data.items.filter((i) => !i.links_to || !i.location || !i.verification_signal || !("depends_on" in i));
    if (incomplete.length) { if (round === 2) return halt("stage5", `${incomplete.length} items missing required fields after retry`); continue; }
    // fresh-agent mappability gate (independent)
    writeFileSync(join(WORK, "s5_plan.json"), JSON.stringify(plan.data, null, 2));
    const map = await runAgent({ name: `s5-mapcheck-r${round}`, model: M_FAST, maxTurns: 40, schema: S5_MAP,
      prompt: `STAGE 5 mappability gate. A change plan is at audit/.work/s5_plan.json. For EACH item, decide: could a fresh engineer open the named location and make a concrete diff WITHOUT asking a clarifying question? Verify the location actually exists (Read/Grep it). Set all_mappable=true only if every item passes; list ambiguous_ids for any that are too vague, mislocated, or lack a concrete verification signal.` });
    obj = plan.data;
    if (!map.ok || map.data.all_mappable) { if (map.ok) console.log("   mappability: all items mappable"); break; }
    writeFileSync(join(WORK, "s5_ambig.json"), JSON.stringify(map.data));
    console.log(`   round ${round}: ${map.data.ambiguous_ids.length} ambiguous items → refine`);
    if (round === 2) console.log("   ⚠ proceeding with residual ambiguity noted in plan");
  }
  const st = loadState();
  await checkpoint("stage5", "05-plan.md", renderS5(obj), "s5_plan_final.json", obj, st);
  console.log(`   Stage 5 ✓ — ${obj.items.length} dependency-ordered items`);
}

// ════════════════════════════════ MAIN ════════════════════════════════
async function main() {
  mkdirSync(WORK, { recursive: true });
  if (FLAG("--fresh")) { rmSync(WORK, { recursive: true, force: true }); mkdirSync(WORK, { recursive: true }); console.log("🧹 fresh run"); }
  BRANCH = (await sh("git", ["rev-parse", "--abbrev-ref", "HEAD"])).out.trim() || "HEAD";
  console.log(`Forensic audit · repo=${REPO} · branch=${BRANCH} · push=${DO_PUSH}`);

  // lightweight auth recheck (background spawn must inherit OAuth)
  const pre = await sh("claude", ["-p", "Reply with exactly: OK", "--output-format", "json", "--model", M_FAST], { stdio: ["ignore", "pipe", "pipe"] });
  let preOk = false;
  try { preOk = JSON.parse(pre.out).subtype === "success"; } catch {}
  if (!preOk) return halt("preflight", "claude -p did not authenticate from the orchestrator process");
  console.log("✓ preflight: claude -p authenticates");

  const state = loadState();
  const done = (s) => state.completed && state.completed[s] && !FLAG("--fresh");
  const only = OPT("--stage", null);
  const from = Number(OPT("--from", "1"));
  const want = (n, key) => (only ? Number(only) === n : n >= from && !done(key));

  const stages = [[1, "stage1", stage1], [2, "stage2", stage2], [3, "stage3", stage3], [4, "stage4", stage4], [5, "stage5", stage5]];
  for (const [n, key, fn] of stages) {
    if (want(n, key)) await fn();
    else console.log(`↩ skip Stage ${n} (${done(key) ? "already checkpointed" : "out of range"})`);
  }

  console.log(`\n✅ pipeline complete. Artifacts in audit/01..05. Cumulative API-equivalent cost $${TOTAL_USD.toFixed(2)} (real subscription draw is far lower).`);
}
main().catch((e) => { console.error("orchestrator crashed:", e); process.exit(1); });

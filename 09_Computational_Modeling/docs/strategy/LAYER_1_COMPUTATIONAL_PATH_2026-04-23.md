# Layer 1 Computational Path — Strategic Analysis
**Date:** 2026-04-23
**Status:** Strategic option analysis; no code changes yet committed
**Context:** Post-audit reframe of Layer 1 scope. Predecessor docs: `docs/investigation/AUDIT_2026-04-23.md`, `docs/investigation/FRAMING_2026-04-23.md`, `01_Vision_and_Strategy/Programmable_Mitochondria_Vision_2026-04-21.md`.

---

## The question

Given what we've built (FBA + protein decay framework, 145-gene essential set, 29h ceiling, cold-chain gap-quantification), and given the demonstrated work pace (entire computational pipeline built in ~2 days wall-clock), **does Layer 1 — the functional transit window — actually require wet lab, or can it be closed computationally?**

## The short answer

**Wet lab is not strictly required for Layer 1.** The claim "FBA can't model non-proteomic failure" conflates one method with all of computation. Existing published models handle the failure modes FBA can't: ODE energetics (Cortassa-Aon), ETC kinetics (Beard 2005), stochastic MPTP (Bazil-Beard 2016), membrane/cardiolipin biophysics (fragmentary). **None have been composed.** That composition is the computational path to Layer 1.

At demonstrated pace, a minimum-viable composite (FBA + ODE coupling) is ~1–2 weeks of focused work, not 3–6 months.

---

## What Layer 1 actually requires

From `01_Vision_and_Strategy/Programmable_Mitochondria_Vision_2026-04-21.md`: *"How long does an extracted mitochondrion remain functional during extracellular transit? The engineering target is the functional transit window — the time between extraction and reuptake threshold."*

Operationalized, Layer 1 completion means:
1. Measure or predict actual transit window under specified conditions
2. Know *why* mitochondria fail (which failure mode is rate-limiting)
3. Predict transit window under varied conditions
4. Identify / validate actionable extension interventions

FBA alone satisfies (2) only for proteomics, contributes partially to (3), and does not address (1) or (4) meaningfully. A composite computational stack can satisfy all four without wet lab — provided it's built and validated honestly.

---

## Scaffolding paper vs completion paper

The q-bio abstract is currently positioned as a Layer 1 **scaffolding** paper, not a Layer 1 **completion** paper. Under the best-case literature scenario (all DocInsight batches return ideal data), the abstract delivers:
- ✓ Protein-decay ceiling (29h) — defined and justified
- ✓ Network topology governing decay — CI 39-subunit AND-clause
- ✓ 145 essential genes + external validation (MitoCarta/DepMap/OMIM)
- ✓ Gap quantification — "ceiling vs empirical → non-proteomic failure dominates"
- ✓ Intervention design space — Q10/MitoQ literature-grounded

What even the best-case abstract does NOT deliver:
- ✗ Direct measurement of actual transit window
- ✗ Modeling of non-proteomic failure (membrane, MPTP, Ca²⁺ — all FBA-inexpressible)
- ✗ Validated preservation intervention
- ✗ Usable extraction-to-transplant protocol

**The scaffolding paper's contribution is legitimate but bounded:** it quantitatively decomposes the transit-viability problem, shows proteomics is NOT the rate-limiter in current protocols, identifies a defensible engineering target (the 29h ceiling), and catalogs structural features (145 genes, CI AND-clause) that future interventions can protect. That's enough for a planting-the-flag publication. It is not Layer 1 completion.

The hard truth about FBA specifically: if empirical window is 4–18h and protein-decay ceiling is 29h, the proteomics model has done its job — it said "it's not proteins, look elsewhere." **But FBA can't see "elsewhere."** Membrane physics, MPTP dynamics, ROS damage kinetics, Ca²⁺ overload — none fit in stoichiometric constraints. The Phase G.5 ROS coupling is a hack that gets the right number from the wrong mechanism (it's proteolysis-acceleration math, not membrane/ROS biology).

---

## Two paths to Layer 1 completion

### Path A: Wet-lab program (the conventional assumption)

Roughly in order:
1. **Wet-lab empirical curve** on mammalian mitochondria in MiR05 (or similar) across 0–24h — closes the circular calibration, gives the framework a real anchor
2. **Mechanism-of-failure assay** — at what point does membrane integrity fail vs protein function fail? Partitions the 4-18h window into proteomic and non-proteomic segments
3. **Intervention validation** — test one literature-reported preservation intervention (MitoQ, trehalose, MPTP inhibitor) and measure actual fold-extension
4. **Protocol iteration** — combine best intervention stack, measure new window, compare to ceiling

Canonical estimate: 6–18 months of wet-lab work.

### Path B: Computational composite (the reframe this doc is about)

See "The creative move: multi-scale composite" below. Estimated 2–3 weeks at demonstrated pace for minimum-viable (option c); ~6 weeks for full multi-scale closure.

**Both paths are legitimate Layer 1 completion routes.** Path B has not been conventionally considered available; this doc argues it is.

---

## What's missing computationally, and what exists

| Failure mode | Existing model | Integrated? |
|---|---|---|
| Protein decay + GPR capacity envelope | MitoMAMMAL + our E-flux layer | ✓ done |
| ΔΨm dynamics post-extraction | **Cortassa-Aon 2003, 2006** (integrated mito energetics) | ✗ separate paradigm (ODE) |
| Ca²⁺ handling + MPTP opening | **Bazil-Beard 2016** (stochastic MPTP), **Magnus-Keizer 1998** | ✗ separate paradigm |
| ETC + substrate kinetics | **Beard 2005** (computational model of oxidative phosphorylation) | ✗ separate paradigm |
| Cardiolipin peroxidation | Fragmentary — Kagan lab, Schlame lab | ✗ no consolidated model |
| ROS production + damage | Aon-Cortassa ROS-Ca²⁺ coupling; our Phase G.5 hack | partial |

Each layer has its own literature with its own experimental validation. **None are in MitoMAMMAL. The gap is composition, not data.**

---

## The creative move: multi-scale composite

```
t=0: extraction event
  ↓
FBA layer (done): proteomics capacity envelope over time
  ↓ feeds as time-varying Vmax into ↓
ODE layer (Cortassa/Beard): ΔΨm, ATP, respiratory flux given capacity envelope
  ↓ feeds state into ↓
Ca²⁺ / MPTP layer (Bazil-Beard): stochastic opening probability given ΔΨm + [Ca²⁺]
  ↓ couples to ↓
Membrane layer (cardiolipin kinetics): OMM/IMM integrity given ROS production
  ↓
Functional failure time = min(proteomics failure, ΔΨm collapse, MPTP opening, membrane rupture)
```

**Novel contribution:** the composition itself. Nobody has integrated proteomics-aware FBA with ODE ETC dynamics with stochastic MPTP with membrane biophysics for extraction viability. Individual models are old; the composite isn't.

### Where the 30× problem disappears

The audit's central scientific fragility is that the 5.1h TW matches MiR05 4–18h only via a single fitted 30× scaling factor. In the composite, **that factor doesn't exist**. It was an artifact of compressing multi-mechanism failure into a single proteomics scalar. When mechanisms are modeled separately, each layer calibrates against its own published data. The circularity dissolves.

This is the strongest scientific argument for going multi-scale.

---

## What wet lab is strictly required for

Going through honestly:
- Proteomics capacity: literature-parameterized (Lam, Fornasiero, Karunadharma) — ✓ no wet lab
- ΔΨm kinetics: Cortassa-Aon rat cardiac parameters, adaptable — no new measurement
- ETC kinetics: Beard 2005 parameters comprehensively characterized — no wet lab
- Ca²⁺ handling: rich cardiac ischemia-reperfusion literature — no wet lab
- MPTP: stochastic models have thousands of validation experiments — use published
- **Cardiolipin peroxidation: weakest layer; literature parameters fragmented. Might need wet lab OR might be acceptable as a range.**
- Coupling parameters (how FBA capacity loss maps to ODE Vmax): not in any single paper. **Derivable as boundary condition on the ODE; no new measurement.**

**Best-case estimate:** 1 potentially-new measurement (cardiolipin peroxidation rate), maybe zero. Everything else is integration work.

---

## Validation strategy without wet lab

If the composite predicts all of:
- Empirical MiR05 4–18h viability range
- Cold-chain ~4× extension (not 14×)
- MitoQ ~30% extension on isolated mito
- Substrate supp ~0h effect
- ΔΨm decay kinetics matching published curves (even sparse ones)

...then it's validated by **multi-point agreement with qualitatively-different published observations simultaneously**. That's stronger than any single wet-lab time course, because it's independent-mechanism co-validation.

The abstract's gap-quantification claim becomes a testable consequence of the model, not a rhetorical frame.

---

## Timeline recalibration

### The error in my first estimate

I initially said 3–6 months for the composite. That was canonical academic-lab pacing, not this project's pace.

### Actual demonstrated pace

- **2026-04-22 20:51:** MitoMAMMAL cloned
- **2026-04-22 23:44:** Experiments 1/1b/1c + v2 fixes + initial audit done (~3h wall-clock)
- **2026-04-23:** Phases A–K, v6 plan, P0–P4, empirical framework, interventions, abstract draft, 6 audit passes

Roughly 2 days of wall-clock for the entire pipeline that exists.

### Recalibrated composite estimate (at demonstrated pace)

- Cortassa-Aon ODE adaptation + FBA coupling: ~1 day
- Bazil-Beard stochastic MPTP module: ~1 day
- Membrane / cardiolipin layer: ~1–2 days
- Coupling + end-to-end simulation: ~1–2 days
- Validation against literature: ~1 day
- **Raw build: ~1 week.**

Audit overhead to match current discipline (the demonstrated pace generates bootstrap-jitter / cold-chain-cap / 30×-fit debt that takes multiple passes to surface): ~1–2 weeks.

**Total realistic: 2–3 weeks.** We have ~5 weeks to May 31.

---

## Options

### (a) Submit abstract as-is (scaffolding paper), composite in June
- **Pros:** zero deadline risk; submission is already drafted
- **Cons:** leaves known-weak claims (30× fit, bootstrap jitter, cold-chain cap) in submitted version
- **Verdict:** safest but accepts audit fragilities into the record

### (b) Full composite before submission
- **Pros:** strongest scientific contribution; removes 30× problem; multi-mechanism validation
- **Cons:** burns all schedule slack; audit debt from rapid iteration compounds; three-layer integration in 2-3 weeks is aggressive even at demonstrated pace
- **Verdict:** achievable, not advisable

### (c) Partial composite — FBA + ODE coupling only
- **Scope:** Cortassa-Aon ODE module + FBA capacity coupling. Skip MPTP and membrane layers.
- **Pros:**
  - Removes the 30× fit circularity (the single biggest audit fragility)
  - Replaces fitted proteomics compression with kinetic ΔΨm derivation
  - Fits comfortably in 5-week window with audit margin (~2 weeks build + audit, ~3 weeks slack)
  - Doesn't require cardiolipin parameters (the weakest literature layer)
  - MPTP + membrane defer to follow-up paper naturally
- **Cons:**
  - Still doesn't close the "membrane + MPTP unmodeled" gap
  - Cold-chain 72h sim-cap issue remains until MPTP layer exists (though ODE version with T_MAX=240h may be enough)
- **Verdict:** sweet spot. Removes the single load-bearing audit fragility without over-scoping.

### Recommendation: Option (c)

Concretely:
1. Pull Cortassa-Aon 2003 / 2006 + Beard 2005 parameter sets from published SI
2. Build ODE module coupling ΔΨm + ATP + respiration
3. Feed FBA capacity envelope as time-varying Vmax constraint on ODE reactions
4. Simulate; report TW from ΔΨm crossing threshold, not from FBA ATP threshold
5. 30× factor disappears — replaced by kinetic derivation of when ΔΨm collapses
6. Re-audit with same discipline as prior passes; update TRUST_LEDGER, FRAMING, abstract
7. Submit updated abstract

---

## What blocks option (c)

Going through honestly, nothing structural:
- **Cortassa-Aon availability:** published with parameters; multiple groups have reproduced/adapted. Accessible.
- **Coupling mechanism:** map FBA capacity envelope to time-varying Vmax in the ODE. This is the novel integration piece. ~1 day math + 1 day code.
- **Species adaptation:** Cortassa is rat cardiac, MitoMAMMAL is mouse cardiac. Cardiac bioenergetics is highly conserved; parameter transfer is a tractable adapter, not a science problem.
- **Validation data:** even without independent empirical anchor, the composite can be validated against Cortassa's own published dynamics (the paper shows ΔΨm traces the ODE reproduces).

None are blockers. All are 1–2 days of work each at demonstrated pace.

---

## Abstract framing implications

Which option is chosen affects how the abstract can honestly be framed. Distinguish clearly:

### Honest framings (all options)

- **"We quantified the protein-decay ceiling and showed the engineering opportunity lies in non-proteomic failure modes"** — true, defensible, novel-ish. Works under option (a).
- **"Composite FBA + ODE framework predicts transit window from first principles without fitting"** — defensible only under option (c) or (b).
- **"Multi-scale model resolves individual failure modes and identifies the rate-limiter"** — defensible only under option (b) with all layers integrated.

### Overclaims to avoid (regardless of option)

- **"We solved transit viability"** — overclaim. No option delivers this.
- **"We validated a preservation strategy"** — overclaim. Requires wet lab in all options.
- **"We predicted the actual transit window"** — overclaim *under option (a)* because it's fitted via 30×. Defensible under (c) once ΔΨm-derived.
- **"145 genes are biologically-validated stabilization targets"** — overclaim. They're FBA-essential, which is weaker. The abstract's current significance paragraph has this tension.

### Title-vs-significance consistency check

Current abstract title: *"The Protein-Decay Ceiling and Engineering Gap for Extracted Mammalian Mitochondria"* — accurate.

Current abstract significance paragraph includes: *"biologically-validated 145-gene stabilization target set"* — overstates because biological validation = mitochondrial GO and (pending) MitoCarta overlap, not stabilization-target validation. The 145 are essential-in-FBA-under-decay, not demonstrated-to-stabilize-transit.

Fix either by tightening significance ("145-gene FBA-essential set, 89% mitochondrial GO, proposed as stabilization targets") or by actually validating via Batch 1 cross-reference.

---

## Strategic takeaway: what the abstract does for the program

"Did literature review hit Layer 1?" is the wrong question. The right question: **does this abstract credibly authorize the next step?**

Under each option:
- **(a) scaffolding:** authorizes either a wet-lab program (Path A) OR a composite-model program (Path B) as follow-up. Both remain open.
- **(c) partial composite:** authorizes the remaining composite work (MPTP + membrane) AND wet-lab falsification of composite predictions.
- **(b) full composite:** authorizes direct wet-lab validation of specific predictions; accelerates Layer 2 engineering (because Layer 2 needs a validated Layer 1 model to design around).

**What a reviewer or collaborator reading the best-case abstract should come away with:** *"The proteomics limit is 29h. Current practice is 4-18h. Closing that gap — whether computationally via multi-scale models or empirically via wet-lab — is the research program. This paper shows that proteomics isn't the bottleneck, which redirects where preservation engineering should focus."*

That takeaway survives any of the three options. The difference is how much of the subsequent program the abstract does itself.

---

## Honest caveats

1. **Cortassa-Aon / Bazil-Beard are rat cardiac, MitoMAMMAL is mouse cardiac.** Adapters exist; this is tractable but nonzero work.
2. **Parameter uncertainty will be substantial.** The payoff is honest uncertainty propagation, not tighter predictions. The composite might report TW = 3–22h rather than 5.1h — less dramatic, more honest.
3. **"Novel composition" is a softer novelty claim than "novel methodology."** Reviewers may not accept it as sufficient. It is a real contribution, but one that requires careful positioning.
4. **Timeline estimates at demonstrated pace assume the same developer continues at the same pace.** Task-switching, debugging multi-scale numerics, and fatigue all erode this.
5. **MPTP + membrane layers still matter for Layer 1 completion.** Option (c) is partial. Full closure still requires the follow-up paper.

---

## What wet lab becomes in option (c)

Wet lab moves from required-for-thesis to valuable-for-confirmation:
- **Specific predictions the composite makes that aren't in literature** (e.g., combined cold chain + MitoQ + CsA → Xh): falsifying the composite
- **User's existing 2024 Taguchi yeast data (if digitized):** independent cross-species check
- **Any preservation-intervention test not yet published:** the composite predicts, wet lab tests

That's a very different strategic posture than "must run wet lab to complete Layer 1."

---

## Decision gates for executing option (c)

| Gate | Check | If fails |
|---|---|---|
| G1 | Cortassa-Aon parameters pullable from published SI? | If not, fall back to Beard 2005 alone |
| G2 | FBA→ODE coupling produces sane dynamics (ΔΨm matches Cortassa reference curves)? | If not, revisit coupling math before adding features |
| G3 | Composite reproduces MiR05 4–18h range without fitted scalar? | If not, investigate: which layer is mis-parameterized? |
| G4 | Cold-chain prediction matches empirical ~4× extension? | If not, either model is wrong OR literature 4× number is an underestimate; investigate |
| G5 | Abstract can be rewritten around composite in <1 day? | If not, option (c) ran over scope; reassess vs (a) |

Any gate failure is a pivot point, not a blocker. Degradation path exists at each step: worst case, fall back to option (a) with no loss of existing work.

---

## Project Structure Decision (2026-04-23)

Decided: **Option A — targeted extension within `09_Computational_Modeling/`**. Rejected Option B (spin out `11_MultiScale_Modeling/`) and Option C (subdivide 09 into fba/composite/).

### Rationale

1. Composite extends FBA work — shares MODEL_PATH, 145-gene set, TRUST_LEDGER discipline, paths.py helpers
2. Reorganization cost is high 5 weeks before submission (every audit doc references paths under 09)
3. If composite fails a decision gate (G1/G2/G3), FBA work is untouched; rollback is just archiving a subfolder
4. Expansion pattern scales — MPTP and membrane layers become additional modules under `scripts/composite/` without further restructuring

### Scaffolding completed 2026-04-23

Directories (empty but present):
- `scripts/composite/` — future `experiment5_fba_ode.py`, `validate_against_cortassa.py`, etc.
- `results/composite/` — future ΔΨm traces, composite TW predictions, validation artifacts
- `Whole_Cell_Modeling/cortassa/` — future Cortassa-Aon + Beard 2005 parameter files

Utility modules (empty placeholders with planned interfaces documented):
- `ode_utils.py` — scipy.integrate helpers for ΔΨm/ATP/respiration dynamics
- `composite_utils.py` — FBA → ODE coupling (capacity envelope → time-varying Vmax)

`paths.py` extended:
- `RESULTS_COMPOSITE = RESULTS_DIR / "composite"`
- `CORTASSA_DIR = PROJECT_ROOT / "Whole_Cell_Modeling" / "cortassa"`
- `SCRIPTS_COMPOSITE = SCRIPTS_DIR / "composite"`

READMEs created (execution contracts, not implementation):
- `scripts/composite/README.md` — entry points, kill criteria, audit discipline
- `Whole_Cell_Modeling/cortassa/README.md` — expected contents, provenance discipline
- `results/composite/README.md` — artifact list

### For the planning session

When the composite planning session begins, the following is already true:
- All paths resolved through `paths.py` (no hardcoding needed)
- Kill criteria and decision gates documented (in `scripts/composite/README.md` and this doc's "Decision gates" section)
- Audit thread location specified (`docs/investigation/COMPOSITE_AUDIT_*.md`, separate from FBA audit in `AUDIT_2026-04-23.md`)
- Planned interfaces for `ode_utils.py` and `composite_utils.py` are stubbed — planning session decides state-vector convention, integrator choice, coupling math
- Kill-branch exists: if composite fails gates, archive `scripts/composite/`, `results/composite/`, `Whole_Cell_Modeling/cortassa/` as a subdirectory marker and proceed with Option (a) submission. No existing FBA work is affected.

**What the planning session needs to decide (scaffolding doesn't predecide):**
- Integrator (scipy `odeint` vs `solve_ivp`); state-vector convention
- Which Cortassa version (2003 baseline, 2006 with ROS, 2014 extensions) to anchor on
- Species-adapter approach (direct transfer, rescaling factor, or skip and accept rat/mouse mismatch as caveat)
- Coupling math specifics: does capacity envelope scale Vmax directly, or modulate a separate capacity variable that couples to Vmax via a Hill function?
- Validation order: replicate Cortassa baseline first, then add FBA coupling; or couple immediately and validate against composite-vs-empirical?
- What "composite audit" looks like — distinct ledger vs extension of TRUST_LEDGER

Accounting for these now means the planning session is a math/science discussion, not a directory-structure discussion.

---

## Expected Outcomes — What the Composite Buys Us

### What the composite is expected to do

**Option (c) — FBA + ODE:**
1. Eliminate the 30× fitted scaling factor — ΔΨm dynamics become mechanistically derived rather than compressed into a single knob
2. Produce a transit-window prediction as model *output*, not model *input* tuned to match literature
3. Let intervention predictions respond mechanistically (Q10 acts on ODE rate constants; MitoQ via ROS coupling) rather than via hand-set scalars
4. Partition failure into "proteomics-driven collapse" vs "ΔΨm-kinetic collapse" — tells us *which mode* fails first

**Option (b) — Full composite (+ MPTP + membrane):**
5. MPTP opening probability over time as separate failure channel
6. Membrane-integrity failure via cardiolipin kinetics
7. TW = min over *all four* mechanisms, each with honest literature uncertainty

### How this advances each Layer 1 requirement

| Layer 1 item | FBA alone (now) | + Option (c) | + Option (b) |
|---|---|---|---|
| 1. Measure/predict actual TW | Weak — fitted via 30× | Medium — kinetically derived | Strong — multi-mechanism |
| 2. Know why mito fail | Proteomics only | + ΔΨm-kinetic identified | + MPTP/membrane resolved |
| 3. Predict under varied conditions | Within proteomics scope | Across temp, substrate, Ca²⁺ | All failure modes respond |
| 4. Extend via interventions | Scalar-tuned | Mechanism-tuned | True design space |

Option (c) moves us from "weak" to "medium" on all four. Option (b) moves us to "strong" on three — #1 stays at medium because clinical-grade empirical measurement still needs wet lab.

### What this does for the q-bio abstract specifically

- **If option (c) completes before May 31:** abstract upgrades from *"we quantified the proteomics ceiling"* to *"we built a composite that predicts TW from first principles, validated against Cortassa reference dynamics and empirical MiR05 range as emergent output."* Novel contribution becomes the composition, which survives reviewer scrutiny better than the current fitted point prediction.
- **If option (c) doesn't complete in time:** scaffolding paper still works; composite referenced as in-progress follow-up.

### What this does for Layers 2–4 (the real payoff)

The composite isn't just Layer 1 closure — it's the substrate for everything downstream.

- **Layer 2 (programmable transplantation):** designing pre-extraction modifications requires predicting how a modification affects transit viability. FBA alone can't simulate modifications that affect ΔΨm, ROS, or membrane integrity. A validated composite lets you virtual-screen candidate modifications: *"if we overexpress gene X, what happens to ΔΨm during 6h transit?"* That's actionable engineering. Without the composite, Layer 2 is empirical-only.
- **Layer 3 (gene delivery):** requires mitochondrial viability through the delivery window. Layer 1 model directly informs this.
- **Layer 4 (autonomous operation):** requires quantitative understanding of every failure mode. Composite is the scaffold; adding proteostasis recovery, mtDNA turnover, fission/fusion layers on top.

**Strategic implication:** the composite isn't Layer 1 completion for its own sake. It's the minimum computational substrate that makes Layers 2–4 computationally tractable at all.

### Honest bounds on what to hope for

Things the composite will NOT give us even in the best case:
- Direct empirical measurement of transit window (still wet lab for clinical translation)
- Parameter uncertainty small enough for tight point predictions (honest propagation may give TW = 2–40h, less dramatic than 5.1h)
- Guaranteed reviewer acceptance of "novel composition" as a contribution class
- Validation against Miguel's yeast Taguchi data (species mismatch remains)

Things that could go wrong:
- Composite produces a TW that doesn't match MiR05 range without a fudge factor. Informative for the science (wrong capacity envelope, or Cortassa params don't transfer) but doesn't help the abstract.
- Integration numerics unstable at 72h+ time scales. Fixable but time-consuming.
- Cortassa parameter files harder to locate than expected. Fallback: Beard 2005 alone (G1 kill gate).

### What "success" looks like concretely

- **Minimum success** (worth the 2–3 weeks): composite reproduces MiR05 4–18h range as emergent output without fitted scalar; reproduces Cortassa's published ΔΨm curves as validation; composition published as methodological contribution.
- **Median success:** the above + one new prediction the composite makes that isn't obvious from either layer alone (e.g., "substrate supplementation extends ΔΨm-kinetic collapse but not proteomics collapse; crossover at 8h of cold storage") — gives the abstract a falsifiable claim reviewers can latch onto.
- **Stretch success:** Layer 2 virtual-screen demonstration. Pick one genetic or chemical modification, show composite predicts a specific transit-viability effect, position as the bridge to Layer 2 engineering.

---

## Next concrete step

If the user green-lights option (c):
1. Locate Cortassa-Aon 2003 + Beard 2005 parameter files (published SI, probably MATLAB/.csv)
2. Scaffold `scripts/experiments_v2/experiment5_fba_ode_composite.py`
3. Implement FBA capacity envelope as time-varying function of t
4. Implement ODE integrator consuming capacity envelope
5. Validate against Cortassa's own published curves (no-perturbation baseline)
6. Run transit-window simulation; report ΔΨm-crossing TW
7. Audit pass before committing to abstract rewrite

---

## Outstanding Work — Composite NOT Complete at Mechanism Level (added 2026-04-24 pass 7)

Pass-7 honest-status audit (`docs/investigation/COMPOSITE_AUDIT_2026-04-24.md`) retracted the Session 8 claim that option (b) mechanistically closed the engineering gap. The composite currently adds a phenomenological single-parameter proton-leak amplifier in a biophysically plausible slot — a framework advance, not mechanism resolution. Before the composite can be honestly called "complete," these additions are required. None depend on DocInsight.

### Mechanism extensions (each ~1 session at demonstrated pace)

**A. Cortassa-Aon 2006 ROS module.** Published model with CellML implementation. Adds:
- O₂·⁻ and H₂O₂ as matrix state variables
- ROS production coupled to ETC fluxes (forward and reverse electron transport at CI/III)
- GSH-Px scavenging dynamics
- IMAC (inner membrane anion channel) providing ROS positive feedback
- Replaces MitoQ-as-halflife-scalar with MitoQ-as-actual-scavenger

**B. Bazil-Dash 2010 MPTP module.** Published model, parameters in SI. Adds:
- Ca²⁺ as state variable with uniporter uptake + NCLX efflux + matrix buffering
- MPTP pore with opening probability coupled to ΔΨm × [Ca²⁺]
- Provides a true ΔΨm-first failure mode distinct from proteomics — addresses the "ATP-first always" artifact
- Under Ca²⁺-loaded scenarios (C), predicted dominant failure mode should shift

**C. Explicit cardiolipin pool + Kagan cycle.** Uses existing cyt c pool in Beard. Adds:
- Cardiolipin as state variable with initial concentration
- Cyt c + H₂O₂ catalyzed cardiolipin peroxidation (Kagan lab kinetics)
- Oxidized-CL fraction coupled to proton leak coefficient
- Replaces the fitted k_membrane scalar with a derived rate; removes the last fitted parameter

### Diagnostic extensions (cheaper, high-value-per-hour)

**D. "ATP-first always" investigation.** Under all composite runs, the FBA ATP flux threshold crossed before the ODE ΔΨm threshold. Is this biological or artifactual? Trace which specific reaction has lowest capacity when ATP threshold crosses. Likely reveals ANT or PiC as unexpected rate-limiter.

**E. Self-consistency vs Phase G.1 algebra.** With k_membrane=0 and uniform halflives, does composite reproduce TW ≈ 2.4×t½? Validates the composite doesn't silently violate the established algebraic claim.

**F. Correlated-parameter sensitivity.** Ex 5.6 treated Beard parameters independently. Real correlations (within-complex subunit halflives; X_C1/X_C3/X_C4 co-vary) not captured. May narrow CI informatively or widen it.

### Priority ordering

**If goal is maximum mechanism-knowledge gain:** B → D → A → C → E → F. MPTP first addresses the "ATP-first always" artifact which blocks meaningful mechanism-partition analysis. Then ROS, then cardiolipin (which requires ROS to be in place for the Kagan cycle).

**If goal is cheap diagnosis before more building:** D → E → F → B → A → C. Catches artifacts before committing to larger extensions.

### Completion criterion

Composite is honestly "complete" when:
1. A + B + C are integrated (ROS + MPTP + cardiolipin dynamics)
2. Mechanism partition shows scenario-dependent failure modes (ΔΨm-first in Ca-loaded / ischemic; ATP-first in substrate-rich)
3. k_membrane-like fitted scalars are derived from state variables, not tuned to empirical range

Until then, the composite's honest contributions are: (1) framework architecture, (2) scenario differentiation, (3) literature-sourced uncertainty quantification, (4) identifying inner-membrane biophysics as the plausible slot for the missing rate-limiting mechanism.

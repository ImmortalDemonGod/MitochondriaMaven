# Layer 1 Scope Reframe — Computational Path May Be Viable
**Date:** 2026-04-23
**Status:** Strategic note; full technical analysis in `09_Computational_Modeling/docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md`

---

## What changed

The working assumption for Layer 1 has been:

> "FBA can't model non-proteomic failure (membrane, ROS, MPTP, Ca²⁺), therefore Layer 1 completion requires wet lab."

This is **partially wrong**. The correct form is:

> "*FBA* can't model non-proteomic failure — but other computational methods can. Layer 1 may be completable by composing existing published models across paradigms."

## Why this matters at vision level

The 4-layer vision implicitly assumed:
- Layer 1 (transit viability) requires wet-lab validation before Layer 2 (programmable transplantation) can proceed meaningfully

The reframe opens a different path:
- Layer 1 may be computationally tractable via multi-scale composite (FBA + ODE energetics + stochastic MPTP + membrane biophysics)
- Wet lab shifts from *required-for-Layer-1* to *valuable-for-confirmation-and-Layer-2*
- Layer 2 engineering (pre-modification of mitochondria) can draw directly on a validated computational Layer 1 predictor without waiting on wet-lab closure

## What's changed in timeline

Previous estimate: "computational Layer 1 completion is 3–6 months."
Recalibrated estimate (based on demonstrated ~2-day pace for the current FBA pipeline): **2–3 weeks for a minimum-viable composite, ~6 weeks for full multi-scale closure.**

The vision-level implication: **Layer 1 computational completion is weeks away at current pace, not quarters away.** This changes near-term prioritization.

## Current near-term actions

1. **q-bio Chicago abstract (May 31):** still the forcing function; submit as scaffolding paper or with minimum-viable composite (see technical doc for Option (c) analysis)
2. **Composite model build:** option (c) — FBA + ODE coupling (Cortassa-Aon) — is the recommended path. Removes the central scientific fragility (30× fitted scaling) without over-scoping
3. **Wet lab remains valuable:** for falsifying composite predictions and for Layer 2 engineering, not for Layer 1 closure

## Pointer

Full technical analysis, including the multi-scale architecture, what wet lab is actually required for, validation strategy without wet lab, option tradeoffs, decision gates, and concrete next steps:

→ `09_Computational_Modeling/docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md`

## What this doesn't change

- The 4-layer vision structure itself (Transit / Programmable / Gene Delivery / Autonomous)
- Layer 2–4 sequencing (Layer 2 still requires Layer 1 to be closed, whether computationally or empirically)
- The broader program's dependence on eventual wet-lab validation for clinical translation

What changes is **how** Layer 1 closes — not whether it does.

---

## Update 2026-04-24 (post-Session 8 pass-7)

Session 8 executed plan option (c) + four stretch extensions. Post-hoc pass-7 honest-status audit caught overclaims:

- **Framework architecture COMPLETE** (FBA↔ODE coupling, scenario propagation, Human-GEM transferability, sensitivity analysis).
- **Mechanism work INCOMPLETE.** What was labeled "option (b) mechanistic closure of engineering gap" turned out to be a single phenomenological proton-leak-amplification parameter relocated to a more plausible physical slot — same class of tuning as the 30× factor it ostensibly replaced. ROS is not modeled. MPTP is not modeled. Cardiolipin pool is not modeled.
- **Layer 1 status:** modestly advanced. Scenario differentiation (real improvement), literature-sourced uncertainty (real improvement), framework ready for future mechanism extensions. But no mechanism resolution, no empirical anchor.

**Required next work for honest Layer 1 completion:** Cortassa 2006 ROS integration, Bazil-Dash 2010 MPTP, explicit cardiolipin pool + Kagan cycle. Each ~1 session at demonstrated pace; none require DocInsight. See `09_Computational_Modeling/docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md` pass-7 section and `09_Computational_Modeling/docs/investigation/COMPOSITE_AUDIT_2026-04-24.md` pass-7 section.

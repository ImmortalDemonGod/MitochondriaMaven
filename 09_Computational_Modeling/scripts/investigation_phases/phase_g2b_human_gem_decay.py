"""
Phase G.2b — Test the algebraic claim on Human-GEM.

Key question: does our uniform-decay TW = 28h emerge from FBA, or from the algebra
(TW = -t½ × log₂(threshold))? Test on Human-GEM (12931 rxns, 23x larger than
MitoMAMMAL) — if it gives the same 28h, the result is model-independent algebra.
"""

import sys
from pathlib import Path
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import PROJECT_ROOT, results_path

import json
import numpy as np
import cobra
from cobra.flux_analysis import pfba

HUMAN_GEM_PATH = PROJECT_ROOT / "Whole_Cell_Modeling" / "Human-GEM" / "model" / "Human-GEM.xml"

UNIFORM_HALFLIFE = 12.0
THRESHOLD = 0.20
T_MAX = 72.0


def main():
    print("Phase G.2b — Algebraic claim on Human-GEM")
    print("=" * 60)

    print("Loading Human-GEM...")
    model = cobra.io.read_sbml_model(str(HUMAN_GEM_PATH))
    print(f"  Loaded: {len(model.reactions)} rxns, {len(model.genes)} genes")

    # Get baseline objective
    print("\nBaseline FBA...")
    sol = pfba(model)
    baseline_obj = sol.objective_value
    print(f"  Objective value: {baseline_obj:.4f}, status: {sol.status}")

    # Get baseline fluxes for all reactions
    baseline_fluxes = {r.id: float(sol.fluxes[r.id]) for r in model.reactions}

    # Test 1: Uniform UB scaling (no GPR, simplest possible decay)
    print("\n[Test 1] Uniform decay applied to ALL reaction UBs at flux-relative scaling")
    print("  (UB[t] = baseline_flux × 1.05 × exp(-ln2 t / 12))")

    t_steps = np.arange(0, T_MAX + 1, 1.0)
    fluxes_over_time = []
    threshold_value = baseline_obj * THRESHOLD

    for t in t_steps:
        decay = np.exp(-np.log(2) * t / UNIFORM_HALFLIFE)
        with model:
            for r in model.reactions:
                bf = baseline_fluxes[r.id]
                if bf > 1e-6:
                    r.upper_bound = abs(bf) * 1.05 * decay
                elif bf < -1e-6:
                    r.lower_bound = -abs(bf) * 1.05 * decay
            try:
                s = model.optimize()
                f = s.objective_value if s.status == 'optimal' else 0
            except Exception:
                f = 0
            fluxes_over_time.append(f)
            if f < threshold_value * 0.01 and t > 5:
                fluxes_over_time.extend([0] * (len(t_steps) - len(fluxes_over_time)))
                break

    fluxes_over_time = np.array(fluxes_over_time[:len(t_steps)])
    if len(fluxes_over_time) < len(t_steps):
        fluxes_over_time = np.concatenate([fluxes_over_time, np.zeros(len(t_steps) - len(fluxes_over_time))])

    # Find TW
    tw = None
    for i, f in enumerate(fluxes_over_time):
        if f < threshold_value:
            tw = float(t_steps[i])
            break

    analytical = -UNIFORM_HALFLIFE * np.log(THRESHOLD) / np.log(2)
    print(f"\n  Analytical prediction (any model): TW = {analytical:.2f}h")
    print(f"  Human-GEM observed: TW = {tw}h")
    print(f"  MitoMAMMAL observed (for comparison): TW = 29h")

    if tw is not None:
        gap = tw - analytical
        print(f"  Gap vs analytical: {gap:+.2f}h (matches buffer scale {1.05}: -t½×log₂(0.20/1.05) = {-UNIFORM_HALFLIFE * np.log(THRESHOLD/1.05) / np.log(2):.2f}h)")

    # Verdict
    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)
    if tw is not None and abs(tw - 29) < 3:
        print(f"Human-GEM gives TW={tw}h, matching MitoMAMMAL's 29h.")
        print("→ The algebraic finding is MODEL-INDEPENDENT.")
        print("→ Any FBA model with flux-relative uniform decay gives the same TW.")
        print("→ The FBA framework adds zero content beyond `TW = -t½ × log₂(threshold) × buffer`.")
    elif tw is not None:
        print(f"Human-GEM gives TW={tw}h, MitoMAMMAL gives 29h. Difference of {abs(tw-29)}h.")
        print("→ Some model-specific component exists (network topology effects?).")

    # Save
    summary = {
        'model': 'Human-GEM',
        'reactions': len(model.reactions),
        'genes': len(model.genes),
        'baseline_objective': float(baseline_obj),
        'analytical_tw': float(analytical),
        'human_gem_tw': tw,
        'mitomammal_tw': 29.0,
        'gap_human_gem_vs_analytical': (tw - analytical) if tw is not None else None,
        'verdict': 'algebraic / model-independent' if (tw is not None and abs(tw - 29) < 3) else 'model-specific component',
    }
    with open(results_path('phase_g', 'g2b_human_gem_uniform_decay.json'), 'w') as f:
        json.dump(summary, f, indent=2)


if __name__ == '__main__':
    main()

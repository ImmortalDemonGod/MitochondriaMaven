"""
composite_utils.py — FBA → ODE coupling for the composite model.

The novel-integration piece. Bridges the FBA-derived capacity envelope
(from decay_utils) with the ODE integrator (ode_utils). Specifically:

1. extract_capacity_envelope: given a COBRApy model + decay expression dict,
   evaluate each reaction's GPR-aware capacity fraction and return
   Dict[fba_rxn_id, fraction ∈ [0,1]]. Mirrors the internals of
   decay_utils.apply_gpr_aware_decay but returns fractions instead of
   setting model bounds.

2. build_capacity_envelope_fn: precomputes the envelope at discrete
   time points over t_range_hours, maps FBA reaction IDs to ODE reaction
   IDs via FBA_ODE_REACTION_MAP, and returns a callable
   `capacity_fn(t_seconds) -> Dict[ode_rxn_id, fraction]` suitable for
   ode_utils.integrate_with_capacity.

3. compose_fba_ode: top-level driver that runs the whole composite
   pipeline and returns a CompositeResult.

Strategic context: `docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md`
Audit: `docs/investigation/COMPOSITE_AUDIT_2026-04-24.md`

Mechanism (the "why coupling works" argument):
    Enzyme subunit decay reduces the fraction of functional enzyme
    molecules. In Michaelis-Menten kinetics at fixed [substrate],
    reaction rate is linear in [enzyme]. So the decay fraction is
    equivalent to a Vmax multiplier. We do NOT rescale Km or kcat —
    only Vmax — which preserves the kinetic structure of Beard 2005.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
from scipy.interpolate import interp1d

# Bootstrap imports
_here = Path(__file__).resolve().parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

from paths import MITOMAMMAL_DIR  # noqa: E402

_mito_str = str(MITOMAMMAL_DIR)
if _mito_str not in sys.path:
    sys.path.insert(0, _mito_str)

from efflux_method import evaluate_gpr_expression, remove_genes  # noqa: E402


# ── FBA ↔ ODE reaction mapping (Constraint 2 — small-N deep dive) ─────
#
# Maps MitoMAMMAL reaction IDs → Beard 2005 ODE reaction tags.
# Only reactions with direct ODE analogs are mapped; non-mapped FBA
# reactions decay normally in the FBA layer but don't feed into the
# ODE. The mapping deep-dives on:
#   - CI_mitoMap ↔ C1 (39-subunit AND-clause from Phase G.1)
#   - CV_mitoMap ↔ F1 (ATP synthase / PMF consumer)
#   - ATPtmB_mitoMap ↔ ANT (kinetic bottleneck)
# per plan Constraint 2.
#
# Caveat: Beard 2005 doesn't model CII separately (succinate dehydrogenase).
# Its "NADH_Dehydrogenase" reaction conceptually covers CI only. If
# MitoMAMMAL's CII_mitoMap capacity drops, it cannot feed into Beard
# directly — succinate-driven respiration is not in the composite scope.
# This is a documented limitation for the option-(c) composite.

FBA_ODE_REACTION_MAP: Dict[str, str] = {
    # ETC complexes
    'CI_mitoMap':   'C1',   # Complex I — 39-subunit AND-clause; deep-dive N=3
    'CIII_mitoMap': 'C3',   # Complex III
    'CIV_mitoMap':  'C4',   # Complex IV
    'CV_mitoMap':   'F1',   # F1F0 ATP synthase — PMF consumer; deep-dive N=3
    # Carriers
    'ATPtmB_mitoMap': 'ANT', # ATP/ADP exchanger — kinetic bottleneck; deep-dive N=3
    'PIt2mB_mitoMap': 'PiC', # Phosphate carrier
    # Note: 'DH' (NADH dehydrogenase substrate feed) and 'Leak' in Beard have no
    # direct FBA analog — DH represents TCA cycle / substrate oxidation, and
    # Leak is a nonspecific proton leak not encoded as a reaction in MitoMAMMAL.
    # These default to capacity=1.0 (no decay) in the composite.
}


# ── Capacity envelope extraction ──────────────────────────────────────

def extract_capacity_envelope(
    model,
    expr_dict: Dict[str, float],
    baseline_fluxes: Dict[str, float],
    ignore_species_prefix: Optional[str] = 'ENSG',
) -> Dict[str, float]:
    """Return Dict[rxn_id, capacity_fraction ∈ [0,1]] for every reaction in the
    model, without setting bounds.

    Mirrors the internals of decay_utils.apply_gpr_aware_decay but returns
    the pure GPR-evaluated decay fraction `df` rather than multiplying by
    baseline flux and setting bounds. Baseline fluxes are only used to
    identify reactions with zero baseline (those are omitted — we have no
    calibration reference for them).

    The returned fractions are suitable for feeding into an ODE layer as
    Vmax multipliers.
    """
    capacity: Dict[str, float] = {}

    for rxn in model.reactions:
        # Skip exchange/demand/sink/objective reactions (handled by scenario
        # constraints, not by GPR decay)
        if rxn.id.startswith(('EX_', 'DM_', 'SK_', 'OF_')):
            continue

        gpr_str = str(rxn._gpr) if hasattr(rxn, '_gpr') else rxn.gene_reaction_rule
        if not gpr_str or gpr_str.strip() in ('', 'None'):
            continue

        if ignore_species_prefix:
            gpr_str = remove_genes(gpr_str, ignore_species_prefix)
            if not gpr_str.strip() or gpr_str.strip() in ('(', ')', '()'):
                continue

        try:
            df = evaluate_gpr_expression(gpr_str, expr_dict, default_val=1.0)
        except Exception:
            continue

        if df is None or not np.isfinite(df):
            continue
        df = max(0.0, min(1.0, float(df)))

        # Skip reactions with zero baseline flux (no calibration reference)
        if abs(baseline_fluxes.get(rxn.id, 0.0)) < 1e-9:
            continue

        capacity[rxn.id] = df

    return capacity


# ── Capacity envelope function builder ─────────────────────────────────

def build_capacity_envelope_fn(
    model,
    halflife_map: Dict[str, float],
    t_range_hours: Tuple[float, float] = (0.0, 72.0),
    dt_hours: float = 1.0,
    reaction_mapping: Dict[str, str] = FBA_ODE_REACTION_MAP,
    baseline_fluxes: Optional[Dict[str, float]] = None,
    flux_buffer: float = 1.05,  # unused here; kept for signature parity
    ignore_species_prefix: Optional[str] = 'ENSG',
) -> Callable[[float], Dict[str, float]]:
    """Precompute capacity envelope at discrete hours over t_range;
    return callable that accepts time in seconds and returns per-ODE-reaction
    capacity fractions.

    Parameters
    ----------
    model : cobra.Model
    halflife_map : Dict[gene_id, t_half_hours]
    t_range_hours : (t_start, t_end)
        Integration window for the FBA+decay precomputation (hours).
    dt_hours : float
        Step size for precomputation (hours). Default 1h.
    reaction_mapping : Dict[fba_rxn_id, ode_rxn_id]
        Which FBA reactions feed into which ODE reactions.
    baseline_fluxes : Dict[rxn_id, signed flux], optional
        If None, computed via `decay_utils.get_signed_baseline_fluxes(model)`.
    ignore_species_prefix : str, optional
        GPR species filter (default 'ENSG' = drop human).

    Returns
    -------
    capacity_fn : Callable[[float], Dict[str, float]]
        capacity_fn(t_seconds) returns {ode_rxn_id: fraction ∈ [0,1]} for each
        ODE reaction in reaction_mapping. Reactions not in the mapping default
        to fraction=1.0 (no decay).
    """
    # Bootstrap baseline_fluxes if not provided
    if baseline_fluxes is None:
        from decay_utils import get_signed_baseline_fluxes
        baseline_fluxes = get_signed_baseline_fluxes(model)

    from decay_utils import build_decay_expr_dict  # local import to avoid hot-load

    # Precompute envelope at each discrete t
    t_values = np.arange(t_range_hours[0], t_range_hours[1] + dt_hours, dt_hours)
    envelope_by_ode_rxn: Dict[str, List[float]] = {
        ode_id: [] for ode_id in reaction_mapping.values()
    }

    for t in t_values:
        expr = build_decay_expr_dict(model, halflife_map, t)
        env = extract_capacity_envelope(model, expr, baseline_fluxes,
                                        ignore_species_prefix=ignore_species_prefix)
        # Map FBA rxn → ODE rxn; missing → 1.0 (no data means no decay applied)
        for fba_id, ode_id in reaction_mapping.items():
            envelope_by_ode_rxn[ode_id].append(env.get(fba_id, 1.0))

    # Build per-reaction interpolators; convert x-axis to seconds for ODE consumption
    t_seconds = t_values * 3600.0
    interpolators: Dict[str, Callable[[float], float]] = {}
    for ode_id, values in envelope_by_ode_rxn.items():
        interp = interp1d(
            t_seconds, values,
            kind='linear',
            bounds_error=False,
            fill_value=(values[0], values[-1]),  # clamp outside range
        )
        interpolators[ode_id] = interp

    def capacity_fn(t_seconds_query: float) -> Dict[str, float]:
        return {ode_id: float(interp(t_seconds_query)) for ode_id, interp in interpolators.items()}

    # Attach metadata for audit/inspection
    capacity_fn.t_hours = t_values  # type: ignore[attr-defined]
    capacity_fn.envelope_by_ode_rxn = envelope_by_ode_rxn  # type: ignore[attr-defined]
    capacity_fn.reaction_mapping = reaction_mapping  # type: ignore[attr-defined]

    return capacity_fn


# ── Scenario propagation into ODE substrate pools ─────────────────────

# Scenario-specific Beard parameter + initial-condition overrides.
# Mirrors the FBA scenario semantics in experiment1_v2_transit_window.apply_scenario:
#   A = intracellular buffer (Beard default MiR05-like)
#   B = arterial blood (elevated O2, dilute adenines)
#   C = ischemic tissue (reduced O2, ADP-heavy, Pi accumulation)
#   B_supplemented = B + elevated substrate oxidation (modeled via X_DH boost)
#
# Rough literature ranges:
#   Arterial PO2: 75–100 mmHg; venous: 40 mmHg; ischemic: < 10 mmHg
#   Blood adenine nucleotides are dilute (μM range) — use 0.1 mM as proxy
#   Ischemic tissue ATP drops, ADP accumulates, Pi accumulates
#
# These are documented approximations. Used to differentiate A/B/C in
# the composite's ODE layer; addresses the Session 8 limitation that
# scenarios produced identical TW.

SCENARIO_ODE_OVERRIDES: Dict[str, Dict[str, Dict[str, float]]] = {
    'A': {  # intracellular buffer / MiR05-like in-vitro (Beard default)
        'params': {},  # no overrides
        'y0': {},      # no overrides
    },
    'B': {  # arterial blood
        'params': {'PO2': 100.0, 'Ca_c': 1e-6},           # arterial O2; slight Ca elevation
        'y0': {'sumATP_c': 0.1e-3, 'sumADP_c': 0.02e-3},  # dilute blood adenines
    },
    'C': {  # ischemic tissue — Ca²⁺ overload (ischemia literature: cyto Ca rises to 5-50 μM)
        'params': {
            'PO2': 5.0,                                   # severe hypoxia
            'Ca_c': 5e-6,                                 # ischemic cyto Ca ~5 μM (MPTP-triggering)
        },
        'y0': {
            'sumATP_c': 0.5e-3,       # ATP drops in ischemia
            'sumADP_c': 0.3e-3,       # ADP accumulates
            'sumPi_c': 2.0e-3,        # Pi accumulates
        },
    },
    'B_supplemented': {  # arterial blood + substrate supplementation
        'params': {'PO2': 100.0, 'X_DH': 0.1732 * 2.0, 'Ca_c': 1e-6},
        'y0': {'sumATP_c': 0.1e-3, 'sumADP_c': 0.02e-3},
    },
}


def apply_scenario_to_ode(scenario: str, params, y0: np.ndarray):
    """Override Beard params + initial conditions per FBA scenario semantics.

    Returns (new_params, new_y0). If scenario not recognized, returns inputs unchanged.
    """
    from dataclasses import replace
    from ode_utils import STATE_IDX  # local import to avoid circularity at module load

    overrides = SCENARIO_ODE_OVERRIDES.get(scenario)
    if overrides is None:
        return params, y0

    # Params override
    param_patch = overrides.get('params', {})
    if param_patch:
        params = replace(params, **param_patch)

    # y0 override (by state name)
    y0_patch = overrides.get('y0', {})
    if y0_patch:
        y0 = y0.copy()
        for state_name, value in y0_patch.items():
            if state_name in STATE_IDX:
                y0[STATE_IDX[state_name]] = value

    return params, y0


# ── Composite result container ─────────────────────────────────────────

@dataclass
class CompositeResult:
    """Result of one composite FBA+ODE simulation."""
    scenario: str
    times_seconds: np.ndarray
    times_hours: np.ndarray = field(init=False)
    delta_psi_trace: np.ndarray = field(default_factory=lambda: np.array([]))  # V
    atp_trace: np.ndarray = field(default_factory=lambda: np.array([]))        # matrix ATP (mol/L)
    nadh_trace: np.ndarray = field(default_factory=lambda: np.array([]))
    tw_delta_psi_hours: Optional[float] = None
    tw_atp_hours: Optional[float] = None
    first_failure_mode: Optional[str] = None  # 'delta_psi' | 'atp' | 'co_limited' | None
    capacity_envelope_traces: Optional[Dict[str, np.ndarray]] = None  # ode_rxn_id → capacity(t)
    integration_success: bool = True
    integration_message: str = ''
    notes: str = ''

    def __post_init__(self) -> None:
        self.times_hours = self.times_seconds / 3600.0


# ── Top-level composite driver ─────────────────────────────────────────

def compose_fba_ode(
    fba_model,
    beard_params,                                   # BeardParams (avoid circular type)
    halflife_map: Dict[str, float],
    scenario: str = 'A',
    t_max_hours: float = 72.0,
    dt_fba_hours: float = 1.0,
    n_eval_ode: int = 500,
    atp_threshold_fraction: float = 0.20,
    delta_psi_threshold_mV: float = -100.0,
    reaction_mapping: Dict[str, str] = FBA_ODE_REACTION_MAP,
) -> CompositeResult:
    """Run the composite FBA+ODE simulation for one scenario.

    Steps:
    1. Apply scenario bounds to FBA model.
    2. Compute baseline_fluxes (signed pFBA).
    3. Build capacity envelope function from halflife_map over t_range.
    4. Integrate Beard ODE over t_max_hours with capacity_fn coupling.
    5. Derive TW from ΔΨm threshold crossing.
    6. Compare against FBA ATP-flux threshold (Ex 5.4 mechanism partition).
    """
    from ode_utils import integrate_with_capacity, find_tw_from_delta_psi_hours, STATE_IDX, DEFAULT_Y0  # noqa: E402
    from decay_utils import get_signed_baseline_fluxes  # noqa: E402

    # Apply scenario to FBA model
    sys.path.insert(0, str(_here / "scripts" / "experiments_v2"))
    try:
        from experiment1_v2_transit_window import apply_scenario
        apply_scenario(fba_model, scenario)
    except ImportError:
        pass  # no scenario application; proceed with default model state

    # Apply scenario to ODE (Session 8.1 stretch — scenario propagation)
    y0_scenario = DEFAULT_Y0.copy()
    beard_params, y0_scenario = apply_scenario_to_ode(scenario, beard_params, y0_scenario)

    # Baseline fluxes for envelope extraction
    baseline_fluxes = get_signed_baseline_fluxes(fba_model)

    # Build capacity function
    capacity_fn = build_capacity_envelope_fn(
        fba_model, halflife_map,
        t_range_hours=(0.0, t_max_hours),
        dt_hours=dt_fba_hours,
        reaction_mapping=reaction_mapping,
        baseline_fluxes=baseline_fluxes,
    )

    # Integrate ODE with scenario-specific y0
    t_span_seconds = (0.0, t_max_hours * 3600.0)
    traj = integrate_with_capacity(
        beard_params, capacity_fn, t_span_seconds,
        y0=y0_scenario,
        n_eval=n_eval_ode,
    )

    # Extract traces
    delta_psi = traj.get('DPsi')
    atp = traj.get('sumATP_x')
    nadh = traj.get('NADH_x')

    # TW from ΔΨm threshold
    tw_dpsi_h = find_tw_from_delta_psi_hours(traj, threshold_mV=delta_psi_threshold_mV)

    # TW from ATP threshold (on cytosolic sumATP_c, which is what FBA's OF_ATP tracks)
    atp_c = traj.get('sumATP_c')
    atp_baseline = atp_c[0] if len(atp_c) > 0 else 5e-3
    atp_threshold_value = atp_baseline * atp_threshold_fraction
    below_atp = atp_c < atp_threshold_value
    if np.any(below_atp):
        tw_atp_h = float(traj.t[np.argmax(below_atp)] / 3600.0)
    else:
        tw_atp_h = None

    # Mechanism partition
    if tw_dpsi_h is None and tw_atp_h is None:
        first_failure = None
    elif tw_dpsi_h is None:
        first_failure = 'atp'
    elif tw_atp_h is None:
        first_failure = 'delta_psi'
    elif abs(tw_dpsi_h - tw_atp_h) < 0.5:  # within 30 min
        first_failure = 'co_limited'
    elif tw_dpsi_h < tw_atp_h:
        first_failure = 'delta_psi'
    else:
        first_failure = 'atp'

    # Collect capacity envelope traces for audit
    cap_traces = {
        ode_id: np.array(values)
        for ode_id, values in getattr(capacity_fn, 'envelope_by_ode_rxn', {}).items()
    }

    return CompositeResult(
        scenario=scenario,
        times_seconds=traj.t,
        delta_psi_trace=delta_psi,
        atp_trace=atp_c,
        nadh_trace=nadh,
        tw_delta_psi_hours=tw_dpsi_h,
        tw_atp_hours=tw_atp_h,
        first_failure_mode=first_failure,
        capacity_envelope_traces=cap_traces,
        integration_success=traj.success,
        integration_message=traj.message,
    )

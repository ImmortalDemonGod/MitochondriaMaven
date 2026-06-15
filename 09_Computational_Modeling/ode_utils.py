"""
ode_utils.py — ODE integration for the composite FBA+ODE model.

Implements the Beard 2005 mitochondrial OXPHOS ODE system with optional
capacity-envelope coupling (time-varying Vmax scaling from the FBA layer).

Parameters and equations sourced from
`Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py`
(Beard 2005 with Beard 2006 stoichiometry erratum corrections; pedagogical
reimplementation from Randall, Barazanji, Beard's QAMAS book).

Strategic context: `docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md`
Audit trail: `docs/investigation/COMPOSITE_AUDIT_2026-04-24.md`

State-vector convention (10 state variables; 3 conserved quantities derived):

    idx | name       | compartment | unit                       | source
    ----|------------|-------------|----------------------------|---------------
     0  | sumATP_x   | matrix      | mol/L_matrix_water         | state
     1  | sumADP_x   | matrix      | mol/L_matrix_water         | state
     2  | sumPi_x    | matrix      | mol/L_matrix_water         | state
     3  | NADH_x     | matrix      | mol/L_matrix_water         | state (NAD_x = NAD_tot - NADH_x)
     4  | QH2_x      | matrix      | mol/L_matrix_water         | state (Q_x = Q_tot - QH2_x)
     5  | cred_i     | IMS         | mol/L_IM_water             | state (cox_i = c_tot - cred_i)
     6  | sumATP_c   | cytosol     | mol/L_cyto_water           | state
     7  | sumADP_c   | cytosol     | mol/L_cyto_water           | state
     8  | sumPi_c    | cytosol     | mol/L_cyto_water           | state
     9  | DPsi       | membrane    | V                          | state

Capacity envelope convention:
    capacity_fn(t: float) -> Dict[reaction_id, fraction ∈ [0,1]]
    reaction_ids: 'C1', 'C3', 'C4', 'F1', 'ANT', 'PiC', 'DH', 'Leak'
    When None (baseline), all capacities = 1.0 (no scaling).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

import numpy as np
from scipy.integrate import solve_ivp


# ── Constants ─────────────────────────────────────────────────────────

STATE_NAMES = [
    'sumATP_x', 'sumADP_x', 'sumPi_x',
    'NADH_x', 'QH2_x', 'cred_i',
    'sumATP_c', 'sumADP_c', 'sumPi_c',
    'DPsi',
    'Ca_x',     # matrix free Ca²⁺ — Session 9 MPTP module (#51)
    'H2O2_x',   # matrix H₂O₂ (post-fast-Mn-SOD; ETC-produced superoxide dismutated instantaneously)
    'CL_ox',    # oxidized cardiolipin fraction [0,1] — Session 9 #54 (Kagan cycle)
]
N_STATES = len(STATE_NAMES)
STATE_IDX = {name: i for i, name in enumerate(STATE_NAMES)}

CAPACITY_REACTIONS = ('C1', 'C3', 'C4', 'F1', 'ANT', 'PiC', 'DH', 'Leak')


# ── Parameter container ───────────────────────────────────────────────

@dataclass
class BeardParams:
    """Beard 2005 OXPHOS model parameters.

    Defaults are from QAMAS in-vitro (isolated mito in buffer) baseline,
    at 37°C, cardiac. Override via load_beard_params(csv) or constructor
    kwargs. See Whole_Cell_Modeling/beards_lab/beard_2005_params.csv for
    per-parameter provenance.
    """
    # Biophysical constants
    R: float = 8.314
    T: float = 310.15
    F: float = 96485.0
    C_m: float = 3.1e-3
    # Volume fractions
    V_c: float = 1.0
    V_m: float = 0.0005
    W_c: float = 1.0
    W_m: float = 0.7238
    # Derived compartment volumes; override only if non-default W_m
    W_x: float = 0.65142     # 0.9 * 0.7238
    W_i: float = 0.07238     # 0.1 * 0.7238
    # Total pools
    NAD_tot: float = 2.97e-3
    Q_tot: float = 1.35e-3
    c_tot: float = 2.7e-3
    # pH + ions (fixed in in-vitro variant)
    pH_x: float = 7.40
    pH_c: float = 7.20
    K_x: float = 100e-3
    K_c: float = 140e-3
    Mg_x: float = 1.0e-3
    Mg_c: float = 1.0e-3
    # O2
    PO2: float = 25.0
    a_3: float = 1.74e-6
    k_O2: float = 1.2e-4
    # Activity parameters (the fitted set; load-bearing for composite)
    X_DH: float = 0.1732
    X_C1: float = 1.0e4
    X_C3: float = 1.0e6
    X_C4: float = 0.0125
    X_F: float = 1.0e3
    E_ANT: float = 0.325
    E_PiC: float = 5.0e6
    X_H: float = 1.0e3
    X_AtC: float = 3e-6
    # Proton stoichiometries
    n_F: float = 8.0 / 3.0
    n_C1: float = 4.0
    n_C3: float = 2.0
    n_C4: float = 4.0
    # Standard Gibbs energies (J/mol)
    DrGo_C1: float = -109680.0
    DrGo_C3: float = 46690.0
    DrGo_C4: float = -202160.0
    DrGo_F: float = 4990.0
    # NADH dehydrogenase kinetics
    r_C1: float = 6.8385
    k_Pi1: float = 4.659e-4
    k_Pi2: float = 6.578e-4
    # ANT kinetics (Metelkin 2006)
    del_D: float = 0.0167
    del_T: float = 0.0699
    k2o_ANT: float = 9.54 / 60.0
    k3o_ANT: float = 30.05 / 60.0
    K0o_D: float = 38.89e-6
    K0o_T: float = 56.05e-6
    A_ANT: float = 0.2829
    B_ANT: float = -0.2086
    C_ANT: float = 0.2372
    # PiC
    k_PiC: float = 1.61e-3
    # Dissociation constants
    K_MgATP: float = 10 ** (-3.88)
    K_MgADP: float = 10 ** (-3.00)
    K_MgPi: float = 10 ** (-1.66)
    K_HATP: float = 10 ** (-6.33)
    K_HADP: float = 10 ** (-6.26)
    K_HPi: float = 10 ** (-6.62)
    K_KATP: float = 10 ** (-1.02)
    K_KADP: float = 10 ** (-0.89)
    K_KPi: float = 10 ** (-0.42)
    # ── Non-proteomic failure mode (Session 8.2 stretch — option b scope) ──
    # Simple representation of membrane integrity decay: proton leak (X_H) grows
    # exponentially with time during extracellular storage, representing combined
    # effects of cardiolipin peroxidation, OMM permeabilization, and ROS-driven
    # direct ETC damage. Default 0 preserves pure-proteomics composite behavior.
    # Literature fragments suggest τ_membrane ≈ 2–8h at 37°C for isolated mito,
    # corresponding to leak_growth_rate ~ 0.05–0.35 /hour.
    leak_growth_rate: float = 0.0  # 1/hours; controls time-varying X_H scaling

    # ── Ca²⁺ + MPTP module (Session 9 task #51 — Bazil-Dash-style) ──
    # Matrix Ca²⁺ dynamics with MCU uptake (ΔΨm-dependent) and NCLX efflux.
    # MPTP opens with sigmoidal probability on matrix Ca²⁺; open MPTP adds
    # a large nonspecific permeability that collapses ΔΨm (bypasses F1F0).
    # Default values approximate cardiac mitochondrial Ca²⁺ handling.
    # Literature: MCU Vmax ~ 0.02 μmol/(s·mg); NCLX ~0.01; MPTP threshold
    # [Ca²⁺]_x ~ 300-500 μM (Bers lab, Bazil-Dash 2010 rat liver adapted).
    #
    # Default mptp_enabled=False preserves pre-MPTP composite behavior;
    # set to True for task #51 MPTP experiments.
    mptp_enabled: bool = False
    Ca_c: float = 0.1e-6              # cytosolic free Ca²⁺ (0.1 μM = 100 nM baseline)
    # MCU with cooperativity — more Ca → MUCH more uptake (Hill)
    V_MCU: float = 0.5e-3             # MCU Vmax (mol/(s·L_mito)) — cardiac MCU at full activity
    K_MCU_Ca: float = 20e-6           # MCU apparent half-max Ca (20 μM)
    mcu_hill: float = 2.0             # MCU Hill coefficient (cooperative Ca binding)
    # NCLX saturates at moderate matrix Ca; below-MPTP-threshold regime
    V_NCLX: float = 0.01e-3           # NCLX Vmax
    K_NCLX_Ca: float = 5e-6
    # MPTP: cardiac-sensitive threshold (Bers lab)
    Ca_MPTP_threshold: float = 100e-6  # [Ca²⁺]_x at half-open probability (100 μM cardiac)
    mptp_hill: float = 6.0            # Steep Hill for MPTP switching behavior
    mptp_permeability_max: float = 1e4  # Max proton-leak amplification when MPTP fully open

    # ── ROS module (Session 9 task #50 — Cortassa-2006-style simplified) ──
    # Lumped matrix ROS pool (treat as H₂O₂-equivalent). Produced at ETC
    # complexes (CI and CIII) as fraction of electron flow that leaks as
    # superoxide → dismutated to H₂O₂ by Mn-SOD (treated as instantaneous
    # within this lumping). Scavenged by baseline GSH-Px + MitoQ (if present).
    # ROS feedback: drives the leak_growth_rate effectively, so k_membrane
    # becomes derived from ROS dynamics rather than fitted scalar.
    #
    # Default ros_enabled=False preserves pre-ROS composite behavior.
    # Literature: Cortassa 2006; ROS leak fraction ~1-4% at baseline; MitoQ
    # k_scavenge ~ 1e8 M⁻¹s⁻¹ rate constant with [MitoQ]_mito ~ 1 μM.
    ros_enabled: bool = False
    # ROS production at ETC — fraction of electron flow leaking as superoxide
    # (immediately dismutated to H₂O₂ by fast Mn-SOD).
    # Literature: ~0.1-1% of O2 consumption appears as ROS (Brand, Balaban).
    # Beard J_C1 ~2 mM/s; 1e-3 → 2 μM/s H₂O₂ production — physiological for stressed isolated mito.
    k_ros_prod_C1: float = 1e-3       # 0.1% fraction of J_C1 electron flow as H₂O₂
    k_ros_prod_C3: float = 5e-4       # 0.05% at Complex III
    # Mn-SOD dismutates superoxide → H₂O₂ (very fast; pseudo-first-order).
    # Literature: [Mn-SOD] ~10 μM in matrix, k_cat ~1e9 M⁻¹s⁻¹ → pseudo-k_SOD ~1e4/s.
    k_SOD: float = 1e4                # Mn-SOD effective first-order rate on O2s
    # H2O2 scavenging: GSH-Px + peroxiredoxin lumped; ~1-10/s physiological.
    k_H2O2_scavenge: float = 10.0
    mitoq_concentration: float = 0.0  # effective matrix [MitoQ] in mol/L
    k_mitoq_scavenge: float = 1e7     # MitoQ × H₂O₂ scavenging rate constant (M⁻¹·s⁻¹)
    # Cardiolipin pool + Kagan cycle parameters (Session 9 #54).
    # Kagan mechanism: cyt c (cox_i proxy for CL-bound peroxidase form) uses H₂O₂ to
    # peroxidize adjacent cardiolipin. Rate = k_kagan × [cox_i] × [H2O2] × (1-CL_ox).
    # Calibrated so cardiac mito reach CL_ox ~30-50% over 4-12h of storage, matching
    # Kagan lab published cardiolipin oxidation time courses.
    # In reality only ~5% of cyt c is CL-bound and thus peroxidase-active; k_kagan
    # is effective rate constant reflecting this. Lower than strict enzyme kcat to
    # allow MitoQ scavenging to compete meaningfully.
    k_kagan: float = 1e5              # effective Kagan CL peroxidation rate (M⁻²·s⁻¹)
    CL_leak_max_fold: float = 20.0    # max proton-leak amplification at full CL_ox (reduced from 50 for numerical stability)

    # Derived quantities (not dataclass fields; properties)
    @property
    def H_x(self) -> float:
        return 10.0 ** (-self.pH_x)

    @property
    def H_c(self) -> float:
        return 10.0 ** (-self.pH_c)

    @property
    def O2_x(self) -> float:
        return self.a_3 * self.PO2

    @property
    def V_m2c(self) -> float:
        return self.V_m / self.V_c


# ── Default initial conditions (from QAMAS in-vitro) ────────────────────

DEFAULT_Y0 = np.array([
    0.5e-3,           # sumATP_x
    9.5e-3,           # sumADP_x
    0.3e-3,           # sumPi_x
    0.1 * 2.97e-3,    # NADH_x (10% reduced)
    0.1 * 1.35e-3,    # QH2_x (10% reduced)
    0.1 * 2.7e-3,     # cred_i (10% reduced)
    5e-3,             # sumATP_c
    0.0,              # sumADP_c (starts empty; ANT builds pool)
    1.0e-3,           # sumPi_c (low-Pi baseline)
    175e-3,           # DPsi (175 mV initial guess)
    0.1e-6,           # Ca_x (100 nM baseline matrix free Ca²⁺)
    1e-8,             # H2O2_x (10 nM baseline matrix H₂O₂ — ETC→O2s→Mn-SOD chain lumped)
    0.0,              # CL_ox (fractional cardiolipin oxidation — starts intact)
])


# ── ODE RHS ───────────────────────────────────────────────────────────

def beard_rhs(
    t: float,
    y: np.ndarray,
    params: BeardParams,
    capacity_fn: Optional[Callable[[float], Dict[str, float]]] = None,
) -> np.ndarray:
    """Beard 2005 RHS with optional capacity-envelope coupling.

    Returns dy/dt as a length-N_STATES array.

    When capacity_fn is None, reproduces the baseline Beard 2005 dynamics
    (no FBA coupling) — this is the mode used for Ex 5.1 validation.
    """
    # Unpack state
    (sumATP_x, sumADP_x, sumPi_x,
     NADH_x, QH2_x, cred_i,
     sumATP_c, sumADP_c, sumPi_c,
     DPsi, Ca_x, H2O2_x, CL_ox) = y

    p = params  # alias

    # Conserved quantities (derived)
    NAD_x = p.NAD_tot - NADH_x
    Q_x = p.Q_tot - QH2_x
    cox_i = p.c_tot - cred_i

    # Capacity scaling (1.0 = no perturbation)
    if capacity_fn is None:
        cap_C1 = cap_C3 = cap_C4 = cap_F1 = cap_ANT = cap_PiC = cap_DH = cap_Leak = 1.0
    else:
        cap = capacity_fn(t)
        cap_C1 = cap.get('C1', 1.0)
        cap_C3 = cap.get('C3', 1.0)
        cap_C4 = cap.get('C4', 1.0)
        cap_F1 = cap.get('F1', 1.0)
        cap_ANT = cap.get('ANT', 1.0)
        cap_PiC = cap.get('PiC', 1.0)
        cap_DH = cap.get('DH', 1.0)
        cap_Leak = cap.get('Leak', 1.0)

    # Binding polynomials (matrix)
    PATP_x = 1 + p.H_x / p.K_HATP + p.Mg_x / p.K_MgATP + p.K_x / p.K_KATP
    PADP_x = 1 + p.H_x / p.K_HADP + p.Mg_x / p.K_MgADP + p.K_x / p.K_KADP
    PPi_x = 1 + p.H_x / p.K_HPi + p.Mg_x / p.K_MgPi + p.K_x / p.K_KPi
    # Cytosol binding polynomials
    PATP_c = 1 + p.H_c / p.K_HATP + p.Mg_c / p.K_MgATP + p.K_c / p.K_KATP
    PADP_c = 1 + p.H_c / p.K_HADP + p.Mg_c / p.K_MgADP + p.K_c / p.K_KADP
    PPi_c = 1 + p.H_c / p.K_HPi + p.Mg_c / p.K_MgPi + p.K_c / p.K_KPi

    # Unbound species
    ATP_x = sumATP_x / PATP_x
    ADP_x = sumADP_x / PADP_x
    Pi_x = sumPi_x / PPi_x
    ATP_c = sumATP_c / PATP_c
    ADP_c = sumADP_c / PADP_c
    Pi_c = sumPi_c / PPi_c

    # NADH dehydrogenase
    J_DH = (cap_DH * p.X_DH *
            (p.r_C1 * NAD_x - NADH_x) *
            ((1 + sumPi_x / p.k_Pi1) / (1 + sumPi_x / p.k_Pi2)))

    # Complex I: NADH_x + Q_x -> NAD_x + QH2_x + 4 H+ (pumped)
    DrGapp_C1 = p.DrGo_C1 - p.R * p.T * np.log(p.H_x)
    Kapp_C1 = (np.exp(-(DrGapp_C1 + p.n_C1 * p.F * DPsi) / (p.R * p.T))
               * (p.H_x / p.H_c) ** p.n_C1)
    J_C1 = cap_C1 * p.X_C1 * (Kapp_C1 * NADH_x * Q_x - NAD_x * QH2_x)

    # Complex III
    DrGapp_C3 = p.DrGo_C3 + 2 * p.R * p.T * np.log(p.H_c)
    Kapp_C3 = (np.exp(-(DrGapp_C3 + p.n_C3 * p.F * DPsi) / (p.R * p.T))
               * (p.H_x / p.H_c) ** p.n_C3)
    J_C3 = cap_C3 * p.X_C3 * (Kapp_C3 * cox_i ** 2 * QH2_x - cred_i ** 2 * Q_x)

    # Complex IV
    DrGapp_C4 = p.DrGo_C4 - 2 * p.R * p.T * np.log(p.H_c)
    Kapp_C4 = (np.exp(-(DrGapp_C4 + p.n_C4 * p.F * DPsi) / (p.R * p.T))
               * (p.H_x / p.H_c) ** p.n_C4)
    J_C4 = (cap_C4 * p.X_C4 *
            (np.sqrt(max(Kapp_C4, 0)) * cred_i * p.O2_x ** 0.25 - cox_i) *
            (1.0 / (1.0 + p.k_O2 / p.O2_x)))

    # F1F0 ATP synthase: ADP + Pi + n_F DPsi -> ATP
    DrGapp_F = p.DrGo_F + p.R * p.T * np.log(p.H_x * PATP_x / (PADP_x * PPi_x))
    Kapp_F = (np.exp((DrGapp_F + p.n_F * p.F * DPsi) / (p.R * p.T))
              * (p.H_c / p.H_x) ** p.n_F)
    J_F1 = cap_F1 * p.X_F * (Kapp_F * sumADP_x * sumPi_x - sumATP_x)

    # ANT (Metelkin 2006 kinetics)
    phi = p.F * DPsi / (p.R * p.T)
    k2_ANT = p.k2o_ANT * np.exp((p.A_ANT * (-3) + p.B_ANT * (-4) + p.C_ANT) * phi)
    k3_ANT = p.k3o_ANT * np.exp((p.A_ANT * (-4) + p.B_ANT * (-3) + p.C_ANT) * phi)
    K0_D = p.K0o_D * np.exp(3 * p.del_D * phi)
    K0_T = p.K0o_T * np.exp(4 * p.del_T * phi)
    q = k3_ANT * K0_D * np.exp(phi) / (k2_ANT * K0_T)
    ANT_num = (k2_ANT * ATP_x * ADP_c * q / K0_D
               - k3_ANT * ADP_x * ATP_c / K0_T)
    ANT_den = (1 + ATP_c / K0_T + ADP_c / K0_D) * (ADP_x + ATP_x * q)
    J_ANT = cap_ANT * p.E_ANT * ANT_num / ANT_den

    # Phosphate carrier (H+ symport)
    HPi_c = Pi_c * (p.H_c / p.K_HPi)
    HPi_x = Pi_x * (p.H_x / p.K_HPi)
    J_PiC = cap_PiC * p.E_PiC * (p.H_c * HPi_c - p.H_x * HPi_x) / (p.k_PiC + HPi_c)

    # Proton leak amplification driven by oxidized cardiolipin fraction (Kagan mechanism).
    # leak_multiplier = 1 + CL_leak_max_fold * CL_ox_fraction (saturates at CL_ox=1).
    # This replaces the generic Damage state with a CL-specific, Kagan-cycle-derived rate.
    # When ros_enabled=False, CL_ox stays at 0 and leak_multiplier ≡ 1.
    cl_ox_clipped = max(min(CL_ox, 1.0), 0.0)
    leak_multiplier = 1.0 + p.CL_leak_max_fold * cl_ox_clipped

    # MPTP opening probability (Session 9 task #51) — sigmoidal on matrix Ca²⁺.
    # When MPTP opens, adds a large nonspecific permeability that short-circuits PMF.
    # Implemented as an additional multiplicative factor on proton leak:
    #   mptp_factor = 1 + mptp_open_prob * mptp_permeability_max
    # Default mptp_enabled=False → factor ≡ 1, preserves pre-MPTP behavior.
    if p.mptp_enabled:
        # Hill function: p_open = Ca_x^n / (Ca_x^n + K^n)
        ca_clipped = max(Ca_x, 0.0)
        num = ca_clipped ** p.mptp_hill
        den = num + p.Ca_MPTP_threshold ** p.mptp_hill
        mptp_open_prob = num / den if den > 0 else 0.0
        mptp_factor = 1.0 + mptp_open_prob * p.mptp_permeability_max
    else:
        mptp_open_prob = 0.0
        mptp_factor = 1.0

    J_leak = cap_Leak * p.X_H * leak_multiplier * mptp_factor * (p.H_c * np.exp(phi / 2) - p.H_x * np.exp(-phi / 2))

    # MCU (Ca²⁺ uniporter) uptake — Hill-cooperative in cyto Ca²⁺, ΔΨm-driven.
    # J_MCU = V_MCU * Hill(Ca_c) * ΔΨm-driving-factor
    # ΔΨm-factor drops as ΔΨm collapses (MCU thermodynamically inactive without PMF).
    if p.mptp_enabled:
        dpsi_factor = max(DPsi, 0) / 0.175
        ca_c_h = p.Ca_c ** p.mcu_hill
        k_mcu_h = p.K_MCU_Ca ** p.mcu_hill
        J_MCU = p.V_MCU * ca_c_h / (ca_c_h + k_mcu_h) * dpsi_factor
        # NCLX (Ca²⁺ efflux) — Michaelis-Menten in matrix Ca²⁺
        J_NCLX = p.V_NCLX * max(Ca_x, 0) / (max(Ca_x, 0) + p.K_NCLX_Ca)
    else:
        J_MCU = 0.0
        J_NCLX = 0.0

    # Cytosolic ATPase (fixed-rate hydrolysis sink)
    J_AtC = p.X_AtC  # mol/(s * L_cuvette)

    # ─── Mass balances ─────────────────────────────────────────────
    # Matrix: divide by W_x to convert mol/(s*L_mito) -> mol/(s*L_matrix_water)
    dsumATP_x = (J_F1 - J_ANT) / p.W_x
    dsumADP_x = (-J_F1 + J_ANT) / p.W_x
    dsumPi_x = (-J_F1 + J_PiC) / p.W_x
    dNADH_x = (J_DH - J_C1) / p.W_x
    dQH2_x = (J_C1 - J_C3) / p.W_x

    # IMS: cyt c reduction = 2*J_C3 (produces cred_i) - 2*J_C4 (consumes cred_i)
    dcred_i = (2 * J_C3 - 2 * J_C4) / p.W_i

    # Cytosol: fluxes in mol/(s*L_mito) * V_m2c -> mol/(s*L_cuvette);
    # divide by W_c to get mol/(s*L_cuvette_water).
    # J_AtC already in mol/(s*L_cuvette), so divide by V_c*W_c (V_c=1 in this setup).
    dsumATP_c = (J_ANT * p.V_m2c / p.W_c) - (J_AtC / (p.V_c * p.W_c))
    dsumADP_c = -(J_ANT * p.V_m2c / p.W_c) + (J_AtC / (p.V_c * p.W_c))
    dsumPi_c = -(J_PiC * p.V_m2c / p.W_c) + (J_AtC / (p.V_c * p.W_c))

    # Membrane potential balance:
    # Positive: proton pumping by C1, C3, C4. Negative: F1F0 consumption, ANT (1 charge out), leak.
    # MCU uptakes Ca²⁺ (2+ charge in) consumes DPsi; NCLX electroneutral (no DPsi effect).
    dDPsi = (p.n_C1 * J_C1 + p.n_C3 * J_C3 + p.n_C4 * J_C4
             - p.n_F * J_F1 - J_ANT - J_leak - 2 * J_MCU) / p.C_m

    # Ca²⁺ dynamics (MPTP module)
    dCa_x = (J_MCU - J_NCLX) / p.W_x

    # H₂O₂ + cardiolipin dynamics (Session 9 #50 + #54 — Kagan cycle)
    # Mn-SOD is fast enough (kcat × [SOD] ~ 10⁴/s) that superoxide is quasi-instantaneously
    # dismutated to H₂O₂; we lump O2s production + SOD into direct H₂O₂ production.
    if p.ros_enabled:
        # Direct H₂O₂ production from ETC (O2s produced then instantly dismutated)
        J_H2O2_prod = (p.k_ros_prod_C1 * max(J_C1, 0.0)
                       + p.k_ros_prod_C3 * max(J_C3, 0.0))
        # Scavenging: GSH-Px + MitoQ
        J_H2O2_scavenge = (p.k_H2O2_scavenge * max(H2O2_x, 0.0)
                           + p.k_mitoq_scavenge * p.mitoq_concentration * max(H2O2_x, 0.0))
        # Kagan cycle flux: cyt c (cox_i proxy for CL-bound peroxidase) × H2O2 × available CL
        J_Kagan = p.k_kagan * max(cox_i, 0.0) * max(H2O2_x, 0.0) * (1.0 - cl_ox_clipped)
        dH2O2_x = (J_H2O2_prod / p.W_x) - J_H2O2_scavenge - J_Kagan
        dCL_ox = J_Kagan
    else:
        dH2O2_x = 0.0
        dCL_ox = 0.0

    # Backwards-compat: leak_growth_rate (option b.1 phenomenological) still available
    if p.leak_growth_rate > 0:
        dCL_ox = dCL_ox + (p.leak_growth_rate / 3600.0) * (1.0 - cl_ox_clipped)

    return np.array([dsumATP_x, dsumADP_x, dsumPi_x,
                     dNADH_x, dQH2_x, dcred_i,
                     dsumATP_c, dsumADP_c, dsumPi_c,
                     dDPsi, dCa_x, dH2O2_x, dCL_ox])


# ── Fluxes at a state (for analysis, not integration) ──────────────────

def compute_fluxes(y: np.ndarray, params: BeardParams,
                   capacity_fn: Optional[Callable[[float], Dict[str, float]]] = None,
                   t: float = 0.0) -> Dict[str, float]:
    """Return a dict of all named fluxes at state y.

    Unit: mol/(s*L_mito). For J_O2 see j_o2_from_fluxes.
    """
    # Reuse logic from beard_rhs; duplicated for clarity since we want
    # the fluxes directly, not just derivatives.
    (sumATP_x, sumADP_x, sumPi_x,
     NADH_x, QH2_x, cred_i,
     sumATP_c, sumADP_c, sumPi_c,
     DPsi, Ca_x, H2O2_x, CL_ox) = y
    p = params
    NAD_x = p.NAD_tot - NADH_x
    Q_x = p.Q_tot - QH2_x
    cox_i = p.c_tot - cred_i

    if capacity_fn is None:
        caps = {k: 1.0 for k in CAPACITY_REACTIONS}
    else:
        caps = {k: 1.0 for k in CAPACITY_REACTIONS}
        caps.update(capacity_fn(t))

    PATP_x = 1 + p.H_x / p.K_HATP + p.Mg_x / p.K_MgATP + p.K_x / p.K_KATP
    PADP_x = 1 + p.H_x / p.K_HADP + p.Mg_x / p.K_MgADP + p.K_x / p.K_KADP
    PPi_x = 1 + p.H_x / p.K_HPi + p.Mg_x / p.K_MgPi + p.K_x / p.K_KPi
    PATP_c = 1 + p.H_c / p.K_HATP + p.Mg_c / p.K_MgATP + p.K_c / p.K_KATP
    PADP_c = 1 + p.H_c / p.K_HADP + p.Mg_c / p.K_MgADP + p.K_c / p.K_KADP
    PPi_c = 1 + p.H_c / p.K_HPi + p.Mg_c / p.K_MgPi + p.K_c / p.K_KPi

    ATP_x = sumATP_x / PATP_x; ADP_x = sumADP_x / PADP_x; Pi_x = sumPi_x / PPi_x
    ATP_c = sumATP_c / PATP_c; ADP_c = sumADP_c / PADP_c; Pi_c = sumPi_c / PPi_c

    J_DH = caps['DH'] * p.X_DH * (p.r_C1 * NAD_x - NADH_x) * ((1 + sumPi_x / p.k_Pi1) / (1 + sumPi_x / p.k_Pi2))
    DrGapp_C1 = p.DrGo_C1 - p.R * p.T * np.log(p.H_x)
    Kapp_C1 = np.exp(-(DrGapp_C1 + p.n_C1 * p.F * DPsi) / (p.R * p.T)) * (p.H_x / p.H_c) ** p.n_C1
    J_C1 = caps['C1'] * p.X_C1 * (Kapp_C1 * NADH_x * Q_x - NAD_x * QH2_x)
    DrGapp_C3 = p.DrGo_C3 + 2 * p.R * p.T * np.log(p.H_c)
    Kapp_C3 = np.exp(-(DrGapp_C3 + p.n_C3 * p.F * DPsi) / (p.R * p.T)) * (p.H_x / p.H_c) ** p.n_C3
    J_C3 = caps['C3'] * p.X_C3 * (Kapp_C3 * cox_i ** 2 * QH2_x - cred_i ** 2 * Q_x)
    DrGapp_C4 = p.DrGo_C4 - 2 * p.R * p.T * np.log(p.H_c)
    Kapp_C4 = np.exp(-(DrGapp_C4 + p.n_C4 * p.F * DPsi) / (p.R * p.T)) * (p.H_x / p.H_c) ** p.n_C4
    J_C4 = caps['C4'] * p.X_C4 * (np.sqrt(max(Kapp_C4, 0)) * cred_i * p.O2_x ** 0.25 - cox_i) * (1.0 / (1.0 + p.k_O2 / p.O2_x))
    DrGapp_F = p.DrGo_F + p.R * p.T * np.log(p.H_x * PATP_x / (PADP_x * PPi_x))
    Kapp_F = np.exp((DrGapp_F + p.n_F * p.F * DPsi) / (p.R * p.T)) * (p.H_c / p.H_x) ** p.n_F
    J_F1 = caps['F1'] * p.X_F * (Kapp_F * sumADP_x * sumPi_x - sumATP_x)
    phi = p.F * DPsi / (p.R * p.T)
    k2_ANT = p.k2o_ANT * np.exp((p.A_ANT * (-3) + p.B_ANT * (-4) + p.C_ANT) * phi)
    k3_ANT = p.k3o_ANT * np.exp((p.A_ANT * (-4) + p.B_ANT * (-3) + p.C_ANT) * phi)
    K0_D = p.K0o_D * np.exp(3 * p.del_D * phi)
    K0_T = p.K0o_T * np.exp(4 * p.del_T * phi)
    q = k3_ANT * K0_D * np.exp(phi) / (k2_ANT * K0_T)
    ANT_num = k2_ANT * ATP_x * ADP_c * q / K0_D - k3_ANT * ADP_x * ATP_c / K0_T
    ANT_den = (1 + ATP_c / K0_T + ADP_c / K0_D) * (ADP_x + ATP_x * q)
    J_ANT = caps['ANT'] * p.E_ANT * ANT_num / ANT_den
    HPi_c = Pi_c * (p.H_c / p.K_HPi); HPi_x = Pi_x * (p.H_x / p.K_HPi)
    J_PiC = caps['PiC'] * p.E_PiC * (p.H_c * HPi_c - p.H_x * HPi_x) / (p.k_PiC + HPi_c)
    t_hours = t / 3600.0
    MEMBRANE_MAX_FOLD = 50.0
    if p.leak_growth_rate > 0:
        leak_multiplier = 1.0 + MEMBRANE_MAX_FOLD * (1.0 - np.exp(-p.leak_growth_rate * t_hours))
    else:
        leak_multiplier = 1.0
    J_leak = caps['Leak'] * p.X_H * leak_multiplier * (p.H_c * np.exp(phi / 2) - p.H_x * np.exp(-phi / 2))

    return {
        'J_DH': J_DH, 'J_C1': J_C1, 'J_C3': J_C3, 'J_C4': J_C4,
        'J_F1': J_F1, 'J_ANT': J_ANT, 'J_PiC': J_PiC, 'J_leak': J_leak,
    }


def j_o2_from_c4(J_C4: float) -> float:
    """Convert Complex IV flux to oxygen consumption (QAMAS convention).

    Returns O2 flux in nmol O2 / (min * Unit-CS), matching Beard/QAMAS figures.
    Factor: J_C4 / 2 (stoichiometry 0.5 O2 per cyt-c cycle, two electron) * 60 * 1e9 * 1.2232e-6
    """
    return J_C4 / 2 * 60 * 1e9 * 0.0000012232


# ── Integration wrappers ──────────────────────────────────────────────

@dataclass
class Trajectory:
    t: np.ndarray                    # shape (n_t,)
    y: np.ndarray                    # shape (n_states, n_t)
    state_names: Tuple[str, ...]
    success: bool
    message: str

    def get(self, name: str) -> np.ndarray:
        return self.y[STATE_IDX[name]]

    @property
    def delta_psi_mV(self) -> np.ndarray:
        return self.get('DPsi') * 1000.0


def integrate_baseline(params: BeardParams, t_span: Tuple[float, float],
                       y0: Optional[np.ndarray] = None,
                       n_eval: int = 500,
                       rtol: float = 1e-6, atol: float = 1e-9) -> Trajectory:
    """Integrate Beard baseline (no FBA coupling) over t_span (seconds).

    Uses scipy.integrate.solve_ivp with LSODA (stiff-capable).
    """
    if y0 is None:
        y0 = DEFAULT_Y0.copy()
    t_eval = np.linspace(t_span[0], t_span[1], n_eval)
    sol = solve_ivp(
        beard_rhs, t_span, y0,
        method='LSODA',
        t_eval=t_eval,
        args=(params, None),
        rtol=rtol, atol=atol,
    )
    return Trajectory(t=sol.t, y=sol.y, state_names=tuple(STATE_NAMES),
                      success=sol.success, message=sol.message)


def integrate_with_capacity(params: BeardParams,
                            capacity_fn: Callable[[float], Dict[str, float]],
                            t_span: Tuple[float, float],
                            y0: Optional[np.ndarray] = None,
                            n_eval: int = 500,
                            rtol: float = 1e-6, atol: float = 1e-9) -> Trajectory:
    """Integrate Beard with time-varying capacity envelope over t_span."""
    if y0 is None:
        y0 = DEFAULT_Y0.copy()
    t_eval = np.linspace(t_span[0], t_span[1], n_eval)
    sol = solve_ivp(
        beard_rhs, t_span, y0,
        method='LSODA',
        t_eval=t_eval,
        args=(params, capacity_fn),
        rtol=rtol, atol=atol,
    )
    return Trajectory(t=sol.t, y=sol.y, state_names=tuple(STATE_NAMES),
                      success=sol.success, message=sol.message)


# ── Transit window derivation ─────────────────────────────────────────

def find_tw_from_delta_psi(traj: Trajectory, threshold_mV: float = -100.0) -> Optional[float]:
    """Return first time (seconds) where ΔΨm magnitude falls below threshold.

    Note: Beard uses positive DPsi convention (~175 mV baseline). Below
    threshold means less negative than -100 mV, i.e. DPsi < 100 mV
    (absolute value interpretation). We report TW when |DPsi|*1000 < |threshold_mV|.

    Returns None if threshold not crossed within t_span.
    """
    dpsi_mV = traj.delta_psi_mV            # baseline ~+175 mV
    # Threshold crossing: |DPsi| falls below |threshold_mV|
    below = np.abs(dpsi_mV) < abs(threshold_mV)
    if not np.any(below):
        return None
    return float(traj.t[np.argmax(below)])


def find_tw_from_delta_psi_hours(traj: Trajectory, threshold_mV: float = -100.0) -> Optional[float]:
    """Same as find_tw_from_delta_psi but returns hours."""
    tw_s = find_tw_from_delta_psi(traj, threshold_mV)
    if tw_s is None:
        return None
    return tw_s / 3600.0


# ── Parameter CSV loader ──────────────────────────────────────────────

def load_beard_params(param_file: Path) -> BeardParams:
    """Load parameters from CSV with (name, value, ...) columns into BeardParams.

    Only parameters with names matching BeardParams field names are loaded;
    unknown names (e.g., auxiliary documentation rows) are silently skipped.
    Derived fields (H_x, H_c, O2_x, V_m2c) are properties and cannot be
    loaded; their source parameters (pH_x, pH_c, a_3, PO2, V_m, V_c) are.
    """
    valid_field_names = {f.name for f in fields(BeardParams)}
    kwargs = {}
    with open(param_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('name', '').strip()
            if name in valid_field_names:
                try:
                    kwargs[name] = float(row['value'])
                except (ValueError, KeyError):
                    continue
    return BeardParams(**kwargs)


def default_param_file() -> Path:
    """Canonical path to beard_2005_params.csv (via paths.py if available)."""
    try:
        from paths import BEARD_DIR
        return BEARD_DIR / "beard_2005_params.csv"
    except ImportError:
        return Path(__file__).resolve().parent / "Whole_Cell_Modeling" / "beards_lab" / "beard_2005_params.csv"

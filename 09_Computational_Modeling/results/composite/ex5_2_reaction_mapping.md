# Ex 5.2 — FBA ↔ ODE Reaction Mapping Audit

**Generated:** 2026-04-24 during Ex 5.2 execution
**Scope:** Composite FBA+ODE coupling — manual unit/sign checks for the three
deep-dive couplings per plan Constraint 2 (small-N named deep dives).

## Full mapping

| FBA reaction (MitoMAMMAL) | ODE reaction (Beard 2005) | Mapping type |
|---|---|---|
| CI_mitoMap   | C1   | ETC complex |
| CIII_mitoMap | C3   | ETC complex |
| CIV_mitoMap  | C4   | ETC complex |
| CV_mitoMap   | F1   | ATP synthase |
| ATPtmB_mitoMap | ANT | Carrier |
| PIt2mB_mitoMap | PiC | Carrier |

## Deep dive: CI_mitoMap ↔ J_C1

**FBA side:** `CI_mitoMap` is MitoMAMMAL's Complex I rate expression,
carrying a 39-subunit AND-clause (Phase G.1 order-statistics finding).
GPR-aware decay returns a capacity fraction that reflects the minimum
remaining fraction across all 39 subunits (stripped of alternative-species
ENSG genes). Stoichiometry: NADH + Q → NAD + QH2 + 4 H+ (pumped).

**ODE side:** `J_C1` in Beard/QAMAS is `X_C1 * (Kapp_C1 * NADH_x * Q_x - NAD_x * QH2_x)`.
X_C1 is the activity parameter; multiplying it by `cap_C1` scales the Vmax
without touching the thermodynamic equilibrium constant Kapp_C1.

**Mechanism check:** Enzyme subunit decay reduces [active enzyme]. At fixed
[NADH], [Q] this linearly reduces J_C1 via Vmax scaling. Km is not part of
the Beard C1 rate expression (it's thermodynamic, not saturable), so no
Km adjustment is needed. ✓

**Unit check:** `cap_C1` is dimensionless [0,1]. X_C1 units are mol/(s·L_mito).
Scaled Vmax remains mol/(s·L_mito). ✓

**Sign check:** At t=0, cap_C1 = 1.0 → no effect → reproduces Beard baseline. ✓

## Deep dive: CV_mitoMap ↔ J_F1

**FBA side:** `CV_mitoMap` is the F1F0 ATP synthase rate expression. Its
GPR-aware capacity represents ATP synthase availability.

**ODE side:** `J_F1 = X_F * (Kapp_F * sumADP_x * sumPi_x - sumATP_x)`. Scaling
X_F via cap_F1 represents the reduced number of functional ATP synthase
complexes, directly analogous to Vmax reduction.

**Mechanism check:** ATP synthase operates near equilibrium; the thermodynamic
driving force `Kapp_F` depends on DPsi and pH gradient, independent of enzyme
count. Capacity scaling correctly modulates only the forward/reverse rate
amplitude, not the equilibrium point. ✓

**Load-bearing:** This coupling is what tests the "ΔΨm collapse is kinetically
derived" thesis — when CV capacity drops, F1F0 cannot consume PMF as fast,
so DPsi maintains higher longer; when capacity of ETC complexes (C1/C3/C4)
also drops, PMF generation drops as well. Which declines faster determines
whether DPsi collapses (kinetic ODE failure) or ATP supply drops (proteomics-
limited FBA failure).

## Deep dive: ATPtmB_mitoMap ↔ J_ANT

**FBA side:** `ATPtmB_mitoMap` is the ATP/ADP translocase (ANT). MitoMAMMAL
assigns the SLC25A4/5/6 family genes as its GPR.

**ODE side:** `J_ANT` in Beard/QAMAS uses the Metelkin 2006 kinetic formulation:
voltage-dependent rate constants k2_ANT, k3_ANT, dissociation constants K0_D,
K0_T, and a quotient q. The overall Vmax-equivalent prefactor is E_ANT (ANT
"expression level"). Scaling E_ANT via cap_ANT represents reduced ANT
copy number.

**Mechanism check:** The Metelkin formulation is asymmetric in ATP/ADP
(reflecting the 4-charge vs 3-charge translocation). Capacity scaling
applies equally to both "forward" and "reverse" translocation, which is
correct under the assumption that decay affects entire protein copies, not
just one direction of transport. ✓

**Load-bearing:** ANT is often the kinetic bottleneck in isolated mito
systems; if its capacity drops faster than CI/CIII/CIV/CV, ATP cannot
be exported to cytosol even when matrix ATP stays high — this would
show up as `TW_atp` < `TW_delta_psi` (proteomics-limited failure).

## Notes on non-mapped reactions

- **DH** (NADH dehydrogenase substrate feed in Beard) has no direct FBA
  analog in MitoMAMMAL — it represents upstream substrate oxidation
  (TCA cycle feeding NADH pool). Defaults to cap=1.0 in the composite.
- **Leak** (nonspecific proton leak) is not a FBA reaction in MitoMAMMAL.
  Defaults to cap=1.0.
- **CII_mitoMap** is not in Beard 2005 (Beard doesn't model succinate-driven
  respiration). In the composite, CII's FBA-layer decay doesn't feed into
  ODE dynamics — this is a documented limitation for option (c).

## Conclusion

Mapping is consistent under the Michaelis-Menten "enzyme fraction → Vmax"
interpretation of capacity. No Km or thermodynamic-equilibrium parameter
adjustments are needed. The three deep-dive couplings are manually
verified: units align, signs align, baseline (t=0) reproduces uncoupled
Beard dynamics.

"""Ex 5.6 — Literature-Sourced Sensitivity Propagation.

Hypothesis: TW 95% CI derived from real literature parameter uncertainty
has defensible provenance and is wider than the ±30% arbitrary jitter in
the pure-FBA bootstrap, but narrow enough to be interpretable.

Method:
1. Select ~8 load-bearing parameters with literature-sourced uncertainty ranges.
2. Latin hypercube sample N=100 from joint uncertainty.
3. Run composite simulation for each sample; record TW_ΔΨm, TW_ATP.
4. Report 95% CI from percentiles.
5. One-at-a-time sensitivity: hold others at central, sweep each across its range.

Outputs:
    results/composite/ex5_6_sensitivity.csv — all N=100 draws with TW results
    results/composite/ex5_6_sensitivity_tornado.png — one-at-a-time tornado plot
"""

from __future__ import annotations

import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent]:
    if (_p / "paths.py").exists():
        sys.path.insert(0, str(_p))
        break

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cobra
from scipy.stats import qmc

from paths import MODEL_PATH, RESULTS_COMPOSITE
from ode_utils import BeardParams
from composite_utils import compose_fba_ode
from decay_utils import configure_atp_objective, MT_ENCODED_IDS

# ── Parameters with literature-sourced uncertainty ranges ──────────
# Each entry: (name, central, relative_uncertainty, provenance_note)
# Central values from beard_2005_params.csv; uncertainties estimated from
# Beard 2005 paper text (fitted-parameter uncertainties reported as 20–40%
# depending on parameter), and halflife uncertainty from the still-disputed
# 30× acceleration factor.

PARAMS_UNCERTAINTY = [
    # (name, central, relative_sigma, source_note)
    ('X_C1',  1.0e4,    0.30, 'Beard 2005 fitted; ~30% typical for activity params'),
    ('X_C3',  1.0e6,    0.30, 'Beard 2005 fitted'),
    ('X_C4',  0.0125,   0.40, 'Beard 2005 fitted; more uncertain (alone-fitted)'),
    ('X_F',   1.0e3,    0.30, 'Beard 2005 fitted'),
    ('E_ANT', 0.325,    0.25, 'Beard 2005 / Metelkin 2006; tighter constraint'),
    ('E_PiC', 5.0e6,    0.30, 'Beard 2005 fitted'),
    ('X_H',   1.0e3,    0.40, 'Beard 2005 proton-leak parameter; large uncertainty'),
    ('halflife_hours', 4.7, 0.50, '30× acceleration factor itself is fitted — widest uncertainty'),
]

N_LATIN = 60                       # sample count (reduced from 100 for speed; still ≥ 50 for percentile stability)
SCENARIO = 'A'
T_MAX_HOURS = 144.0                # extended to catch ΔΨm threshold for most samples


def latin_hypercube_samples(n: int, seed: int = 42) -> np.ndarray:
    """Return n × k array of samples in [0, 1] for k parameters."""
    k = len(PARAMS_UNCERTAINTY)
    sampler = qmc.LatinHypercube(d=k, seed=seed)
    return sampler.random(n=n)


def scale_samples_to_params(samples: np.ndarray) -> list[dict]:
    """Convert [0,1] Latin-hypercube samples to parameter dicts.

    Interpret each column as: central × exp(sigma * z) where z maps
    [0,1] → [-3, 3] via inverse-normal. This gives log-normal uncertainty,
    which is standard for rate constants / halflives.
    """
    from scipy.stats import norm
    result = []
    for sample_row in samples:
        d = {}
        for (name, central, rel_sigma, _), u in zip(PARAMS_UNCERTAINTY, sample_row):
            z = norm.ppf(max(min(u, 0.999), 0.001))  # clip to avoid infinity
            d[name] = central * np.exp(rel_sigma * z)
        result.append(d)
    return result


def build_params_and_halflife(sample: dict, model) -> tuple[BeardParams, dict]:
    p = BeardParams()
    for key, val in sample.items():
        if key == 'halflife_hours':
            continue
        setattr(p, key, val)
    halflife_hours = sample['halflife_hours']
    halflife_map = {
        g.id: (1e9 if g.id in MT_ENCODED_IDS else halflife_hours)
        for g in model.genes
    }
    return p, halflife_map


def run_sensitivity_batch():
    print("=" * 68)
    print(f"Ex 5.6 — Latin-hypercube sensitivity (N={N_LATIN}) on composite TW")
    print("=" * 68)
    print(f"Scenario: {SCENARIO} | T_MAX: {T_MAX_HOURS}h | Parameters:")
    for name, central, sigma, source in PARAMS_UNCERTAINTY:
        print(f"  {name:20s} = {central:.4g} (σ_rel={sigma:.2f}) — {source}")
    print()

    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)

    samples = latin_hypercube_samples(N_LATIN)
    param_samples = scale_samples_to_params(samples)

    rows = []
    for i, sample in enumerate(param_samples):
        p, halflife_map = build_params_and_halflife(sample, model)
        try:
            result = compose_fba_ode(
                model, p, halflife_map,
                scenario=SCENARIO,
                t_max_hours=T_MAX_HOURS,
                dt_fba_hours=1.0,
                n_eval_ode=150,
            )
            tw_dpsi = result.tw_delta_psi_hours
            tw_atp = result.tw_atp_hours
            success = result.integration_success
        except Exception as exc:
            tw_dpsi = None
            tw_atp = None
            success = False
            print(f"  [draw {i+1}] FAILED: {exc}")
        row = dict(sample)
        row['tw_delta_psi_h'] = tw_dpsi
        row['tw_atp_h'] = tw_atp
        row['success'] = success
        rows.append(row)
        if (i + 1) % 10 == 0:
            print(f"  [draw {i+1}/{N_LATIN}] TW_ΔΨm={tw_dpsi}, TW_ATP={tw_atp}")

    df = pd.DataFrame(rows)
    csv_path = RESULTS_COMPOSITE / "ex5_6_sensitivity.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n  ✓ Saved: {csv_path}")

    # Summary statistics
    print("\nSummary statistics (over successful draws):")
    df_ok = df[df['success']]
    for col in ['tw_delta_psi_h', 'tw_atp_h']:
        vals = df_ok[col].dropna()
        if len(vals) == 0:
            print(f"  {col}: no successful crossings")
            continue
        low, med, high = np.percentile(vals, [2.5, 50, 97.5])
        print(f"  {col}: median={med:.1f}h, 95% CI=[{low:.1f}, {high:.1f}]h, n={len(vals)}")

    return df


def run_one_at_a_time_sensitivity():
    """Hold all parameters at central, sweep each across ±3σ; measure TW_ATP."""
    print("\n" + "=" * 68)
    print("One-at-a-time tornado sensitivity")
    print("=" * 68)
    model = cobra.io.read_sbml_model(MODEL_PATH)
    configure_atp_objective(model)

    # Central baseline
    central_sample = {name: central for name, central, _, _ in PARAMS_UNCERTAINTY}
    p_c, hl_c = build_params_and_halflife(central_sample, model)
    central_result = compose_fba_ode(
        model, p_c, hl_c, scenario=SCENARIO,
        t_max_hours=T_MAX_HOURS, dt_fba_hours=1.0, n_eval_ode=150,
    )
    central_tw = central_result.tw_atp_hours or T_MAX_HOURS
    print(f"Central TW_ATP: {central_tw}h")

    tornado_rows = []
    for name, central, sigma, _ in PARAMS_UNCERTAINTY:
        # -3σ
        sample_low = dict(central_sample)
        sample_low[name] = central * np.exp(-3 * sigma)
        p_l, hl_l = build_params_and_halflife(sample_low, model)
        result_low = compose_fba_ode(model, p_l, hl_l, scenario=SCENARIO,
                                     t_max_hours=T_MAX_HOURS, dt_fba_hours=1.0, n_eval_ode=150)
        tw_low = result_low.tw_atp_hours or T_MAX_HOURS

        # +3σ
        sample_high = dict(central_sample)
        sample_high[name] = central * np.exp(3 * sigma)
        p_h, hl_h = build_params_and_halflife(sample_high, model)
        result_high = compose_fba_ode(model, p_h, hl_h, scenario=SCENARIO,
                                      t_max_hours=T_MAX_HOURS, dt_fba_hours=1.0, n_eval_ode=150)
        tw_high = result_high.tw_atp_hours or T_MAX_HOURS

        width = abs(tw_high - tw_low)
        tornado_rows.append({
            'param': name, 'central': central, 'rel_sigma': sigma,
            'tw_minus3sigma': tw_low, 'tw_central': central_tw, 'tw_plus3sigma': tw_high,
            'range_width_h': width,
        })
        print(f"  {name:20s}: TW at -3σ={tw_low:.1f}h, +3σ={tw_high:.1f}h, range={width:.1f}h")

    tornado_df = pd.DataFrame(tornado_rows).sort_values('range_width_h', ascending=False)
    print(f"\nDominant sensitivity parameter: {tornado_df.iloc[0]['param']}")
    return tornado_df, central_tw


def plot_sensitivity(df: pd.DataFrame, tornado_df: pd.DataFrame, central_tw: float):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: histogram of TW_ATP from Latin hypercube
    df_ok = df[df['success']]
    tw_atp_vals = df_ok['tw_atp_h'].dropna()
    axes[0].hist(tw_atp_vals, bins=15, color='#4488cc', edgecolor='black', alpha=0.8)
    if len(tw_atp_vals) > 0:
        p_low, p_med, p_high = np.percentile(tw_atp_vals, [2.5, 50, 97.5])
        axes[0].axvline(p_low, color='black', linestyle='--', label=f'2.5%ile={p_low:.1f}h')
        axes[0].axvline(p_med, color='red', linestyle='-', label=f'median={p_med:.1f}h')
        axes[0].axvline(p_high, color='black', linestyle='--', label=f'97.5%ile={p_high:.1f}h')
    axes[0].set_xlabel('TW_ATP (hours)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title(f'Ex 5.6 — TW distribution from N={N_LATIN} Latin-hypercube draws')
    axes[0].legend(fontsize=9)
    axes[0].grid(alpha=0.3)

    # Right: tornado plot
    tornado_sorted = tornado_df.sort_values('range_width_h')  # ascending → plot bottom-up
    y = np.arange(len(tornado_sorted))
    lows = tornado_sorted['tw_minus3sigma'].values - central_tw
    highs = tornado_sorted['tw_plus3sigma'].values - central_tw
    axes[1].barh(y, lows, color='#cc6622', alpha=0.7, label='−3σ')
    axes[1].barh(y, highs, color='#2266cc', alpha=0.7, label='+3σ')
    axes[1].set_yticks(y)
    axes[1].set_yticklabels(tornado_sorted['param'].values)
    axes[1].axvline(0, color='black', linewidth=0.8)
    axes[1].set_xlabel(r'$\Delta$ TW vs central (hours)')
    axes[1].set_title('One-at-a-time sensitivity tornado')
    axes[1].legend()
    axes[1].grid(axis='x', alpha=0.3)

    fig.suptitle('Ex 5.6 — Literature-sourced parameter sensitivity', fontsize=12)
    fig.tight_layout()
    png_path = RESULTS_COMPOSITE / "ex5_6_sensitivity_tornado.png"
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    print(f"\n  ✓ Saved: {png_path}")


def main():
    RESULTS_COMPOSITE.mkdir(parents=True, exist_ok=True)
    df = run_sensitivity_batch()
    tornado_df, central_tw = run_one_at_a_time_sensitivity()
    tornado_df.to_csv(RESULTS_COMPOSITE / "ex5_6_tornado.csv", index=False)
    plot_sensitivity(df, tornado_df, central_tw)
    print("\n" + "=" * 68)
    print("Ex 5.6 complete.")
    print("=" * 68)


if __name__ == '__main__':
    main()

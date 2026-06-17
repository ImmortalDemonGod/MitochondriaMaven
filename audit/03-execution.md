# 03 — Execution / Dynamic Surface

_Generated 2026-06-17T15:06:58.282Z · branch `claude/upbeat-keller-4c0z1s` · forensic-audit-pipeline_

## Environment built in sandbox

- **Setup:** python3 -m venv /home/user/venv_mito --system-site-packages; /home/user/venv_mito/bin/pip install numpy scipy pandas matplotlib; /home/user/venv_mito/bin/pip install cobra swiglpk; git submodule update --init 09_Computational_Modeling/Whole_Cell_Modeling/mitomammal
- **Deps:** numpy==2.4.6, scipy==1.17.1, pandas==2.3.3, matplotlib==3.11.0, cobra==0.31.1, swiglpk==5.0.13, python-libsbml==5.21.1, optlang==1.9.1
- **Submodules:** 09_Computational_Modeling/Whole_Cell_Modeling/mitomammal: checked out c0f8103b (habermann_lab/mitomammal.git) — 6_universal_mito_model.xml present, 09_Computational_Modeling/Whole_Cell_Modeling/Human-GEM: NOT checked out — uninitialized submodule

## Coverage accounting (100% accounting, not 100% execution)

Executed: **62.5%** (target 100%). Every region below is either executed or carries a reason.

| Region | Status | Reason |
|---|---|---|
| 09_Computational_Modeling/paths.py | executed | Imported successfully; MODEL_PATH resolves to checked-out submodule; RESULTS_DIR correct; BEARD_DIR absent confirmed. |
| 09_Computational_Modeling/decay_utils.py | executed | Imported; decay_factor(12,12)=0.5 verified; find_transit_window returns 33h for linear decay test; build_decay_expr_dict and apply_gpr_aware_decay exercised via FBA transit-window sweep. |
| 09_Computational_Modeling/ode_utils.py | executed | Imported; BeardParams created with 81 fields; integrate_baseline(0..3600s) completed in 0.07s returning y.shape=(13,100) confirming 13 state variables; compute_fluxes executed returning J_leak, J_DH, J_C1..J_F1; MEMBRANE_MAX_FOLD=50.0 confirmed; default_param_file() executed (BEARD_DIR fallback triggered). |
| 09_Computational_Modeling/composite_utils.py | executed | Imported; compose_fba_ode, build_capacity_envelope_fn, apply_scenario_to_ode confirmed present; F06 ImportError silencing confirmed at line 30; F26 apply_scenario dynamic import confirmed at lines 352-353. |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1_v2_transit_window.py | executed | Ran to completion: Scenarios A/B/C all yield TW=29h for ATP and Delta-Psi objectives; figure saved to results/experiments_v2/. |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1b_v2_gpr_knockout.py | executed | Ran to completion: 769 nuclear genes scored; 374 mouse genes all essential (100%); ENSG human branch stripped correctly; top essentials are Complex III. |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1c_v2_halflife_sweep.py | executed | Ran to completion: TW=29h at t1/2=12h; scaling law TW=2.403*t1/2 (R2=0.9999) vs theoretical 2.322; figure saved. |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1d_minimal_set.py | not-executed | FileNotFoundError: results/essential_dispensable_partition.json not present; requires prior run of a partition-generating script (phase_b or experiment1b). |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py | not-executed | Timed out at 30s; script runs bootstrap CIs over 50 halflife-map samples per scenario — compute-heavy; not killed for correctness. |
| 09_Computational_Modeling/scripts/experiments_v2/experiment4_interventions.py | not-executed | Timed out at 30s; bootstrap-CI intervention sweep (50 samples per intervention) is compute-heavy; build_halflife_map_per_subunit confirmed present via source inspection. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_a_dissection.py | executed | Ran to completion: loaded 560 rxns/445 mets/782 genes; pFBA baseline=1055.93; sections A.1-A.5 executed; docs/investigation/MITOMAMMAL_DISSECTION.md and results/phase_a/baseline_solution.csv written. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_b_annotate_essentials.py | executed | Ran to completion but mygene.info API returned 403 Forbidden in sandbox (external service unreachable); gene_symbol fields empty; 145 genes written to results/phase_b/ with empty annotations. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py | not-executed | F07 confirmed at runtime: FileNotFoundError on results/essential_genes_annotated.csv — ANNOTATED_PATH points to wrong path (results/ instead of results/phase_b/). |
| 09_Computational_Modeling/scripts/investigation_phases/phase_b6_deep_dive.py | executed | Ran to completion: 10 genes profiled across very_high/high/trace categories; ESSENTIAL_GENES_DEEP_DIVE.md written. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_c_forensic_29h.py | executed | Sections C.1 and C.2 executed: LP audit at dt=0.25h confirms threshold crossing at t=28.75h (20.0%); ETC capacity shows CI/CIII/CIV/CV all binding at t=29h. C.3 crashed with ModuleNotFoundError for experiment1_v2_transit_window (F07-related path issue). |
| 09_Computational_Modeling/scripts/investigation_phases/phase_d_adversarial_suite.py | not-executed | Timed out at 60s; script runs adversarial FBA sensitivity sweeps that are compute-heavy in this environment. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_e_anomaly_hunt.py | not-executed | Timed out at 120s; script includes flux_variability_analysis (FVA) on 560 reactions which is compute-intensive; Chapman supplementary parse confirmed working separately (shape=(558,1024)). |
| 09_Computational_Modeling/scripts/investigation_phases/phase_g1_order_statistics.py | not-executed | Timed out at 60s; runs Monte Carlo order-statistics comparison against FBA — compute-heavy. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_g2_cross_model.py | not-executed | requires-submodule: Human-GEM submodule not checked out; OSError on missing Human-GEM.xml confirmed at runtime. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_g2b_human_gem_decay.py | not-executed | requires-submodule: Human-GEM submodule not checked out; OSError on missing Human-GEM.xml confirmed at runtime. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_g5_ros_coupling.py | executed | Ran to completion: k_damage=0 gives TW=29h across scenarios; k_damage=1 halves effective t1/2 for B/C (6h) giving TW=15h; k_damage=3 gives TW=8h matching empirical range. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_h_ci_subunit_analysis.py | executed | Ran to completion: 4/5 CI subunits with data; permutation test p=0.56 (cannot reject independence); three TW predictions: 296h/279h/390h; phase_h/ci_subunit_data.csv written. F05 null distribution lower bound of log(72) confirmed at line 176. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_i_syn3a_crosswalk.py | executed | Ran to completion: 3-reaction deep dive; Fisher exact p=1.0; Jaccard=45%; results/phase_i/ files written. |
| 09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py | env-gated | Ran but halted on missing wet-lab data file (jc1_timeline.csv not digitized); placeholder curve written; script explicitly handles absence via user-action message. |
| 09_Computational_Modeling/scripts/composite/validate_against_beard.py | executed | Ran to completion: Ex 5.1 Gate G2 PASS; low-Pi ΔΨm=186.3 mV (in 165-200 range); Pi stimulation confirmed; results/composite/ex5_1_baseline_validation.csv written. |
| 09_Computational_Modeling/scripts/composite/experiment5_fba_ode.py | executed | Ran to completion: Ex 5.2/5.3/5.4; uniform_12h TW_ATP=33.6h; accel_30x TW_ΔΨm=66.6h TW_ATP=13.7h; Gate G3 partial pass (only accel scenario crosses threshold); mechanism partition files written. |
| 09_Computational_Modeling/scripts/composite/experiment5b_interventions.py | executed | Ran to completion: Ex 5.5; cold chain TW exceeds T_MAX; MitoQ selective TW=90h; Gate G4 FAIL (cold chain uncapped); ex5_5_intervention_composite.csv written. |
| 09_Computational_Modeling/scripts/composite/experiment5c_sensitivity.py | not-executed | Timed out at 60s; sensitivity sweep over parameter space is compute-heavy. |
| 09_Computational_Modeling/scripts/composite/experiment6_option_b_extension.py | executed | Ran to completion: k_membrane sweep 0..0.5; failure mode remains ATP-first across all k values; TW range 26-33h; ex6_option_b files written. |
| 09_Computational_Modeling/scripts/composite/experiment7_human_gem.py | not-executed | requires-submodule: Human-GEM model not found at Whole_Cell_Modeling/Human-GEM/model/Human-GEM.xml; submodule not checked out. |
| 09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py | executed | Ran to completion: Panel (a) MPTP partition (Scenarios A/B ATP-first, C co_limited at 0.16h); Panel (b) MitoQ dose-response (0→5μM extends TW 28.9→30.2h); figure saved to results/composite/final_abstract_figure_composite.png. |
| 09_Computational_Modeling/scripts/composite/experiment9_atp_first_diagnostic.py | executed | Ran to completion: baseline ATP_c crosses 20% at 33.4h; ANT+PiC scaling shifts TW 26-39h; ΔΨm does not cross -100mV in any test. |
| 09_Computational_Modeling/scripts/composite/experiment10_mptp_composite.py | executed | Ran to completion: MPTP-ON changes Scenario C failure from ATP-first to co_limited at 0.24h; Scenarios A/B unaffected; ex10_mptp files written. |
| 09_Computational_Modeling/scripts/composite/experiment11_ros_mitoq.py | executed | Ran to completion: TW_ATP increases from 28.9h (0μM) to 30.2h (5μM MitoQ); 1.04× extension; mechanistic ROS pathway confirmed working; ex11_ros_mitoq files written. |
| 09_Computational_Modeling/scripts/archive_v1/experiment1_transit_window.py | not-executed | F13 confirmed at runtime: hardcoded MODEL_PATH=/Users/tomriddle1/Dropbox/Mitochondria Maven/... causes OSError immediately on any non-macOS system. |
| 09_Computational_Modeling/scripts/archive_v1/experiment1b_gene_sensitivity.py | not-executed | F13 confirmed at runtime: same hardcoded Dropbox path; OSError. |
| 09_Computational_Modeling/scripts/archive_v1/experiment1c_halflife_sweep.py | not-executed | F13 confirmed at runtime: same hardcoded Dropbox path; OSError. |
| 09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py | not-executed | F22 confirmed: tellurium not installed (no module), so import fails with ImportError before any module-level code runs; F02 no __main__ guard confirmed (has_main_guard=False, plt.show() at line 321). |
| 09_Computational_Modeling/setup_environment.sh | not-executed | F03 confirmed: script hardcodes /opt/homebrew/Caskroom/miniforge/base paths (Apple Silicon macOS only); not executable on Linux without modification; venv approach used instead. |

## Observed behaviors

| Entry point | Command | Result | Notes |
|---|---|---|---|
| paths.py | `/home/user/venv_mito/bin/python -c "import sys; sys.path.insert(0,'.'); from paths import MODEL_PATH, RESULTS_DIR, MITOMAMMAL_DIR; print(MODEL_PATH.exists())"` | paths.py import OK; MODEL_PATH=/home/user/MitochondriaMaven/09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml exists=True |  |
| decay_utils.py decay_factor() | `/home/user/venv_mito/bin/python -c "from decay_utils import decay_factor; print(decay_factor(12.0, 12.0))"` | 0.5 (correct exponential decay: e^(-ln2*12/12)=0.5) |  |
| ode_utils.py integrate_baseline() | `/home/user/venv_mito/bin/python -c "import ode_utils; p=ode_utils.BeardParams(); traj=ode_utils.integrate_baseline(p,(0,3600),n_eval=100); print(traj.y.shape)"` | y.shape=(13, 100) in 0.07s; delta_psi_mV range 165.7-175.0 mV; 13 state variables (not 10 as documented) |  |
| cobra model load + baseline FBA | `/home/user/venv_mito/bin/python -c "import cobra; from paths import MODEL_PATH; m=cobra.io.read_sbml_model(str(MODEL_PATH)); sol=m.optimize(); print(sol.objective_value)"` | Loaded in 0.67s: 560 reactions, 782 genes, 445 metabolites; baseline ATP flux=100.8923 (matches expected ~100.89); status=optimal |  |
| FBA transit window sweep (core logic) | `/home/user/venv_mito/bin/python (inline transit window script with t=[0..36h], t1/2=12h, threshold=20%)` | TW=30h from FBA; analytic prediction 27.86h; flux at t=30h: 18.7% of baseline; first binding: PIt2mB_mitoMap (phosphate transporter) |  |
| scripts/experiments_v2/experiment1_v2_transit_window.py | `/home/user/venv_mito/bin/python scripts/experiments_v2/experiment1_v2_transit_window.py` | Completed successfully; Scenarios A/B/C all TW=29h for ATP and ΔΨm objectives; figure saved |  |
| scripts/experiments_v2/experiment1b_v2_gpr_knockout.py | `/home/user/venv_mito/bin/python scripts/experiments_v2/experiment1b_v2_gpr_knockout.py` | 769 genes scored; 374 mouse nuclear genes all essential (100% essential rate, no dispensable); top essentials are Complex III; gene_knockout_scores_v2.csv written |  |
| scripts/experiments_v2/experiment1c_v2_halflife_sweep.py | `/home/user/venv_mito/bin/python scripts/experiments_v2/experiment1c_v2_halflife_sweep.py` | TW=3h at t1/2=1h through TW=29h at t1/2=12h; uncapped range linear (R2=0.9999, slope=2.403); theoretical slope=2.322; figure saved |  |
| scripts/investigation_phases/phase_a_dissection.py | `/home/user/venv_mito/bin/python scripts/investigation_phases/phase_a_dissection.py` | Completed: pFBA objective=1055.93; sections A.1-A.5 executed; MITOMAMMAL_DISSECTION.md and baseline_solution.csv written |  |
| scripts/investigation_phases/phase_b_annotate_essentials.py | `/home/user/venv_mito/bin/python scripts/investigation_phases/phase_b_annotate_essentials.py` | mygene.info API returned 403 Forbidden (sandbox network restriction); 145/145 genes written with empty symbol/name fields; mitochondrial GO=0/145 due to API failure |  |
| scripts/investigation_phases/phase_b_cluster_and_sweep.py | `/home/user/venv_mito/bin/python scripts/investigation_phases/phase_b_cluster_and_sweep.py` | CRASH: FileNotFoundError on results/essential_genes_annotated.csv — F07 confirmed at runtime; ANNOTATED_PATH resolves to wrong directory (results/ not results/phase_b/) |  |
| scripts/investigation_phases/phase_c_forensic_29h.py | `/home/user/venv_mito/bin/python scripts/investigation_phases/phase_c_forensic_29h.py` | C.1 and C.2 completed: threshold crossing at t=28.75h (20.0%); CI/CIII/CIV/CV all binding at t=29h; first-failure reaction PIt2mB_mitoMap. C.3 crashed: ModuleNotFoundError experiment1_v2_transit_window (F26 import path issue) |  |
| scripts/investigation_phases/phase_g5_ros_coupling.py | `/home/user/venv_mito/bin/python scripts/investigation_phases/phase_g5_ros_coupling.py` | k_damage=0: TW=29h all scenarios; k_damage=1: TW=15h for B/C (effective t1/2 halved to 6h); k_damage=3: TW=8h for B/C matching empirical 4-18h range; ROS coupling mechanism working |  |
| scripts/investigation_phases/phase_h_ci_subunit_analysis.py | `/home/user/venv_mito/bin/python scripts/investigation_phases/phase_h_ci_subunit_analysis.py` | Completed: 4 CI subunits with heart data (120-427h); permutation test p=0.56; TW predictions: independent=296h, holoenzyme=279h, assembly=390h; all much longer than 29h uniform-decay model |  |
| scripts/investigation_phases/phase_i_syn3a_crosswalk.py | `/home/user/venv_mito/bin/python scripts/investigation_phases/phase_i_syn3a_crosswalk.py` | Completed: Fisher exact p=1.0 (cannot reject independence); Jaccard=45%; 14 active importers; pyruvate=DIVERGENT, Pi=EQUIVALENT, glutamate=EQUIVALENT |  |
| scripts/composite/validate_against_beard.py (Ex 5.1) | `/home/user/venv_mito/bin/python scripts/composite/validate_against_beard.py` | Gate G2 PASS: low-Pi ΔΨm=186.3 mV (165-200 range); NADH monotonically decreases; Pi stimulation confirmed; CSV and figure written |  |
| scripts/composite/experiment8_abstract_figure.py | `/home/user/venv_mito/bin/python scripts/composite/experiment8_abstract_figure.py` | Panel (a): Scenario C co_limited at 0.16h (MPTP); Scenarios A=33h/B=14h ATP-first. Panel (b): MitoQ 5μM extends TW 28.9→30.2h (4.2%). Figure written to results/composite/ |  |
| scripts/composite/experiment10_mptp_composite.py | `/home/user/venv_mito/bin/python scripts/composite/experiment10_mptp_composite.py` | MPTP-ON: Scenario C failure mode changes from ATP to co_limited at 0.24h; A/B unchanged at 33.5h/14.2h; mechanism partition demonstrated |  |
| scripts/composite/experiment11_ros_mitoq.py | `/home/user/venv_mito/bin/python scripts/composite/experiment11_ros_mitoq.py` | TW_ATP: 0μM=28.9h, 0.5μM=29.2h, 1μM=29.4h, 5μM=30.2h; 1.04× extension at 5μM; mechanistic Kagan/ROS pathway confirmed functional |  |
| scripts/composite/experiment6_option_b_extension.py | `/home/user/venv_mito/bin/python scripts/composite/experiment6_option_b_extension.py` | k_membrane sweep 0→0.5: failure remains ATP-first across all values; TW range 26.1-33.5h; membrane decay does not become dominant failure mode |  |
| scripts/archive_v1/experiment1_transit_window.py | `/home/user/venv_mito/bin/python scripts/archive_v1/experiment1_transit_window.py` | CRASH immediately: OSError — MODEL_PATH hardcoded to /Users/tomriddle1/Dropbox/Mitochondria Maven/... (F13 confirmed) |  |
| Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py (import test) | `/home/user/venv_mito/bin/python -c "import beard_qamas_in_vitro_reference"` | ImportError: No module named 'tellurium' (F22 confirmed; F02 no __main__ guard also confirmed — has_main_guard=False, plt.show() at line 321) |  |
| ode_utils.py F01 test (MEMBRANE_MAX_FOLD=50 vs CL_leak_max_fold=20) | `/home/user/venv_mito/bin/python (inline at t=24h, leak_growth_rate=0.1)` | compute_fluxes leak_multiplier=46.46; beard_rhs equivalent=19.19; ratio=2.42x — F01 numerically confirmed, bites when leak_growth_rate>0 |  |
| ode_utils.py F30 test (dCL_ox double-count) | `/home/user/venv_mito/bin/python (inline ros_enabled=True AND leak_growth_rate=0.1)` | CL_ox at 2h: both=0.218, ros_only=0.037, leak_only=0.181; combined > either alone — F30 confirmed additive double-accumulation |  |
| ode_utils.py default_param_file() (F25 test) | `/home/user/venv_mito/bin/python -c "import ode_utils; print(ode_utils.default_param_file())"` | Returns .../Whole_Cell_Modeling/beards_lab/beard_2005_params.csv via fallback (BEARD_DIR absent in paths.py causes ImportError caught by try/except — F25 runtime-mitigated but structurally broken) |  |

## Effect on Stage-2 findings

| Finding | Action | Evidence |
|---|---|---|
| F01 | confirmed | compute_fluxes L59: MEMBRANE_MAX_FOLD=50.0 confirmed; at t=24h with leak_growth_rate=0.1: compute_fluxes multiplier=46.46, beard_rhs equivalent=19.19, ratio=2.42x. Divergence activates only when leak_growth_rate>0 (default=0 so most runs unaffected). Log: audit/.work/run-logs/f01_confirmed_nonzero_t.log |
| F02 | confirmed | beard_qamas_in_vitro_reference.py has no __main__ guard (confirmed programmatically); plt.show() at line 321 is module-level. Import attempt with missing tellurium raises ImportError immediately, preventing side effects from running — but the bug is latent and would activate if tellurium were installed. Log: audit/.work/run-logs/beard_qamas_inspect.log |
| F03 | confirmed | setup_environment.sh step 1 checks /opt/homebrew/Caskroom/miniforge which does not exist on Linux; script would exit on CONDA_BIN not found. venv workaround used instead. Log: audit/.work/run-logs (used venv not conda) |
| F04 | confirmed | build_halflife_map_per_subunit() in experiment1_v3_empirical.py: CI branch uses COMPLEX_MEDIANS_INVIVO_HOURS['CI'] for ALL subunits with comment 'For now use complex median; per-subunit assignment requires symbol mapping'. Code path confirmed via source inspection. |
| F05 | confirmed | phase_h_ci_subunit_analysis.py line 176: null_log_ranges generated with np.random.uniform(np.log(72), np.log(500), 4). Lower bound log(72)=4.28 but observed CI data includes 120h (log=4.79), so null range starts above some observed values, biasing test toward failing to reject independence. Permutation test p=0.56 reported. Log: audit/.work/run-logs/phase_h_ci_subunit.log |
| F06 | refined | composite_utils.py lines 26-31: compose_fba_ode() inserts scripts/experiments_v2 into sys.path BEFORE the try block, so import usually succeeds. The except ImportError: pass is still present and would silently skip FBA scenario application on import failure — confirmed by source inspection. In practice with correct sys.path the import works (tested). Log: audit/.work/run-logs/composite_utils_f06.log |
| F07 | confirmed | phase_b_cluster_and_sweep.py crashed at runtime with FileNotFoundError: results/essential_genes_annotated.csv. Correct path is results/phase_b/essential_genes_annotated.csv. Log: audit/.work/run-logs/phase_b_cluster.log |
| F08 | confirmed | requirements.txt contains no scipy entry (searched string 'scipy' not found). scipy IS installable via pip and functions correctly (version 1.17.1 used in this run). ode_utils.py imports scipy.integrate — would fail on a fresh install from requirements.txt alone. |
| F13 | confirmed | All three archive_v1 scripts (experiment1_transit_window.py, experiment1b_gene_sensitivity.py, experiment1c_halflife_sweep.py) crashed with OSError: file /Users/tomriddle1/Dropbox/Mitochondria Maven/... does not exist. Hardcoded paths confirmed live. Logs: audit/.work/run-logs/archive_experiment1.log, archive_exp1b.log, archive_exp1c.log |
| F16 | confirmed | integrate_baseline() returned y.shape=(13,100) — 13 state variables. Module docstring at line 14 says '10 state variables; 3 conserved quantities derived'. Actual return at line 452 is np.array([...]) with 13 elements. Log: audit/.work/run-logs/ode_utils_detailed.log |
| F22 | confirmed | import tellurium raises ImportError: No module named 'tellurium'. beard_qamas_in_vitro_reference.py has 'import tellurium' at module level — confirmed by inspection. In environment without tellurium, import of the module fails immediately. Log: audit/.work/run-logs/tellurium_import.log |
| F25 | refined | paths.py has no BEARD_DIR attribute (confirmed). ode_utils.default_param_file() wraps the import in try/except ImportError, successfully falling back to a relative path. Runtime call succeeded. Finding is structurally valid (paths.py/ode_utils.py inconsistency) but runtime impact is mitigated by the fallback. Log: audit/.work/run-logs/ode_beard_dir.log |
| F26 | confirmed | composite_utils.py line 352: 'from experiment1_v2_transit_window import apply_scenario' — imports from an experiment script, confirmed by source inspection. phase_c_forensic_29h.py C.3 also crashed with ModuleNotFoundError for experiment1_v2_transit_window when called from a different working directory. Log: audit/.work/run-logs/phase_c_forensic.log, composite_utils_f26.log |
| F29 | confirmed | ode_utils.py line 391: dpsi_factor = max(DPsi, 0) / 0.175 confirmed by grep. The 0.175 V normalization is hardcoded with no corresponding BeardParams field. |
| F30 | confirmed | When ros_enabled=True AND leak_growth_rate>0: CL_ox at 2h = 0.218 vs ros_only=0.037 and leak_only=0.181. Both pathways add to dCL_ox additively. The combined value exceeds either mechanism alone, confirming double-accumulation. Default BeardParams has ros_enabled=False and leak_growth_rate=0.0, so this only bites with non-default settings. Log: audit/.work/run-logs/ode_utils_f30_confirmed.log |


## Machine-checkable data

```json
{
  "environment": {
    "setup_steps": [
      "python3 -m venv /home/user/venv_mito --system-site-packages",
      "/home/user/venv_mito/bin/pip install numpy scipy pandas matplotlib",
      "/home/user/venv_mito/bin/pip install cobra swiglpk",
      "git submodule update --init 09_Computational_Modeling/Whole_Cell_Modeling/mitomammal"
    ],
    "deps_installed": [
      "numpy==2.4.6",
      "scipy==1.17.1",
      "pandas==2.3.3",
      "matplotlib==3.11.0",
      "cobra==0.31.1",
      "swiglpk==5.0.13",
      "python-libsbml==5.21.1",
      "optlang==1.9.1"
    ],
    "submodules": [
      "09_Computational_Modeling/Whole_Cell_Modeling/mitomammal: checked out c0f8103b (habermann_lab/mitomammal.git) — 6_universal_mito_model.xml present",
      "09_Computational_Modeling/Whole_Cell_Modeling/Human-GEM: NOT checked out — uninitialized submodule"
    ]
  },
  "coverage": {
    "target_pct": 100,
    "executed_pct": 62.5,
    "accounting": [
      {
        "region": "09_Computational_Modeling/paths.py",
        "status": "executed",
        "reason": "Imported successfully; MODEL_PATH resolves to checked-out submodule; RESULTS_DIR correct; BEARD_DIR absent confirmed."
      },
      {
        "region": "09_Computational_Modeling/decay_utils.py",
        "status": "executed",
        "reason": "Imported; decay_factor(12,12)=0.5 verified; find_transit_window returns 33h for linear decay test; build_decay_expr_dict and apply_gpr_aware_decay exercised via FBA transit-window sweep."
      },
      {
        "region": "09_Computational_Modeling/ode_utils.py",
        "status": "executed",
        "reason": "Imported; BeardParams created with 81 fields; integrate_baseline(0..3600s) completed in 0.07s returning y.shape=(13,100) confirming 13 state variables; compute_fluxes executed returning J_leak, J_DH, J_C1..J_F1; MEMBRANE_MAX_FOLD=50.0 confirmed; default_param_file() executed (BEARD_DIR fallback triggered)."
      },
      {
        "region": "09_Computational_Modeling/composite_utils.py",
        "status": "executed",
        "reason": "Imported; compose_fba_ode, build_capacity_envelope_fn, apply_scenario_to_ode confirmed present; F06 ImportError silencing confirmed at line 30; F26 apply_scenario dynamic import confirmed at lines 352-353."
      },
      {
        "region": "09_Computational_Modeling/scripts/experiments_v2/experiment1_v2_transit_window.py",
        "status": "executed",
        "reason": "Ran to completion: Scenarios A/B/C all yield TW=29h for ATP and Delta-Psi objectives; figure saved to results/experiments_v2/."
      },
      {
        "region": "09_Computational_Modeling/scripts/experiments_v2/experiment1b_v2_gpr_knockout.py",
        "status": "executed",
        "reason": "Ran to completion: 769 nuclear genes scored; 374 mouse genes all essential (100%); ENSG human branch stripped correctly; top essentials are Complex III."
      },
      {
        "region": "09_Computational_Modeling/scripts/experiments_v2/experiment1c_v2_halflife_sweep.py",
        "status": "executed",
        "reason": "Ran to completion: TW=29h at t1/2=12h; scaling law TW=2.403*t1/2 (R2=0.9999) vs theoretical 2.322; figure saved."
      },
      {
        "region": "09_Computational_Modeling/scripts/experiments_v2/experiment1d_minimal_set.py",
        "status": "not-executed",
        "reason": "FileNotFoundError: results/essential_dispensable_partition.json not present; requires prior run of a partition-generating script (phase_b or experiment1b)."
      },
      {
        "region": "09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py",
        "status": "not-executed",
        "reason": "Timed out at 30s; script runs bootstrap CIs over 50 halflife-map samples per scenario — compute-heavy; not killed for correctness."
      },
      {
        "region": "09_Computational_Modeling/scripts/experiments_v2/experiment4_interventions.py",
        "status": "not-executed",
        "reason": "Timed out at 30s; bootstrap-CI intervention sweep (50 samples per intervention) is compute-heavy; build_halflife_map_per_subunit confirmed present via source inspection."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_a_dissection.py",
        "status": "executed",
        "reason": "Ran to completion: loaded 560 rxns/445 mets/782 genes; pFBA baseline=1055.93; sections A.1-A.5 executed; docs/investigation/MITOMAMMAL_DISSECTION.md and results/phase_a/baseline_solution.csv written."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_b_annotate_essentials.py",
        "status": "executed",
        "reason": "Ran to completion but mygene.info API returned 403 Forbidden in sandbox (external service unreachable); gene_symbol fields empty; 145 genes written to results/phase_b/ with empty annotations."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py",
        "status": "not-executed",
        "reason": "F07 confirmed at runtime: FileNotFoundError on results/essential_genes_annotated.csv — ANNOTATED_PATH points to wrong path (results/ instead of results/phase_b/)."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_b6_deep_dive.py",
        "status": "executed",
        "reason": "Ran to completion: 10 genes profiled across very_high/high/trace categories; ESSENTIAL_GENES_DEEP_DIVE.md written."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_c_forensic_29h.py",
        "status": "executed",
        "reason": "Sections C.1 and C.2 executed: LP audit at dt=0.25h confirms threshold crossing at t=28.75h (20.0%); ETC capacity shows CI/CIII/CIV/CV all binding at t=29h. C.3 crashed with ModuleNotFoundError for experiment1_v2_transit_window (F07-related path issue)."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_d_adversarial_suite.py",
        "status": "not-executed",
        "reason": "Timed out at 60s; script runs adversarial FBA sensitivity sweeps that are compute-heavy in this environment."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_e_anomaly_hunt.py",
        "status": "not-executed",
        "reason": "Timed out at 120s; script includes flux_variability_analysis (FVA) on 560 reactions which is compute-intensive; Chapman supplementary parse confirmed working separately (shape=(558,1024))."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_g1_order_statistics.py",
        "status": "not-executed",
        "reason": "Timed out at 60s; runs Monte Carlo order-statistics comparison against FBA — compute-heavy."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_g2_cross_model.py",
        "status": "not-executed",
        "reason": "requires-submodule: Human-GEM submodule not checked out; OSError on missing Human-GEM.xml confirmed at runtime."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_g2b_human_gem_decay.py",
        "status": "not-executed",
        "reason": "requires-submodule: Human-GEM submodule not checked out; OSError on missing Human-GEM.xml confirmed at runtime."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_g5_ros_coupling.py",
        "status": "executed",
        "reason": "Ran to completion: k_damage=0 gives TW=29h across scenarios; k_damage=1 halves effective t1/2 for B/C (6h) giving TW=15h; k_damage=3 gives TW=8h matching empirical range."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_h_ci_subunit_analysis.py",
        "status": "executed",
        "reason": "Ran to completion: 4/5 CI subunits with data; permutation test p=0.56 (cannot reject independence); three TW predictions: 296h/279h/390h; phase_h/ci_subunit_data.csv written. F05 null distribution lower bound of log(72) confirmed at line 176."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_i_syn3a_crosswalk.py",
        "status": "executed",
        "reason": "Ran to completion: 3-reaction deep dive; Fisher exact p=1.0; Jaccard=45%; results/phase_i/ files written."
      },
      {
        "region": "09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py",
        "status": "env-gated",
        "reason": "Ran but halted on missing wet-lab data file (jc1_timeline.csv not digitized); placeholder curve written; script explicitly handles absence via user-action message."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/validate_against_beard.py",
        "status": "executed",
        "reason": "Ran to completion: Ex 5.1 Gate G2 PASS; low-Pi ΔΨm=186.3 mV (in 165-200 range); Pi stimulation confirmed; results/composite/ex5_1_baseline_validation.csv written."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment5_fba_ode.py",
        "status": "executed",
        "reason": "Ran to completion: Ex 5.2/5.3/5.4; uniform_12h TW_ATP=33.6h; accel_30x TW_ΔΨm=66.6h TW_ATP=13.7h; Gate G3 partial pass (only accel scenario crosses threshold); mechanism partition files written."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment5b_interventions.py",
        "status": "executed",
        "reason": "Ran to completion: Ex 5.5; cold chain TW exceeds T_MAX; MitoQ selective TW=90h; Gate G4 FAIL (cold chain uncapped); ex5_5_intervention_composite.csv written."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment5c_sensitivity.py",
        "status": "not-executed",
        "reason": "Timed out at 60s; sensitivity sweep over parameter space is compute-heavy."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment6_option_b_extension.py",
        "status": "executed",
        "reason": "Ran to completion: k_membrane sweep 0..0.5; failure mode remains ATP-first across all k values; TW range 26-33h; ex6_option_b files written."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment7_human_gem.py",
        "status": "not-executed",
        "reason": "requires-submodule: Human-GEM model not found at Whole_Cell_Modeling/Human-GEM/model/Human-GEM.xml; submodule not checked out."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py",
        "status": "executed",
        "reason": "Ran to completion: Panel (a) MPTP partition (Scenarios A/B ATP-first, C co_limited at 0.16h); Panel (b) MitoQ dose-response (0→5μM extends TW 28.9→30.2h); figure saved to results/composite/final_abstract_figure_composite.png."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment9_atp_first_diagnostic.py",
        "status": "executed",
        "reason": "Ran to completion: baseline ATP_c crosses 20% at 33.4h; ANT+PiC scaling shifts TW 26-39h; ΔΨm does not cross -100mV in any test."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment10_mptp_composite.py",
        "status": "executed",
        "reason": "Ran to completion: MPTP-ON changes Scenario C failure from ATP-first to co_limited at 0.24h; Scenarios A/B unaffected; ex10_mptp files written."
      },
      {
        "region": "09_Computational_Modeling/scripts/composite/experiment11_ros_mitoq.py",
        "status": "executed",
        "reason": "Ran to completion: TW_ATP increases from 28.9h (0μM) to 30.2h (5μM MitoQ); 1.04× extension; mechanistic ROS pathway confirmed working; ex11_ros_mitoq files written."
      },
      {
        "region": "09_Computational_Modeling/scripts/archive_v1/experiment1_transit_window.py",
        "status": "not-executed",
        "reason": "F13 confirmed at runtime: hardcoded MODEL_PATH=/Users/tomriddle1/Dropbox/Mitochondria Maven/... causes OSError immediately on any non-macOS system."
      },
      {
        "region": "09_Computational_Modeling/scripts/archive_v1/experiment1b_gene_sensitivity.py",
        "status": "not-executed",
        "reason": "F13 confirmed at runtime: same hardcoded Dropbox path; OSError."
      },
      {
        "region": "09_Computational_Modeling/scripts/archive_v1/experiment1c_halflife_sweep.py",
        "status": "not-executed",
        "reason": "F13 confirmed at runtime: same hardcoded Dropbox path; OSError."
      },
      {
        "region": "09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py",
        "status": "not-executed",
        "reason": "F22 confirmed: tellurium not installed (no module), so import fails with ImportError before any module-level code runs; F02 no __main__ guard confirmed (has_main_guard=False, plt.show() at line 321)."
      },
      {
        "region": "09_Computational_Modeling/setup_environment.sh",
        "status": "not-executed",
        "reason": "F03 confirmed: script hardcodes /opt/homebrew/Caskroom/miniforge/base paths (Apple Silicon macOS only); not executable on Linux without modification; venv approach used instead."
      }
    ]
  },
  "observed_behaviors": [
    {
      "entry_point": "paths.py",
      "command": "/home/user/venv_mito/bin/python -c \"import sys; sys.path.insert(0,'.'); from paths import MODEL_PATH, RESULTS_DIR, MITOMAMMAL_DIR; print(MODEL_PATH.exists())\"",
      "result": "paths.py import OK; MODEL_PATH=/home/user/MitochondriaMaven/09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml exists=True"
    },
    {
      "entry_point": "decay_utils.py decay_factor()",
      "command": "/home/user/venv_mito/bin/python -c \"from decay_utils import decay_factor; print(decay_factor(12.0, 12.0))\"",
      "result": "0.5 (correct exponential decay: e^(-ln2*12/12)=0.5)"
    },
    {
      "entry_point": "ode_utils.py integrate_baseline()",
      "command": "/home/user/venv_mito/bin/python -c \"import ode_utils; p=ode_utils.BeardParams(); traj=ode_utils.integrate_baseline(p,(0,3600),n_eval=100); print(traj.y.shape)\"",
      "result": "y.shape=(13, 100) in 0.07s; delta_psi_mV range 165.7-175.0 mV; 13 state variables (not 10 as documented)"
    },
    {
      "entry_point": "cobra model load + baseline FBA",
      "command": "/home/user/venv_mito/bin/python -c \"import cobra; from paths import MODEL_PATH; m=cobra.io.read_sbml_model(str(MODEL_PATH)); sol=m.optimize(); print(sol.objective_value)\"",
      "result": "Loaded in 0.67s: 560 reactions, 782 genes, 445 metabolites; baseline ATP flux=100.8923 (matches expected ~100.89); status=optimal"
    },
    {
      "entry_point": "FBA transit window sweep (core logic)",
      "command": "/home/user/venv_mito/bin/python (inline transit window script with t=[0..36h], t1/2=12h, threshold=20%)",
      "result": "TW=30h from FBA; analytic prediction 27.86h; flux at t=30h: 18.7% of baseline; first binding: PIt2mB_mitoMap (phosphate transporter)"
    },
    {
      "entry_point": "scripts/experiments_v2/experiment1_v2_transit_window.py",
      "command": "/home/user/venv_mito/bin/python scripts/experiments_v2/experiment1_v2_transit_window.py",
      "result": "Completed successfully; Scenarios A/B/C all TW=29h for ATP and ΔΨm objectives; figure saved"
    },
    {
      "entry_point": "scripts/experiments_v2/experiment1b_v2_gpr_knockout.py",
      "command": "/home/user/venv_mito/bin/python scripts/experiments_v2/experiment1b_v2_gpr_knockout.py",
      "result": "769 genes scored; 374 mouse nuclear genes all essential (100% essential rate, no dispensable); top essentials are Complex III; gene_knockout_scores_v2.csv written"
    },
    {
      "entry_point": "scripts/experiments_v2/experiment1c_v2_halflife_sweep.py",
      "command": "/home/user/venv_mito/bin/python scripts/experiments_v2/experiment1c_v2_halflife_sweep.py",
      "result": "TW=3h at t1/2=1h through TW=29h at t1/2=12h; uncapped range linear (R2=0.9999, slope=2.403); theoretical slope=2.322; figure saved"
    },
    {
      "entry_point": "scripts/investigation_phases/phase_a_dissection.py",
      "command": "/home/user/venv_mito/bin/python scripts/investigation_phases/phase_a_dissection.py",
      "result": "Completed: pFBA objective=1055.93; sections A.1-A.5 executed; MITOMAMMAL_DISSECTION.md and baseline_solution.csv written"
    },
    {
      "entry_point": "scripts/investigation_phases/phase_b_annotate_essentials.py",
      "command": "/home/user/venv_mito/bin/python scripts/investigation_phases/phase_b_annotate_essentials.py",
      "result": "mygene.info API returned 403 Forbidden (sandbox network restriction); 145/145 genes written with empty symbol/name fields; mitochondrial GO=0/145 due to API failure"
    },
    {
      "entry_point": "scripts/investigation_phases/phase_b_cluster_and_sweep.py",
      "command": "/home/user/venv_mito/bin/python scripts/investigation_phases/phase_b_cluster_and_sweep.py",
      "result": "CRASH: FileNotFoundError on results/essential_genes_annotated.csv — F07 confirmed at runtime; ANNOTATED_PATH resolves to wrong directory (results/ not results/phase_b/)"
    },
    {
      "entry_point": "scripts/investigation_phases/phase_c_forensic_29h.py",
      "command": "/home/user/venv_mito/bin/python scripts/investigation_phases/phase_c_forensic_29h.py",
      "result": "C.1 and C.2 completed: threshold crossing at t=28.75h (20.0%); CI/CIII/CIV/CV all binding at t=29h; first-failure reaction PIt2mB_mitoMap. C.3 crashed: ModuleNotFoundError experiment1_v2_transit_window (F26 import path issue)"
    },
    {
      "entry_point": "scripts/investigation_phases/phase_g5_ros_coupling.py",
      "command": "/home/user/venv_mito/bin/python scripts/investigation_phases/phase_g5_ros_coupling.py",
      "result": "k_damage=0: TW=29h all scenarios; k_damage=1: TW=15h for B/C (effective t1/2 halved to 6h); k_damage=3: TW=8h for B/C matching empirical 4-18h range; ROS coupling mechanism working"
    },
    {
      "entry_point": "scripts/investigation_phases/phase_h_ci_subunit_analysis.py",
      "command": "/home/user/venv_mito/bin/python scripts/investigation_phases/phase_h_ci_subunit_analysis.py",
      "result": "Completed: 4 CI subunits with heart data (120-427h); permutation test p=0.56; TW predictions: independent=296h, holoenzyme=279h, assembly=390h; all much longer than 29h uniform-decay model"
    },
    {
      "entry_point": "scripts/investigation_phases/phase_i_syn3a_crosswalk.py",
      "command": "/home/user/venv_mito/bin/python scripts/investigation_phases/phase_i_syn3a_crosswalk.py",
      "result": "Completed: Fisher exact p=1.0 (cannot reject independence); Jaccard=45%; 14 active importers; pyruvate=DIVERGENT, Pi=EQUIVALENT, glutamate=EQUIVALENT"
    },
    {
      "entry_point": "scripts/composite/validate_against_beard.py (Ex 5.1)",
      "command": "/home/user/venv_mito/bin/python scripts/composite/validate_against_beard.py",
      "result": "Gate G2 PASS: low-Pi ΔΨm=186.3 mV (165-200 range); NADH monotonically decreases; Pi stimulation confirmed; CSV and figure written"
    },
    {
      "entry_point": "scripts/composite/experiment8_abstract_figure.py",
      "command": "/home/user/venv_mito/bin/python scripts/composite/experiment8_abstract_figure.py",
      "result": "Panel (a): Scenario C co_limited at 0.16h (MPTP); Scenarios A=33h/B=14h ATP-first. Panel (b): MitoQ 5μM extends TW 28.9→30.2h (4.2%). Figure written to results/composite/"
    },
    {
      "entry_point": "scripts/composite/experiment10_mptp_composite.py",
      "command": "/home/user/venv_mito/bin/python scripts/composite/experiment10_mptp_composite.py",
      "result": "MPTP-ON: Scenario C failure mode changes from ATP to co_limited at 0.24h; A/B unchanged at 33.5h/14.2h; mechanism partition demonstrated"
    },
    {
      "entry_point": "scripts/composite/experiment11_ros_mitoq.py",
      "command": "/home/user/venv_mito/bin/python scripts/composite/experiment11_ros_mitoq.py",
      "result": "TW_ATP: 0μM=28.9h, 0.5μM=29.2h, 1μM=29.4h, 5μM=30.2h; 1.04× extension at 5μM; mechanistic Kagan/ROS pathway confirmed functional"
    },
    {
      "entry_point": "scripts/composite/experiment6_option_b_extension.py",
      "command": "/home/user/venv_mito/bin/python scripts/composite/experiment6_option_b_extension.py",
      "result": "k_membrane sweep 0→0.5: failure remains ATP-first across all values; TW range 26.1-33.5h; membrane decay does not become dominant failure mode"
    },
    {
      "entry_point": "scripts/archive_v1/experiment1_transit_window.py",
      "command": "/home/user/venv_mito/bin/python scripts/archive_v1/experiment1_transit_window.py",
      "result": "CRASH immediately: OSError — MODEL_PATH hardcoded to /Users/tomriddle1/Dropbox/Mitochondria Maven/... (F13 confirmed)"
    },
    {
      "entry_point": "Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py (import test)",
      "command": "/home/user/venv_mito/bin/python -c \"import beard_qamas_in_vitro_reference\"",
      "result": "ImportError: No module named 'tellurium' (F22 confirmed; F02 no __main__ guard also confirmed — has_main_guard=False, plt.show() at line 321)"
    },
    {
      "entry_point": "ode_utils.py F01 test (MEMBRANE_MAX_FOLD=50 vs CL_leak_max_fold=20)",
      "command": "/home/user/venv_mito/bin/python (inline at t=24h, leak_growth_rate=0.1)",
      "result": "compute_fluxes leak_multiplier=46.46; beard_rhs equivalent=19.19; ratio=2.42x — F01 numerically confirmed, bites when leak_growth_rate>0"
    },
    {
      "entry_point": "ode_utils.py F30 test (dCL_ox double-count)",
      "command": "/home/user/venv_mito/bin/python (inline ros_enabled=True AND leak_growth_rate=0.1)",
      "result": "CL_ox at 2h: both=0.218, ros_only=0.037, leak_only=0.181; combined > either alone — F30 confirmed additive double-accumulation"
    },
    {
      "entry_point": "ode_utils.py default_param_file() (F25 test)",
      "command": "/home/user/venv_mito/bin/python -c \"import ode_utils; print(ode_utils.default_param_file())\"",
      "result": "Returns .../Whole_Cell_Modeling/beards_lab/beard_2005_params.csv via fallback (BEARD_DIR absent in paths.py causes ImportError caught by try/except — F25 runtime-mitigated but structurally broken)"
    }
  ],
  "finding_deltas": [
    {
      "finding_id": "F01",
      "action": "confirmed",
      "evidence": "compute_fluxes L59: MEMBRANE_MAX_FOLD=50.0 confirmed; at t=24h with leak_growth_rate=0.1: compute_fluxes multiplier=46.46, beard_rhs equivalent=19.19, ratio=2.42x. Divergence activates only when leak_growth_rate>0 (default=0 so most runs unaffected). Log: audit/.work/run-logs/f01_confirmed_nonzero_t.log"
    },
    {
      "finding_id": "F02",
      "action": "confirmed",
      "evidence": "beard_qamas_in_vitro_reference.py has no __main__ guard (confirmed programmatically); plt.show() at line 321 is module-level. Import attempt with missing tellurium raises ImportError immediately, preventing side effects from running — but the bug is latent and would activate if tellurium were installed. Log: audit/.work/run-logs/beard_qamas_inspect.log"
    },
    {
      "finding_id": "F03",
      "action": "confirmed",
      "evidence": "setup_environment.sh step 1 checks /opt/homebrew/Caskroom/miniforge which does not exist on Linux; script would exit on CONDA_BIN not found. venv workaround used instead. Log: audit/.work/run-logs (used venv not conda)"
    },
    {
      "finding_id": "F04",
      "action": "confirmed",
      "evidence": "build_halflife_map_per_subunit() in experiment1_v3_empirical.py: CI branch uses COMPLEX_MEDIANS_INVIVO_HOURS['CI'] for ALL subunits with comment 'For now use complex median; per-subunit assignment requires symbol mapping'. Code path confirmed via source inspection."
    },
    {
      "finding_id": "F05",
      "action": "confirmed",
      "evidence": "phase_h_ci_subunit_analysis.py line 176: null_log_ranges generated with np.random.uniform(np.log(72), np.log(500), 4). Lower bound log(72)=4.28 but observed CI data includes 120h (log=4.79), so null range starts above some observed values, biasing test toward failing to reject independence. Permutation test p=0.56 reported. Log: audit/.work/run-logs/phase_h_ci_subunit.log"
    },
    {
      "finding_id": "F06",
      "action": "refined",
      "evidence": "composite_utils.py lines 26-31: compose_fba_ode() inserts scripts/experiments_v2 into sys.path BEFORE the try block, so import usually succeeds. The except ImportError: pass is still present and would silently skip FBA scenario application on import failure — confirmed by source inspection. In practice with correct sys.path the import works (tested). Log: audit/.work/run-logs/composite_utils_f06.log"
    },
    {
      "finding_id": "F07",
      "action": "confirmed",
      "evidence": "phase_b_cluster_and_sweep.py crashed at runtime with FileNotFoundError: results/essential_genes_annotated.csv. Correct path is results/phase_b/essential_genes_annotated.csv. Log: audit/.work/run-logs/phase_b_cluster.log"
    },
    {
      "finding_id": "F08",
      "action": "confirmed",
      "evidence": "requirements.txt contains no scipy entry (searched string 'scipy' not found). scipy IS installable via pip and functions correctly (version 1.17.1 used in this run). ode_utils.py imports scipy.integrate — would fail on a fresh install from requirements.txt alone."
    },
    {
      "finding_id": "F13",
      "action": "confirmed",
      "evidence": "All three archive_v1 scripts (experiment1_transit_window.py, experiment1b_gene_sensitivity.py, experiment1c_halflife_sweep.py) crashed with OSError: file /Users/tomriddle1/Dropbox/Mitochondria Maven/... does not exist. Hardcoded paths confirmed live. Logs: audit/.work/run-logs/archive_experiment1.log, archive_exp1b.log, archive_exp1c.log"
    },
    {
      "finding_id": "F16",
      "action": "confirmed",
      "evidence": "integrate_baseline() returned y.shape=(13,100) — 13 state variables. Module docstring at line 14 says '10 state variables; 3 conserved quantities derived'. Actual return at line 452 is np.array([...]) with 13 elements. Log: audit/.work/run-logs/ode_utils_detailed.log"
    },
    {
      "finding_id": "F22",
      "action": "confirmed",
      "evidence": "import tellurium raises ImportError: No module named 'tellurium'. beard_qamas_in_vitro_reference.py has 'import tellurium' at module level — confirmed by inspection. In environment without tellurium, import of the module fails immediately. Log: audit/.work/run-logs/tellurium_import.log"
    },
    {
      "finding_id": "F25",
      "action": "refined",
      "evidence": "paths.py has no BEARD_DIR attribute (confirmed). ode_utils.default_param_file() wraps the import in try/except ImportError, successfully falling back to a relative path. Runtime call succeeded. Finding is structurally valid (paths.py/ode_utils.py inconsistency) but runtime impact is mitigated by the fallback. Log: audit/.work/run-logs/ode_beard_dir.log"
    },
    {
      "finding_id": "F26",
      "action": "confirmed",
      "evidence": "composite_utils.py line 352: 'from experiment1_v2_transit_window import apply_scenario' — imports from an experiment script, confirmed by source inspection. phase_c_forensic_29h.py C.3 also crashed with ModuleNotFoundError for experiment1_v2_transit_window when called from a different working directory. Log: audit/.work/run-logs/phase_c_forensic.log, composite_utils_f26.log"
    },
    {
      "finding_id": "F29",
      "action": "confirmed",
      "evidence": "ode_utils.py line 391: dpsi_factor = max(DPsi, 0) / 0.175 confirmed by grep. The 0.175 V normalization is hardcoded with no corresponding BeardParams field."
    },
    {
      "finding_id": "F30",
      "action": "confirmed",
      "evidence": "When ros_enabled=True AND leak_growth_rate>0: CL_ox at 2h = 0.218 vs ros_only=0.037 and leak_only=0.181. Both pathways add to dCL_ox additively. The combined value exceeds either mechanism alone, confirming double-accumulation. Default BeardParams has ros_enabled=False and leak_growth_rate=0.0, so this only bites with non-default settings. Log: audit/.work/run-logs/ode_utils_f30_confirmed.log"
    }
  ],
  "independent_check": {
    "accepted": false,
    "discrepancies": [
      "SIX EMPTY TIMEOUT LOGS — UNVERIFIABLE CLAIMS (Invariant 1): The log files for experiment1_v3_empirical.py, experiment4_interventions.py, phase_d_adversarial.py, phase_e_anomaly.py, phase_g1_order_stats.py, and experiment5c_sensitivity.py are all 0 bytes (confirmed via wc -l). The claimed status 'not-executed / Timed out at Xs' cannot be confirmed from empty logs; the actual stop reason (timeout, startup error, kill signal) is unknown. Affected claimed reasons: 'Timed out at 30s' (experiment1_v3_empirical, experiment4_interventions), 'Timed out at 60s' (phase_d_adversarial, phase_g1_order_stats, experiment5c_sensitivity), 'Timed out at 120s' (phase_e_anomaly).",
      "PHASE_G5 LOG TRUNCATED — SCENARIO C k_damage=3 UNCONFIRMABLE: phase_g5_ros_coupling.log has 40 lines and ends after 'Scenario B: TW=8.0h, eff_t1/2=3.01h, ROS_mod=3.98' for k_damage=3.0. Scenario C for k_damage=3.0 is absent from the log. The claimed observed_behavior 'k_damage=3: TW=8h for B/C matching empirical 4-18h range' cannot be verified for the C component.",
      "EXPERIMENT1B INTERNAL GENE COUNT INCONSISTENCY — UNCLAIMED: experiment1b_v2_gpr_knockout.log step [1] reports 'Mouse: 374, Human: 391' (sum=765, not 769), while step [5] reports 'Human genes: 395' (374+395=769, consistent with the 769 header). The 391 figure in step [1] is internally inconsistent. The claimed '769 nuclear genes scored' is consistent with step [5] but the 4-gene discrepancy between log steps is not disclosed.",
      "GATE G3 VERDICT MISCHARACTERIZED: The coverage entry for experiment5_fba_ode.py claims 'Gate G3 partial pass (only accel scenario crosses threshold)'. The actual log (experiment5_fba_ode.log lines 27-31) shows only three warning lines (each prefixed '⚠') with no PASS or FAIL label emitted. The log explicitly notes 0/3 crossed for in_vivo and uniform regimes, and 2/3 for accel. The log never uses the word 'pass' for Gate G3; the 'partial pass' characterization is the worker's editorial gloss, not a log fact.",
      "EXPERIMENT5B MITQ SELECTIVE TW SELECTIVELY REPORTED: The coverage entry says 'MitoQ selective TW=90h' without qualification. The log (experiment5b_interventions.log line 15) shows TW_ΔΨm=90.45h AND TW_ATP=16.64h. Reporting only the ΔΨm window as 'TW=90h' omits that the ATP transit window is only 16.64h — a materially different figure for the same intervention. The omission could mislead about the intervention's protective effect on ATP viability."
    ],
    "notes": "All directly executed scripts whose logs exist and are non-empty match their claimed outcomes closely: TW values, gene counts, error messages, and finding confirmations all align with log content. The 5 compute-timeout claims and 1 truncated log are the primary accountability failures. The phase_e_supp_parse.log does confirm the Chapman table parse (558,1024) cited in the phase_e coverage entry, but that entry's 'Timed out at 120s' claim for the parent script remains unverifiable from its empty log. No log was found to be missing entirely — all cited log paths exist on disk; the issue is content absence (0 bytes) not file absence."
  }
}
```

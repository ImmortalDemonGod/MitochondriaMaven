# 02 — Static Audit

_Generated 2026-06-17T14:40:45.349Z · branch `claude/upbeat-keller-4c0z1s` · forensic-audit-pipeline_

**44 findings**, each survived an adversarial falsification pass (Stage-2 fixpoint).

## Summary

| Severity | Count |
|---|---|
| high | 7 |
| medium | 21 |
| low | 15 |
| info | 1 |

## Findings

### F02 · [HIGH] beard_qamas_in_vitro_reference.py executes two simulation loops and matplotlib.show() at module level without __main__ guard
- **Class:** reproducibility
- **Location:** `09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py:1`
- **Evidence:** Lines 6-246 build and simulate a Tellurium/RoadRunner model. Lines 257-322 run two nested for-loops (60 iterations each), each calling r.simulate(0,3000,500), then call plt.show() at line 322. There is no 'if __name__ == "__main__":' guard anywhere in the file. Any Python import of this module (e.g., to access constants) triggers ~600 s of simulation and blocks on an interactive matplotlib window. The s1_inventory notes: 'runs at module level without __main__ guard'. This prevents the file from being used as a library and makes CI/automated runs hang.
- **Falsification:** upheld: Module-level te.loada build + sequential simulate loops + plt.show() with no __main__ guard causes import-hang / CI block. 'nested' vs sequential is cosmetic. High justified.

### F03 · [HIGH] setup_environment.sh hardcodes Apple Silicon macOS paths, fails completely on Linux (the current platform)
- **Class:** reproducibility
- **Location:** `09_Computational_Modeling/setup_environment.sh:30`
- **Evidence:** Lines 30-31: CONDA_BIN="/opt/homebrew/Caskroom/miniforge/base/bin/conda" and ENV_PYTHON="/opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/python" are hardcoded to Homebrew on macOS ARM64. Lines 35, 43, 50 then use these variables for conda create, pip install, and the smoke test. The runtime environment (per system notes) is Linux, where /opt/homebrew does not exist. The script will fail at line 35 attempting to run a non-existent CONDA_BIN path. The header comment confirms 'Tested on Apple Silicon (arm64) macOS, April 2026' with no Linux path. Running 'bash setup_environment.sh' on Linux yields command not found errors; the environment cannot be bootstrapped.
- **Falsification:** upheld: Verified setup_environment.sh:30-31 hardcode /opt/homebrew/Caskroom/miniforge conda/python paths; absent on the current Linux platform, so conda create fails under set -e. High appropriate.

### F07 · [HIGH] ANNOTATED_PATH in phase_b_cluster_and_sweep.py resolves to results/essential_genes_annotated.csv but the actual file is at results/phase_b/essential_genes_annotated.csv
- **Class:** bug
- **Location:** `09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py:40`
- **Evidence:** Line 40: ANNOTATED_PATH = results_path('essential_genes_annotated.csv'). results_path() in paths.py joins RESULTS_DIR with the argument, giving 09_Computational_Modeling/results/essential_genes_annotated.csv. The s1_inventory (denominator file) shows the actual written output at 09_Computational_Modeling/results/phase_b/essential_genes_annotated.csv (role: generated, note: '145 essential genes with functional cluster annotations'). phase_b2_clustering() at line 111 calls pd.read_csv(ANNOTATED_PATH), which raises FileNotFoundError at runtime. This breaks Phase B.2 (functional clustering) and consequently Phase B.5 (single-gene sweep, line 217), making the primary B-phase results unreproducible.
- **Falsification:** upheld: phase_b_cluster_and_sweep.py:40 ANNOTATED_PATH=results_path('essential_genes_annotated.csv') resolves flat; disk find confirms the file exists only at results/phase_b/essential_genes_annotated.csv. pd.read_csv raises FileNotFoundError. High upheld.

### F08 · [HIGH] scipy is absent from requirements.txt despite being directly imported by ode_utils.py and phase_k_wet_lab_validation.py
- **Class:** reproducibility
- **Location:** `09_Computational_Modeling/requirements.txt:1`
- **Evidence:** requirements.txt is a complete pip-freeze (all transitive deps pinned: lark, overrides, defusedxml, ruamel.yaml, etc.) but contains no scipy entry. Alphabetically it would appear between Send2Trash==2.1.0 (line 105) and six==1.17.0 (line 106) — absent. ode_utils.py line 45 imports 'from scipy.integrate import solve_ivp' (the core ODE solver used by all composite experiments). phase_k_wet_lab_validation.py line 43 imports 'from scipy.stats import ks_2samp'. Running 'pip install -r requirements.txt' on a clean environment will not install scipy, yielding ImportError when any composite or phase_k script is executed. The entire composite FBA+ODE pipeline (Ex 5-11) and the wet-lab validation (Phase K) are non-functional from a clean install.
- **Falsification:** upheld: grep -i scipy on requirements.txt returns nothing while ode_utils imports solve_ivp from scipy.integrate and phase_k uses scipy.stats.ks_2samp. Clean install ImportErrors the ODE/composite pipeline. High.

### F10 · [HIGH] Verbatim copyrighted journal article text committed — PDF_Metadata JSON files contain full extracted article body
- **Class:** security
- **Location:** `05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.json:1; .gitignore:27-31`
- **Evidence:** .gitignore:28 reads: '05_Extracted_Data/Structured_JSON/ (verbatim paper text — owner opted to include)' and .gitignore:29 reads: '06_Synthesis/Consolidated_Protocols.txt (verbatim front-matter — owner opted to include)'. Reading Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.json confirms its 'article' field contains multi-chunk verbatim extraction of the full Frontiers in Physiology 2021 paper (Caldeira et al., doi:10.3389/fphys.2021.748261), including complete Introduction and Materials sections. The knowledge_triplets section also re-records the author correspondence email address (category: PII, not quoted per policy). The Structured_JSON files (91 files) and PDF_Metadata files (22 files) both contain verbatim extracted text from publisher-copyrighted journal articles. All these files are now tracked (previously excluded prior to the 2026-06-15 gitignore change).
- **Falsification:** upheld: PDF_Metadata JSON git-tracked with an 'article' field holding chunked verbatim journal text; gitignore:27-31 records the owner decision to track Structured_JSON/PDF_Metadata. Copyright exposure real. High.

### F22 · [HIGH] beard_qamas_in_vitro_reference.py imports tellurium and roadrunner at module level; neither is in requirements.txt
- **Class:** reproducibility
- **Location:** `09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py:2-5`
- **Evidence:** Lines 2-4: 'import matplotlib.pyplot as plt; import tellurium as te; import roadrunner'. Line 6: 'r = te.loada(...)' executes immediately at module level without a __main__ guard. requirements.txt (127 entries) contains no tellurium or roadrunner. The inventory note confirms 'runs at module level without main guard'. Any import of this module — or any attempt to reproduce the baseline QAMAS reference run — fails with ImportError on a fresh environment built from requirements.txt.
- **Falsification:** upheld: beard_qamas_in_vitro_reference.py imports tellurium and roadrunner; te.loada runs at module level; requirements.txt has neither (confirmed scipy/tellurium absence). Fresh-env reproduction ImportErrors. High.

### F31 · [HIGH] Uninitialized git submodule leaves MODEL_PATH pointing to non-existent SBML file
- **Class:** reproducibility
- **Location:** `09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/`
- **Evidence:** Shell listing of Whole_Cell_Modeling/mitomammal/ returns empty — the submodule directory contains no files. paths.py:22 sets MODEL_PATH = MITOMAMMAL_DIR / '6_universal_mito_model.xml', which therefore does not exist. Every simulation script (experiment1_v2_transit_window.py, experiment1_v3_empirical.py, phase_k_wet_lab_validation.py, all composite scripts) calls cobra.io.read_sbml_model(MODEL_PATH) and will raise FileNotFoundError immediately. LAB_NOTEBOOK.md:33-50 documents the repo as having been cloned and inspected with model file present, indicating the submodule was registered via .gitmodules (SECURITY-6) without running git submodule update --init, silently voiding the entire computational pipeline.
- **Falsification:** upheld: Confirmed Whole_Cell_Modeling/mitomammal/ is empty so paths.py:22 MODEL_PATH does not exist and cobra.io.read_sbml_model raises FileNotFoundError across all sim scripts. High appropriate.

### F01 · [MEDIUM] compute_fluxes() uses hardcoded MEMBRANE_MAX_FOLD=50.0, inconsistent with beard_rhs() CL_leak_max_fold=20.0
- **Class:** bug
- **Location:** `09_Computational_Modeling/ode_utils.py:520`
- **Evidence:** In beard_rhs() (line 367): leak_multiplier = 1.0 + p.CL_leak_max_fold * cl_ox_clipped, where CL_leak_max_fold defaults to 20.0 (BeardParams line 216). In compute_fluxes() (line 520): MEMBRANE_MAX_FOLD = 50.0 is hardcoded and used in the analogous formula. When leak_growth_rate > 0, compute_fluxes() returns J_leak at 2.5x the magnitude beard_rhs() would produce for the same parameter set. Additionally, beard_rhs drives CL_ox via ODE integration (dCL_ox = (leak_growth_rate/3600)*(1-CL_ox)), then reads it back through leak_multiplier; compute_fluxes() bypasses the ODE state and applies the phenomenological formula directly with the wrong max-fold constant. These two functions are expected to return consistent flux values for the same state.
- **Falsification:** upheld: ode_utils.py:520-525 confirmed: MEMBRANE_MAX_FOLD=50.0 with a time-driven exp leak formula and no MPTP factor, versus beard_rhs:367 leak_multiplier=1+p.CL_leak_max_fold(=20.0)*cl_ox_clipped driven by integrated CL_ox. Constant, driver, and MPTP coupling genuinely inconsistent; bites only when leak_growth_rate>0. Medium fair.

### F04 · [MEDIUM] build_halflife_map_per_subunit() assigns complex-median half-lives to all CI subunits; per-subunit independence assumption is never actually tested
- **Class:** intent-mismatch
- **Location:** `09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py:123`
- **Evidence:** The function (lines 110-132) is documented as the 'per-subunit (independence)' regime, intended to assign individual measured half-lives (from CI_HALFLIVES_INVIVO_HOURS: NDUFS1=138h, NDUFS2=427h, NDUFA9=144h, NDUFB10=120h) to specific CI subunits. Instead, lines 124-131 assign COMPLEX_MEDIANS_INVIVO_HOURS['CI'] (141h) to ALL CI subunits with the comment 'per-subunit assignment requires symbol mapping' not yet implemented. The consequence: both the 'per-subunit (independence)' regime and the 'per-complex (correlated/holoenzyme)' regime (line 136-151) use the same 141h for all CI genes when scale_factor-divided. The core P2 comparison — whether independence vs correlation assumption changes the transit window — tests identical inputs and cannot distinguish the two models. Results reported in phase_h/transit_window_empirical.csv are scientifically invalid for this comparison.
- **Falsification:** amended: Headline defect real at experiment1_v3_empirical.py:124 (per-subunit regime assigns complex median to all CI subunits). But the evidence sub-claim that both regimes test identical inputs is false (per_complex uses a different statistic), so the comparison is not fully degenerate; scope narrowed, defect stands.

### F05 · [MEDIUM] Phase H permutation test null distribution lower bound is log(72h) instead of documented ~3h, biasing toward 'cannot reject independence'
- **Class:** bug
- **Location:** `09_Computational_Modeling/scripts/investigation_phases/phase_h_ci_subunit_analysis.py:176`
- **Evidence:** Lines 174-177: the null is built by sampling from np.random.uniform(np.log(72), np.log(500), 4), giving a log-uniform null on [72h, 500h]. The inline comment states 'broad mitochondrial t½ distribution (~3-500h)' and the intent is to represent any mitochondrial protein. However, the CI subunit observed values span [120h, 427h], which almost entirely overlaps the null [72h, 500h]. Sampling a narrow null that mirrors the data inflates the fraction of null log-ranges >= observed log-range, pushing p_value toward 1.0. The correct lower bound per the comment would be ~np.log(3) (3h). The script reports 'CANNOT REJECT independence' based on this miscalibrated test and the conclusion propagates to ci_correlation_analysis.json and CI_SUBUNIT_DEEP_DIVE.md.
- **Falsification:** upheld: phase_h:176 null lower bound np.log(72) while comment line 175 says '~3-500h'; lower bound should be log(3). Narrowed null overlapping data [120-427h] inflates p toward 'cannot reject'. Medium upheld.

### F09 · [MEDIUM] Third-party PII — Dr. Justin Nash full name and title committed in three tracked files
- **Class:** security
- **Location:** `01_Vision_and_Strategy/Notebook_Transcription_Otter.txt:272; INDEX.md:136; 08_Experimental_Work/Experiments_Overview.md:11`
- **Evidence:** All three files name a former external collaborator by full name and professional title. Notebook_Transcription_Otter.txt:272 reads: 'I think this is when Dr Nash. Justin Nash was asking, how can we use extra funding? He was going to do another grant. He … actually left before the grant came in.' INDEX.md:136 reads: 'Dr. Justin Nash — Former collaborator (departed before grant funding)'. Experiments_Overview.md:11 reads: 'Collaborator: Dr. Justin Nash (departed before grant was funded)'. This individual is not the project lead; no indication of consent for public disclosure of their identity and participation status.
- **Falsification:** upheld: Three cited tracked files name Dr. Justin Nash (former external collaborator) with departure status; no consent indication. Third-party PII at medium appropriate.

### F11 · [MEDIUM] README copyright exclusion claim is now false — README.md:89 states verbatim text extractions are kept local but they are tracked
- **Class:** doc-drift
- **Location:** `README.md:89; .gitignore:27-31`
- **Evidence:** README.md:89 reads: 'Copyrighted source papers — 108 journal PDFs and their verbatim text extractions' are intentionally excluded. However, .gitignore:27-31 contains the block: 'Owner decision 2026-06-15 — the following ARE now tracked (previously excluded): 05_Extracted_Data/Structured_JSON/ (verbatim paper text — owner opted to include) … 06_Synthesis/Consolidated_Protocols.txt (verbatim front-matter — owner opted to include)'. The Structured_JSON directory contains 91 AI-extracted files explicitly labelled 'verbatim paper text'. The README exclusion statement is now factually incorrect, which obscures the current copyright exposure from anyone reading the repository.
- **Falsification:** upheld: README.md:89 lists verbatim text extractions as intentionally excluded, but gitignore:27-31 now tracks the Structured_JSON verbatim-text files. README claim factually false; medium doc-drift correct.

### F13 · [MEDIUM] macOS username 'tomriddle1' and absolute Dropbox paths committed across multiple active documentation files
- **Class:** security
- **Location:** `09_Computational_Modeling/scripts/archive_v1/experiment1_transit_window.py:29; 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_AGENT_HANDOFF.md:46; 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_MITO_QUERY_GUIDE.md:189; 09_Computational_Modeling/LAB_NOTEBOOK.md:600`
- **Evidence:** experiment1_transit_window.py:29 reads: MODEL_PATH = "/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml". DOCINSIGHT_AGENT_HANDOFF.md:46 embeds '/Users/tomriddle1/Dropbox/Mitochondria Maven/…' across at least 10 lines (lines 46-75). DOCINSIGHT_MITO_QUERY_GUIDE.md:189-217 has JSON tool-call fragments with full absolute paths including '/Users/tomriddle1/Dropbox/…'. LAB_NOTEBOOK.md:600 reads: 'Approved plan in /Users/tomriddle1/.claude/plans/silly-drifting-twilight.md'. The username 'tomriddle1', the Dropbox sync layout, and an internal Claude Code plan filename are all committed.
- **Falsification:** upheld: Four anchors contain /Users/tomriddle1/ Dropbox absolute paths plus an internal .claude plan filename across active docs/scripts. Medium reasonable.

### F14 · [MEDIUM] Git submodules registered without pinned commit references — unpinned supply chain for the primary computational models
- **Class:** security
- **Location:** `.gitmodules:1-6`
- **Evidence:** .gitmodules registers two submodules by URL only: (1) mitomammal at https://gitlab.com/habermann_lab/mitomammal.git and (2) Human-GEM at https://github.com/SysBioChalmers/Human-GEM.git. No 'branch =' or 'tag =' constraint is present. While the commit SHA that was active at clone time is stored in the git index, running 'git submodule update --remote' (or a fresh clone that diverges from the stored index commit) silently fetches HEAD of the default branch. MitoMAMMAL is the primary FBA model for all transit-window computations; a silent upstream change to model stoichiometry or gene identifiers would alter all experiment outputs without any visible diff in this repository's tracked files.
- **Falsification:** upheld: .gitmodules registers mitomammal and Human-GEM by URL only with no branch=/tag= pin; 'git submodule update --remote' would fetch upstream HEAD of the primary FBA model. Medium defensible.

### F16 · [MEDIUM] ode_utils.py docstring claims 10 state variables; code defines 13
- **Class:** doc-drift
- **Location:** `09_Computational_Modeling/ode_utils.py:15`
- **Evidence:** Line 15 reads: 'State-vector convention (10 state variables; 3 conserved quantities derived)'. However STATE_NAMES at lines 49-57 has 13 entries: sumATP_x, sumADP_x, sumPi_x, NADH_x, QH2_x, cred_i, sumATP_c, sumADP_c, sumPi_c, DPsi (the original 10) plus Ca_x, H2O2_x, CL_ox added during Session 9 MPTP/ROS work. N_STATES = len(STATE_NAMES) = 13 (line 58). The docstring was never updated after Ca2+, H2O2, and CL_ox states were appended.
- **Falsification:** upheld: Verified ode_utils.py:15 docstring says '10 state variables' but STATE_NAMES has 13 entries (adds Ca_x, H2O2_x, CL_ox) and beard_rhs emits 13 derivatives. Stale docstring. Medium upheld.

### F17 · [MEDIUM] 09_Computational_Modeling/README.md directory map is stale — omits composite scripts and phases G-K
- **Class:** doc-drift
- **Location:** `09_Computational_Modeling/README.md:82-112`
- **Evidence:** The scripts/ tree at lines 82-99 lists only scripts/investigation_phases/{phase_a,phase_b_annotate,phase_b_cluster,phase_b6,phase_c,phase_d,phase_e} and scripts/experiments_v2/{experiment1_v2..1d}. It omits the entire scripts/composite/ directory (experiment5_fba_ode.py through experiment11_ros_mitoq.py, validate_against_beard.py) and phases G-K scripts (phase_g1_order_statistics.py, phase_g2_cross_model.py, phase_g2b_human_gem_decay.py, phase_g5_ros_coupling.py, phase_h_ci_subunit_analysis.py, phase_i_syn3a_crosswalk.py, phase_k_wet_lab_validation.py). The results/ tree (lines 101-108) similarly omits composite/, phase_g/ through phase_k/. These directories exist with populated outputs per the Stage-1 inventory.
- **Falsification:** upheld: 09 README scripts tree (82-99) lists only investigation_phases phase_a..phase_e and experiments_v2; omits scripts/composite/ and phases G-K which exist on disk. Medium.

### F18 · [MEDIUM] scripts/composite/README.md declares all composite experiments 'Not written' but all are implemented with results
- **Class:** doc-drift
- **Location:** `09_Computational_Modeling/scripts/composite/README.md:31-33`
- **Evidence:** README.md lines 31-33 table: experiment5_fba_ode.py='Not written', validate_against_cortassa.py='Not written', experiment6_full_composite.py='Deferred'. In reality the following scripts all exist (confirmed by inventory) and have produced results under results/composite/: experiment5_fba_ode.py, experiment5b_interventions.py, experiment5c_sensitivity.py, experiment6_option_b_extension.py, experiment7_human_gem.py, experiment8_abstract_figure.py, experiment9_atp_first_diagnostic.py, experiment10_mptp_composite.py, experiment11_ros_mitoq.py, validate_against_beard.py. Result files include ex5_1_baseline_validation.csv through ex11_ros_mitoq.csv and multiple PNGs.
- **Falsification:** upheld: composite/README.md marks experiment5_fba_ode.py 'Not written'/experiment6 'Deferred', yet experiment5-11 plus validate_against_beard.py exist with results/composite/ outputs. Medium.

### F19 · [MEDIUM] scripts/composite/README.md names validate_against_cortassa.py but actual file is validate_against_beard.py
- **Class:** doc-drift
- **Location:** `09_Computational_Modeling/scripts/composite/README.md:32`
- **Evidence:** README.md line 32 entry: '| validate_against_cortassa.py | Reference-curve validation of ODE layer in isolation | Not written |'. The actual file on disk is scripts/composite/validate_against_beard.py (inventory role: 'Beard 2005 baseline PO-curve reproduction validation script'). There is no validate_against_cortassa.py file in the repository. The plan intended Cortassa-Aon validation but the implementation targeted Beard 2005.
- **Falsification:** upheld: composite/README.md:32 names validate_against_cortassa.py 'Not written'; actual file is validate_against_beard.py and no cortassa file exists. Medium.

### F21 · [MEDIUM] compute_fluxes uses hardcoded MEMBRANE_MAX_FOLD=50.0 and old leak formula, inconsistent with beard_rhs which uses p.CL_leak_max_fold=20.0 and the Kagan CL_ox mechanism
- **Class:** bug
- **Location:** `09_Computational_Modeling/ode_utils.py:519-525`
- **Evidence:** beard_rhs (lines 362-385) computes proton leak as: cl_ox_clipped = max(min(CL_ox,1),0); leak_multiplier = 1.0 + p.CL_leak_max_fold * cl_ox_clipped (p.CL_leak_max_fold defaults to 20.0 per BeardParams line 216). compute_fluxes (lines 519-525) instead uses: MEMBRANE_MAX_FOLD = 50.0; if p.leak_growth_rate > 0: leak_multiplier = 1.0 + MEMBRANE_MAX_FOLD * (1.0 - np.exp(-p.leak_growth_rate * t_hours)). The constant differs (50 vs 20), the formula differs (exponential growth vs linear-in-CL_ox), and compute_fluxes ignores the MPTP factor entirely. Any flux-analysis call using compute_fluxes when leak_growth_rate > 0 yields a J_leak inconsistent with what beard_rhs integrates.
- **Falsification:** upheld: Verified ode_utils.py:519-525 — same defect as BUGS-1 (MEMBRANE_MAX_FOLD=50.0 time-exp leak, no MPTP factor) vs beard_rhs CL_ox-driven leak at CL_leak_max_fold=20.0. Redundant with BUGS-1 but independently true. Medium accurate.

### F23 · [MEDIUM] INDEX.md describes Consolidated_Protocols.txt as 'All extraction protocols unified' but the file is pip install terminal output
- **Class:** doc-drift
- **Location:** `INDEX.md:69`
- **Evidence:** INDEX.md line 69: '| Consolidated_Protocols.txt | All extraction protocols unified (13,268 lines) |'. The actual file 06_Synthesis/Consolidated_Protocols.txt begins: 'Requirement already satisfied: pydantic in /home/epas/miniconda3/envs/autogen/lib/python3.11/site-packages (2.6.1)...' — it is terminal output from a pip install session accidentally redirected to this file. The inventory (Stage 1) flags the file as 'Accidental pip-install terminal output captured to file; not a protocol'. No protocol content exists in this file.
- **Falsification:** upheld: INDEX.md:69 describes Consolidated_Protocols.txt as 'All extraction protocols unified' but the file head is pip 'Requirement already satisfied' terminal output (SECURITY-4 anchor); no protocol content. Medium.

### F26 · [MEDIUM] composite_utils.py utility module imports apply_scenario from an experiment script at runtime via sys.path injection — inverted dependency
- **Class:** design
- **Location:** `09_Computational_Modeling/composite_utils.py:351-356`
- **Evidence:** composite_utils.py lines 351-356 inside compose_fba_ode(): 'sys.path.insert(0, str(_here / "scripts" / "experiments_v2")); try: from experiment1_v2_transit_window import apply_scenario; apply_scenario(fba_model, scenario); except ImportError: pass'. A shared utility module (composite_utils.py) depends on a specific experiment script (experiment1_v2_transit_window.py). If the import fails, the exception is silently swallowed and scenarios A/B/C are applied without exchange-bound constraints, producing incorrect results with no warning. The architectural inversion also means moving or renaming experiment1_v2_transit_window.py silently breaks composite scenario logic.
- **Falsification:** upheld: Verified composite_utils.py:351-356: shared utility injects scripts/experiments_v2 on sys.path and imports apply_scenario from a specific experiment script with 'except ImportError: pass'. Inverted dependency + silent failure accurate. Medium.

### F28 · [MEDIUM] q-bio Chicago 2026 abstract deadline (May 31) has passed; README.md still marks it as merely 'drafted' with no submission record in the repository
- **Class:** intent-mismatch
- **Location:** `README.md:99`
- **Evidence:** LAB_NOTEBOOK.md line 2: 'q-bio Chicago 2026 abstract (deadline May 31, 2026)'. INDEX.md line 91: 'Status: ACTIVE — q-bio Chicago 2026 abstract deadline May 31.' 09_Computational_Modeling/README.md line 2: 'Deliverable: q-bio Chicago 2026 abstract (May 31, 2026)'. README.md line 99: '✅ Conference-style abstract + full manuscript outline — drafted'. The declared primary deliverable of the provisional intent was a submitted conference abstract. Current date is June 17, 2026. No file in the repository documents submission, acceptance, rejection, or a decision to withdraw. The status symbol '✅' implies completion but the text says only 'drafted', leaving the near-term tractable goal in an unresolved state relative to the stated deadline.
- **Falsification:** upheld: README.md:99 '✅ ... abstract ... drafted' with May 31 2026 deadline passed (today 2026-06-17) and no submission/decision record; ✅ implies completion while text says only drafted. Medium reasonable.

### F30 · [MEDIUM] Double-counted dCL_ox when ros_enabled=True and leak_growth_rate>0 simultaneously
- **Class:** bug
- **Location:** `09_Computational_Modeling/ode_utils.py:444,449-451`
- **Evidence:** beard_rhs(): line 444 sets `dCL_ox = J_Kagan` (Kagan-cycle CL oxidation) when ros_enabled=True. Lines 449-451 then unconditionally add `(p.leak_growth_rate / 3600.0) * (1.0 - cl_ox_clipped)` if leak_growth_rate>0. The two paths are not mutually exclusive — any scenario with ros_enabled=True and a non-zero leak_growth_rate double-counts CL_ox accumulation, producing inflated oxidation and an incorrect leak_multiplier. The comment calls the second path 'backwards-compat' but provides no guard against simultaneous use.
- **Falsification:** upheld: Verified beard_rhs:444 sets dCL_ox=J_Kagan when ros_enabled, then lines 449-451 unconditionally add the leak_growth_rate term with no mutual-exclusion guard — a real latent double-count if both are set; not active in shipped scenarios. Medium upheld.

### F33 · [MEDIUM] Phase K uses two-sample KS test to compare deterministic model output against observations
- **Class:** intent-mismatch
- **Location:** `09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py:169-173`
- **Evidence:** Lines 169-173: flux_at_empirical_t is produced by np.interp (deterministic, no sampling noise) from the MitoMAMMAL predicted curve; empirical_normalized is the digitized JC-1 values. ks_2samp is then called on these two arrays. The two-sample KS test assumes both inputs are iid random samples from unknown distributions; applying it to a deterministic interpolation versus observations violates this assumption and makes the p-value uninterpretable. A one-sample KS test against a fitted CDF, or a goodness-of-fit metric such as RMSE, would be statistically valid here.
- **Falsification:** upheld: phase_k:169 flux_at_empirical_t=np.interp (deterministic) and line 173 ks_2samp against digitized observations; two-sample KS assumes iid samples from both, so the p-value is uninterpretable. Valid statistical critique. Medium.

### F38 · [MEDIUM] read_mitocarta_crossref() uses CWD-relative path, silently falls back to hardcoded stale values
- **Class:** reproducibility
- **Location:** `09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py:95`
- **Evidence:** Line 95: `path = Path('results/phase_b/essential_genes_mitocarta_crossref.csv')` is a bare relative path unlike all other scripts which use results_path(). If script is run from any directory other than 09_Computational_Modeling/, path resolution fails silently and line 97 returns hardcoded fallback (145, 127) without warning, causing the abstract figure to show potentially stale MitoCarta counts.
- **Falsification:** upheld: experiment8_abstract_figure.py:95 path=Path('results/phase_b/...') bare relative (unlike results_path() elsewhere); line 97 returns hardcoded (145,127) when missing, so running from another dir silently yields stale counts. Medium reasonable.

### F41 · [MEDIUM] CompositeResult.atp_trace field stores cytosolic ATP but is documented as matrix ATP
- **Class:** intent-mismatch
- **Location:** `09_Computational_Modeling/composite_utils.py:309,384,424`
- **Evidence:** Field definition at line 309: `atp_trace: np.ndarray = field(default_factory=lambda: np.array([]))  # matrix ATP (mol/L)`. In compose_fba_ode() at line 384, `atp = traj.get('sumATP_x')` (matrix ATP) is a dead assignment never used. At line 424, the return sets `atp_trace=atp_c` where `atp_c = traj.get('sumATP_c')` (cytosolic ATP). Callers reading CompositeResult.atp_trace receive cytosolic ATP while the comment/name implies matrix ATP.
- **Falsification:** upheld: Verified composite_utils.py:309 comment '# matrix ATP (mol/L)', line 384 atp=traj.get('sumATP_x') is a dead assignment, and line 424 returns atp_trace=atp_c (cytosolic sumATP_c). The field stores cytosolic ATP while its comment says matrix ATP — genuine mislabel. Medium upheld.

### F42 · [MEDIUM] compute_fluxes() omits mptp_factor from J_leak, diverging from beard_rhs() by up to 10001x when MPTP is enabled
- **Class:** bug
- **Location:** `09_Computational_Modeling/ode_utils.py:525`
- **Evidence:** beard_rhs() at line 385 computes `J_leak = cap_Leak * p.X_H * leak_multiplier * mptp_factor * (p.H_c * exp(...) - p.H_x * exp(...))` where mptp_factor = 1 + mptp_open_prob * p.mptp_permeability_max (default 1e4). compute_fluxes() at line 525 computes `J_leak = caps['Leak'] * p.X_H * leak_multiplier * (p.H_c * exp(phi/2) - p.H_x * exp(-phi/2))` with no mptp_factor term. When mptp_enabled=True and the pore is open, J_leak reported by compute_fluxes() underestimates actual leak by up to (1 + 1e4) = 10001-fold, making all diagnostic flux readouts at MPTP-active states incorrect.
- **Falsification:** amended: Verified beard_rhs:385 includes mptp_factor (1+mptp_open_prob*p.mptp_permeability_max, default 1e4 at line 180) while compute_fluxes:525 omits it. But compute_fluxes is only called by experiment9 and validate_against_beard, neither of which enables MPTP, so the 10001x divergence is latent, not active. High overstated.

### F43 · [MEDIUM] PARTITION_PATH in experiment1d_minimal_set.py and phase_b_cluster_and_sweep.py resolves to wrong directory, causing FileNotFoundError at runtime
- **Class:** bug
- **Location:** `09_Computational_Modeling/scripts/experiments_v2/experiment1d_minimal_set.py:50,09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py:41`
- **Evidence:** Both files use `results_path('essential_dispensable_partition.json')` which resolves to `results/essential_dispensable_partition.json`. The canonical writer, phase_b_annotate_essentials.py line 31, writes to `results_path('phase_b', 'essential_dispensable_partition.json')` i.e. `results/phase_b/essential_dispensable_partition.json`. No code creates the file at the flat path. Both scripts will raise FileNotFoundError on the open() call. Note: BUGS-7 covers only the ANNOTATED_PATH variable in phase_b_cluster_and_sweep.py, not PARTITION_PATH in either script.
- **Falsification:** upheld: Verified experiment1d_minimal_set.py:50 and phase_b_cluster_and_sweep.py:41 both use results_path('essential_dispensable_partition.json') (flat); disk find confirms the file exists only at results/phase_b/. Distinct from BUGS-7 (ANNOTATED_PATH). FileNotFoundError at runtime. Medium.

### F06 · [LOW] compose_fba_ode() silently swallows ImportError for apply_scenario, leaving FBA model in default state for all scenarios
- **Class:** bug
- **Location:** `09_Computational_Modeling/composite_utils.py:354`
- **Evidence:** Lines 351-356: sys.path.insert(0, str(_here / 'scripts' / 'experiments_v2')); try: from experiment1_v2_transit_window import apply_scenario; apply_scenario(fba_model, scenario); except ImportError: pass. The bare 'pass' means that if the import fails (e.g., wrong working directory, path issue, circular import), no exception is raised and no warning is logged. The FBA model proceeds with default exchange bounds regardless of scenario='B' (arterial) or scenario='C' (ischemic). All downstream composite simulations across scenarios A/B/C would receive identical FBA inputs, making scenario-dependent results impossible. This silent failure mode is undetectable from result CSVs alone.
- **Falsification:** amended: composite_utils.py:351-356 silent 'except ImportError: pass' confirmed, but sys.path.insert prepends the correct experiments_v2 dir so the import normally succeeds and apply_scenario runs; the claimed 'default state for ALL scenarios' is not demonstrated. Real latent risk, not an active failure.

### F12 · [LOW] Development-machine username 'epas' and absolute filesystem paths committed in Consolidated_Protocols.txt
- **Class:** security
- **Location:** `06_Synthesis/Consolidated_Protocols.txt:1; 06_Synthesis/Consolidated_Protocols.txt:207`
- **Evidence:** The file begins (line 1) with pip install output from an earlier machine: 'Requirement already satisfied: pydantic in /home/epas/miniconda3/envs/autogen/lib/python3.11/site-packages'. At approximately line 207 it also contains: 'Successfully saved data to /home/epas/Documents/MitoMAVEN/full_texts/…'. The username 'epas' and the directory layout /home/epas/Documents/MitoMAVEN/ are committed. The Stage-1 inventory confirms this file was accidental terminal output ('Accidental pip-install terminal output captured to file'). The file is 1.4 MB of pipeline log, not a research artifact, yet it is explicitly opted into tracking via .gitignore:29.
- **Falsification:** upheld: Consolidated_Protocols.txt contains /home/epas/ paths from pip-install terminal output; username and local dir layout committed in an accidental log opted into tracking. Low appropriate.

### F15 · [LOW] Shell injection surface in setup_environment.sh — $MITO_DIR interpolated bare into Python inline script string
- **Class:** security
- **Location:** `09_Computational_Modeling/setup_environment.sh:74`
- **Evidence:** setup_environment.sh:74 contains: m = cobra.io.read_sbml_model('$MITO_DIR/6_universal_mito_model.xml') inside a bash double-quoted python -c "..." block. $MITO_DIR is expanded by bash inside the double-quoted string before Python sees it. If the expanded path contains a single-quote character (e.g., if the repo is checked out to a directory containing an apostrophe), the Python string literal becomes malformed, causing a syntax error or — in an adversarially constructed path — injecting arbitrary Python code. In practice the path is derived from the script's own location (SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"), so exploitability requires attacker control over the checkout path. Severity is low but the fix is trivial (use Python's sys.argv or pass the path via a shell variable rather than string interpolation).
- **Falsification:** upheld: setup_environment.sh:74 interpolates bare $MITO_DIR into a python -c block via read_sbml_model('$MITO_DIR/...'); a quote in the path breaks/injects the literal. Exploit needs checkout-path control; low correct.

### F20 · [LOW] Composite README planned Cortassa-Aon 2003/2006 ODE; implementation is exclusively Beard 2005
- **Class:** intent-mismatch
- **Location:** `09_Computational_Modeling/scripts/composite/README.md:13`
- **Evidence:** scripts/composite/README.md line 13: 'ODE energetics (Cortassa-Aon 2003/2006; Beard 2005)' — Cortassa-Aon is listed as the primary ODE choice. The actual ode_utils.py (line 6) states: 'Implements the Beard 2005 mitochondrial OXPHOS ODE system'; composite_utils.py (line 21) similarly references 'Beard-2005 biophysical OXPHOS ODE'. The Whole_Cell_Modeling/cortassa/ directory exists (defined in paths.py:49) but contains only a README with no implementation. Cortassa-Aon was never implemented; the stated design intent was not realized.
- **Falsification:** upheld: composite/README.md:13 lists 'Cortassa-Aon 2003/2006; Beard 2005' but ode_utils/composite_utils implement only Beard 2005; cortassa/ dir has no implementation. Low upheld.

### F24 · [LOW] INDEX.md lists 03_Study_Registry/source_archive.zip as a repository file but it does not exist
- **Class:** doc-drift
- **Location:** `INDEX.md:41`
- **Evidence:** INDEX.md line 41: '| source_archive.zip | Original import bundle from literature search |'. A Glob search for /home/user/MitochondriaMaven/03_Study_Registry/source_archive.zip returns no results. The Stage-1 inventory of 319 files does not list this path. The file is documented as existing but is absent from the repository.
- **Falsification:** upheld: INDEX.md lists 03_Study_Registry/source_archive.zip but the path is absent on disk. Documented-but-absent file. Low.

### F25 · [LOW] paths.py omits BEARD_DIR which ode_utils.py attempts to import from it; paths.py contract as single source of truth is broken
- **Class:** design
- **Location:** `09_Computational_Modeling/ode_utils.py:657-659`
- **Evidence:** ode_utils.py lines 657-659: 'try: from paths import BEARD_DIR; return BEARD_DIR / "beard_2005_params.csv"; except ImportError: return Path(__file__).resolve().parent / "Whole_Cell_Modeling" / "beards_lab" / "beard_2005_params.csv"'. paths.py defines MITOMAMMAL_DIR, CORTASSA_DIR, and all script/result dirs, but has no BEARD_DIR. The import always fails, the fallback hardcodes the path. paths.py (line 9) documents itself as 'single source of truth for all paths'; the omission of BEARD_DIR violates this contract, and the silent fallback means the violation is never surfaced.
- **Falsification:** upheld: ode_utils.py:657-659 'try: from paths import BEARD_DIR except ImportError: hardcoded fallback'; paths.py has no BEARD_DIR so the import always fails and the fallback always runs, contradicting paths.py 'single source of truth'. Low.

### F27 · [LOW] LAB_NOTEBOOK.md Session 1 states efflux_method.py 'we do NOT need it'; it is now a core dependency imported by every experiment
- **Class:** doc-drift
- **Location:** `09_Computational_Modeling/LAB_NOTEBOOK.md:49`
- **Evidence:** LAB_NOTEBOOK.md line 49 (Session 1 MitoMAMMAL repo inspection): 'efflux_method.py — E-Flux constraint function (used in their analysis; we do NOT need it)'. By Session 3 the GPR-aware decay audit (Session 2 fix #4) reversed this decision. decay_utils.py line 32: 'from efflux_method import evaluate_gpr_expression, remove_genes'. composite_utils.py line 54: 'from efflux_method import evaluate_gpr_expression, remove_genes'. The original assessment is preserved unchanged in the notebook while the actual usage is opposite; a reader following the notebook would expect the dependency not to exist.
- **Falsification:** upheld: LAB_NOTEBOOK Session-1 note says efflux_method.py 'we do NOT need it' yet decay_utils.py:32 and composite_utils.py:54 both import from efflux_method — now a core dependency, opposite of the preserved note. Low.

### F29 · [LOW] Hardcoded 0.175 V DPsi normalization in MCU uptake formula
- **Class:** bug
- **Location:** `09_Computational_Modeling/ode_utils.py:391`
- **Evidence:** Line 391: `dpsi_factor = max(DPsi, 0) / 0.175` hardcodes the nominal resting ΔΨm as a literal 0.175 V. The parametrized baseline is 175e-3 V (stored elsewhere), but this normalization constant is not drawn from BeardParams. If SCENARIO_ODE_OVERRIDES or direct BeardParams edits change the baseline DPsi, the MCU thermodynamic driving-force scaling becomes incorrect while no warning is emitted.
- **Falsification:** upheld: Verified ode_utils.py:391 dpsi_factor=max(DPsi,0)/0.175 hardcodes resting ΔΨm normalization rather than drawing from BeardParams. Accurate; narrow blast radius. Low correct.

### F32 · [LOW] INDEX.md:98 stale claim that MitoMAMMAL repo is still awaiting cloning
- **Class:** doc-drift
- **Location:** `INDEX.md:98`
- **Evidence:** INDEX.md:98 states 'Awaiting cloned repos (Luthey-Schulten Lab Minimal_Cell + Habermann Lab MitoMAMMAL)'. LAB_NOTEBOOK.md:33 documents 'Cloned from: https://gitlab.com/habermann_lab/mitomammal.git' and lines 36-54 record a full inspection of repo contents (model filename discrepancy, reaction/gene/metabolite counts, efflux_method.py contents). The INDEX.md master status table therefore misrepresents the project state to any reader using it as a source of truth.
- **Falsification:** upheld: INDEX.md:98 'Awaiting cloned repos ... MitoMAMMAL' while LAB_NOTEBOOK documents the repo cloned and inspected. Stale status. Low.

### F34 · [LOW] Phase K imports build_halflife_map_per_subunit from experiments_v2 via sys.path injection
- **Class:** design
- **Location:** `09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py:50-51`
- **Evidence:** Lines 50-51: `sys.path.insert(0, str(Path(__file__).parent.parent / 'experiments_v2'))` followed by `from experiment1_v3_empirical import build_halflife_map_per_subunit`. This is the same inverted-dependency anti-pattern flagged in DRIFT-11 for composite_utils.py, but it is a separate occurrence in a different module (investigation phase script importing from an experiment script). The function should be factored into a shared utility module rather than requiring scripts to mutate sys.path to reach peer-level experiment code.
- **Falsification:** upheld: phase_k:50-51 sys.path.insert(.../experiments_v2) then import build_halflife_map_per_subunit from experiment1_v3_empirical — a distinct occurrence of the inverted-dependency pattern. Low.

### F35 · [LOW] flux_buffer parameter declared in build_capacity_envelope_fn but explicitly never used
- **Class:** design
- **Location:** `09_Computational_Modeling/composite_utils.py:154`
- **Evidence:** Line 154: `flux_buffer: float = 1.05,  # unused here; kept for signature parity`. The parameter is accepted by the function signature but the comment confirms it is never applied inside the function body. No caller documentation identifies which external signature it is matching. This represents an incomplete refactoring — either the flux-boundary scaling the parameter implies was removed without updating callers, or the parameter was added preemptively and the implementation was never written.
- **Falsification:** upheld: composite_utils.py:154 'flux_buffer: float = 1.05,  # unused here; kept for signature parity' — accepted but never applied; incomplete-refactoring smell. Low.

### F36 · [LOW] Dead 'if False' branch in MPTP experiment leaves Ca²⁺ trajectory permanently unaudited
- **Class:** bug
- **Location:** `09_Computational_Modeling/scripts/composite/experiment10_mptp_composite.py:82`
- **Evidence:** Line 82: `ca_x_peak = np.max(result.delta_psi_trace) if False else None  # placeholder` — the `if False` guard is permanently False so ca_x_peak is always None. Comments at lines 83-84 confirm Ca_x is not exposed through CompositeResult. Even if the condition were True, it would compute max(ΔΨm), not Ca²⁺ peak — the wrong metric for an MPTP audit.
- **Falsification:** upheld: Verified experiment10_mptp_composite.py:82 'ca_x_peak = np.max(result.delta_psi_trace) if False else None  # placeholder'; always None and would compute ΔΨm max not Ca peak, and never added to output rows. Benign acknowledged placeholder; low correct.

### F37 · [LOW] Abstract figure labels Kagan-cycle panel as 'Ex 12' but no Ex 12 exists; only Ex 11
- **Class:** doc-drift
- **Location:** `09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py:188`
- **Evidence:** Line 188: label='Kagan-cycle mechanistic (Ex 12)' and docstring line 6: 'Ex 12 Kagan-cycle data'. The only ROS/MitoQ experiment in the repository is experiment11_ros_mitoq.py. No Ex 12 script or output exists. This mislabeling appears in the conference abstract figure final_abstract_figure_composite.png.
- **Falsification:** upheld: Verified experiment8_abstract_figure.py:188 label='Kagan-cycle mechanistic (Ex 12)' while only experiment11_ros_mitoq.py exists. Cosmetic legend mislabel that ships in the figure; low correct.

### F40 · [LOW] phase_g5_ros_coupling computes O2s-rate variables that go unused; comment and implementation describe different coupling mechanisms
- **Class:** intent-mismatch
- **Location:** `09_Computational_Modeling/scripts/investigation_phases/phase_g5_ros_coupling.py:57`
- **Evidence:** Lines 57 and 63 compute baseline_o2s_rate and ref_o2s_rate from CI flux * 0.002, log them, but never use them in the modifier. The comment at lines 69-70 states 'ROS_modifier = 1 + k x (baseline_o2s_rate / ref_o2s_rate)' but the implementation at lines 73-74 uses `o2_relative_drop = max(0, 1 - o2_uptake / ref_o2); ros_modifier = 1.0 + k_damage * o2_relative_drop` — an O2-uptake-ratio proxy, not an O2s-rate ratio. Intended and implemented coupling mechanisms differ.
- **Falsification:** amended: phase_g5:57,63 compute baseline_o2s_rate/ref_o2s_rate and never use them — real dead computation. But the 'mechanisms differ' framing is overstated: the comment documents the implemented O2-drop mechanism that lines 73-74 actually use. Defect is unused vars, not a hidden mechanism swap.

### F44 · [LOW] Dead params dict in phase_b_annotate_essentials.py silently drops the size=1 MyGene.info result-count limit
- **Class:** bug
- **Location:** `09_Computational_Modeling/scripts/investigation_phases/phase_b_annotate_essentials.py:44-63`
- **Evidence:** Lines 44-55 build a `params` dict containing `'size': 1` and `'q': ','.join(batch)`. The subsequent requests.post() at line 58 constructs its own inline dict `{'ids': ','.join(batch), 'scopes': 'ensembl.gene', 'species': species, 'fields': params['fields']}`, extracting only `params['fields']`. The `size`, `q`, and other keys in `params` are never sent. The MyGene.info batch endpoint defaults to returning multiple hits per query gene; the intended `size: 1` guard against multi-hit pollution is silently absent, potentially returning duplicate or off-target annotations per gene ID.
- **Falsification:** upheld: Verified phase_b_annotate_essentials.py:44-55 build a params dict with 'size':1 and 'q', but the requests.post at 58-63 sends its own inline dict extracting only params['fields']; 'size' and 'q' are dropped, so the size=1 multi-hit guard is silently absent. Low correct.

### F39 · [INFO] validate_against_beard.py run_steady_state return-type annotation claims 3-tuple but function returns 4-tuple
- **Class:** doc-drift
- **Location:** `09_Computational_Modeling/scripts/composite/validate_against_beard.py:51`
- **Evidence:** Line 51: `def run_steady_state(params: BeardParams, y0: np.ndarray) -> tuple[np.ndarray, dict, float]:` annotates a 3-element return. Line 57 actually returns `return y_ss, fluxes, j_o2, traj.success` (4 elements). Caller at line 67 correctly unpacks 4 values so runtime is unaffected, but the annotation is wrong.
- **Falsification:** upheld: validate_against_beard.py:51 annotation '-> tuple[np.ndarray, dict, float]' (3) while line 57 returns 4 and caller line 67 unpacks 4. Annotation wrong, runtime unaffected. Info correct.



## Machine-checkable data

```json
{
  "findings": [
    {
      "id": "F01",
      "title": "compute_fluxes() uses hardcoded MEMBRANE_MAX_FOLD=50.0, inconsistent with beard_rhs() CL_leak_max_fold=20.0",
      "location": "09_Computational_Modeling/ode_utils.py:520",
      "class": "bug",
      "severity": "medium",
      "evidence": "In beard_rhs() (line 367): leak_multiplier = 1.0 + p.CL_leak_max_fold * cl_ox_clipped, where CL_leak_max_fold defaults to 20.0 (BeardParams line 216). In compute_fluxes() (line 520): MEMBRANE_MAX_FOLD = 50.0 is hardcoded and used in the analogous formula. When leak_growth_rate > 0, compute_fluxes() returns J_leak at 2.5x the magnitude beard_rhs() would produce for the same parameter set. Additionally, beard_rhs drives CL_ox via ODE integration (dCL_ox = (leak_growth_rate/3600)*(1-CL_ox)), then reads it back through leak_multiplier; compute_fluxes() bypasses the ODE state and applies the phenomenological formula directly with the wrong max-fold constant. These two functions are expected to return consistent flux values for the same state.",
      "falsification": "upheld: ode_utils.py:520-525 confirmed: MEMBRANE_MAX_FOLD=50.0 with a time-driven exp leak formula and no MPTP factor, versus beard_rhs:367 leak_multiplier=1+p.CL_leak_max_fold(=20.0)*cl_ox_clipped driven by integrated CL_ox. Constant, driver, and MPTP coupling genuinely inconsistent; bites only when leak_growth_rate>0. Medium fair."
    },
    {
      "id": "F02",
      "title": "beard_qamas_in_vitro_reference.py executes two simulation loops and matplotlib.show() at module level without __main__ guard",
      "location": "09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py:1",
      "class": "reproducibility",
      "severity": "high",
      "evidence": "Lines 6-246 build and simulate a Tellurium/RoadRunner model. Lines 257-322 run two nested for-loops (60 iterations each), each calling r.simulate(0,3000,500), then call plt.show() at line 322. There is no 'if __name__ == \"__main__\":' guard anywhere in the file. Any Python import of this module (e.g., to access constants) triggers ~600 s of simulation and blocks on an interactive matplotlib window. The s1_inventory notes: 'runs at module level without __main__ guard'. This prevents the file from being used as a library and makes CI/automated runs hang.",
      "falsification": "upheld: Module-level te.loada build + sequential simulate loops + plt.show() with no __main__ guard causes import-hang / CI block. 'nested' vs sequential is cosmetic. High justified."
    },
    {
      "id": "F03",
      "title": "setup_environment.sh hardcodes Apple Silicon macOS paths, fails completely on Linux (the current platform)",
      "location": "09_Computational_Modeling/setup_environment.sh:30",
      "class": "reproducibility",
      "severity": "high",
      "evidence": "Lines 30-31: CONDA_BIN=\"/opt/homebrew/Caskroom/miniforge/base/bin/conda\" and ENV_PYTHON=\"/opt/homebrew/Caskroom/miniforge/base/envs/mitomammal/bin/python\" are hardcoded to Homebrew on macOS ARM64. Lines 35, 43, 50 then use these variables for conda create, pip install, and the smoke test. The runtime environment (per system notes) is Linux, where /opt/homebrew does not exist. The script will fail at line 35 attempting to run a non-existent CONDA_BIN path. The header comment confirms 'Tested on Apple Silicon (arm64) macOS, April 2026' with no Linux path. Running 'bash setup_environment.sh' on Linux yields command not found errors; the environment cannot be bootstrapped.",
      "falsification": "upheld: Verified setup_environment.sh:30-31 hardcode /opt/homebrew/Caskroom/miniforge conda/python paths; absent on the current Linux platform, so conda create fails under set -e. High appropriate."
    },
    {
      "id": "F04",
      "title": "build_halflife_map_per_subunit() assigns complex-median half-lives to all CI subunits; per-subunit independence assumption is never actually tested",
      "location": "09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py:123",
      "class": "intent-mismatch",
      "severity": "medium",
      "evidence": "The function (lines 110-132) is documented as the 'per-subunit (independence)' regime, intended to assign individual measured half-lives (from CI_HALFLIVES_INVIVO_HOURS: NDUFS1=138h, NDUFS2=427h, NDUFA9=144h, NDUFB10=120h) to specific CI subunits. Instead, lines 124-131 assign COMPLEX_MEDIANS_INVIVO_HOURS['CI'] (141h) to ALL CI subunits with the comment 'per-subunit assignment requires symbol mapping' not yet implemented. The consequence: both the 'per-subunit (independence)' regime and the 'per-complex (correlated/holoenzyme)' regime (line 136-151) use the same 141h for all CI genes when scale_factor-divided. The core P2 comparison — whether independence vs correlation assumption changes the transit window — tests identical inputs and cannot distinguish the two models. Results reported in phase_h/transit_window_empirical.csv are scientifically invalid for this comparison.",
      "falsification": "amended: Headline defect real at experiment1_v3_empirical.py:124 (per-subunit regime assigns complex median to all CI subunits). But the evidence sub-claim that both regimes test identical inputs is false (per_complex uses a different statistic), so the comparison is not fully degenerate; scope narrowed, defect stands."
    },
    {
      "id": "F05",
      "title": "Phase H permutation test null distribution lower bound is log(72h) instead of documented ~3h, biasing toward 'cannot reject independence'",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_h_ci_subunit_analysis.py:176",
      "class": "bug",
      "severity": "medium",
      "evidence": "Lines 174-177: the null is built by sampling from np.random.uniform(np.log(72), np.log(500), 4), giving a log-uniform null on [72h, 500h]. The inline comment states 'broad mitochondrial t½ distribution (~3-500h)' and the intent is to represent any mitochondrial protein. However, the CI subunit observed values span [120h, 427h], which almost entirely overlaps the null [72h, 500h]. Sampling a narrow null that mirrors the data inflates the fraction of null log-ranges >= observed log-range, pushing p_value toward 1.0. The correct lower bound per the comment would be ~np.log(3) (3h). The script reports 'CANNOT REJECT independence' based on this miscalibrated test and the conclusion propagates to ci_correlation_analysis.json and CI_SUBUNIT_DEEP_DIVE.md.",
      "falsification": "upheld: phase_h:176 null lower bound np.log(72) while comment line 175 says '~3-500h'; lower bound should be log(3). Narrowed null overlapping data [120-427h] inflates p toward 'cannot reject'. Medium upheld."
    },
    {
      "id": "F06",
      "title": "compose_fba_ode() silently swallows ImportError for apply_scenario, leaving FBA model in default state for all scenarios",
      "location": "09_Computational_Modeling/composite_utils.py:354",
      "class": "bug",
      "severity": "low",
      "evidence": "Lines 351-356: sys.path.insert(0, str(_here / 'scripts' / 'experiments_v2')); try: from experiment1_v2_transit_window import apply_scenario; apply_scenario(fba_model, scenario); except ImportError: pass. The bare 'pass' means that if the import fails (e.g., wrong working directory, path issue, circular import), no exception is raised and no warning is logged. The FBA model proceeds with default exchange bounds regardless of scenario='B' (arterial) or scenario='C' (ischemic). All downstream composite simulations across scenarios A/B/C would receive identical FBA inputs, making scenario-dependent results impossible. This silent failure mode is undetectable from result CSVs alone.",
      "falsification": "amended: composite_utils.py:351-356 silent 'except ImportError: pass' confirmed, but sys.path.insert prepends the correct experiments_v2 dir so the import normally succeeds and apply_scenario runs; the claimed 'default state for ALL scenarios' is not demonstrated. Real latent risk, not an active failure."
    },
    {
      "id": "F07",
      "title": "ANNOTATED_PATH in phase_b_cluster_and_sweep.py resolves to results/essential_genes_annotated.csv but the actual file is at results/phase_b/essential_genes_annotated.csv",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py:40",
      "class": "bug",
      "severity": "high",
      "evidence": "Line 40: ANNOTATED_PATH = results_path('essential_genes_annotated.csv'). results_path() in paths.py joins RESULTS_DIR with the argument, giving 09_Computational_Modeling/results/essential_genes_annotated.csv. The s1_inventory (denominator file) shows the actual written output at 09_Computational_Modeling/results/phase_b/essential_genes_annotated.csv (role: generated, note: '145 essential genes with functional cluster annotations'). phase_b2_clustering() at line 111 calls pd.read_csv(ANNOTATED_PATH), which raises FileNotFoundError at runtime. This breaks Phase B.2 (functional clustering) and consequently Phase B.5 (single-gene sweep, line 217), making the primary B-phase results unreproducible.",
      "falsification": "upheld: phase_b_cluster_and_sweep.py:40 ANNOTATED_PATH=results_path('essential_genes_annotated.csv') resolves flat; disk find confirms the file exists only at results/phase_b/essential_genes_annotated.csv. pd.read_csv raises FileNotFoundError. High upheld."
    },
    {
      "id": "F08",
      "title": "scipy is absent from requirements.txt despite being directly imported by ode_utils.py and phase_k_wet_lab_validation.py",
      "location": "09_Computational_Modeling/requirements.txt:1",
      "class": "reproducibility",
      "severity": "high",
      "evidence": "requirements.txt is a complete pip-freeze (all transitive deps pinned: lark, overrides, defusedxml, ruamel.yaml, etc.) but contains no scipy entry. Alphabetically it would appear between Send2Trash==2.1.0 (line 105) and six==1.17.0 (line 106) — absent. ode_utils.py line 45 imports 'from scipy.integrate import solve_ivp' (the core ODE solver used by all composite experiments). phase_k_wet_lab_validation.py line 43 imports 'from scipy.stats import ks_2samp'. Running 'pip install -r requirements.txt' on a clean environment will not install scipy, yielding ImportError when any composite or phase_k script is executed. The entire composite FBA+ODE pipeline (Ex 5-11) and the wet-lab validation (Phase K) are non-functional from a clean install.",
      "falsification": "upheld: grep -i scipy on requirements.txt returns nothing while ode_utils imports solve_ivp from scipy.integrate and phase_k uses scipy.stats.ks_2samp. Clean install ImportErrors the ODE/composite pipeline. High."
    },
    {
      "id": "F09",
      "title": "Third-party PII — Dr. Justin Nash full name and title committed in three tracked files",
      "location": "01_Vision_and_Strategy/Notebook_Transcription_Otter.txt:272; INDEX.md:136; 08_Experimental_Work/Experiments_Overview.md:11",
      "class": "security",
      "severity": "medium",
      "evidence": "All three files name a former external collaborator by full name and professional title. Notebook_Transcription_Otter.txt:272 reads: 'I think this is when Dr Nash. Justin Nash was asking, how can we use extra funding? He was going to do another grant. He … actually left before the grant came in.' INDEX.md:136 reads: 'Dr. Justin Nash — Former collaborator (departed before grant funding)'. Experiments_Overview.md:11 reads: 'Collaborator: Dr. Justin Nash (departed before grant was funded)'. This individual is not the project lead; no indication of consent for public disclosure of their identity and participation status.",
      "falsification": "upheld: Three cited tracked files name Dr. Justin Nash (former external collaborator) with departure status; no consent indication. Third-party PII at medium appropriate."
    },
    {
      "id": "F10",
      "title": "Verbatim copyrighted journal article text committed — PDF_Metadata JSON files contain full extracted article body",
      "location": "05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.json:1; .gitignore:27-31",
      "class": "security",
      "severity": "high",
      "evidence": ".gitignore:28 reads: '05_Extracted_Data/Structured_JSON/ (verbatim paper text — owner opted to include)' and .gitignore:29 reads: '06_Synthesis/Consolidated_Protocols.txt (verbatim front-matter — owner opted to include)'. Reading Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.json confirms its 'article' field contains multi-chunk verbatim extraction of the full Frontiers in Physiology 2021 paper (Caldeira et al., doi:10.3389/fphys.2021.748261), including complete Introduction and Materials sections. The knowledge_triplets section also re-records the author correspondence email address (category: PII, not quoted per policy). The Structured_JSON files (91 files) and PDF_Metadata files (22 files) both contain verbatim extracted text from publisher-copyrighted journal articles. All these files are now tracked (previously excluded prior to the 2026-06-15 gitignore change).",
      "falsification": "upheld: PDF_Metadata JSON git-tracked with an 'article' field holding chunked verbatim journal text; gitignore:27-31 records the owner decision to track Structured_JSON/PDF_Metadata. Copyright exposure real. High."
    },
    {
      "id": "F11",
      "title": "README copyright exclusion claim is now false — README.md:89 states verbatim text extractions are kept local but they are tracked",
      "location": "README.md:89; .gitignore:27-31",
      "class": "doc-drift",
      "severity": "medium",
      "evidence": "README.md:89 reads: 'Copyrighted source papers — 108 journal PDFs and their verbatim text extractions' are intentionally excluded. However, .gitignore:27-31 contains the block: 'Owner decision 2026-06-15 — the following ARE now tracked (previously excluded): 05_Extracted_Data/Structured_JSON/ (verbatim paper text — owner opted to include) … 06_Synthesis/Consolidated_Protocols.txt (verbatim front-matter — owner opted to include)'. The Structured_JSON directory contains 91 AI-extracted files explicitly labelled 'verbatim paper text'. The README exclusion statement is now factually incorrect, which obscures the current copyright exposure from anyone reading the repository.",
      "falsification": "upheld: README.md:89 lists verbatim text extractions as intentionally excluded, but gitignore:27-31 now tracks the Structured_JSON verbatim-text files. README claim factually false; medium doc-drift correct."
    },
    {
      "id": "F12",
      "title": "Development-machine username 'epas' and absolute filesystem paths committed in Consolidated_Protocols.txt",
      "location": "06_Synthesis/Consolidated_Protocols.txt:1; 06_Synthesis/Consolidated_Protocols.txt:207",
      "class": "security",
      "severity": "low",
      "evidence": "The file begins (line 1) with pip install output from an earlier machine: 'Requirement already satisfied: pydantic in /home/epas/miniconda3/envs/autogen/lib/python3.11/site-packages'. At approximately line 207 it also contains: 'Successfully saved data to /home/epas/Documents/MitoMAVEN/full_texts/…'. The username 'epas' and the directory layout /home/epas/Documents/MitoMAVEN/ are committed. The Stage-1 inventory confirms this file was accidental terminal output ('Accidental pip-install terminal output captured to file'). The file is 1.4 MB of pipeline log, not a research artifact, yet it is explicitly opted into tracking via .gitignore:29.",
      "falsification": "upheld: Consolidated_Protocols.txt contains /home/epas/ paths from pip-install terminal output; username and local dir layout committed in an accidental log opted into tracking. Low appropriate."
    },
    {
      "id": "F13",
      "title": "macOS username 'tomriddle1' and absolute Dropbox paths committed across multiple active documentation files",
      "location": "09_Computational_Modeling/scripts/archive_v1/experiment1_transit_window.py:29; 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_AGENT_HANDOFF.md:46; 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_MITO_QUERY_GUIDE.md:189; 09_Computational_Modeling/LAB_NOTEBOOK.md:600",
      "class": "security",
      "severity": "medium",
      "evidence": "experiment1_transit_window.py:29 reads: MODEL_PATH = \"/Users/tomriddle1/Dropbox/Mitochondria Maven/09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml\". DOCINSIGHT_AGENT_HANDOFF.md:46 embeds '/Users/tomriddle1/Dropbox/Mitochondria Maven/…' across at least 10 lines (lines 46-75). DOCINSIGHT_MITO_QUERY_GUIDE.md:189-217 has JSON tool-call fragments with full absolute paths including '/Users/tomriddle1/Dropbox/…'. LAB_NOTEBOOK.md:600 reads: 'Approved plan in /Users/tomriddle1/.claude/plans/silly-drifting-twilight.md'. The username 'tomriddle1', the Dropbox sync layout, and an internal Claude Code plan filename are all committed.",
      "falsification": "upheld: Four anchors contain /Users/tomriddle1/ Dropbox absolute paths plus an internal .claude plan filename across active docs/scripts. Medium reasonable."
    },
    {
      "id": "F14",
      "title": "Git submodules registered without pinned commit references — unpinned supply chain for the primary computational models",
      "location": ".gitmodules:1-6",
      "class": "security",
      "severity": "medium",
      "evidence": ".gitmodules registers two submodules by URL only: (1) mitomammal at https://gitlab.com/habermann_lab/mitomammal.git and (2) Human-GEM at https://github.com/SysBioChalmers/Human-GEM.git. No 'branch =' or 'tag =' constraint is present. While the commit SHA that was active at clone time is stored in the git index, running 'git submodule update --remote' (or a fresh clone that diverges from the stored index commit) silently fetches HEAD of the default branch. MitoMAMMAL is the primary FBA model for all transit-window computations; a silent upstream change to model stoichiometry or gene identifiers would alter all experiment outputs without any visible diff in this repository's tracked files.",
      "falsification": "upheld: .gitmodules registers mitomammal and Human-GEM by URL only with no branch=/tag= pin; 'git submodule update --remote' would fetch upstream HEAD of the primary FBA model. Medium defensible."
    },
    {
      "id": "F15",
      "title": "Shell injection surface in setup_environment.sh — $MITO_DIR interpolated bare into Python inline script string",
      "location": "09_Computational_Modeling/setup_environment.sh:74",
      "class": "security",
      "severity": "low",
      "evidence": "setup_environment.sh:74 contains: m = cobra.io.read_sbml_model('$MITO_DIR/6_universal_mito_model.xml') inside a bash double-quoted python -c \"...\" block. $MITO_DIR is expanded by bash inside the double-quoted string before Python sees it. If the expanded path contains a single-quote character (e.g., if the repo is checked out to a directory containing an apostrophe), the Python string literal becomes malformed, causing a syntax error or — in an adversarially constructed path — injecting arbitrary Python code. In practice the path is derived from the script's own location (SCRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"), so exploitability requires attacker control over the checkout path. Severity is low but the fix is trivial (use Python's sys.argv or pass the path via a shell variable rather than string interpolation).",
      "falsification": "upheld: setup_environment.sh:74 interpolates bare $MITO_DIR into a python -c block via read_sbml_model('$MITO_DIR/...'); a quote in the path breaks/injects the literal. Exploit needs checkout-path control; low correct."
    },
    {
      "id": "F16",
      "title": "ode_utils.py docstring claims 10 state variables; code defines 13",
      "location": "09_Computational_Modeling/ode_utils.py:15",
      "class": "doc-drift",
      "severity": "medium",
      "evidence": "Line 15 reads: 'State-vector convention (10 state variables; 3 conserved quantities derived)'. However STATE_NAMES at lines 49-57 has 13 entries: sumATP_x, sumADP_x, sumPi_x, NADH_x, QH2_x, cred_i, sumATP_c, sumADP_c, sumPi_c, DPsi (the original 10) plus Ca_x, H2O2_x, CL_ox added during Session 9 MPTP/ROS work. N_STATES = len(STATE_NAMES) = 13 (line 58). The docstring was never updated after Ca2+, H2O2, and CL_ox states were appended.",
      "falsification": "upheld: Verified ode_utils.py:15 docstring says '10 state variables' but STATE_NAMES has 13 entries (adds Ca_x, H2O2_x, CL_ox) and beard_rhs emits 13 derivatives. Stale docstring. Medium upheld."
    },
    {
      "id": "F17",
      "title": "09_Computational_Modeling/README.md directory map is stale — omits composite scripts and phases G-K",
      "location": "09_Computational_Modeling/README.md:82-112",
      "class": "doc-drift",
      "severity": "medium",
      "evidence": "The scripts/ tree at lines 82-99 lists only scripts/investigation_phases/{phase_a,phase_b_annotate,phase_b_cluster,phase_b6,phase_c,phase_d,phase_e} and scripts/experiments_v2/{experiment1_v2..1d}. It omits the entire scripts/composite/ directory (experiment5_fba_ode.py through experiment11_ros_mitoq.py, validate_against_beard.py) and phases G-K scripts (phase_g1_order_statistics.py, phase_g2_cross_model.py, phase_g2b_human_gem_decay.py, phase_g5_ros_coupling.py, phase_h_ci_subunit_analysis.py, phase_i_syn3a_crosswalk.py, phase_k_wet_lab_validation.py). The results/ tree (lines 101-108) similarly omits composite/, phase_g/ through phase_k/. These directories exist with populated outputs per the Stage-1 inventory.",
      "falsification": "upheld: 09 README scripts tree (82-99) lists only investigation_phases phase_a..phase_e and experiments_v2; omits scripts/composite/ and phases G-K which exist on disk. Medium."
    },
    {
      "id": "F18",
      "title": "scripts/composite/README.md declares all composite experiments 'Not written' but all are implemented with results",
      "location": "09_Computational_Modeling/scripts/composite/README.md:31-33",
      "class": "doc-drift",
      "severity": "medium",
      "evidence": "README.md lines 31-33 table: experiment5_fba_ode.py='Not written', validate_against_cortassa.py='Not written', experiment6_full_composite.py='Deferred'. In reality the following scripts all exist (confirmed by inventory) and have produced results under results/composite/: experiment5_fba_ode.py, experiment5b_interventions.py, experiment5c_sensitivity.py, experiment6_option_b_extension.py, experiment7_human_gem.py, experiment8_abstract_figure.py, experiment9_atp_first_diagnostic.py, experiment10_mptp_composite.py, experiment11_ros_mitoq.py, validate_against_beard.py. Result files include ex5_1_baseline_validation.csv through ex11_ros_mitoq.csv and multiple PNGs.",
      "falsification": "upheld: composite/README.md marks experiment5_fba_ode.py 'Not written'/experiment6 'Deferred', yet experiment5-11 plus validate_against_beard.py exist with results/composite/ outputs. Medium."
    },
    {
      "id": "F19",
      "title": "scripts/composite/README.md names validate_against_cortassa.py but actual file is validate_against_beard.py",
      "location": "09_Computational_Modeling/scripts/composite/README.md:32",
      "class": "doc-drift",
      "severity": "medium",
      "evidence": "README.md line 32 entry: '| validate_against_cortassa.py | Reference-curve validation of ODE layer in isolation | Not written |'. The actual file on disk is scripts/composite/validate_against_beard.py (inventory role: 'Beard 2005 baseline PO-curve reproduction validation script'). There is no validate_against_cortassa.py file in the repository. The plan intended Cortassa-Aon validation but the implementation targeted Beard 2005.",
      "falsification": "upheld: composite/README.md:32 names validate_against_cortassa.py 'Not written'; actual file is validate_against_beard.py and no cortassa file exists. Medium."
    },
    {
      "id": "F20",
      "title": "Composite README planned Cortassa-Aon 2003/2006 ODE; implementation is exclusively Beard 2005",
      "location": "09_Computational_Modeling/scripts/composite/README.md:13",
      "class": "intent-mismatch",
      "severity": "low",
      "evidence": "scripts/composite/README.md line 13: 'ODE energetics (Cortassa-Aon 2003/2006; Beard 2005)' — Cortassa-Aon is listed as the primary ODE choice. The actual ode_utils.py (line 6) states: 'Implements the Beard 2005 mitochondrial OXPHOS ODE system'; composite_utils.py (line 21) similarly references 'Beard-2005 biophysical OXPHOS ODE'. The Whole_Cell_Modeling/cortassa/ directory exists (defined in paths.py:49) but contains only a README with no implementation. Cortassa-Aon was never implemented; the stated design intent was not realized.",
      "falsification": "upheld: composite/README.md:13 lists 'Cortassa-Aon 2003/2006; Beard 2005' but ode_utils/composite_utils implement only Beard 2005; cortassa/ dir has no implementation. Low upheld."
    },
    {
      "id": "F21",
      "title": "compute_fluxes uses hardcoded MEMBRANE_MAX_FOLD=50.0 and old leak formula, inconsistent with beard_rhs which uses p.CL_leak_max_fold=20.0 and the Kagan CL_ox mechanism",
      "location": "09_Computational_Modeling/ode_utils.py:519-525",
      "class": "bug",
      "severity": "medium",
      "evidence": "beard_rhs (lines 362-385) computes proton leak as: cl_ox_clipped = max(min(CL_ox,1),0); leak_multiplier = 1.0 + p.CL_leak_max_fold * cl_ox_clipped (p.CL_leak_max_fold defaults to 20.0 per BeardParams line 216). compute_fluxes (lines 519-525) instead uses: MEMBRANE_MAX_FOLD = 50.0; if p.leak_growth_rate > 0: leak_multiplier = 1.0 + MEMBRANE_MAX_FOLD * (1.0 - np.exp(-p.leak_growth_rate * t_hours)). The constant differs (50 vs 20), the formula differs (exponential growth vs linear-in-CL_ox), and compute_fluxes ignores the MPTP factor entirely. Any flux-analysis call using compute_fluxes when leak_growth_rate > 0 yields a J_leak inconsistent with what beard_rhs integrates.",
      "falsification": "upheld: Verified ode_utils.py:519-525 — same defect as BUGS-1 (MEMBRANE_MAX_FOLD=50.0 time-exp leak, no MPTP factor) vs beard_rhs CL_ox-driven leak at CL_leak_max_fold=20.0. Redundant with BUGS-1 but independently true. Medium accurate."
    },
    {
      "id": "F22",
      "title": "beard_qamas_in_vitro_reference.py imports tellurium and roadrunner at module level; neither is in requirements.txt",
      "location": "09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py:2-5",
      "class": "reproducibility",
      "severity": "high",
      "evidence": "Lines 2-4: 'import matplotlib.pyplot as plt; import tellurium as te; import roadrunner'. Line 6: 'r = te.loada(...)' executes immediately at module level without a __main__ guard. requirements.txt (127 entries) contains no tellurium or roadrunner. The inventory note confirms 'runs at module level without main guard'. Any import of this module — or any attempt to reproduce the baseline QAMAS reference run — fails with ImportError on a fresh environment built from requirements.txt.",
      "falsification": "upheld: beard_qamas_in_vitro_reference.py imports tellurium and roadrunner; te.loada runs at module level; requirements.txt has neither (confirmed scipy/tellurium absence). Fresh-env reproduction ImportErrors. High."
    },
    {
      "id": "F23",
      "title": "INDEX.md describes Consolidated_Protocols.txt as 'All extraction protocols unified' but the file is pip install terminal output",
      "location": "INDEX.md:69",
      "class": "doc-drift",
      "severity": "medium",
      "evidence": "INDEX.md line 69: '| Consolidated_Protocols.txt | All extraction protocols unified (13,268 lines) |'. The actual file 06_Synthesis/Consolidated_Protocols.txt begins: 'Requirement already satisfied: pydantic in /home/epas/miniconda3/envs/autogen/lib/python3.11/site-packages (2.6.1)...' — it is terminal output from a pip install session accidentally redirected to this file. The inventory (Stage 1) flags the file as 'Accidental pip-install terminal output captured to file; not a protocol'. No protocol content exists in this file.",
      "falsification": "upheld: INDEX.md:69 describes Consolidated_Protocols.txt as 'All extraction protocols unified' but the file head is pip 'Requirement already satisfied' terminal output (SECURITY-4 anchor); no protocol content. Medium."
    },
    {
      "id": "F24",
      "title": "INDEX.md lists 03_Study_Registry/source_archive.zip as a repository file but it does not exist",
      "location": "INDEX.md:41",
      "class": "doc-drift",
      "severity": "low",
      "evidence": "INDEX.md line 41: '| source_archive.zip | Original import bundle from literature search |'. A Glob search for /home/user/MitochondriaMaven/03_Study_Registry/source_archive.zip returns no results. The Stage-1 inventory of 319 files does not list this path. The file is documented as existing but is absent from the repository.",
      "falsification": "upheld: INDEX.md lists 03_Study_Registry/source_archive.zip but the path is absent on disk. Documented-but-absent file. Low."
    },
    {
      "id": "F25",
      "title": "paths.py omits BEARD_DIR which ode_utils.py attempts to import from it; paths.py contract as single source of truth is broken",
      "location": "09_Computational_Modeling/ode_utils.py:657-659",
      "class": "design",
      "severity": "low",
      "evidence": "ode_utils.py lines 657-659: 'try: from paths import BEARD_DIR; return BEARD_DIR / \"beard_2005_params.csv\"; except ImportError: return Path(__file__).resolve().parent / \"Whole_Cell_Modeling\" / \"beards_lab\" / \"beard_2005_params.csv\"'. paths.py defines MITOMAMMAL_DIR, CORTASSA_DIR, and all script/result dirs, but has no BEARD_DIR. The import always fails, the fallback hardcodes the path. paths.py (line 9) documents itself as 'single source of truth for all paths'; the omission of BEARD_DIR violates this contract, and the silent fallback means the violation is never surfaced.",
      "falsification": "upheld: ode_utils.py:657-659 'try: from paths import BEARD_DIR except ImportError: hardcoded fallback'; paths.py has no BEARD_DIR so the import always fails and the fallback always runs, contradicting paths.py 'single source of truth'. Low."
    },
    {
      "id": "F26",
      "title": "composite_utils.py utility module imports apply_scenario from an experiment script at runtime via sys.path injection — inverted dependency",
      "location": "09_Computational_Modeling/composite_utils.py:351-356",
      "class": "design",
      "severity": "medium",
      "evidence": "composite_utils.py lines 351-356 inside compose_fba_ode(): 'sys.path.insert(0, str(_here / \"scripts\" / \"experiments_v2\")); try: from experiment1_v2_transit_window import apply_scenario; apply_scenario(fba_model, scenario); except ImportError: pass'. A shared utility module (composite_utils.py) depends on a specific experiment script (experiment1_v2_transit_window.py). If the import fails, the exception is silently swallowed and scenarios A/B/C are applied without exchange-bound constraints, producing incorrect results with no warning. The architectural inversion also means moving or renaming experiment1_v2_transit_window.py silently breaks composite scenario logic.",
      "falsification": "upheld: Verified composite_utils.py:351-356: shared utility injects scripts/experiments_v2 on sys.path and imports apply_scenario from a specific experiment script with 'except ImportError: pass'. Inverted dependency + silent failure accurate. Medium."
    },
    {
      "id": "F27",
      "title": "LAB_NOTEBOOK.md Session 1 states efflux_method.py 'we do NOT need it'; it is now a core dependency imported by every experiment",
      "location": "09_Computational_Modeling/LAB_NOTEBOOK.md:49",
      "class": "doc-drift",
      "severity": "low",
      "evidence": "LAB_NOTEBOOK.md line 49 (Session 1 MitoMAMMAL repo inspection): 'efflux_method.py — E-Flux constraint function (used in their analysis; we do NOT need it)'. By Session 3 the GPR-aware decay audit (Session 2 fix #4) reversed this decision. decay_utils.py line 32: 'from efflux_method import evaluate_gpr_expression, remove_genes'. composite_utils.py line 54: 'from efflux_method import evaluate_gpr_expression, remove_genes'. The original assessment is preserved unchanged in the notebook while the actual usage is opposite; a reader following the notebook would expect the dependency not to exist.",
      "falsification": "upheld: LAB_NOTEBOOK Session-1 note says efflux_method.py 'we do NOT need it' yet decay_utils.py:32 and composite_utils.py:54 both import from efflux_method — now a core dependency, opposite of the preserved note. Low."
    },
    {
      "id": "F28",
      "title": "q-bio Chicago 2026 abstract deadline (May 31) has passed; README.md still marks it as merely 'drafted' with no submission record in the repository",
      "location": "README.md:99",
      "class": "intent-mismatch",
      "severity": "medium",
      "evidence": "LAB_NOTEBOOK.md line 2: 'q-bio Chicago 2026 abstract (deadline May 31, 2026)'. INDEX.md line 91: 'Status: ACTIVE — q-bio Chicago 2026 abstract deadline May 31.' 09_Computational_Modeling/README.md line 2: 'Deliverable: q-bio Chicago 2026 abstract (May 31, 2026)'. README.md line 99: '✅ Conference-style abstract + full manuscript outline — drafted'. The declared primary deliverable of the provisional intent was a submitted conference abstract. Current date is June 17, 2026. No file in the repository documents submission, acceptance, rejection, or a decision to withdraw. The status symbol '✅' implies completion but the text says only 'drafted', leaving the near-term tractable goal in an unresolved state relative to the stated deadline.",
      "falsification": "upheld: README.md:99 '✅ ... abstract ... drafted' with May 31 2026 deadline passed (today 2026-06-17) and no submission/decision record; ✅ implies completion while text says only drafted. Medium reasonable."
    },
    {
      "id": "F29",
      "title": "Hardcoded 0.175 V DPsi normalization in MCU uptake formula",
      "location": "09_Computational_Modeling/ode_utils.py:391",
      "class": "bug",
      "severity": "low",
      "evidence": "Line 391: `dpsi_factor = max(DPsi, 0) / 0.175` hardcodes the nominal resting ΔΨm as a literal 0.175 V. The parametrized baseline is 175e-3 V (stored elsewhere), but this normalization constant is not drawn from BeardParams. If SCENARIO_ODE_OVERRIDES or direct BeardParams edits change the baseline DPsi, the MCU thermodynamic driving-force scaling becomes incorrect while no warning is emitted.",
      "falsification": "upheld: Verified ode_utils.py:391 dpsi_factor=max(DPsi,0)/0.175 hardcodes resting ΔΨm normalization rather than drawing from BeardParams. Accurate; narrow blast radius. Low correct."
    },
    {
      "id": "F30",
      "title": "Double-counted dCL_ox when ros_enabled=True and leak_growth_rate>0 simultaneously",
      "location": "09_Computational_Modeling/ode_utils.py:444,449-451",
      "class": "bug",
      "severity": "medium",
      "evidence": "beard_rhs(): line 444 sets `dCL_ox = J_Kagan` (Kagan-cycle CL oxidation) when ros_enabled=True. Lines 449-451 then unconditionally add `(p.leak_growth_rate / 3600.0) * (1.0 - cl_ox_clipped)` if leak_growth_rate>0. The two paths are not mutually exclusive — any scenario with ros_enabled=True and a non-zero leak_growth_rate double-counts CL_ox accumulation, producing inflated oxidation and an incorrect leak_multiplier. The comment calls the second path 'backwards-compat' but provides no guard against simultaneous use.",
      "falsification": "upheld: Verified beard_rhs:444 sets dCL_ox=J_Kagan when ros_enabled, then lines 449-451 unconditionally add the leak_growth_rate term with no mutual-exclusion guard — a real latent double-count if both are set; not active in shipped scenarios. Medium upheld."
    },
    {
      "id": "F31",
      "title": "Uninitialized git submodule leaves MODEL_PATH pointing to non-existent SBML file",
      "location": "09_Computational_Modeling/Whole_Cell_Modeling/mitomammal/",
      "class": "reproducibility",
      "severity": "high",
      "evidence": "Shell listing of Whole_Cell_Modeling/mitomammal/ returns empty — the submodule directory contains no files. paths.py:22 sets MODEL_PATH = MITOMAMMAL_DIR / '6_universal_mito_model.xml', which therefore does not exist. Every simulation script (experiment1_v2_transit_window.py, experiment1_v3_empirical.py, phase_k_wet_lab_validation.py, all composite scripts) calls cobra.io.read_sbml_model(MODEL_PATH) and will raise FileNotFoundError immediately. LAB_NOTEBOOK.md:33-50 documents the repo as having been cloned and inspected with model file present, indicating the submodule was registered via .gitmodules (SECURITY-6) without running git submodule update --init, silently voiding the entire computational pipeline.",
      "falsification": "upheld: Confirmed Whole_Cell_Modeling/mitomammal/ is empty so paths.py:22 MODEL_PATH does not exist and cobra.io.read_sbml_model raises FileNotFoundError across all sim scripts. High appropriate."
    },
    {
      "id": "F32",
      "title": "INDEX.md:98 stale claim that MitoMAMMAL repo is still awaiting cloning",
      "location": "INDEX.md:98",
      "class": "doc-drift",
      "severity": "low",
      "evidence": "INDEX.md:98 states 'Awaiting cloned repos (Luthey-Schulten Lab Minimal_Cell + Habermann Lab MitoMAMMAL)'. LAB_NOTEBOOK.md:33 documents 'Cloned from: https://gitlab.com/habermann_lab/mitomammal.git' and lines 36-54 record a full inspection of repo contents (model filename discrepancy, reaction/gene/metabolite counts, efflux_method.py contents). The INDEX.md master status table therefore misrepresents the project state to any reader using it as a source of truth.",
      "falsification": "upheld: INDEX.md:98 'Awaiting cloned repos ... MitoMAMMAL' while LAB_NOTEBOOK documents the repo cloned and inspected. Stale status. Low."
    },
    {
      "id": "F33",
      "title": "Phase K uses two-sample KS test to compare deterministic model output against observations",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py:169-173",
      "class": "intent-mismatch",
      "severity": "medium",
      "evidence": "Lines 169-173: flux_at_empirical_t is produced by np.interp (deterministic, no sampling noise) from the MitoMAMMAL predicted curve; empirical_normalized is the digitized JC-1 values. ks_2samp is then called on these two arrays. The two-sample KS test assumes both inputs are iid random samples from unknown distributions; applying it to a deterministic interpolation versus observations violates this assumption and makes the p-value uninterpretable. A one-sample KS test against a fitted CDF, or a goodness-of-fit metric such as RMSE, would be statistically valid here.",
      "falsification": "upheld: phase_k:169 flux_at_empirical_t=np.interp (deterministic) and line 173 ks_2samp against digitized observations; two-sample KS assumes iid samples from both, so the p-value is uninterpretable. Valid statistical critique. Medium."
    },
    {
      "id": "F34",
      "title": "Phase K imports build_halflife_map_per_subunit from experiments_v2 via sys.path injection",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py:50-51",
      "class": "design",
      "severity": "low",
      "evidence": "Lines 50-51: `sys.path.insert(0, str(Path(__file__).parent.parent / 'experiments_v2'))` followed by `from experiment1_v3_empirical import build_halflife_map_per_subunit`. This is the same inverted-dependency anti-pattern flagged in DRIFT-11 for composite_utils.py, but it is a separate occurrence in a different module (investigation phase script importing from an experiment script). The function should be factored into a shared utility module rather than requiring scripts to mutate sys.path to reach peer-level experiment code.",
      "falsification": "upheld: phase_k:50-51 sys.path.insert(.../experiments_v2) then import build_halflife_map_per_subunit from experiment1_v3_empirical — a distinct occurrence of the inverted-dependency pattern. Low."
    },
    {
      "id": "F35",
      "title": "flux_buffer parameter declared in build_capacity_envelope_fn but explicitly never used",
      "location": "09_Computational_Modeling/composite_utils.py:154",
      "class": "design",
      "severity": "low",
      "evidence": "Line 154: `flux_buffer: float = 1.05,  # unused here; kept for signature parity`. The parameter is accepted by the function signature but the comment confirms it is never applied inside the function body. No caller documentation identifies which external signature it is matching. This represents an incomplete refactoring — either the flux-boundary scaling the parameter implies was removed without updating callers, or the parameter was added preemptively and the implementation was never written.",
      "falsification": "upheld: composite_utils.py:154 'flux_buffer: float = 1.05,  # unused here; kept for signature parity' — accepted but never applied; incomplete-refactoring smell. Low."
    },
    {
      "id": "F36",
      "title": "Dead 'if False' branch in MPTP experiment leaves Ca²⁺ trajectory permanently unaudited",
      "location": "09_Computational_Modeling/scripts/composite/experiment10_mptp_composite.py:82",
      "class": "bug",
      "severity": "low",
      "evidence": "Line 82: `ca_x_peak = np.max(result.delta_psi_trace) if False else None  # placeholder` — the `if False` guard is permanently False so ca_x_peak is always None. Comments at lines 83-84 confirm Ca_x is not exposed through CompositeResult. Even if the condition were True, it would compute max(ΔΨm), not Ca²⁺ peak — the wrong metric for an MPTP audit.",
      "falsification": "upheld: Verified experiment10_mptp_composite.py:82 'ca_x_peak = np.max(result.delta_psi_trace) if False else None  # placeholder'; always None and would compute ΔΨm max not Ca peak, and never added to output rows. Benign acknowledged placeholder; low correct."
    },
    {
      "id": "F37",
      "title": "Abstract figure labels Kagan-cycle panel as 'Ex 12' but no Ex 12 exists; only Ex 11",
      "location": "09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py:188",
      "class": "doc-drift",
      "severity": "low",
      "evidence": "Line 188: label='Kagan-cycle mechanistic (Ex 12)' and docstring line 6: 'Ex 12 Kagan-cycle data'. The only ROS/MitoQ experiment in the repository is experiment11_ros_mitoq.py. No Ex 12 script or output exists. This mislabeling appears in the conference abstract figure final_abstract_figure_composite.png.",
      "falsification": "upheld: Verified experiment8_abstract_figure.py:188 label='Kagan-cycle mechanistic (Ex 12)' while only experiment11_ros_mitoq.py exists. Cosmetic legend mislabel that ships in the figure; low correct."
    },
    {
      "id": "F38",
      "title": "read_mitocarta_crossref() uses CWD-relative path, silently falls back to hardcoded stale values",
      "location": "09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py:95",
      "class": "reproducibility",
      "severity": "medium",
      "evidence": "Line 95: `path = Path('results/phase_b/essential_genes_mitocarta_crossref.csv')` is a bare relative path unlike all other scripts which use results_path(). If script is run from any directory other than 09_Computational_Modeling/, path resolution fails silently and line 97 returns hardcoded fallback (145, 127) without warning, causing the abstract figure to show potentially stale MitoCarta counts.",
      "falsification": "upheld: experiment8_abstract_figure.py:95 path=Path('results/phase_b/...') bare relative (unlike results_path() elsewhere); line 97 returns hardcoded (145,127) when missing, so running from another dir silently yields stale counts. Medium reasonable."
    },
    {
      "id": "F39",
      "title": "validate_against_beard.py run_steady_state return-type annotation claims 3-tuple but function returns 4-tuple",
      "location": "09_Computational_Modeling/scripts/composite/validate_against_beard.py:51",
      "class": "doc-drift",
      "severity": "info",
      "evidence": "Line 51: `def run_steady_state(params: BeardParams, y0: np.ndarray) -> tuple[np.ndarray, dict, float]:` annotates a 3-element return. Line 57 actually returns `return y_ss, fluxes, j_o2, traj.success` (4 elements). Caller at line 67 correctly unpacks 4 values so runtime is unaffected, but the annotation is wrong.",
      "falsification": "upheld: validate_against_beard.py:51 annotation '-> tuple[np.ndarray, dict, float]' (3) while line 57 returns 4 and caller line 67 unpacks 4. Annotation wrong, runtime unaffected. Info correct."
    },
    {
      "id": "F40",
      "title": "phase_g5_ros_coupling computes O2s-rate variables that go unused; comment and implementation describe different coupling mechanisms",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_g5_ros_coupling.py:57",
      "class": "intent-mismatch",
      "severity": "low",
      "evidence": "Lines 57 and 63 compute baseline_o2s_rate and ref_o2s_rate from CI flux * 0.002, log them, but never use them in the modifier. The comment at lines 69-70 states 'ROS_modifier = 1 + k x (baseline_o2s_rate / ref_o2s_rate)' but the implementation at lines 73-74 uses `o2_relative_drop = max(0, 1 - o2_uptake / ref_o2); ros_modifier = 1.0 + k_damage * o2_relative_drop` — an O2-uptake-ratio proxy, not an O2s-rate ratio. Intended and implemented coupling mechanisms differ.",
      "falsification": "amended: phase_g5:57,63 compute baseline_o2s_rate/ref_o2s_rate and never use them — real dead computation. But the 'mechanisms differ' framing is overstated: the comment documents the implemented O2-drop mechanism that lines 73-74 actually use. Defect is unused vars, not a hidden mechanism swap."
    },
    {
      "id": "F41",
      "title": "CompositeResult.atp_trace field stores cytosolic ATP but is documented as matrix ATP",
      "location": "09_Computational_Modeling/composite_utils.py:309,384,424",
      "class": "intent-mismatch",
      "severity": "medium",
      "evidence": "Field definition at line 309: `atp_trace: np.ndarray = field(default_factory=lambda: np.array([]))  # matrix ATP (mol/L)`. In compose_fba_ode() at line 384, `atp = traj.get('sumATP_x')` (matrix ATP) is a dead assignment never used. At line 424, the return sets `atp_trace=atp_c` where `atp_c = traj.get('sumATP_c')` (cytosolic ATP). Callers reading CompositeResult.atp_trace receive cytosolic ATP while the comment/name implies matrix ATP.",
      "falsification": "upheld: Verified composite_utils.py:309 comment '# matrix ATP (mol/L)', line 384 atp=traj.get('sumATP_x') is a dead assignment, and line 424 returns atp_trace=atp_c (cytosolic sumATP_c). The field stores cytosolic ATP while its comment says matrix ATP — genuine mislabel. Medium upheld."
    },
    {
      "id": "F42",
      "title": "compute_fluxes() omits mptp_factor from J_leak, diverging from beard_rhs() by up to 10001x when MPTP is enabled",
      "location": "09_Computational_Modeling/ode_utils.py:525",
      "class": "bug",
      "severity": "medium",
      "evidence": "beard_rhs() at line 385 computes `J_leak = cap_Leak * p.X_H * leak_multiplier * mptp_factor * (p.H_c * exp(...) - p.H_x * exp(...))` where mptp_factor = 1 + mptp_open_prob * p.mptp_permeability_max (default 1e4). compute_fluxes() at line 525 computes `J_leak = caps['Leak'] * p.X_H * leak_multiplier * (p.H_c * exp(phi/2) - p.H_x * exp(-phi/2))` with no mptp_factor term. When mptp_enabled=True and the pore is open, J_leak reported by compute_fluxes() underestimates actual leak by up to (1 + 1e4) = 10001-fold, making all diagnostic flux readouts at MPTP-active states incorrect.",
      "falsification": "amended: Verified beard_rhs:385 includes mptp_factor (1+mptp_open_prob*p.mptp_permeability_max, default 1e4 at line 180) while compute_fluxes:525 omits it. But compute_fluxes is only called by experiment9 and validate_against_beard, neither of which enables MPTP, so the 10001x divergence is latent, not active. High overstated."
    },
    {
      "id": "F43",
      "title": "PARTITION_PATH in experiment1d_minimal_set.py and phase_b_cluster_and_sweep.py resolves to wrong directory, causing FileNotFoundError at runtime",
      "location": "09_Computational_Modeling/scripts/experiments_v2/experiment1d_minimal_set.py:50,09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py:41",
      "class": "bug",
      "severity": "medium",
      "evidence": "Both files use `results_path('essential_dispensable_partition.json')` which resolves to `results/essential_dispensable_partition.json`. The canonical writer, phase_b_annotate_essentials.py line 31, writes to `results_path('phase_b', 'essential_dispensable_partition.json')` i.e. `results/phase_b/essential_dispensable_partition.json`. No code creates the file at the flat path. Both scripts will raise FileNotFoundError on the open() call. Note: BUGS-7 covers only the ANNOTATED_PATH variable in phase_b_cluster_and_sweep.py, not PARTITION_PATH in either script.",
      "falsification": "upheld: Verified experiment1d_minimal_set.py:50 and phase_b_cluster_and_sweep.py:41 both use results_path('essential_dispensable_partition.json') (flat); disk find confirms the file exists only at results/phase_b/. Distinct from BUGS-7 (ANNOTATED_PATH). FileNotFoundError at runtime. Medium."
    },
    {
      "id": "F44",
      "title": "Dead params dict in phase_b_annotate_essentials.py silently drops the size=1 MyGene.info result-count limit",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_b_annotate_essentials.py:44-63",
      "class": "bug",
      "severity": "low",
      "evidence": "Lines 44-55 build a `params` dict containing `'size': 1` and `'q': ','.join(batch)`. The subsequent requests.post() at line 58 constructs its own inline dict `{'ids': ','.join(batch), 'scopes': 'ensembl.gene', 'species': species, 'fields': params['fields']}`, extracting only `params['fields']`. The `size`, `q`, and other keys in `params` are never sent. The MyGene.info batch endpoint defaults to returning multiple hits per query gene; the intended `size: 1` guard against multi-hit pollution is silently absent, potentially returning duplicate or off-target annotations per gene ID.",
      "falsification": "upheld: Verified phase_b_annotate_essentials.py:44-55 build a params dict with 'size':1 and 'q', but the requests.post at 58-63 sends its own inline dict extracting only params['fields']; 'size' and 'q' are dropped, so the size=1 multi-hit guard is silently absent. Low correct."
    }
  ],
  "denominator": 319
}
```

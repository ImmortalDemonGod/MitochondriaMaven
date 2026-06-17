# 01 — Comprehensive Understanding

_Generated 2026-06-17T13:56:13.142Z · branch `claude/upbeat-keller-4c0z1s` · forensic-audit-pipeline_

**Coverage denominator:** 319 files (full repo surface; the basis for every later stage).

## Provisional intent (judged-against until Stage 4)

> PROVISIONAL: An independent-researcher R&D program (lead Miguel Ingram, per README.md:103) to engineer autonomous/programmable extracellular mitochondria, whose tractable near-term aim is computationally predicting the 'transit window' — how long an extracted mitochondrion keeps producing ATP/ΔΨm before reuptake viability is lost — packaged toward a q-bio Chicago 2026 conference abstract (README.md:11-23).

## Architecture

The repository is a single-researcher R&D knowledge base + computational pipeline organized as a 10-stage, pipeline-ordered folder structure (01_Vision_and_Strategy through 10_Research_Questions; see INDEX.md and README.md). Stages 01-08 are a document/data pipeline: vision/strategy docs (.docx/.md), a literature-screening methodology, a 114-paper study registry (03_Study_Registry/studies.csv), source-paper summaries, and three tiers of AI-extracted data (05_Extracted_Data/{Structured_JSON,PDF_Metadata,Protocol_Summaries}) feeding cross-paper synthesis (06_Synthesis) and a bench lab manual (07_Lab_Manual). Of 319 inventoried files, the overwhelming majority are static data/doc artifacts (extracted-paper JSON, .docx, .txt). The live executable system lives entirely in 09_Computational_Modeling/, a Python (3.10) scientific pipeline. Compute flow: a centralized paths.py is the single source of truth resolving the MitoMAMMAL genome-scale model (Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml, a git submodule) and results/ output dirs. decay_utils.py runs pFBA on the COBRApy model to get signed baseline fluxes, then applies time-stepped, GPR-aware protein decay (AND-clause=min of subunit decay factors, OR=summed isozyme pooling via MitoMAMMAL's efflux_method) to scale reaction bounds, producing a 'capacity envelope' over time as nuclear-encoded proteins decay on literature half-lives (mt-encoded genes exempt). composite_utils.py bridges that FBA capacity envelope into a Beard-2005 biophysical OXPHOS ODE (ode_utils.py, SciPy LSODA) via FBA_ODE_REACTION_MAP, treating decay fractions as Vmax multipliers, and integrates ΔΨm/ATP/NADH trajectories to derive a 'transit window'. Scripts are organized by generation/phase: scripts/archive_v1 (deprecated), scripts/experiments_v2 (FBA-centric), scripts/investigation_phases (phase_a..phase_k forensic/validation), and scripts/composite (FBA+ODE coupling); each writes versioned outputs under results/ and is documented in LAB_NOTEBOOK.md and docs/investigation/ audit threads.

### Components

| Component | Role |
|---|---|
| 01_Vision_and_Strategy | Thesis, 4-layer long-range vision, and assumption/strategy audits (README.md:46) |
| 02_Methodology | Literature search, screening, and ranking methodology incl. BSHR_Loop (INDEX.md:25-33) |
| 03_Study_Registry | studies.csv — 114 screened papers (1955-2024) with inclusion probabilities (README.md:48) |
| 04_Source_Literature / 05_Extracted_Data | Source-paper summaries plus 3 tiers of AI extraction (Structured_JSON, PDF_Metadata, Protocol_Summaries) (INDEX.md:44-60) |
| 06_Synthesis | Cross-paper comparative analyses and consolidated protocols (INDEX.md:62-69) |
| 07_Lab_Manual / 08_Experimental_Work | Bench-ready isolation manual and planned/completed wet-lab experiments E1-E8 (INDEX.md:71-88) |
| 09_Computational_Modeling | The active executable pipeline: time-stepped FBA + ODE transit-window modeling (README.md:11-21) |
| paths.py | Single source of truth for model/results/docs paths and sys.path bootstrap (paths.py:1-11) |
| decay_utils.py | GPR-aware FBA protein-decay capacity-envelope engine imported by all experiments (decay_utils.py:1-10) |
| ode_utils.py | Beard-2005 OXPHOS ODE integration library (SciPy LSODA) for ΔΨm/ATP dynamics (s1_files.json ode_utils note) |
| composite_utils.py | FBA->ODE coupling: maps decay fractions to ODE Vmax multipliers and drives composite simulations (composite_utils.py:1-31) |
| scripts/{archive_v1,experiments_v2,investigation_phases,composite} | Generationally/phase-organized experiment entry points writing versioned results/ outputs (paths.py:60-65) |
| Whole_Cell_Modeling submodules | External MitoMAMMAL (primary) and Human-GEM (cross-check) genome-scale models as git submodules (.gitmodules; README.md:74) |
| results/ + docs/ + LAB_NOTEBOOK.md | Versioned simulation outputs and self-audited investigation/conference-planning documentation trail (README.md:21) |

## Roles (file count by classification)

| Role | Count |
|---|---|
| data | 140 |
| doc | 69 |
| generated | 59 |
| source | 38 |
| asset | 6 |
| config | 4 |
| submodule | 2 |
| dead | 1 |

## Entry points

| Name | Kind | Location | What it is |
|---|---|---|---|
| composite_utils | module | 09_Computational_Modeling/composite_utils.py | Shared utility module exporting compose_fba_ode, build_capacity_envelope_fn, and extract_capacity_envelope for FBA+ODE coupling; imported by all composite experiment scripts |
| experiment5b_interventions | script | 09_Computational_Modeling/scripts/composite/experiment5b_interventions.py | CLI script modeling cold chain, MitoQ, and substrate supplementation interventions through the composite FBA+ODE model; outputs ex5_5_intervention_composite.csv |
| experiment8_abstract_figure | script | 09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py | CLI script generating the 2-panel q-bio abstract figure from MPTP scenario and MitoQ dose-response data |
| experiment1_v3_empirical | script | 09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py | Primary FBA transit-window experiment using empirical per-subunit half-lives with 50-sample bootstrap CI; outputs transit_window_empirical.csv |
| experiment4_interventions | script | 09_Computational_Modeling/scripts/experiments_v2/experiment4_interventions.py | FBA-layer three-intervention modeling (cold chain, MitoQ, substrate) with bootstrap CI; outputs intervention_bar_chart.png |
| phase_b_cluster_and_sweep | script | 09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py | Phase B functional clustering and single-gene immortalization sweep over all 145 essential genes; outputs essential_genes_annotated.csv and gene_knockout_scores_v2.csv |
| phase_g1_order_statistics | script | 09_Computational_Modeling/scripts/investigation_phases/phase_g1_order_statistics.py | Validation test comparing non-FBA order-statistics TW prediction against FBA output; outputs g1_order_stats_vs_fba.csv |
| phase_h_ci_subunit_analysis | script | 09_Computational_Modeling/scripts/investigation_phases/phase_h_ci_subunit_analysis.py | Complex I subunit half-life deep dive with pairwise Pearson correlation and permutation test; outputs ci_correlation_analysis.json |
| decay_utils | shared_module | 09_Computational_Modeling/decay_utils.py | Shared utility imported by all experiment scripts; provides GPR-aware FBA decay, objective configuration, and transit window helpers |
| beard_qamas_in_vitro_reference | script | 09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py | Beard QAMAS reference ODE model of mitochondrial bioenergetics; runs top-level without __main__ guard |
| experiment1_transit_window | cli_main | 09_Computational_Modeling/scripts/archive_v1/experiment1_transit_window.py | Archived v1 CLI: time-stepped FBA predicting mitochondrial ATP viability window post-extraction |
| experiment10_mptp_composite | cli_main | 09_Computational_Modeling/scripts/composite/experiment10_mptp_composite.py | CLI: tests MPTP Ca2+-driven ΔΨm collapse vs proteomics-limited ATP-first failure partition |
| experiment5c_sensitivity | cli_main | 09_Computational_Modeling/scripts/composite/experiment5c_sensitivity.py | CLI: Latin hypercube sensitivity propagation using literature-sourced parameter uncertainty ranges |
| experiment9_atp_first_diagnostic | cli_main | 09_Computational_Modeling/scripts/composite/experiment9_atp_first_diagnostic.py | CLI: diagnoses ATP-first paradox by partitioning capacity bottleneck vs Vmax vs threshold hypotheses |
| experiment1b_v2_gpr_knockout | cli_main | 09_Computational_Modeling/scripts/experiments_v2/experiment1b_v2_gpr_knockout.py | CLI: GPR-aware gene knockout scoring correcting v1 OR-rule over-kill bug |
| phase_a_dissection | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_a_dissection.py | CLI: MitoMAMMAL mechanistic dissection runs A.1–A.5 generating MITOMAMMAL_DISSECTION.md |
| phase_c_forensic_29h | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_c_forensic_29h.py | CLI: forensic dissection of why transit window is 29 hours |
| phase_g2_cross_model | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_g2_cross_model.py | CLI: cross-model validation replicating decay findings in Human-GEM mitochondrial subset |
| phase_i_syn3a_crosswalk | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_i_syn3a_crosswalk.py | CLI: compares 3 mitochondrial transport reactions against Syn3A minimal cell equivalents |
| ode_utils | shared_utility | 09_Computational_Modeling/ode_utils.py | Core ODE library (BeardParams, integrate_with_capacity, beard_rhs) imported by all composite experiment scripts |
| experiment1b_gene_sensitivity | cli_main | 09_Computational_Modeling/scripts/archive_v1/experiment1b_gene_sensitivity.py | Ranks nuclear-encoded genes by knockout impact on ATP and transit window (archive v1) |
| experiment11_ros_mitoq | cli_main | 09_Computational_Modeling/scripts/composite/experiment11_ros_mitoq.py | Sweeps MitoQ concentration as ROS scavenger in composite FBA+ODE model |
| experiment6_option_b_extension | cli_main | 09_Computational_Modeling/scripts/composite/experiment6_option_b_extension.py | Models membrane-integrity decay as non-proteomic failure mode via proton-leak growth |
| validate_against_beard | cli_main | 09_Computational_Modeling/scripts/composite/validate_against_beard.py | Reproduces Beard 2005 QAMAS PO-curve to gate the ode_utils implementation |
| experiment1c_v2_halflife_sweep | cli_main | 09_Computational_Modeling/scripts/experiments_v2/experiment1c_v2_halflife_sweep.py | Sweeps protein half-life 1-72h with GPR-aware decay under dual ATP/DPsi objectives |
| phase_b6_deep_dive | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_b6_deep_dive.py | Generates structured profiles for 10 selected essential mitochondrial genes |
| phase_d_adversarial_suite | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_d_adversarial_suite.py | Runs adversarial perturbation tests (buffer sensitivity, Monte Carlo, threshold sweeps) |
| phase_g2b_human_gem_decay | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_g2b_human_gem_decay.py | Tests uniform-decay transit window algebraic claim on Human-GEM (12931 reactions) |
| phase_k_wet_lab_validation | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py | Overlays model-predicted decay curves against user-digitized 2024 yeast JC-1 data |
| paths.py | shared_utility | 09_Computational_Modeling/paths.py | Single source of truth for all project paths; imported by every computation script via bootstrap pattern |
| setup_environment.sh | cli_script | 09_Computational_Modeling/setup_environment.sh | Bootstraps Miniforge conda env, installs COBRApy via pip, clones MitoMAMMAL repo from GitLab |
| experiment1c_halflife_sweep.py | cli_main | 09_Computational_Modeling/scripts/archive_v1/experiment1c_halflife_sweep.py | Archived v1 script: sweeps uniform nuclear protein half-life vs transit window over 12 values |
| experiment5_fba_ode.py | cli_main | 09_Computational_Modeling/scripts/composite/experiment5_fba_ode.py | Composite FBA+ODE driver for Ex 5.2-5.4: ΔΨm coupling sanity, TW derivation, failure partition |
| experiment7_human_gem.py | cli_main | 09_Computational_Modeling/scripts/composite/experiment7_human_gem.py | Cross-model composite validation run on Human-GEM to rule out MitoMAMMAL-specific artifacts |
| experiment1_v2_transit_window.py | cli_main | 09_Computational_Modeling/scripts/experiments_v2/experiment1_v2_transit_window.py | Corrected v2 transit window simulation with GPR-aware decay, signed flux, and dual ATP/ΔΨm objectives |
| experiment1d_minimal_set.py | cli_main | 09_Computational_Modeling/scripts/experiments_v2/experiment1d_minimal_set.py | Direct test of Assumption A3: minimal essential gene set decay vs full 374-gene nuclear decay |
| phase_b_annotate_essentials.py | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_b_annotate_essentials.py | Annotates 145 essential mouse genes with GO terms and disease associations via MyGene.info API |
| phase_e_anomaly_hunt.py | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_e_anomaly_hunt.py | Phase E: resolves anomalies, runs FVA, characterizes non-uniform decay heterogeneity |
| phase_g5_ros_coupling.py | cli_main | 09_Computational_Modeling/scripts/investigation_phases/phase_g5_ros_coupling.py | Phase G.5: models ROS-coupled protein damage acceleration across scenarios A/B/C |

## Full inventory

| Path | Role | Note |
|---|---|---|
| .gitignore | config | Git version control ignore patterns |
| 01_Vision_and_Strategy/IMOL-ERT_Vision.docx | doc | Business plan and overarching vision document |
| 01_Vision_and_Strategy/Project_Overview.docx | doc | Master project document with objectives and progress |
| 02_Methodology/Inclusion_Exclusion_Criteria.docx | doc | 8-category taxonomy with inclusion and exclusion rules |
| 03_Study_Registry/studies.csv | data | 114 screened papers with metadata and inclusion scores |
| 04_Source_Literature/Mitochondrial_Transfer/Mitochondria transplantation between living cells_ (Gäbelein et al. 2021).docx | doc | Summary of Gäbelein 2021 mitochondria transfer paper |
| 05_Extracted_Data/PDF_Metadata/A mitosome purification protocol based on percoll density gradients and its use in validating t.txt | data | PDF metadata extraction output for mitosome paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_and_bioenergetic_characterization_of_mitochondria_from_Pichia_pastoris.json | data | PDF metadata for Pichia pastoris isolation paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.json | data | PDF metadata for mice lung tissue isolation paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_of_brain_mitochondria_from_neonatal_mice.json | data | PDF metadata for neonatal mice brain isolation paper |
| 05_Extracted_Data/PDF_Metadata/Mitochondria_isolated_from_lipid_droplets_of_white_adipose_tissue_reveal_functional_differences.json | data | PDF metadata for adipose lipid droplet isolation paper |
| 05_Extracted_Data/PDF_Metadata/Rapid_isolation_of_respiring_skeletal_muscle_mitochondria_using_nitrogen_cavitation.json | data | PDF metadata for nitrogen cavitation isolation paper |
| 05_Extracted_Data/Protocol_Summaries/combined_content30.txt | data | Batch 30 standardized protocol summaries from literature |
| 05_Extracted_Data/Protocol_Summaries/combined_content70.txt | data | Batch 70 standardized protocol summaries from literature |
| 05_Extracted_Data/Structured_JSON/A_high-yield_preparative_method_for_isolation_of_rat_liver_mitochondria.json | data | AI-extracted structured data from rat liver isolation paper |
| 05_Extracted_Data/Structured_JSON/A_novel,_simple_and_rapid_method_for_the_isolation_of_mitochondria_which_exhibit_respiratory_co.json | data | AI-extracted structured data from novel rapid isolation paper |
| 05_Extracted_Data/Structured_JSON/Affordable_de_novo_generation_of_fish_mitogenomes_using_amplification-free_enrichment_of_mitoch.json | data | AI-extracted structured data from fish mitogenome paper |
| 05_Extracted_Data/Structured_JSON/An_improved_technique_for_the_isolation_of_mitochondria_from_plant_tissue.json | data | AI-extracted structured data from plant tissue isolation paper |
| 05_Extracted_Data/Structured_JSON/Delivery_of_mitochondria_confers_cardioprotection_through_mitochondria_replenishment_and_metabo.json | data | AI-extracted structured data from cardioprotection delivery paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_Characterization_of_Concanavalin_A-labeled_Plasma_Membranes_of_Carrot_Protoplasts.json | data | AI-extracted structured data from carrot protoplast paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_Respiratory_Measurements_of_Mitochondria_from_Arabidopsis_thaliana.json | data | AI-extracted structured data from Arabidopsis isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_functional_analysis_of_mitochondria_from_cultured_cells_and_mouse_tissue.json | data | AI-extracted structured data from cultured cells isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_Intact_Mitochondria_from_Skeletal_Muscle_by_Differential_Centrifugation_for_High-r.json | data | AI-extracted structured data from skeletal muscle isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_Mitochondria_from_Ustilago_maydis_Protoplasts.json | data | AI-extracted structured data from Ustilago maydis paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_functional_pure_mitochondria_by_superparamagnetic_microbeads.json | data | AI-extracted structured data from magnetic bead isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_by_gentle_cell_membrane_disruption,_and_their_subsequent_characteriza.json | data | AI-extracted structured data from gentle disruption paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_cultured_cells_and_liver_tissue_biopsies_for_molecular_and_bioch.json | data | AI-extracted structured data from liver biopsy isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_with_high_respiratory_control_from_primary_cultures_of_neurons_and_as.json | data | AI-extracted structured data from neuron/astrocyte isolation paper |
| 05_Extracted_Data/Structured_JSON/Measurement_of_mitochondrial_respiratory_chain_enzymatic_activities_in_Drosophila_melanogaster_.json | data | AI-extracted structured data from Drosophila respiratory chain paper |
| 05_Extracted_Data/Structured_JSON/Mitochondrial_Isolation_and_Purification_from_Mouse_Spinal_Cord.json | data | AI-extracted structured data from mouse spinal cord paper |
| 05_Extracted_Data/Structured_JSON/Mitochondrial_structure_and_function_are_disrupted_by_standard_isolation_methods.json | data | AI-extracted structured data from isolation artifact critique paper |
| 05_Extracted_Data/Structured_JSON/Optimization_of_preparation_of_mitochondria_from_25-100_mg_skeletal_muscle.json | data | AI-extracted structured data from small skeletal muscle prep paper |
| 05_Extracted_Data/Structured_JSON/Preservation_of_mitochondrial_functional_integrity_in_mitochondria_isolated_from_small_cryopres.json | data | AI-extracted structured data from cryopreservation integrity paper |
| 05_Extracted_Data/Structured_JSON/Purification_of_functional_mouse_skeletal_muscle_mitochondria_using_percoll_density_gradient_ce(1).json | data | AI-extracted structured data from Percoll gradient purification paper |
| 05_Extracted_Data/Structured_JSON/Rapid_isolation_and_purification_of_mitochondria_for_transplantation_by_tissue_dissociation_and.json | data | AI-extracted structured data from transplantation isolation paper |
| 05_Extracted_Data/Structured_JSON/Scalable_Isolation_of_Mammalian_Mitochondria_for_Nucleic_Acid_and_Nucleoid_Analysis.json | data | AI-extracted structured data from scalable mammalian isolation paper |
| 05_Extracted_Data/Structured_JSON/Tightly_coupled_mitochondria_from_human_early_placenta.json | data | AI-extracted structured data from human placenta isolation paper |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_20.docx | doc | Cross-paper pattern synthesis batch 20 |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_60-2.docx | doc | Cross-paper pattern synthesis batch 60 revision 2 |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_80-2.docx | doc | Cross-paper pattern synthesis batch 80 revision 2 |
| 07_Lab_Manual/Mitochondrial_Isolation_Report.pdf | doc | 32-page bench-ready mitochondrial isolation manual |
| 09_Computational_Modeling/Synth3a/Syn3A_Research_Notes_RemNote.md | doc | RemNote export of Syn3A whole-cell modeling research notes |
| 09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_2005_params.csv | data | Beard 2005 ODE model parameters for mitochondrial energetics |
| 09_Computational_Modeling/composite_utils.py | source | Shared FBA+ODE coupling utilities imported by composite experiments |
| 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_FINDINGS_2026-05-09.md | doc | DocInsight tool findings for conference submission audit |
| 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_VERIFICATION_AUDIT_2026-05-10.md | doc | Verification audit of DocInsight pipeline findings |
| 09_Computational_Modeling/docs/conference_planning/qbio_conference_analysis_2026-04-21.md | doc | q-bio Chicago 2026 conference details and submission strategy |
| 09_Computational_Modeling/docs/investigation/AUDIT_2026-04-23.md | doc | Living audit document for computational pipeline claims |
| 09_Computational_Modeling/docs/investigation/FRAMING_2026-04-23.md | doc | Corrected framing of model output vs biological reality |
| 09_Computational_Modeling/docs/investigation/PHASE_G_SYNTHESIS.md | doc | Phase G validation test synthesis and open-item resolution |
| 09_Computational_Modeling/docs/investigation/WHY_29_HOURS.md | doc | Investigation into 29-hour baseline transit window finding |
| 09_Computational_Modeling/requirements.txt | config | Pinned Python dependency list for the computational pipeline |
| 09_Computational_Modeling/results/archive_v1/experiment1b_summary.json | generated | Archived v1 experiment 1b simulation summary output |
| 09_Computational_Modeling/results/archive_v1/halflife_sweep_figure.png | generated | Archived half-life sweep parameter sensitivity figure |
| 09_Computational_Modeling/results/composite/ex10_mptp_scenarios.csv | generated | Ex 10 MPTP scenario comparison simulation results |
| 09_Computational_Modeling/results/composite/ex5_1_baseline_validation.csv | generated | Ex 5.1 composite baseline validation simulation results |
| 09_Computational_Modeling/results/composite/ex5_2_reaction_mapping.md | generated | Auto-generated FBA-to-ODE reaction mapping audit table |
| 09_Computational_Modeling/results/composite/ex5_5_intervention_composite.csv | generated | Ex 5.5 composite intervention re-prediction results |
| 09_Computational_Modeling/results/composite/ex6_option_b_membrane.csv | generated | Ex 6 option-B membrane model simulation results |
| 09_Computational_Modeling/results/composite/ex9_atp_first_diagnostic.png | generated | Ex 9 ATP-first failure mode diagnostic plot |
| 09_Computational_Modeling/results/experiments_v2/experiment1_v2_summary.json | generated | Experiment 1 v2 transit window simulation summary |
| 09_Computational_Modeling/results/experiments_v2/experiment1d_summary.json | generated | Experiment 1d simulation variant summary output |
| 09_Computational_Modeling/results/phase_b/essential_genes_annotated.csv | generated | 145 essential genes with functional cluster annotations |
| 09_Computational_Modeling/results/phase_b/gene_knockout_scores_v2.csv | generated | Phase B gene knockout leverage scores version 2 |
| 09_Computational_Modeling/results/phase_d/phase_d_adversarial_results.json | generated | Phase D adversarial model stress-test results |
| 09_Computational_Modeling/results/phase_g/g1_order_stats_vs_fba.csv | generated | Order-statistics vs FBA transit window comparison results |
| 09_Computational_Modeling/results/phase_h/ci_correlation_analysis.json | generated | CI subunit pairwise correlation and permutation test results |
| 09_Computational_Modeling/results/phase_i/category_overlap_fisher.json | generated | Fisher test results for gene category overlap |
| 09_Computational_Modeling/results/phase_j/intervention_bar_chart.png | generated | Bar chart of intervention mechanism modeling results |
| 09_Computational_Modeling/results/phase_k/wet_lab_overlay.png | generated | Computational predictions overlaid on wet lab JC-1 data |
| 09_Computational_Modeling/scripts/composite/README.md | doc | Overview, entry points, and kill criteria for composite experiments |
| 09_Computational_Modeling/scripts/composite/experiment5b_interventions.py | source | Runs three interventions through composite FBA+ODE model |
| 09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py | source | Generates 2-panel abstract figure with MPTP and MitoQ data |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py | source | Empirical half-life transit window experiment with bootstrap CI |
| 09_Computational_Modeling/scripts/experiments_v2/experiment4_interventions.py | source | Three-intervention mechanism modeling with bootstrap CI |
| 09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py | source | Gene clustering and full immortalization sweep over 145 genes |
| 09_Computational_Modeling/scripts/investigation_phases/phase_g1_order_statistics.py | source | Order-statistics test comparing analytic vs FBA transit window |
| 09_Computational_Modeling/scripts/investigation_phases/phase_h_ci_subunit_analysis.py | source | Phase H Complex I subunit deep-dive correlation analysis |
| 10_Research_Questions/Research_Questions.md | doc | Ten core research questions with literature and status tracking |
| INDEX.md | doc | Project navigation index with folder-level descriptions |
| .gitmodules | config | Declares Human-GEM and mitomammal git submodules |
| 01_Vision_and_Strategy/Layer_1_Scope_Reframe_2026-04-23.md | doc | Strategic scope reframe document dated 2026-04-23 |
| 01_Vision_and_Strategy/Research_Hypotheses.docx | doc | Research hypotheses for mitochondria viability project |
| 02_Methodology/Literature_Mapping.docx | doc | Literature mapping methodology document |
| 04_Source_Literature/Mitochondrial_Transfer/Artificial Mitochondria Transfer_ Current Challenges, Advances, and Future Applications.docx | doc | Source paper on artificial mitochondrial transfer methods |
| 04_Source_Literature/Mitochondrial_Transfer/Mitochondrial phenotypes in purified human immune cell subtypes and cell mixtures.docx | doc | Source paper on mitochondrial phenotypes in immune cells |
| 05_Extracted_Data/PDF_Metadata/Isolation and bioenergetic characterization of mitochondria from Pichia pastoris.txt | data | Extracted PDF metadata; identical duplicate of underscore-named file |
| 05_Extracted_Data/PDF_Metadata/Isolation_and_bioenergetic_characterization_of_mitochondria_from_Pichia_pastoris.txt | data | Extracted PDF metadata; identical duplicate of space-named file |
| 05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.txt | data | Extracted PDF metadata for mouse lung mitochondria isolation paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_of_functionally_active_and_highly_purified_neuronal_mitochondria_from_human_cortex.json | data | Extracted PDF metadata in JSON for neuronal mitochondria paper |
| 05_Extracted_Data/PDF_Metadata/Mitochondria_isolated_from_lipid_droplets_of_white_adipose_tissue_reveal_functional_differences.txt | data | Extracted PDF metadata for adipose mitochondria paper |
| 05_Extracted_Data/PDF_Metadata/Rapid_isolation_of_respiring_skeletal_muscle_mitochondria_using_nitrogen_cavitation.txt | data | Extracted PDF metadata for skeletal muscle isolation paper |
| 05_Extracted_Data/Protocol_Summaries/combined_content40.txt | generated | Batch-concatenated protocol summaries from multiple papers |
| 05_Extracted_Data/Protocol_Summaries/combined_content80.txt | generated | Batch-concatenated protocol summaries from multiple papers |
| 05_Extracted_Data/Structured_JSON/A_method_for_isolating_intact_mitochondria_and_nuclei_from_the_same_homogenate,_and_the_influen.json | data | Structured extracted data from mitochondria/nuclei co-isolation paper |
| 05_Extracted_Data/Structured_JSON/A_rapid_method_for_the_isolation_of_intact_mitochondria_from_isolated_rat_liver_cells.json | data | Structured extracted data from rat liver mitochondria isolation paper |
| 05_Extracted_Data/Structured_JSON/An_Improved_Method_for_Preparation_of_Uniform_and_Functional_Mitochondria_from_Fresh_Liver.json | data | Structured extracted data from improved liver mitochondria prep paper |
| 05_Extracted_Data/Structured_JSON/Assay_of_succinate_dehydrogenase_activity_by_the_tetrazolium_method_evaluation_of_an_improved_t.json | data | Structured extracted data from succinate dehydrogenase assay paper |
| 05_Extracted_Data/Structured_JSON/Efficient_isolation_of_pure_and_functional_mitochondria_from_mouse_tissues_using_automated_tiss.json | data | Structured extracted data from automated mouse tissue isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_Electron_Microscopic_Analysis_of_Liver_Cancer_Cell_Mitochondria.json | data | Structured extracted data from liver cancer mitochondria EM paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_Structural_Studies_of_Mitochondria_from_Pea_Roots.json | data | Structured extracted data from pea root mitochondria isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_functional_assessment_of_mitochondria_from_small_amounts_of_mouse_brain_tissue.json | data | Structured extracted data from mouse brain mitochondria isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_Large_Amounts_of_Highly_Pure_Mitochondria_for_Omics_Studies.json | data | Structured extracted data from large-scale mitochondria isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_Physiologically_Active_and_Intact_Mitochondria_from_Chickpea.json | data | Structured extracted data from chickpea mitochondria isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_functionally_active_and_highly_purified_neuronal_mitochondria_from_human_cortex.json | data | Structured extracted data from human cortex neuronal mitochondria paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_for_biogenetical_studies_An_update.json | data | Structured extracted data from mitochondria biogenesis isolation update |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_procyclic_Trypanosoma_brucei.json | data | Structured extracted data from Trypanosoma brucei mitochondria paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondrial_subpopulations_from_skeletal_muscle_Optimizing_recovery_and_preservi.json | data | Structured extracted data from skeletal muscle subpopulation paper |
| 05_Extracted_Data/Structured_JSON/Mitochondria_and_peroxisomes_from_the_cellular_slime_mould_Dictyostelium_discoideum._Isolation_.json | data | Structured extracted data from Dictyostelium organelle isolation paper |
| 05_Extracted_Data/Structured_JSON/Mitochondrial_Isolation_and_Real-Time_Monitoring_of_MOMP.json | data | Structured extracted data from MOMP monitoring isolation paper |
| 05_Extracted_Data/Structured_JSON/Mouse_Liver_Mitochondria_Isolation,_Size_Fractionation,_and_Real-time_MOMP_Measurement.json | data | Structured extracted data from mouse liver MOMP measurement paper |
| 05_Extracted_Data/Structured_JSON/Organelle_isolation_functional_mitochondria_from_mouse_liver,_muscle_and_cultured_fibroblasts.json | data | Structured extracted data from multi-tissue organelle isolation paper |
| 05_Extracted_Data/Structured_JSON/Protocol_for_mitochondrial_isolation_and_sub-cellular_localization_assay_for_mitochondrial_prot.json | data | Structured extracted data from mitochondrial localization assay paper |
| 05_Extracted_Data/Structured_JSON/Purity_matters_A_workflow_for_the_valid_high-resolution_lipid_profiling_of_mitochondria_from_ce.json | data | Structured extracted data from mitochondrial lipid profiling paper |
| 05_Extracted_Data/Structured_JSON/Rapid_isolation_of_metabolically_active_mitochondria_from_rat_brain_and_subregions_using_Percol.json | data | Structured extracted data from rat brain Percoll isolation paper |
| 05_Extracted_Data/Structured_JSON/Simultaneous_isolation_of_pure_and_intact_chloroplasts_and_mitochondria_from_moss_as_the_basis_.json | data | Structured extracted data from moss organelle co-isolation paper |
| 05_Extracted_Data/Structured_JSON/Two-Step_Tag-Free_Isolation_of_Mitochondria_for_Improved_Protein_Discovery_and_Quantification.json | data | Structured extracted data from tag-free mitochondria proteomics paper |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_40.docx | generated | Batch-combined comparative analysis synthesis document |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_70-1.docx | generated | Batch-combined comparative analysis synthesis document |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_90-3.docx | generated | Batch-combined comparative analysis synthesis document |
| 08_Experimental_Work/Experiments_Overview.md | doc | Overview document for experimental work planning |
| 09_Computational_Modeling/Whole_Cell_Modeling/Human-GEM | submodule | SysBioChalmers Human-GEM genome-scale metabolic model submodule |
| 09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py | source | Beard QAMAS in vitro ODE model; runs at module level without main guard |
| 09_Computational_Modeling/decay_utils.py | source | Shared utility: GPR-aware FBA decay; imported by all experiment scripts |
| 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_FOLLOWUP_PLAN_2026-05-09.md | doc | Operational plan for DocInsight literature follow-up actions |
| 09_Computational_Modeling/docs/conference_planning/Modeling_Overview.md | doc | Overview document for computational modeling approach |
| 09_Computational_Modeling/docs/conference_planning/syn3a_notes_analysis_2026-04-21.md | doc | Analysis notes on Syn3A minimal cell crosswalk |
| 09_Computational_Modeling/docs/investigation/CI_SUBUNIT_DEEP_DIVE.md | doc | Investigation notes on Complex I subunit analysis |
| 09_Computational_Modeling/docs/investigation/INTERVENTION_MECHANISMS.md | doc | Investigation notes on intervention mechanism candidates |
| 09_Computational_Modeling/docs/investigation/SYN3A_CROSSWALK.md | doc | Investigation notes on Syn3A vs mitochondria crosswalk |
| 09_Computational_Modeling/docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md | doc | Strategic computational path document dated 2026-04-23 |
| 09_Computational_Modeling/results/archive_v1/complex_sensitivity.csv | data | Archived v1 complex sensitivity analysis results |
| 09_Computational_Modeling/results/archive_v1/gene_knockout_scores.csv | data | Archived v1 gene knockout impact scores |
| 09_Computational_Modeling/results/archive_v1/sensitivity_figure.png | asset | Archived v1 sensitivity analysis figure |
| 09_Computational_Modeling/results/composite/ex10_mptp_traces.png | asset | Experiment 10 MPTP scenario trace figure |
| 09_Computational_Modeling/results/composite/ex5_1_reference_validation.png | asset | Experiment 5.1 reference validation figure |
| 09_Computational_Modeling/results/composite/ex5_3_scenario_tw.csv | data | Experiment 5.3 scenario transit window results |
| 09_Computational_Modeling/results/composite/ex5_6_sensitivity.csv | data | Experiment 5.6 literature-sourced sensitivity results |
| 09_Computational_Modeling/results/composite/ex6_option_b_traces.png | asset | Experiment 6 option-B extension trace figure |
| 09_Computational_Modeling/results/composite/final_abstract_figure_composite.png | asset | Final composite figure for abstract submission |
| 09_Computational_Modeling/results/experiments_v2/experiment1c_v2_halflife_sweep.png | asset | Experiment 1c v2 half-life sweep figure |
| 09_Computational_Modeling/results/phase_a/baseline_solution.csv | data | Phase A baseline FBA solution data |
| 09_Computational_Modeling/results/phase_b/essential_genes_clustered.csv | data | Phase B essential genes with clustering assignments |
| 09_Computational_Modeling/results/phase_b/phase_b_summary.json | data | Phase B summary statistics and results JSON |
| 09_Computational_Modeling/results/phase_e/chapman_table_parsed.csv | data | Phase E parsed Chapman literature table data |
| 09_Computational_Modeling/results/phase_g/g2_human_gem_inspection.json | data | Phase G Human-GEM cross-model inspection results |
| 09_Computational_Modeling/results/phase_h/ci_subunit_data.csv | data | Phase H Complex I subunit analysis data |
| 09_Computational_Modeling/results/phase_i/syn3a_crosswalk_3rxns.csv | data | Phase I Syn3A three-reaction crosswalk comparison data |
| 09_Computational_Modeling/results/phase_j/intervention_delta_tw.csv | data | Phase J intervention delta transit-window results |
| 09_Computational_Modeling/scripts/archive_v1/experiment1_transit_window.py | source | Archived v1 transit window FBA script; has __main__ entry |
| 09_Computational_Modeling/scripts/composite/experiment10_mptp_composite.py | source | MPTP composite experiment testing Ca2+ scenario partition |
| 09_Computational_Modeling/scripts/composite/experiment5c_sensitivity.py | source | Literature-sourced sensitivity propagation experiment |
| 09_Computational_Modeling/scripts/composite/experiment9_atp_first_diagnostic.py | source | ATP-first paradox diagnostic partitioning three hypotheses |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1b_v2_gpr_knockout.py | source | GPR-aware gene knockout scoring correcting v1 OR-rule bug |
| 09_Computational_Modeling/scripts/investigation_phases/phase_a_dissection.py | source | MitoMAMMAL mechanistic dissection A.1–A.5 runs |
| 09_Computational_Modeling/scripts/investigation_phases/phase_c_forensic_29h.py | source | Forensic dissection of 29-hour transit window result |
| 09_Computational_Modeling/scripts/investigation_phases/phase_g2_cross_model.py | source | Cross-model validation using Human-GEM mitochondrial subset |
| 09_Computational_Modeling/scripts/investigation_phases/phase_i_syn3a_crosswalk.py | source | Syn3A vs mitochondria 3-reaction transport comparison |
| Archive/Old-Unneeded/Mitochondrial_Autonomy_Techniques_and_Insights.docx | dead | Archived unused document in Old-Unneeded folder |
| Mitochondrial Research and Aging: Innovations, Questions, and Strategies.md | doc | Root-level research overview on mitochondria aging strategies |
| 01_Vision_and_Strategy/Executive_Summary_2026-04-21.md | doc | Project executive summary dated April 2026 |
| 01_Vision_and_Strategy/Notebook_Transcription_Otter.txt | data | Otter.ai audio transcription of planning notebook session |
| 01_Vision_and_Strategy/Strategy_Critique_and_Assumptions_2026-04-21.md | doc | Critical review of strategy assumptions April 2026 |
| 02_Methodology/Paper_Ranking_Framework.docx | doc | Framework for ranking source literature papers by quality |
| 04_Source_Literature/Mitochondrial_Transfer/Characterization and origins of cell-free mitochondria in healthy murine and human blood.docx | data | Imported copy of source literature paper on cell-free mito |
| 04_Source_Literature/Mitochondrial_Transfer/Mitochondrial transfer_transplantation_ an emerging therapeutic approach for multiple diseases.docx | data | Imported copy of source literature therapeutic review paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_and_Respiratory_Measurements_of_Mitochondria_from_Arabidopsis_thaliana.json | data | PDF metadata extracted from Arabidopsis respiratory paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_and_reconstruction_of_cardiac_mitochondria_from_SBEM_images_using_a_deep_learning-bas.json | data | PDF metadata extracted from cardiac SBEM deep-learning paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_from_Ustilago_maydis_Protoplasts.json | data | PDF metadata extracted from fungal protoplast isolation paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_of_intact,_functional_mitochondria_from_the_model_plant_Arabidopsis_thaliana.json | data | PDF metadata extracted from Arabidopsis functional mito paper |
| 05_Extracted_Data/PDF_Metadata/Organelle_isolation_functional_mitochondria_from_mouse_liver,_muscle_and_cultured_fibroblasts.json | data | PDF metadata extracted from multi-tissue mouse isolation paper |
| 05_Extracted_Data/Protocol_Summaries/combined_content10.txt | data | Aggregated protocol text content batch 10 |
| 05_Extracted_Data/Protocol_Summaries/combined_content50.txt | data | Aggregated protocol text content batch 50 |
| 05_Extracted_Data/Protocol_Summaries/combined_content_over_80.txt | data | Aggregated protocol text content batch 80-plus |
| 05_Extracted_Data/Structured_JSON/A_microcalorimetric_study_of_the_effect_of_La3+_on_mitochondria_isolated_from_Star-Cross_288_ch.json | data | Structured JSON extraction of microcalorimetry paper data |
| 05_Extracted_Data/Structured_JSON/A_semi-automated_method_for_isolating_functionally_intact_mitochondria_from_cultured_cells_and_.json | data | Structured JSON extraction of semi-automated isolation paper |
| 05_Extracted_Data/Structured_JSON/An_Update_on_Isolation_of_Functional_Mitochondria_from_Cells_for_Bioenergetics_Studies.json | data | Structured JSON extraction of bioenergetics isolation update paper |
| 05_Extracted_Data/Structured_JSON/Characterization_of_growth_plate_mitochondria.json | data | Structured JSON extraction of growth plate mitochondria paper |
| 05_Extracted_Data/Structured_JSON/Genome-wide_analysis_of_RNA_extracted_from_isolated_mitochondria.json | data | Structured JSON extraction of genome-wide RNA analysis paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_Metabolic_Assessment_of_Cancer_Cell_Mitochondria.json | data | Structured JSON extraction of cancer cell mito assessment paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_bioenergetic_characterization_of_mitochondria_from_Pichia_pastoris.json | data | Structured JSON extraction of yeast Pichia bioenergetics paper |
| 05_Extracted_Data/Structured_JSON/Isolation_and_quality_control_of_functional_mitochondria.json | data | Structured JSON extraction of mito QC isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.json | data | Structured JSON extraction of mouse lung mito isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_brain_mitochondria_from_neonatal_mice.json | data | Structured JSON extraction of neonatal mouse brain mito paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_intact,_functional_mitochondria_from_the_model_plant_Arabidopsis_thaliana.json | data | Structured JSON extraction of Arabidopsis intact mito paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_animal_tissue.json | data | Structured JSON extraction of animal tissue isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_the_CNS.json | data | Structured JSON extraction of CNS mito isolation paper |
| 05_Extracted_Data/Structured_JSON/Isolation_of_rat_adrenocortical_mitochondria.json | data | Structured JSON extraction of rat adrenocortical mito paper |
| 05_Extracted_Data/Structured_JSON/Mitochondria_from_the_hepatopancreas_of_the_marine_clam_Mercenaria_mercenaria_substrate_prefere.json | data | Structured JSON extraction of marine clam hepatopancreas paper |
| 05_Extracted_Data/Structured_JSON/Mitochondrial_Respiration_of_Platelets_Comparison_of_Isolation_Methods.json | data | Structured JSON extraction of platelet respiration isolation paper |
| 05_Extracted_Data/Structured_JSON/Optimal_isolation_of_mitochondria_for_proteomic_analyses.json | data | Structured JSON extraction of proteomics isolation paper |
| 05_Extracted_Data/Structured_JSON/Preparation_of_highly_coupled_rat_heart_mitochondria.json | data | Structured JSON extraction of rat heart coupled mito paper |
| 05_Extracted_Data/Structured_JSON/Purification_of_Functional_Platelet_Mitochondria_Using_a_Discontinuous_Percoll_Gradient.json | data | Structured JSON extraction of Percoll platelet mito paper |
| 05_Extracted_Data/Structured_JSON/Qualitative_Characterization_of_the_Rat_Liver_Mitochondrial_Lipidome_Using_All_Ion_Fragmentatio.json | data | Structured JSON extraction of rat liver lipidome paper |
| 05_Extracted_Data/Structured_JSON/Rapid_isolation_of_respiring_skeletal_muscle_mitochondria_using_nitrogen_cavitation.json | data | Structured JSON extraction of nitrogen cavitation muscle paper |
| 05_Extracted_Data/Structured_JSON/The_isolation_and_properties_of_mitochondria_from_rat_pancreas.json | data | Structured JSON extraction of rat pancreas mito paper |
| 06_Synthesis/Annotated_Bibliography.docx | doc | Annotated bibliography of curated source literature |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_50.docx | doc | Comparative analysis synthesis document chunk 50 |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_70-2.docx | doc | Comparative analysis synthesis document chunk 70-2 |
| 06_Synthesis/Comparative_Analysis/combined_content_30.docx | doc | Combined content synthesis document chunk 30 |
| 09_Computational_Modeling/LAB_NOTEBOOK.md | doc | Lab notebook logging computational modeling sessions |
| 09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/README.md | doc | README for Beard lab whole-cell model subdirectory |
| 09_Computational_Modeling/Whole_Cell_Modeling/cortassa/README.md | doc | README for Cortassa model subdirectory |
| 09_Computational_Modeling/docs/conference_planning/ABSTRACT_DRAFT_2026-04-23.md | doc | Draft conference abstract April 2026 |
| 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_MITO_QUERY_GUIDE.md | doc | Guide for querying DocInsight mito literature tool |
| 09_Computational_Modeling/docs/conference_planning/qbio_analysis_2026-04-21.md | doc | qBio conference analysis and planning notes |
| 09_Computational_Modeling/docs/investigation/ANOMALIES_AND_HIDDEN_FINDINGS.md | doc | Documented anomalies and unexpected model findings |
| 09_Computational_Modeling/docs/investigation/COMPOSITE_AUDIT_2026-04-24.md | doc | Audit trail for composite FBA+ODE model experiments |
| 09_Computational_Modeling/docs/investigation/INVESTIGATION_SYNTHESIS_2026-04-23.md | doc | Synthesis of multi-phase investigation results April 2026 |
| 09_Computational_Modeling/docs/investigation/TIMELINE_NOTE.md | doc | Short timeline note for investigation chronology context |
| 09_Computational_Modeling/ode_utils.py | source | Shared ODE integration library for Beard 2005 OXPHOS model |
| 09_Computational_Modeling/results/archive_v1/decay_curves.png | generated | Archive v1 decay curve plot output |
| 09_Computational_Modeling/results/archive_v1/halflife_sweep.csv | generated | Archive v1 half-life sweep simulation results |
| 09_Computational_Modeling/results/archive_v1/transit_window_results.csv | generated | Archive v1 transit window computation results |
| 09_Computational_Modeling/results/composite/ex11_ros_mitoq.csv | generated | Experiment 11 ROS MitoQ simulation output CSV |
| 09_Computational_Modeling/results/composite/ex5_2_coupling_dynamics.csv | generated | Experiment 5.2 coupling dynamics simulation output |
| 09_Computational_Modeling/results/composite/ex5_4_mechanism_partition.csv | generated | Experiment 5.4 mechanism partition simulation output |
| 09_Computational_Modeling/results/composite/ex5_6_sensitivity_tornado.png | generated | Experiment 5.6 sensitivity tornado chart output |
| 09_Computational_Modeling/results/composite/ex7_human_gem_composite.csv | generated | Experiment 7 Human-GEM composite simulation output |
| 09_Computational_Modeling/results/experiments_v2/experiment1_v2_decay_curves.png | generated | Experiment 1 v2 decay curve plot output |
| 09_Computational_Modeling/results/experiments_v2/experiment1c_v2_summary.json | generated | Experiment 1c v2 half-life sweep summary JSON output |
| 09_Computational_Modeling/results/phase_b/deep_dive_profiles.json | generated | Phase B essential gene deep dive profile data |
| 09_Computational_Modeling/results/phase_b/essential_genes_mitocarta_crossref.csv | generated | Phase B essential genes MitoCarta cross-reference output |
| 09_Computational_Modeling/results/phase_b/single_gene_leverage.csv | generated | Phase B single-gene leverage score rankings |
| 09_Computational_Modeling/results/phase_e/fva_baseline.csv | generated | Phase E FVA baseline flux variability analysis output |
| 09_Computational_Modeling/results/phase_g/g2b_human_gem_uniform_decay.json | generated | Phase G2b Human-GEM uniform decay claim test output |
| 09_Computational_Modeling/results/phase_h/decay_curves_empirical.png | generated | Phase H empirical overlay decay curve plot |
| 09_Computational_Modeling/results/phase_j/final_abstract_figure.png | generated | Phase J final conference abstract figure output |
| 09_Computational_Modeling/results/phase_j/intervention_mechanisms.csv | generated | Phase J intervention mechanism simulation output |
| 09_Computational_Modeling/scripts/archive_v1/experiment1b_gene_sensitivity.py | source | Archived v1 gene sensitivity and engineering target ranking |
| 09_Computational_Modeling/scripts/composite/experiment11_ros_mitoq.py | source | ROS module with MitoQ as mechanistic scavenger experiment |
| 09_Computational_Modeling/scripts/composite/experiment6_option_b_extension.py | source | Membrane integrity non-proteomic failure mode experiment |
| 09_Computational_Modeling/scripts/composite/validate_against_beard.py | source | Beard 2005 baseline PO-curve reproduction validation script |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1c_v2_halflife_sweep.py | source | Half-life sweep v2 with GPR-aware decay and dual objective |
| 09_Computational_Modeling/scripts/investigation_phases/phase_b6_deep_dive.py | source | Phase B.6 deep dive profiling 10 selected essential genes |
| 09_Computational_Modeling/scripts/investigation_phases/phase_d_adversarial_suite.py | source | Phase D adversarial perturbation and trust-framework suite |
| 09_Computational_Modeling/scripts/investigation_phases/phase_g2b_human_gem_decay.py | source | Phase G.2b Human-GEM algebraic decay claim cross-check |
| 09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py | source | Phase K overlay predicted decay vs 2024 wet-lab yeast data |
| Archive/SYN3a_NOTES_RemNoteExport_Knowledge-Database_md_2026-04-21_12-55.zip | data | Archived RemNote knowledge base export zip April 2026 |
| README.md | doc | Top-level project README |
| 01_Vision_and_Strategy/Exploratory_Landscape.docx | doc | Vision/strategy landscape exploration document (binary Word format) |
| 01_Vision_and_Strategy/Programmable_Mitochondria_Vision_2026-04-21.md | doc | Project vision: programmable mitochondria as engineerable vectors |
| 02_Methodology/BSHR_Loop.txt | doc | Methodology guide: Brainstorm-Search-Hypothesize-Refine LLM loop |
| 03_Study_Registry/references.ris | data | Bibliography in RIS format for study registry citations |
| 04_Source_Literature/Mitochondrial_Transfer/Isolation of Mitochondria from Saccharomyces cerevisiae.docx | doc | Source paper: yeast mitochondria isolation protocol (Word format) |
| 04_Source_Literature/Mitochondrial_Transfer/The Functions, Methods, and Mobility of Mitochondrial Transfer Between Cells.docx | doc | Source paper: mitochondrial transfer methods review (Word format) |
| 05_Extracted_Data/PDF_Metadata/Isolation_and_Respiratory_Measurements_of_Mitochondria_from_Arabidopsis_thaliana.txt | data | Extracted PDF metadata from Arabidopsis mitochondria isolation paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_and_reconstruction_of_cardiac_mitochondria_from_SBEM_images_using_a_deep_learning-bas.txt | data | Extracted PDF metadata for cardiac SBEM mitochondria paper |
| 05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_from_Ustilago_maydis_Protoplasts.txt | data | Extracted PDF metadata for U. maydis mitochondria isolation |
| 05_Extracted_Data/PDF_Metadata/Isolation_of_intact,_functional_mitochondria_from_the_model_plant_Arabidopsis_thaliana.txt | data | Extracted PDF metadata: intact functional mitochondria from Arabidopsis |
| 05_Extracted_Data/PDF_Metadata/Organelle_isolation_functional_mitochondria_from_mouse_liver,_muscle_and_cultured_fibroblasts.txt | data | Extracted PDF metadata: mouse liver/muscle organelle isolation paper |
| 05_Extracted_Data/Protocol_Summaries/combined_content20.txt | data | Combined protocol content batch 20 from source literature |
| 05_Extracted_Data/Protocol_Summaries/combined_content60.txt | data | Combined protocol content batch 60 from source literature |
| 05_Extracted_Data/Structured_JSON/A_critical_comparison_between_two_classical_and_a_kit-based_method_for_mitochondria_isolation.json | data | Structured extraction: classical vs kit-based mitochondria isolation |
| 05_Extracted_Data/Structured_JSON/A_mitosome_purification_protocol_based_on_percoll_density_gradients_and_its_use_in_validating_t.json | data | Structured extraction: mitosome Percoll purification protocol |
| 05_Extracted_Data/Structured_JSON/A_simplified_method_to_isolate_rice_mitochondria.json | data | Structured extraction: rice mitochondria isolation protocol |
| 05_Extracted_Data/Structured_JSON/An_improved_method_with_a_wider_applicability_to_isolate_plant_mitochondria_for_mtDNA_extractio.json | data | Structured extraction: plant mitochondria isolation for mtDNA |
| 05_Extracted_Data/Structured_JSON/Comparison_of_three_methods_for_mitochondria_isolation_from_the_human_liver_cell_line_(HepG2).json | data | Structured extraction: three isolation methods compared for HepG2 |
| 05_Extracted_Data/Structured_JSON/Improved_method_for_isolation_of_mitochondria_from_chick_breast_muscle_using_Nagarse.json | data | Structured extraction: Nagarse-based chick muscle isolation |
| 05_Extracted_Data/Structured_JSON/Isolation_and_Purification_of_Mitochondria_from_Cell_Culture_for_Proteomic_Analyses.json | data | Structured extraction: cell culture mitochondria for proteomics |
| 05_Extracted_Data/Structured_JSON/Isolation_and_comparative_proteomic_analysis_of_mitochondria_from_the_pulp_of_ripening_citrus_f.json | data | Structured extraction: citrus fruit pulp mitochondria proteomics |
| 05_Extracted_Data/Structured_JSON/Isolation_and_reconstruction_of_cardiac_mitochondria_from_SBEM_images_using_a_deep_learning-bas.json | data | Structured extraction: deep-learning cardiac SBEM reconstruction |
| 05_Extracted_Data/Structured_JSON/Isolation_of_Mitochondria_from_Minimal_Quantities_of_Mouse_Skeletal_Muscle_for_High_Throughput_.json | data | Structured extraction: minimal quantity mouse muscle isolation |
| 05_Extracted_Data/Structured_JSON/Isolation_of_functional_mitochondria_from_rat_kidney_and_skeletal_muscle_without_manual_homogen.json | data | Structured extraction: rat kidney/muscle without manual homogenization |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_and_mitochondrial_RNA_from_Crithidia_fasciculata.json | data | Structured extraction: Crithidia fasciculata mitochondria/RNA |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_ascites_tumor_cells_permeabilized_with_digitonin.json | data | Structured extraction: digitonin-permeabilized tumor cell isolation |
| 05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_tissue_culture_cells.json | data | Structured extraction: tissue culture cell mitochondria isolation |
| 05_Extracted_Data/Structured_JSON/Magnetic_nanoparticles_an_improved_method_for_mitochondrial_isolation.json | data | Structured extraction: magnetic nanoparticle isolation method |
| 05_Extracted_Data/Structured_JSON/Mitochondria_isolated_from_lipid_droplets_of_white_adipose_tissue_reveal_functional_differences.json | data | Structured extraction: lipid droplet-associated mitochondria |
| 05_Extracted_Data/Structured_JSON/Mitochondrial_isolation_from_skeletal_muscle.json | data | Structured extraction: skeletal muscle mitochondria isolation |
| 05_Extracted_Data/Structured_JSON/Optimization_of_differential_filtration-based_mitochondrial_isolation_for_mitochondrial_transpl.json | data | Structured extraction: filtration-based isolation for transplantation |
| 05_Extracted_Data/Structured_JSON/Preparation_of_physiologically_active_inside-out_vesicles_from_plant_inner_mitochondrial_membra.json | data | Structured extraction: inside-out plant IMM vesicle preparation |
| 05_Extracted_Data/Structured_JSON/Purification_of_functional_mouse_skeletal_muscle_mitochondria_using_Percoll_density_gradient_ce.json | data | Structured extraction: Percoll gradient mouse muscle purification |
| 05_Extracted_Data/Structured_JSON/Rapid_isolation_and_purification_of_functional_platelet_mitochondria_using_a_discontinuous_Perc.json | data | Structured extraction: platelet mitochondria discontinuous Percoll |
| 05_Extracted_Data/Structured_JSON/Rapid_isolation_techniques_for_mitochondria_technique_for_rat_liver_mitochondria.json | data | Structured extraction: rapid rat liver mitochondria isolation |
| 05_Extracted_Data/Structured_JSON/The_isolation_of_coupled_mitochondria_from_Physarum_polycephalum_and_their_response_to_Ca2+.json | data | Structured extraction: P. polycephalum coupled mitochondria and Ca2+ |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_10.docx | doc | Synthesis comparative analysis document batch 10 (Word format) |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_60-1.docx | doc | Synthesis comparative analysis document batch 60 (Word format) |
| 06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_80-1.docx | doc | Synthesis comparative analysis document batch 80 (Word format) |
| 06_Synthesis/Consolidated_Protocols.txt | generated | Accidental pip-install terminal output captured to file; not a protocol |
| 09_Computational_Modeling/README.md | doc | Computational modeling overview, quickstart, directory map, key findings |
| 09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_2005_initial_conditions.csv | data | Beard 2005 OXPHOS ODE model initial conditions from published SI |
| 09_Computational_Modeling/Whole_Cell_Modeling/mitomammal | submodule | Empty dir; populated by setup_environment.sh via git clone from GitLab |
| 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_AGENT_HANDOFF.md | doc | Handoff briefing for literature-search agent (q-bio Chicago 2026) |
| 09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_PROPAGATION_PATCH_2026-05-10.md | doc | Citation verification patch over DocInsight audit replacement citations |
| 09_Computational_Modeling/docs/conference_planning/qbio_chicago_lodging_2026-04-21.md | doc | Conference logistics: lodging options for q-bio Chicago 2026 |
| 09_Computational_Modeling/docs/investigation/AUDIT_2026-04-22.md | doc | Systematic audit of computational claims pre-Phase G validation |
| 09_Computational_Modeling/docs/investigation/ESSENTIAL_GENES_DEEP_DIVE.md | doc | Phase B findings: deep-dive profiles of 10 essential mouse genes |
| 09_Computational_Modeling/docs/investigation/MITOMAMMAL_DISSECTION.md | doc | Phase A: baseline FBA trace and model structure characterization |
| 09_Computational_Modeling/docs/investigation/TRUST_LEDGER.md | doc | Adversarial suite: claim-by-claim falsification ledger (Phase D) |
| 09_Computational_Modeling/paths.py | source | Shared utility: single source of truth for all project paths |
| 09_Computational_Modeling/results/archive_v1/experiment1_summary.json | generated | Archived v1 experiment 1 summary JSON output |
| 09_Computational_Modeling/results/archive_v1/halflife_sweep_curves.csv | generated | Archived v1 half-life sweep decay curves CSV |
| 09_Computational_Modeling/results/composite/README.md | doc | Documents outputs produced in results/composite/ directory |
| 09_Computational_Modeling/results/composite/ex11_ros_mitoq.png | generated | Plot: Ex 11 ROS-MitoQ coupling analysis figure |
| 09_Computational_Modeling/results/composite/ex5_2_delta_psi_traces.png | generated | Plot: Ex 5.2 ΔΨm traces under three halflife regimes |
| 09_Computational_Modeling/results/composite/ex5_5_intervention_comparison.png | generated | Plot: Ex 5.5 intervention strategy comparison figure |
| 09_Computational_Modeling/results/composite/ex5_6_tornado.csv | generated | Ex 5.6 tornado sensitivity analysis CSV output |
| 09_Computational_Modeling/results/composite/ex9_atp_first_diagnostic.csv | generated | Ex 9 ATP first-failure diagnostic CSV output |
| 09_Computational_Modeling/results/experiments_v2/experiment1_v2_results.csv | generated | V2 experiment 1 time-stepped FBA flux results CSV |
| 09_Computational_Modeling/results/experiments_v2/experiment1d_minimal_set.png | generated | Plot: minimal vs full essential gene set decay comparison |
| 09_Computational_Modeling/results/phase_b/essential_dispensable_partition.json | generated | Phase B: 145 essential vs 229 dispensable mouse gene partition |
| 09_Computational_Modeling/results/phase_b/experiment1b_v2_summary.json | generated | Phase B v2 gene sensitivity knockout summary JSON |
| 09_Computational_Modeling/results/phase_c/phase_c_summary.json | generated | Phase C forensic 29h derivation summary JSON |
| 09_Computational_Modeling/results/phase_e/phase_e_summary.json | generated | Phase E anomaly hunt and heterogeneity findings JSON |
| 09_Computational_Modeling/results/phase_g/g5_ros_coupling.csv | generated | Phase G5 ROS-coupled accelerated protein decay CSV |
| 09_Computational_Modeling/results/phase_h/transit_window_empirical.csv | generated | Phase H empirical transit window re-run CSV |
| 09_Computational_Modeling/results/phase_j/intervention_analysis.json | generated | Phase J intervention modeling analysis JSON |
| 09_Computational_Modeling/results/phase_k/ks_test_result.json | generated | Phase K KS-test statistical validation result JSON |
| 09_Computational_Modeling/scripts/archive_v1/experiment1c_halflife_sweep.py | source | Archived v1: uniform half-life sweep vs transit window (hardcoded paths) |
| 09_Computational_Modeling/scripts/composite/experiment5_fba_ode.py | source | Composite FBA+ODE Ex 5.2-5.4: ΔΨm coupling sanity and TW derivation |
| 09_Computational_Modeling/scripts/composite/experiment7_human_gem.py | source | Cross-model validation: composite FBA+ODE run on Human-GEM |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1_v2_transit_window.py | source | V2 transit window: GPR-aware decay, signed flux, dual objective |
| 09_Computational_Modeling/scripts/experiments_v2/experiment1d_minimal_set.py | source | Direct A3 test: minimal essential gene set vs full decay |
| 09_Computational_Modeling/scripts/investigation_phases/phase_b_annotate_essentials.py | source | Annotates 145 essential genes via MyGene.info API |
| 09_Computational_Modeling/scripts/investigation_phases/phase_e_anomaly_hunt.py | source | FVA and non-uniform decay characterization (Phase E) |
| 09_Computational_Modeling/scripts/investigation_phases/phase_g5_ros_coupling.py | source | ROS-coupled protein damage acceleration model (Phase G.5) |
| 09_Computational_Modeling/setup_environment.sh | config | Bootstraps conda env, installs pip deps, clones MitoMAMMAL from GitLab |
| DIY Yeast Media.md | doc | DIY yeast media recipe using household ingredients |


## Machine-checkable data

```json
{
  "files": [
    {
      "path": ".gitignore",
      "role": "config",
      "note": "Git version control ignore patterns"
    },
    {
      "path": "01_Vision_and_Strategy/IMOL-ERT_Vision.docx",
      "role": "doc",
      "note": "Business plan and overarching vision document"
    },
    {
      "path": "01_Vision_and_Strategy/Project_Overview.docx",
      "role": "doc",
      "note": "Master project document with objectives and progress"
    },
    {
      "path": "02_Methodology/Inclusion_Exclusion_Criteria.docx",
      "role": "doc",
      "note": "8-category taxonomy with inclusion and exclusion rules"
    },
    {
      "path": "03_Study_Registry/studies.csv",
      "role": "data",
      "note": "114 screened papers with metadata and inclusion scores"
    },
    {
      "path": "04_Source_Literature/Mitochondrial_Transfer/Mitochondria transplantation between living cells_ (Gäbelein et al. 2021).docx",
      "role": "doc",
      "note": "Summary of Gäbelein 2021 mitochondria transfer paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/A mitosome purification protocol based on percoll density gradients and its use in validating t.txt",
      "role": "data",
      "note": "PDF metadata extraction output for mitosome paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_and_bioenergetic_characterization_of_mitochondria_from_Pichia_pastoris.json",
      "role": "data",
      "note": "PDF metadata for Pichia pastoris isolation paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.json",
      "role": "data",
      "note": "PDF metadata for mice lung tissue isolation paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_of_brain_mitochondria_from_neonatal_mice.json",
      "role": "data",
      "note": "PDF metadata for neonatal mice brain isolation paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Mitochondria_isolated_from_lipid_droplets_of_white_adipose_tissue_reveal_functional_differences.json",
      "role": "data",
      "note": "PDF metadata for adipose lipid droplet isolation paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Rapid_isolation_of_respiring_skeletal_muscle_mitochondria_using_nitrogen_cavitation.json",
      "role": "data",
      "note": "PDF metadata for nitrogen cavitation isolation paper"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content30.txt",
      "role": "data",
      "note": "Batch 30 standardized protocol summaries from literature"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content70.txt",
      "role": "data",
      "note": "Batch 70 standardized protocol summaries from literature"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_high-yield_preparative_method_for_isolation_of_rat_liver_mitochondria.json",
      "role": "data",
      "note": "AI-extracted structured data from rat liver isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_novel,_simple_and_rapid_method_for_the_isolation_of_mitochondria_which_exhibit_respiratory_co.json",
      "role": "data",
      "note": "AI-extracted structured data from novel rapid isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Affordable_de_novo_generation_of_fish_mitogenomes_using_amplification-free_enrichment_of_mitoch.json",
      "role": "data",
      "note": "AI-extracted structured data from fish mitogenome paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/An_improved_technique_for_the_isolation_of_mitochondria_from_plant_tissue.json",
      "role": "data",
      "note": "AI-extracted structured data from plant tissue isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Delivery_of_mitochondria_confers_cardioprotection_through_mitochondria_replenishment_and_metabo.json",
      "role": "data",
      "note": "AI-extracted structured data from cardioprotection delivery paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_Characterization_of_Concanavalin_A-labeled_Plasma_Membranes_of_Carrot_Protoplasts.json",
      "role": "data",
      "note": "AI-extracted structured data from carrot protoplast paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_Respiratory_Measurements_of_Mitochondria_from_Arabidopsis_thaliana.json",
      "role": "data",
      "note": "AI-extracted structured data from Arabidopsis isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_functional_analysis_of_mitochondria_from_cultured_cells_and_mouse_tissue.json",
      "role": "data",
      "note": "AI-extracted structured data from cultured cells isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_Intact_Mitochondria_from_Skeletal_Muscle_by_Differential_Centrifugation_for_High-r.json",
      "role": "data",
      "note": "AI-extracted structured data from skeletal muscle isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_Mitochondria_from_Ustilago_maydis_Protoplasts.json",
      "role": "data",
      "note": "AI-extracted structured data from Ustilago maydis paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_functional_pure_mitochondria_by_superparamagnetic_microbeads.json",
      "role": "data",
      "note": "AI-extracted structured data from magnetic bead isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_by_gentle_cell_membrane_disruption,_and_their_subsequent_characteriza.json",
      "role": "data",
      "note": "AI-extracted structured data from gentle disruption paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_cultured_cells_and_liver_tissue_biopsies_for_molecular_and_bioch.json",
      "role": "data",
      "note": "AI-extracted structured data from liver biopsy isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_with_high_respiratory_control_from_primary_cultures_of_neurons_and_as.json",
      "role": "data",
      "note": "AI-extracted structured data from neuron/astrocyte isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Measurement_of_mitochondrial_respiratory_chain_enzymatic_activities_in_Drosophila_melanogaster_.json",
      "role": "data",
      "note": "AI-extracted structured data from Drosophila respiratory chain paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mitochondrial_Isolation_and_Purification_from_Mouse_Spinal_Cord.json",
      "role": "data",
      "note": "AI-extracted structured data from mouse spinal cord paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mitochondrial_structure_and_function_are_disrupted_by_standard_isolation_methods.json",
      "role": "data",
      "note": "AI-extracted structured data from isolation artifact critique paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Optimization_of_preparation_of_mitochondria_from_25-100_mg_skeletal_muscle.json",
      "role": "data",
      "note": "AI-extracted structured data from small skeletal muscle prep paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Preservation_of_mitochondrial_functional_integrity_in_mitochondria_isolated_from_small_cryopres.json",
      "role": "data",
      "note": "AI-extracted structured data from cryopreservation integrity paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Purification_of_functional_mouse_skeletal_muscle_mitochondria_using_percoll_density_gradient_ce(1).json",
      "role": "data",
      "note": "AI-extracted structured data from Percoll gradient purification paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Rapid_isolation_and_purification_of_mitochondria_for_transplantation_by_tissue_dissociation_and.json",
      "role": "data",
      "note": "AI-extracted structured data from transplantation isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Scalable_Isolation_of_Mammalian_Mitochondria_for_Nucleic_Acid_and_Nucleoid_Analysis.json",
      "role": "data",
      "note": "AI-extracted structured data from scalable mammalian isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Tightly_coupled_mitochondria_from_human_early_placenta.json",
      "role": "data",
      "note": "AI-extracted structured data from human placenta isolation paper"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_20.docx",
      "role": "doc",
      "note": "Cross-paper pattern synthesis batch 20"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_60-2.docx",
      "role": "doc",
      "note": "Cross-paper pattern synthesis batch 60 revision 2"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_80-2.docx",
      "role": "doc",
      "note": "Cross-paper pattern synthesis batch 80 revision 2"
    },
    {
      "path": "07_Lab_Manual/Mitochondrial_Isolation_Report.pdf",
      "role": "doc",
      "note": "32-page bench-ready mitochondrial isolation manual"
    },
    {
      "path": "09_Computational_Modeling/Synth3a/Syn3A_Research_Notes_RemNote.md",
      "role": "doc",
      "note": "RemNote export of Syn3A whole-cell modeling research notes"
    },
    {
      "path": "09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_2005_params.csv",
      "role": "data",
      "note": "Beard 2005 ODE model parameters for mitochondrial energetics"
    },
    {
      "path": "09_Computational_Modeling/composite_utils.py",
      "role": "source",
      "note": "Shared FBA+ODE coupling utilities imported by composite experiments"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_FINDINGS_2026-05-09.md",
      "role": "doc",
      "note": "DocInsight tool findings for conference submission audit"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_VERIFICATION_AUDIT_2026-05-10.md",
      "role": "doc",
      "note": "Verification audit of DocInsight pipeline findings"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/qbio_conference_analysis_2026-04-21.md",
      "role": "doc",
      "note": "q-bio Chicago 2026 conference details and submission strategy"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/AUDIT_2026-04-23.md",
      "role": "doc",
      "note": "Living audit document for computational pipeline claims"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/FRAMING_2026-04-23.md",
      "role": "doc",
      "note": "Corrected framing of model output vs biological reality"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/PHASE_G_SYNTHESIS.md",
      "role": "doc",
      "note": "Phase G validation test synthesis and open-item resolution"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/WHY_29_HOURS.md",
      "role": "doc",
      "note": "Investigation into 29-hour baseline transit window finding"
    },
    {
      "path": "09_Computational_Modeling/requirements.txt",
      "role": "config",
      "note": "Pinned Python dependency list for the computational pipeline"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/experiment1b_summary.json",
      "role": "generated",
      "note": "Archived v1 experiment 1b simulation summary output"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/halflife_sweep_figure.png",
      "role": "generated",
      "note": "Archived half-life sweep parameter sensitivity figure"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex10_mptp_scenarios.csv",
      "role": "generated",
      "note": "Ex 10 MPTP scenario comparison simulation results"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_1_baseline_validation.csv",
      "role": "generated",
      "note": "Ex 5.1 composite baseline validation simulation results"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_2_reaction_mapping.md",
      "role": "generated",
      "note": "Auto-generated FBA-to-ODE reaction mapping audit table"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_5_intervention_composite.csv",
      "role": "generated",
      "note": "Ex 5.5 composite intervention re-prediction results"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex6_option_b_membrane.csv",
      "role": "generated",
      "note": "Ex 6 option-B membrane model simulation results"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex9_atp_first_diagnostic.png",
      "role": "generated",
      "note": "Ex 9 ATP-first failure mode diagnostic plot"
    },
    {
      "path": "09_Computational_Modeling/results/experiments_v2/experiment1_v2_summary.json",
      "role": "generated",
      "note": "Experiment 1 v2 transit window simulation summary"
    },
    {
      "path": "09_Computational_Modeling/results/experiments_v2/experiment1d_summary.json",
      "role": "generated",
      "note": "Experiment 1d simulation variant summary output"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/essential_genes_annotated.csv",
      "role": "generated",
      "note": "145 essential genes with functional cluster annotations"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/gene_knockout_scores_v2.csv",
      "role": "generated",
      "note": "Phase B gene knockout leverage scores version 2"
    },
    {
      "path": "09_Computational_Modeling/results/phase_d/phase_d_adversarial_results.json",
      "role": "generated",
      "note": "Phase D adversarial model stress-test results"
    },
    {
      "path": "09_Computational_Modeling/results/phase_g/g1_order_stats_vs_fba.csv",
      "role": "generated",
      "note": "Order-statistics vs FBA transit window comparison results"
    },
    {
      "path": "09_Computational_Modeling/results/phase_h/ci_correlation_analysis.json",
      "role": "generated",
      "note": "CI subunit pairwise correlation and permutation test results"
    },
    {
      "path": "09_Computational_Modeling/results/phase_i/category_overlap_fisher.json",
      "role": "generated",
      "note": "Fisher test results for gene category overlap"
    },
    {
      "path": "09_Computational_Modeling/results/phase_j/intervention_bar_chart.png",
      "role": "generated",
      "note": "Bar chart of intervention mechanism modeling results"
    },
    {
      "path": "09_Computational_Modeling/results/phase_k/wet_lab_overlay.png",
      "role": "generated",
      "note": "Computational predictions overlaid on wet lab JC-1 data"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/README.md",
      "role": "doc",
      "note": "Overview, entry points, and kill criteria for composite experiments"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment5b_interventions.py",
      "role": "source",
      "note": "Runs three interventions through composite FBA+ODE model"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py",
      "role": "source",
      "note": "Generates 2-panel abstract figure with MPTP and MitoQ data"
    },
    {
      "path": "09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py",
      "role": "source",
      "note": "Empirical half-life transit window experiment with bootstrap CI"
    },
    {
      "path": "09_Computational_Modeling/scripts/experiments_v2/experiment4_interventions.py",
      "role": "source",
      "note": "Three-intervention mechanism modeling with bootstrap CI"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py",
      "role": "source",
      "note": "Gene clustering and full immortalization sweep over 145 genes"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_g1_order_statistics.py",
      "role": "source",
      "note": "Order-statistics test comparing analytic vs FBA transit window"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_h_ci_subunit_analysis.py",
      "role": "source",
      "note": "Phase H Complex I subunit deep-dive correlation analysis"
    },
    {
      "path": "10_Research_Questions/Research_Questions.md",
      "role": "doc",
      "note": "Ten core research questions with literature and status tracking"
    },
    {
      "path": "INDEX.md",
      "role": "doc",
      "note": "Project navigation index with folder-level descriptions"
    },
    {
      "path": ".gitmodules",
      "role": "config",
      "note": "Declares Human-GEM and mitomammal git submodules"
    },
    {
      "path": "01_Vision_and_Strategy/Layer_1_Scope_Reframe_2026-04-23.md",
      "role": "doc",
      "note": "Strategic scope reframe document dated 2026-04-23"
    },
    {
      "path": "01_Vision_and_Strategy/Research_Hypotheses.docx",
      "role": "doc",
      "note": "Research hypotheses for mitochondria viability project"
    },
    {
      "path": "02_Methodology/Literature_Mapping.docx",
      "role": "doc",
      "note": "Literature mapping methodology document"
    },
    {
      "path": "04_Source_Literature/Mitochondrial_Transfer/Artificial Mitochondria Transfer_ Current Challenges, Advances, and Future Applications.docx",
      "role": "doc",
      "note": "Source paper on artificial mitochondrial transfer methods"
    },
    {
      "path": "04_Source_Literature/Mitochondrial_Transfer/Mitochondrial phenotypes in purified human immune cell subtypes and cell mixtures.docx",
      "role": "doc",
      "note": "Source paper on mitochondrial phenotypes in immune cells"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation and bioenergetic characterization of mitochondria from Pichia pastoris.txt",
      "role": "data",
      "note": "Extracted PDF metadata; identical duplicate of underscore-named file"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_and_bioenergetic_characterization_of_mitochondria_from_Pichia_pastoris.txt",
      "role": "data",
      "note": "Extracted PDF metadata; identical duplicate of space-named file"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.txt",
      "role": "data",
      "note": "Extracted PDF metadata for mouse lung mitochondria isolation paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_of_functionally_active_and_highly_purified_neuronal_mitochondria_from_human_cortex.json",
      "role": "data",
      "note": "Extracted PDF metadata in JSON for neuronal mitochondria paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Mitochondria_isolated_from_lipid_droplets_of_white_adipose_tissue_reveal_functional_differences.txt",
      "role": "data",
      "note": "Extracted PDF metadata for adipose mitochondria paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Rapid_isolation_of_respiring_skeletal_muscle_mitochondria_using_nitrogen_cavitation.txt",
      "role": "data",
      "note": "Extracted PDF metadata for skeletal muscle isolation paper"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content40.txt",
      "role": "generated",
      "note": "Batch-concatenated protocol summaries from multiple papers"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content80.txt",
      "role": "generated",
      "note": "Batch-concatenated protocol summaries from multiple papers"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_method_for_isolating_intact_mitochondria_and_nuclei_from_the_same_homogenate,_and_the_influen.json",
      "role": "data",
      "note": "Structured extracted data from mitochondria/nuclei co-isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_rapid_method_for_the_isolation_of_intact_mitochondria_from_isolated_rat_liver_cells.json",
      "role": "data",
      "note": "Structured extracted data from rat liver mitochondria isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/An_Improved_Method_for_Preparation_of_Uniform_and_Functional_Mitochondria_from_Fresh_Liver.json",
      "role": "data",
      "note": "Structured extracted data from improved liver mitochondria prep paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Assay_of_succinate_dehydrogenase_activity_by_the_tetrazolium_method_evaluation_of_an_improved_t.json",
      "role": "data",
      "note": "Structured extracted data from succinate dehydrogenase assay paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Efficient_isolation_of_pure_and_functional_mitochondria_from_mouse_tissues_using_automated_tiss.json",
      "role": "data",
      "note": "Structured extracted data from automated mouse tissue isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_Electron_Microscopic_Analysis_of_Liver_Cancer_Cell_Mitochondria.json",
      "role": "data",
      "note": "Structured extracted data from liver cancer mitochondria EM paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_Structural_Studies_of_Mitochondria_from_Pea_Roots.json",
      "role": "data",
      "note": "Structured extracted data from pea root mitochondria isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_functional_assessment_of_mitochondria_from_small_amounts_of_mouse_brain_tissue.json",
      "role": "data",
      "note": "Structured extracted data from mouse brain mitochondria isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_Large_Amounts_of_Highly_Pure_Mitochondria_for_Omics_Studies.json",
      "role": "data",
      "note": "Structured extracted data from large-scale mitochondria isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_Physiologically_Active_and_Intact_Mitochondria_from_Chickpea.json",
      "role": "data",
      "note": "Structured extracted data from chickpea mitochondria isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_functionally_active_and_highly_purified_neuronal_mitochondria_from_human_cortex.json",
      "role": "data",
      "note": "Structured extracted data from human cortex neuronal mitochondria paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_for_biogenetical_studies_An_update.json",
      "role": "data",
      "note": "Structured extracted data from mitochondria biogenesis isolation update"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_procyclic_Trypanosoma_brucei.json",
      "role": "data",
      "note": "Structured extracted data from Trypanosoma brucei mitochondria paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondrial_subpopulations_from_skeletal_muscle_Optimizing_recovery_and_preservi.json",
      "role": "data",
      "note": "Structured extracted data from skeletal muscle subpopulation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mitochondria_and_peroxisomes_from_the_cellular_slime_mould_Dictyostelium_discoideum._Isolation_.json",
      "role": "data",
      "note": "Structured extracted data from Dictyostelium organelle isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mitochondrial_Isolation_and_Real-Time_Monitoring_of_MOMP.json",
      "role": "data",
      "note": "Structured extracted data from MOMP monitoring isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mouse_Liver_Mitochondria_Isolation,_Size_Fractionation,_and_Real-time_MOMP_Measurement.json",
      "role": "data",
      "note": "Structured extracted data from mouse liver MOMP measurement paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Organelle_isolation_functional_mitochondria_from_mouse_liver,_muscle_and_cultured_fibroblasts.json",
      "role": "data",
      "note": "Structured extracted data from multi-tissue organelle isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Protocol_for_mitochondrial_isolation_and_sub-cellular_localization_assay_for_mitochondrial_prot.json",
      "role": "data",
      "note": "Structured extracted data from mitochondrial localization assay paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Purity_matters_A_workflow_for_the_valid_high-resolution_lipid_profiling_of_mitochondria_from_ce.json",
      "role": "data",
      "note": "Structured extracted data from mitochondrial lipid profiling paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Rapid_isolation_of_metabolically_active_mitochondria_from_rat_brain_and_subregions_using_Percol.json",
      "role": "data",
      "note": "Structured extracted data from rat brain Percoll isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Simultaneous_isolation_of_pure_and_intact_chloroplasts_and_mitochondria_from_moss_as_the_basis_.json",
      "role": "data",
      "note": "Structured extracted data from moss organelle co-isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Two-Step_Tag-Free_Isolation_of_Mitochondria_for_Improved_Protein_Discovery_and_Quantification.json",
      "role": "data",
      "note": "Structured extracted data from tag-free mitochondria proteomics paper"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_40.docx",
      "role": "generated",
      "note": "Batch-combined comparative analysis synthesis document"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_70-1.docx",
      "role": "generated",
      "note": "Batch-combined comparative analysis synthesis document"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_90-3.docx",
      "role": "generated",
      "note": "Batch-combined comparative analysis synthesis document"
    },
    {
      "path": "08_Experimental_Work/Experiments_Overview.md",
      "role": "doc",
      "note": "Overview document for experimental work planning"
    },
    {
      "path": "09_Computational_Modeling/Whole_Cell_Modeling/Human-GEM",
      "role": "submodule",
      "note": "SysBioChalmers Human-GEM genome-scale metabolic model submodule"
    },
    {
      "path": "09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py",
      "role": "source",
      "note": "Beard QAMAS in vitro ODE model; runs at module level without main guard"
    },
    {
      "path": "09_Computational_Modeling/decay_utils.py",
      "role": "source",
      "note": "Shared utility: GPR-aware FBA decay; imported by all experiment scripts"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_FOLLOWUP_PLAN_2026-05-09.md",
      "role": "doc",
      "note": "Operational plan for DocInsight literature follow-up actions"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/Modeling_Overview.md",
      "role": "doc",
      "note": "Overview document for computational modeling approach"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/syn3a_notes_analysis_2026-04-21.md",
      "role": "doc",
      "note": "Analysis notes on Syn3A minimal cell crosswalk"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/CI_SUBUNIT_DEEP_DIVE.md",
      "role": "doc",
      "note": "Investigation notes on Complex I subunit analysis"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/INTERVENTION_MECHANISMS.md",
      "role": "doc",
      "note": "Investigation notes on intervention mechanism candidates"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/SYN3A_CROSSWALK.md",
      "role": "doc",
      "note": "Investigation notes on Syn3A vs mitochondria crosswalk"
    },
    {
      "path": "09_Computational_Modeling/docs/strategy/LAYER_1_COMPUTATIONAL_PATH_2026-04-23.md",
      "role": "doc",
      "note": "Strategic computational path document dated 2026-04-23"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/complex_sensitivity.csv",
      "role": "data",
      "note": "Archived v1 complex sensitivity analysis results"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/gene_knockout_scores.csv",
      "role": "data",
      "note": "Archived v1 gene knockout impact scores"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/sensitivity_figure.png",
      "role": "asset",
      "note": "Archived v1 sensitivity analysis figure"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex10_mptp_traces.png",
      "role": "asset",
      "note": "Experiment 10 MPTP scenario trace figure"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_1_reference_validation.png",
      "role": "asset",
      "note": "Experiment 5.1 reference validation figure"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_3_scenario_tw.csv",
      "role": "data",
      "note": "Experiment 5.3 scenario transit window results"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_6_sensitivity.csv",
      "role": "data",
      "note": "Experiment 5.6 literature-sourced sensitivity results"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex6_option_b_traces.png",
      "role": "asset",
      "note": "Experiment 6 option-B extension trace figure"
    },
    {
      "path": "09_Computational_Modeling/results/composite/final_abstract_figure_composite.png",
      "role": "asset",
      "note": "Final composite figure for abstract submission"
    },
    {
      "path": "09_Computational_Modeling/results/experiments_v2/experiment1c_v2_halflife_sweep.png",
      "role": "asset",
      "note": "Experiment 1c v2 half-life sweep figure"
    },
    {
      "path": "09_Computational_Modeling/results/phase_a/baseline_solution.csv",
      "role": "data",
      "note": "Phase A baseline FBA solution data"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/essential_genes_clustered.csv",
      "role": "data",
      "note": "Phase B essential genes with clustering assignments"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/phase_b_summary.json",
      "role": "data",
      "note": "Phase B summary statistics and results JSON"
    },
    {
      "path": "09_Computational_Modeling/results/phase_e/chapman_table_parsed.csv",
      "role": "data",
      "note": "Phase E parsed Chapman literature table data"
    },
    {
      "path": "09_Computational_Modeling/results/phase_g/g2_human_gem_inspection.json",
      "role": "data",
      "note": "Phase G Human-GEM cross-model inspection results"
    },
    {
      "path": "09_Computational_Modeling/results/phase_h/ci_subunit_data.csv",
      "role": "data",
      "note": "Phase H Complex I subunit analysis data"
    },
    {
      "path": "09_Computational_Modeling/results/phase_i/syn3a_crosswalk_3rxns.csv",
      "role": "data",
      "note": "Phase I Syn3A three-reaction crosswalk comparison data"
    },
    {
      "path": "09_Computational_Modeling/results/phase_j/intervention_delta_tw.csv",
      "role": "data",
      "note": "Phase J intervention delta transit-window results"
    },
    {
      "path": "09_Computational_Modeling/scripts/archive_v1/experiment1_transit_window.py",
      "role": "source",
      "note": "Archived v1 transit window FBA script; has __main__ entry"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment10_mptp_composite.py",
      "role": "source",
      "note": "MPTP composite experiment testing Ca2+ scenario partition"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment5c_sensitivity.py",
      "role": "source",
      "note": "Literature-sourced sensitivity propagation experiment"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment9_atp_first_diagnostic.py",
      "role": "source",
      "note": "ATP-first paradox diagnostic partitioning three hypotheses"
    },
    {
      "path": "09_Computational_Modeling/scripts/experiments_v2/experiment1b_v2_gpr_knockout.py",
      "role": "source",
      "note": "GPR-aware gene knockout scoring correcting v1 OR-rule bug"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_a_dissection.py",
      "role": "source",
      "note": "MitoMAMMAL mechanistic dissection A.1–A.5 runs"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_c_forensic_29h.py",
      "role": "source",
      "note": "Forensic dissection of 29-hour transit window result"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_g2_cross_model.py",
      "role": "source",
      "note": "Cross-model validation using Human-GEM mitochondrial subset"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_i_syn3a_crosswalk.py",
      "role": "source",
      "note": "Syn3A vs mitochondria 3-reaction transport comparison"
    },
    {
      "path": "Archive/Old-Unneeded/Mitochondrial_Autonomy_Techniques_and_Insights.docx",
      "role": "dead",
      "note": "Archived unused document in Old-Unneeded folder"
    },
    {
      "path": "Mitochondrial Research and Aging: Innovations, Questions, and Strategies.md",
      "role": "doc",
      "note": "Root-level research overview on mitochondria aging strategies"
    },
    {
      "path": "01_Vision_and_Strategy/Executive_Summary_2026-04-21.md",
      "role": "doc",
      "note": "Project executive summary dated April 2026"
    },
    {
      "path": "01_Vision_and_Strategy/Notebook_Transcription_Otter.txt",
      "role": "data",
      "note": "Otter.ai audio transcription of planning notebook session"
    },
    {
      "path": "01_Vision_and_Strategy/Strategy_Critique_and_Assumptions_2026-04-21.md",
      "role": "doc",
      "note": "Critical review of strategy assumptions April 2026"
    },
    {
      "path": "02_Methodology/Paper_Ranking_Framework.docx",
      "role": "doc",
      "note": "Framework for ranking source literature papers by quality"
    },
    {
      "path": "04_Source_Literature/Mitochondrial_Transfer/Characterization and origins of cell-free mitochondria in healthy murine and human blood.docx",
      "role": "data",
      "note": "Imported copy of source literature paper on cell-free mito"
    },
    {
      "path": "04_Source_Literature/Mitochondrial_Transfer/Mitochondrial transfer_transplantation_ an emerging therapeutic approach for multiple diseases.docx",
      "role": "data",
      "note": "Imported copy of source literature therapeutic review paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_and_Respiratory_Measurements_of_Mitochondria_from_Arabidopsis_thaliana.json",
      "role": "data",
      "note": "PDF metadata extracted from Arabidopsis respiratory paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_and_reconstruction_of_cardiac_mitochondria_from_SBEM_images_using_a_deep_learning-bas.json",
      "role": "data",
      "note": "PDF metadata extracted from cardiac SBEM deep-learning paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_from_Ustilago_maydis_Protoplasts.json",
      "role": "data",
      "note": "PDF metadata extracted from fungal protoplast isolation paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_of_intact,_functional_mitochondria_from_the_model_plant_Arabidopsis_thaliana.json",
      "role": "data",
      "note": "PDF metadata extracted from Arabidopsis functional mito paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Organelle_isolation_functional_mitochondria_from_mouse_liver,_muscle_and_cultured_fibroblasts.json",
      "role": "data",
      "note": "PDF metadata extracted from multi-tissue mouse isolation paper"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content10.txt",
      "role": "data",
      "note": "Aggregated protocol text content batch 10"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content50.txt",
      "role": "data",
      "note": "Aggregated protocol text content batch 50"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content_over_80.txt",
      "role": "data",
      "note": "Aggregated protocol text content batch 80-plus"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_microcalorimetric_study_of_the_effect_of_La3+_on_mitochondria_isolated_from_Star-Cross_288_ch.json",
      "role": "data",
      "note": "Structured JSON extraction of microcalorimetry paper data"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_semi-automated_method_for_isolating_functionally_intact_mitochondria_from_cultured_cells_and_.json",
      "role": "data",
      "note": "Structured JSON extraction of semi-automated isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/An_Update_on_Isolation_of_Functional_Mitochondria_from_Cells_for_Bioenergetics_Studies.json",
      "role": "data",
      "note": "Structured JSON extraction of bioenergetics isolation update paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Characterization_of_growth_plate_mitochondria.json",
      "role": "data",
      "note": "Structured JSON extraction of growth plate mitochondria paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Genome-wide_analysis_of_RNA_extracted_from_isolated_mitochondria.json",
      "role": "data",
      "note": "Structured JSON extraction of genome-wide RNA analysis paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_Metabolic_Assessment_of_Cancer_Cell_Mitochondria.json",
      "role": "data",
      "note": "Structured JSON extraction of cancer cell mito assessment paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_bioenergetic_characterization_of_mitochondria_from_Pichia_pastoris.json",
      "role": "data",
      "note": "Structured JSON extraction of yeast Pichia bioenergetics paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_quality_control_of_functional_mitochondria.json",
      "role": "data",
      "note": "Structured JSON extraction of mito QC isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_Mitochondria_From_Fresh_Mice_Lung_Tissue.json",
      "role": "data",
      "note": "Structured JSON extraction of mouse lung mito isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_brain_mitochondria_from_neonatal_mice.json",
      "role": "data",
      "note": "Structured JSON extraction of neonatal mouse brain mito paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_intact,_functional_mitochondria_from_the_model_plant_Arabidopsis_thaliana.json",
      "role": "data",
      "note": "Structured JSON extraction of Arabidopsis intact mito paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_animal_tissue.json",
      "role": "data",
      "note": "Structured JSON extraction of animal tissue isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_the_CNS.json",
      "role": "data",
      "note": "Structured JSON extraction of CNS mito isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_rat_adrenocortical_mitochondria.json",
      "role": "data",
      "note": "Structured JSON extraction of rat adrenocortical mito paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mitochondria_from_the_hepatopancreas_of_the_marine_clam_Mercenaria_mercenaria_substrate_prefere.json",
      "role": "data",
      "note": "Structured JSON extraction of marine clam hepatopancreas paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mitochondrial_Respiration_of_Platelets_Comparison_of_Isolation_Methods.json",
      "role": "data",
      "note": "Structured JSON extraction of platelet respiration isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Optimal_isolation_of_mitochondria_for_proteomic_analyses.json",
      "role": "data",
      "note": "Structured JSON extraction of proteomics isolation paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Preparation_of_highly_coupled_rat_heart_mitochondria.json",
      "role": "data",
      "note": "Structured JSON extraction of rat heart coupled mito paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Purification_of_Functional_Platelet_Mitochondria_Using_a_Discontinuous_Percoll_Gradient.json",
      "role": "data",
      "note": "Structured JSON extraction of Percoll platelet mito paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Qualitative_Characterization_of_the_Rat_Liver_Mitochondrial_Lipidome_Using_All_Ion_Fragmentatio.json",
      "role": "data",
      "note": "Structured JSON extraction of rat liver lipidome paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Rapid_isolation_of_respiring_skeletal_muscle_mitochondria_using_nitrogen_cavitation.json",
      "role": "data",
      "note": "Structured JSON extraction of nitrogen cavitation muscle paper"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/The_isolation_and_properties_of_mitochondria_from_rat_pancreas.json",
      "role": "data",
      "note": "Structured JSON extraction of rat pancreas mito paper"
    },
    {
      "path": "06_Synthesis/Annotated_Bibliography.docx",
      "role": "doc",
      "note": "Annotated bibliography of curated source literature"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_50.docx",
      "role": "doc",
      "note": "Comparative analysis synthesis document chunk 50"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_70-2.docx",
      "role": "doc",
      "note": "Comparative analysis synthesis document chunk 70-2"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_content_30.docx",
      "role": "doc",
      "note": "Combined content synthesis document chunk 30"
    },
    {
      "path": "09_Computational_Modeling/LAB_NOTEBOOK.md",
      "role": "doc",
      "note": "Lab notebook logging computational modeling sessions"
    },
    {
      "path": "09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/README.md",
      "role": "doc",
      "note": "README for Beard lab whole-cell model subdirectory"
    },
    {
      "path": "09_Computational_Modeling/Whole_Cell_Modeling/cortassa/README.md",
      "role": "doc",
      "note": "README for Cortassa model subdirectory"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/ABSTRACT_DRAFT_2026-04-23.md",
      "role": "doc",
      "note": "Draft conference abstract April 2026"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_MITO_QUERY_GUIDE.md",
      "role": "doc",
      "note": "Guide for querying DocInsight mito literature tool"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/qbio_analysis_2026-04-21.md",
      "role": "doc",
      "note": "qBio conference analysis and planning notes"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/ANOMALIES_AND_HIDDEN_FINDINGS.md",
      "role": "doc",
      "note": "Documented anomalies and unexpected model findings"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/COMPOSITE_AUDIT_2026-04-24.md",
      "role": "doc",
      "note": "Audit trail for composite FBA+ODE model experiments"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/INVESTIGATION_SYNTHESIS_2026-04-23.md",
      "role": "doc",
      "note": "Synthesis of multi-phase investigation results April 2026"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/TIMELINE_NOTE.md",
      "role": "doc",
      "note": "Short timeline note for investigation chronology context"
    },
    {
      "path": "09_Computational_Modeling/ode_utils.py",
      "role": "source",
      "note": "Shared ODE integration library for Beard 2005 OXPHOS model"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/decay_curves.png",
      "role": "generated",
      "note": "Archive v1 decay curve plot output"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/halflife_sweep.csv",
      "role": "generated",
      "note": "Archive v1 half-life sweep simulation results"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/transit_window_results.csv",
      "role": "generated",
      "note": "Archive v1 transit window computation results"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex11_ros_mitoq.csv",
      "role": "generated",
      "note": "Experiment 11 ROS MitoQ simulation output CSV"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_2_coupling_dynamics.csv",
      "role": "generated",
      "note": "Experiment 5.2 coupling dynamics simulation output"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_4_mechanism_partition.csv",
      "role": "generated",
      "note": "Experiment 5.4 mechanism partition simulation output"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_6_sensitivity_tornado.png",
      "role": "generated",
      "note": "Experiment 5.6 sensitivity tornado chart output"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex7_human_gem_composite.csv",
      "role": "generated",
      "note": "Experiment 7 Human-GEM composite simulation output"
    },
    {
      "path": "09_Computational_Modeling/results/experiments_v2/experiment1_v2_decay_curves.png",
      "role": "generated",
      "note": "Experiment 1 v2 decay curve plot output"
    },
    {
      "path": "09_Computational_Modeling/results/experiments_v2/experiment1c_v2_summary.json",
      "role": "generated",
      "note": "Experiment 1c v2 half-life sweep summary JSON output"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/deep_dive_profiles.json",
      "role": "generated",
      "note": "Phase B essential gene deep dive profile data"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/essential_genes_mitocarta_crossref.csv",
      "role": "generated",
      "note": "Phase B essential genes MitoCarta cross-reference output"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/single_gene_leverage.csv",
      "role": "generated",
      "note": "Phase B single-gene leverage score rankings"
    },
    {
      "path": "09_Computational_Modeling/results/phase_e/fva_baseline.csv",
      "role": "generated",
      "note": "Phase E FVA baseline flux variability analysis output"
    },
    {
      "path": "09_Computational_Modeling/results/phase_g/g2b_human_gem_uniform_decay.json",
      "role": "generated",
      "note": "Phase G2b Human-GEM uniform decay claim test output"
    },
    {
      "path": "09_Computational_Modeling/results/phase_h/decay_curves_empirical.png",
      "role": "generated",
      "note": "Phase H empirical overlay decay curve plot"
    },
    {
      "path": "09_Computational_Modeling/results/phase_j/final_abstract_figure.png",
      "role": "generated",
      "note": "Phase J final conference abstract figure output"
    },
    {
      "path": "09_Computational_Modeling/results/phase_j/intervention_mechanisms.csv",
      "role": "generated",
      "note": "Phase J intervention mechanism simulation output"
    },
    {
      "path": "09_Computational_Modeling/scripts/archive_v1/experiment1b_gene_sensitivity.py",
      "role": "source",
      "note": "Archived v1 gene sensitivity and engineering target ranking"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment11_ros_mitoq.py",
      "role": "source",
      "note": "ROS module with MitoQ as mechanistic scavenger experiment"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment6_option_b_extension.py",
      "role": "source",
      "note": "Membrane integrity non-proteomic failure mode experiment"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/validate_against_beard.py",
      "role": "source",
      "note": "Beard 2005 baseline PO-curve reproduction validation script"
    },
    {
      "path": "09_Computational_Modeling/scripts/experiments_v2/experiment1c_v2_halflife_sweep.py",
      "role": "source",
      "note": "Half-life sweep v2 with GPR-aware decay and dual objective"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_b6_deep_dive.py",
      "role": "source",
      "note": "Phase B.6 deep dive profiling 10 selected essential genes"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_d_adversarial_suite.py",
      "role": "source",
      "note": "Phase D adversarial perturbation and trust-framework suite"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_g2b_human_gem_decay.py",
      "role": "source",
      "note": "Phase G.2b Human-GEM algebraic decay claim cross-check"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py",
      "role": "source",
      "note": "Phase K overlay predicted decay vs 2024 wet-lab yeast data"
    },
    {
      "path": "Archive/SYN3a_NOTES_RemNoteExport_Knowledge-Database_md_2026-04-21_12-55.zip",
      "role": "data",
      "note": "Archived RemNote knowledge base export zip April 2026"
    },
    {
      "path": "README.md",
      "role": "doc",
      "note": "Top-level project README"
    },
    {
      "path": "01_Vision_and_Strategy/Exploratory_Landscape.docx",
      "role": "doc",
      "note": "Vision/strategy landscape exploration document (binary Word format)"
    },
    {
      "path": "01_Vision_and_Strategy/Programmable_Mitochondria_Vision_2026-04-21.md",
      "role": "doc",
      "note": "Project vision: programmable mitochondria as engineerable vectors"
    },
    {
      "path": "02_Methodology/BSHR_Loop.txt",
      "role": "doc",
      "note": "Methodology guide: Brainstorm-Search-Hypothesize-Refine LLM loop"
    },
    {
      "path": "03_Study_Registry/references.ris",
      "role": "data",
      "note": "Bibliography in RIS format for study registry citations"
    },
    {
      "path": "04_Source_Literature/Mitochondrial_Transfer/Isolation of Mitochondria from Saccharomyces cerevisiae.docx",
      "role": "doc",
      "note": "Source paper: yeast mitochondria isolation protocol (Word format)"
    },
    {
      "path": "04_Source_Literature/Mitochondrial_Transfer/The Functions, Methods, and Mobility of Mitochondrial Transfer Between Cells.docx",
      "role": "doc",
      "note": "Source paper: mitochondrial transfer methods review (Word format)"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_and_Respiratory_Measurements_of_Mitochondria_from_Arabidopsis_thaliana.txt",
      "role": "data",
      "note": "Extracted PDF metadata from Arabidopsis mitochondria isolation paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_and_reconstruction_of_cardiac_mitochondria_from_SBEM_images_using_a_deep_learning-bas.txt",
      "role": "data",
      "note": "Extracted PDF metadata for cardiac SBEM mitochondria paper"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_of_Mitochondria_from_Ustilago_maydis_Protoplasts.txt",
      "role": "data",
      "note": "Extracted PDF metadata for U. maydis mitochondria isolation"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Isolation_of_intact,_functional_mitochondria_from_the_model_plant_Arabidopsis_thaliana.txt",
      "role": "data",
      "note": "Extracted PDF metadata: intact functional mitochondria from Arabidopsis"
    },
    {
      "path": "05_Extracted_Data/PDF_Metadata/Organelle_isolation_functional_mitochondria_from_mouse_liver,_muscle_and_cultured_fibroblasts.txt",
      "role": "data",
      "note": "Extracted PDF metadata: mouse liver/muscle organelle isolation paper"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content20.txt",
      "role": "data",
      "note": "Combined protocol content batch 20 from source literature"
    },
    {
      "path": "05_Extracted_Data/Protocol_Summaries/combined_content60.txt",
      "role": "data",
      "note": "Combined protocol content batch 60 from source literature"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_critical_comparison_between_two_classical_and_a_kit-based_method_for_mitochondria_isolation.json",
      "role": "data",
      "note": "Structured extraction: classical vs kit-based mitochondria isolation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_mitosome_purification_protocol_based_on_percoll_density_gradients_and_its_use_in_validating_t.json",
      "role": "data",
      "note": "Structured extraction: mitosome Percoll purification protocol"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/A_simplified_method_to_isolate_rice_mitochondria.json",
      "role": "data",
      "note": "Structured extraction: rice mitochondria isolation protocol"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/An_improved_method_with_a_wider_applicability_to_isolate_plant_mitochondria_for_mtDNA_extractio.json",
      "role": "data",
      "note": "Structured extraction: plant mitochondria isolation for mtDNA"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Comparison_of_three_methods_for_mitochondria_isolation_from_the_human_liver_cell_line_(HepG2).json",
      "role": "data",
      "note": "Structured extraction: three isolation methods compared for HepG2"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Improved_method_for_isolation_of_mitochondria_from_chick_breast_muscle_using_Nagarse.json",
      "role": "data",
      "note": "Structured extraction: Nagarse-based chick muscle isolation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_Purification_of_Mitochondria_from_Cell_Culture_for_Proteomic_Analyses.json",
      "role": "data",
      "note": "Structured extraction: cell culture mitochondria for proteomics"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_comparative_proteomic_analysis_of_mitochondria_from_the_pulp_of_ripening_citrus_f.json",
      "role": "data",
      "note": "Structured extraction: citrus fruit pulp mitochondria proteomics"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_and_reconstruction_of_cardiac_mitochondria_from_SBEM_images_using_a_deep_learning-bas.json",
      "role": "data",
      "note": "Structured extraction: deep-learning cardiac SBEM reconstruction"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_Mitochondria_from_Minimal_Quantities_of_Mouse_Skeletal_Muscle_for_High_Throughput_.json",
      "role": "data",
      "note": "Structured extraction: minimal quantity mouse muscle isolation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_functional_mitochondria_from_rat_kidney_and_skeletal_muscle_without_manual_homogen.json",
      "role": "data",
      "note": "Structured extraction: rat kidney/muscle without manual homogenization"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_and_mitochondrial_RNA_from_Crithidia_fasciculata.json",
      "role": "data",
      "note": "Structured extraction: Crithidia fasciculata mitochondria/RNA"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_ascites_tumor_cells_permeabilized_with_digitonin.json",
      "role": "data",
      "note": "Structured extraction: digitonin-permeabilized tumor cell isolation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Isolation_of_mitochondria_from_tissue_culture_cells.json",
      "role": "data",
      "note": "Structured extraction: tissue culture cell mitochondria isolation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Magnetic_nanoparticles_an_improved_method_for_mitochondrial_isolation.json",
      "role": "data",
      "note": "Structured extraction: magnetic nanoparticle isolation method"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mitochondria_isolated_from_lipid_droplets_of_white_adipose_tissue_reveal_functional_differences.json",
      "role": "data",
      "note": "Structured extraction: lipid droplet-associated mitochondria"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Mitochondrial_isolation_from_skeletal_muscle.json",
      "role": "data",
      "note": "Structured extraction: skeletal muscle mitochondria isolation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Optimization_of_differential_filtration-based_mitochondrial_isolation_for_mitochondrial_transpl.json",
      "role": "data",
      "note": "Structured extraction: filtration-based isolation for transplantation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Preparation_of_physiologically_active_inside-out_vesicles_from_plant_inner_mitochondrial_membra.json",
      "role": "data",
      "note": "Structured extraction: inside-out plant IMM vesicle preparation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Purification_of_functional_mouse_skeletal_muscle_mitochondria_using_Percoll_density_gradient_ce.json",
      "role": "data",
      "note": "Structured extraction: Percoll gradient mouse muscle purification"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Rapid_isolation_and_purification_of_functional_platelet_mitochondria_using_a_discontinuous_Perc.json",
      "role": "data",
      "note": "Structured extraction: platelet mitochondria discontinuous Percoll"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/Rapid_isolation_techniques_for_mitochondria_technique_for_rat_liver_mitochondria.json",
      "role": "data",
      "note": "Structured extraction: rapid rat liver mitochondria isolation"
    },
    {
      "path": "05_Extracted_Data/Structured_JSON/The_isolation_of_coupled_mitochondria_from_Physarum_polycephalum_and_their_response_to_Ca2+.json",
      "role": "data",
      "note": "Structured extraction: P. polycephalum coupled mitochondria and Ca2+"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_10.docx",
      "role": "doc",
      "note": "Synthesis comparative analysis document batch 10 (Word format)"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_60-1.docx",
      "role": "doc",
      "note": "Synthesis comparative analysis document batch 60 (Word format)"
    },
    {
      "path": "06_Synthesis/Comparative_Analysis/combined_Comparative Analysis_80-1.docx",
      "role": "doc",
      "note": "Synthesis comparative analysis document batch 80 (Word format)"
    },
    {
      "path": "06_Synthesis/Consolidated_Protocols.txt",
      "role": "generated",
      "note": "Accidental pip-install terminal output captured to file; not a protocol"
    },
    {
      "path": "09_Computational_Modeling/README.md",
      "role": "doc",
      "note": "Computational modeling overview, quickstart, directory map, key findings"
    },
    {
      "path": "09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_2005_initial_conditions.csv",
      "role": "data",
      "note": "Beard 2005 OXPHOS ODE model initial conditions from published SI"
    },
    {
      "path": "09_Computational_Modeling/Whole_Cell_Modeling/mitomammal",
      "role": "submodule",
      "note": "Empty dir; populated by setup_environment.sh via git clone from GitLab"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_AGENT_HANDOFF.md",
      "role": "doc",
      "note": "Handoff briefing for literature-search agent (q-bio Chicago 2026)"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/DOCINSIGHT_PROPAGATION_PATCH_2026-05-10.md",
      "role": "doc",
      "note": "Citation verification patch over DocInsight audit replacement citations"
    },
    {
      "path": "09_Computational_Modeling/docs/conference_planning/qbio_chicago_lodging_2026-04-21.md",
      "role": "doc",
      "note": "Conference logistics: lodging options for q-bio Chicago 2026"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/AUDIT_2026-04-22.md",
      "role": "doc",
      "note": "Systematic audit of computational claims pre-Phase G validation"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/ESSENTIAL_GENES_DEEP_DIVE.md",
      "role": "doc",
      "note": "Phase B findings: deep-dive profiles of 10 essential mouse genes"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/MITOMAMMAL_DISSECTION.md",
      "role": "doc",
      "note": "Phase A: baseline FBA trace and model structure characterization"
    },
    {
      "path": "09_Computational_Modeling/docs/investigation/TRUST_LEDGER.md",
      "role": "doc",
      "note": "Adversarial suite: claim-by-claim falsification ledger (Phase D)"
    },
    {
      "path": "09_Computational_Modeling/paths.py",
      "role": "source",
      "note": "Shared utility: single source of truth for all project paths"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/experiment1_summary.json",
      "role": "generated",
      "note": "Archived v1 experiment 1 summary JSON output"
    },
    {
      "path": "09_Computational_Modeling/results/archive_v1/halflife_sweep_curves.csv",
      "role": "generated",
      "note": "Archived v1 half-life sweep decay curves CSV"
    },
    {
      "path": "09_Computational_Modeling/results/composite/README.md",
      "role": "doc",
      "note": "Documents outputs produced in results/composite/ directory"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex11_ros_mitoq.png",
      "role": "generated",
      "note": "Plot: Ex 11 ROS-MitoQ coupling analysis figure"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_2_delta_psi_traces.png",
      "role": "generated",
      "note": "Plot: Ex 5.2 ΔΨm traces under three halflife regimes"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_5_intervention_comparison.png",
      "role": "generated",
      "note": "Plot: Ex 5.5 intervention strategy comparison figure"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex5_6_tornado.csv",
      "role": "generated",
      "note": "Ex 5.6 tornado sensitivity analysis CSV output"
    },
    {
      "path": "09_Computational_Modeling/results/composite/ex9_atp_first_diagnostic.csv",
      "role": "generated",
      "note": "Ex 9 ATP first-failure diagnostic CSV output"
    },
    {
      "path": "09_Computational_Modeling/results/experiments_v2/experiment1_v2_results.csv",
      "role": "generated",
      "note": "V2 experiment 1 time-stepped FBA flux results CSV"
    },
    {
      "path": "09_Computational_Modeling/results/experiments_v2/experiment1d_minimal_set.png",
      "role": "generated",
      "note": "Plot: minimal vs full essential gene set decay comparison"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/essential_dispensable_partition.json",
      "role": "generated",
      "note": "Phase B: 145 essential vs 229 dispensable mouse gene partition"
    },
    {
      "path": "09_Computational_Modeling/results/phase_b/experiment1b_v2_summary.json",
      "role": "generated",
      "note": "Phase B v2 gene sensitivity knockout summary JSON"
    },
    {
      "path": "09_Computational_Modeling/results/phase_c/phase_c_summary.json",
      "role": "generated",
      "note": "Phase C forensic 29h derivation summary JSON"
    },
    {
      "path": "09_Computational_Modeling/results/phase_e/phase_e_summary.json",
      "role": "generated",
      "note": "Phase E anomaly hunt and heterogeneity findings JSON"
    },
    {
      "path": "09_Computational_Modeling/results/phase_g/g5_ros_coupling.csv",
      "role": "generated",
      "note": "Phase G5 ROS-coupled accelerated protein decay CSV"
    },
    {
      "path": "09_Computational_Modeling/results/phase_h/transit_window_empirical.csv",
      "role": "generated",
      "note": "Phase H empirical transit window re-run CSV"
    },
    {
      "path": "09_Computational_Modeling/results/phase_j/intervention_analysis.json",
      "role": "generated",
      "note": "Phase J intervention modeling analysis JSON"
    },
    {
      "path": "09_Computational_Modeling/results/phase_k/ks_test_result.json",
      "role": "generated",
      "note": "Phase K KS-test statistical validation result JSON"
    },
    {
      "path": "09_Computational_Modeling/scripts/archive_v1/experiment1c_halflife_sweep.py",
      "role": "source",
      "note": "Archived v1: uniform half-life sweep vs transit window (hardcoded paths)"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment5_fba_ode.py",
      "role": "source",
      "note": "Composite FBA+ODE Ex 5.2-5.4: ΔΨm coupling sanity and TW derivation"
    },
    {
      "path": "09_Computational_Modeling/scripts/composite/experiment7_human_gem.py",
      "role": "source",
      "note": "Cross-model validation: composite FBA+ODE run on Human-GEM"
    },
    {
      "path": "09_Computational_Modeling/scripts/experiments_v2/experiment1_v2_transit_window.py",
      "role": "source",
      "note": "V2 transit window: GPR-aware decay, signed flux, dual objective"
    },
    {
      "path": "09_Computational_Modeling/scripts/experiments_v2/experiment1d_minimal_set.py",
      "role": "source",
      "note": "Direct A3 test: minimal essential gene set vs full decay"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_b_annotate_essentials.py",
      "role": "source",
      "note": "Annotates 145 essential genes via MyGene.info API"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_e_anomaly_hunt.py",
      "role": "source",
      "note": "FVA and non-uniform decay characterization (Phase E)"
    },
    {
      "path": "09_Computational_Modeling/scripts/investigation_phases/phase_g5_ros_coupling.py",
      "role": "source",
      "note": "ROS-coupled protein damage acceleration model (Phase G.5)"
    },
    {
      "path": "09_Computational_Modeling/setup_environment.sh",
      "role": "config",
      "note": "Bootstraps conda env, installs pip deps, clones MitoMAMMAL from GitLab"
    },
    {
      "path": "DIY Yeast Media.md",
      "role": "doc",
      "note": "DIY yeast media recipe using household ingredients"
    }
  ],
  "entry_points": [
    {
      "name": "composite_utils",
      "kind": "module",
      "location": "09_Computational_Modeling/composite_utils.py",
      "description": "Shared utility module exporting compose_fba_ode, build_capacity_envelope_fn, and extract_capacity_envelope for FBA+ODE coupling; imported by all composite experiment scripts"
    },
    {
      "name": "experiment5b_interventions",
      "kind": "script",
      "location": "09_Computational_Modeling/scripts/composite/experiment5b_interventions.py",
      "description": "CLI script modeling cold chain, MitoQ, and substrate supplementation interventions through the composite FBA+ODE model; outputs ex5_5_intervention_composite.csv"
    },
    {
      "name": "experiment8_abstract_figure",
      "kind": "script",
      "location": "09_Computational_Modeling/scripts/composite/experiment8_abstract_figure.py",
      "description": "CLI script generating the 2-panel q-bio abstract figure from MPTP scenario and MitoQ dose-response data"
    },
    {
      "name": "experiment1_v3_empirical",
      "kind": "script",
      "location": "09_Computational_Modeling/scripts/experiments_v2/experiment1_v3_empirical.py",
      "description": "Primary FBA transit-window experiment using empirical per-subunit half-lives with 50-sample bootstrap CI; outputs transit_window_empirical.csv"
    },
    {
      "name": "experiment4_interventions",
      "kind": "script",
      "location": "09_Computational_Modeling/scripts/experiments_v2/experiment4_interventions.py",
      "description": "FBA-layer three-intervention modeling (cold chain, MitoQ, substrate) with bootstrap CI; outputs intervention_bar_chart.png"
    },
    {
      "name": "phase_b_cluster_and_sweep",
      "kind": "script",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_b_cluster_and_sweep.py",
      "description": "Phase B functional clustering and single-gene immortalization sweep over all 145 essential genes; outputs essential_genes_annotated.csv and gene_knockout_scores_v2.csv"
    },
    {
      "name": "phase_g1_order_statistics",
      "kind": "script",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_g1_order_statistics.py",
      "description": "Validation test comparing non-FBA order-statistics TW prediction against FBA output; outputs g1_order_stats_vs_fba.csv"
    },
    {
      "name": "phase_h_ci_subunit_analysis",
      "kind": "script",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_h_ci_subunit_analysis.py",
      "description": "Complex I subunit half-life deep dive with pairwise Pearson correlation and permutation test; outputs ci_correlation_analysis.json"
    },
    {
      "name": "decay_utils",
      "kind": "shared_module",
      "location": "09_Computational_Modeling/decay_utils.py",
      "description": "Shared utility imported by all experiment scripts; provides GPR-aware FBA decay, objective configuration, and transit window helpers"
    },
    {
      "name": "beard_qamas_in_vitro_reference",
      "kind": "script",
      "location": "09_Computational_Modeling/Whole_Cell_Modeling/beards_lab/beard_qamas_in_vitro_reference.py",
      "description": "Beard QAMAS reference ODE model of mitochondrial bioenergetics; runs top-level without __main__ guard"
    },
    {
      "name": "experiment1_transit_window",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/archive_v1/experiment1_transit_window.py",
      "description": "Archived v1 CLI: time-stepped FBA predicting mitochondrial ATP viability window post-extraction"
    },
    {
      "name": "experiment10_mptp_composite",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/composite/experiment10_mptp_composite.py",
      "description": "CLI: tests MPTP Ca2+-driven ΔΨm collapse vs proteomics-limited ATP-first failure partition"
    },
    {
      "name": "experiment5c_sensitivity",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/composite/experiment5c_sensitivity.py",
      "description": "CLI: Latin hypercube sensitivity propagation using literature-sourced parameter uncertainty ranges"
    },
    {
      "name": "experiment9_atp_first_diagnostic",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/composite/experiment9_atp_first_diagnostic.py",
      "description": "CLI: diagnoses ATP-first paradox by partitioning capacity bottleneck vs Vmax vs threshold hypotheses"
    },
    {
      "name": "experiment1b_v2_gpr_knockout",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/experiments_v2/experiment1b_v2_gpr_knockout.py",
      "description": "CLI: GPR-aware gene knockout scoring correcting v1 OR-rule over-kill bug"
    },
    {
      "name": "phase_a_dissection",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_a_dissection.py",
      "description": "CLI: MitoMAMMAL mechanistic dissection runs A.1–A.5 generating MITOMAMMAL_DISSECTION.md"
    },
    {
      "name": "phase_c_forensic_29h",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_c_forensic_29h.py",
      "description": "CLI: forensic dissection of why transit window is 29 hours"
    },
    {
      "name": "phase_g2_cross_model",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_g2_cross_model.py",
      "description": "CLI: cross-model validation replicating decay findings in Human-GEM mitochondrial subset"
    },
    {
      "name": "phase_i_syn3a_crosswalk",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_i_syn3a_crosswalk.py",
      "description": "CLI: compares 3 mitochondrial transport reactions against Syn3A minimal cell equivalents"
    },
    {
      "name": "ode_utils",
      "kind": "shared_utility",
      "location": "09_Computational_Modeling/ode_utils.py",
      "description": "Core ODE library (BeardParams, integrate_with_capacity, beard_rhs) imported by all composite experiment scripts"
    },
    {
      "name": "experiment1b_gene_sensitivity",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/archive_v1/experiment1b_gene_sensitivity.py",
      "description": "Ranks nuclear-encoded genes by knockout impact on ATP and transit window (archive v1)"
    },
    {
      "name": "experiment11_ros_mitoq",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/composite/experiment11_ros_mitoq.py",
      "description": "Sweeps MitoQ concentration as ROS scavenger in composite FBA+ODE model"
    },
    {
      "name": "experiment6_option_b_extension",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/composite/experiment6_option_b_extension.py",
      "description": "Models membrane-integrity decay as non-proteomic failure mode via proton-leak growth"
    },
    {
      "name": "validate_against_beard",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/composite/validate_against_beard.py",
      "description": "Reproduces Beard 2005 QAMAS PO-curve to gate the ode_utils implementation"
    },
    {
      "name": "experiment1c_v2_halflife_sweep",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/experiments_v2/experiment1c_v2_halflife_sweep.py",
      "description": "Sweeps protein half-life 1-72h with GPR-aware decay under dual ATP/DPsi objectives"
    },
    {
      "name": "phase_b6_deep_dive",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_b6_deep_dive.py",
      "description": "Generates structured profiles for 10 selected essential mitochondrial genes"
    },
    {
      "name": "phase_d_adversarial_suite",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_d_adversarial_suite.py",
      "description": "Runs adversarial perturbation tests (buffer sensitivity, Monte Carlo, threshold sweeps)"
    },
    {
      "name": "phase_g2b_human_gem_decay",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_g2b_human_gem_decay.py",
      "description": "Tests uniform-decay transit window algebraic claim on Human-GEM (12931 reactions)"
    },
    {
      "name": "phase_k_wet_lab_validation",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_k_wet_lab_validation.py",
      "description": "Overlays model-predicted decay curves against user-digitized 2024 yeast JC-1 data"
    },
    {
      "name": "paths.py",
      "kind": "shared_utility",
      "location": "09_Computational_Modeling/paths.py",
      "description": "Single source of truth for all project paths; imported by every computation script via bootstrap pattern"
    },
    {
      "name": "setup_environment.sh",
      "kind": "cli_script",
      "location": "09_Computational_Modeling/setup_environment.sh",
      "description": "Bootstraps Miniforge conda env, installs COBRApy via pip, clones MitoMAMMAL repo from GitLab"
    },
    {
      "name": "experiment1c_halflife_sweep.py",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/archive_v1/experiment1c_halflife_sweep.py",
      "description": "Archived v1 script: sweeps uniform nuclear protein half-life vs transit window over 12 values"
    },
    {
      "name": "experiment5_fba_ode.py",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/composite/experiment5_fba_ode.py",
      "description": "Composite FBA+ODE driver for Ex 5.2-5.4: ΔΨm coupling sanity, TW derivation, failure partition"
    },
    {
      "name": "experiment7_human_gem.py",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/composite/experiment7_human_gem.py",
      "description": "Cross-model composite validation run on Human-GEM to rule out MitoMAMMAL-specific artifacts"
    },
    {
      "name": "experiment1_v2_transit_window.py",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/experiments_v2/experiment1_v2_transit_window.py",
      "description": "Corrected v2 transit window simulation with GPR-aware decay, signed flux, and dual ATP/ΔΨm objectives"
    },
    {
      "name": "experiment1d_minimal_set.py",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/experiments_v2/experiment1d_minimal_set.py",
      "description": "Direct test of Assumption A3: minimal essential gene set decay vs full 374-gene nuclear decay"
    },
    {
      "name": "phase_b_annotate_essentials.py",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_b_annotate_essentials.py",
      "description": "Annotates 145 essential mouse genes with GO terms and disease associations via MyGene.info API"
    },
    {
      "name": "phase_e_anomaly_hunt.py",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_e_anomaly_hunt.py",
      "description": "Phase E: resolves anomalies, runs FVA, characterizes non-uniform decay heterogeneity"
    },
    {
      "name": "phase_g5_ros_coupling.py",
      "kind": "cli_main",
      "location": "09_Computational_Modeling/scripts/investigation_phases/phase_g5_ros_coupling.py",
      "description": "Phase G.5: models ROS-coupled protein damage acceleration across scenarios A/B/C"
    }
  ],
  "architecture_summary": "The repository is a single-researcher R&D knowledge base + computational pipeline organized as a 10-stage, pipeline-ordered folder structure (01_Vision_and_Strategy through 10_Research_Questions; see INDEX.md and README.md). Stages 01-08 are a document/data pipeline: vision/strategy docs (.docx/.md), a literature-screening methodology, a 114-paper study registry (03_Study_Registry/studies.csv), source-paper summaries, and three tiers of AI-extracted data (05_Extracted_Data/{Structured_JSON,PDF_Metadata,Protocol_Summaries}) feeding cross-paper synthesis (06_Synthesis) and a bench lab manual (07_Lab_Manual). Of 319 inventoried files, the overwhelming majority are static data/doc artifacts (extracted-paper JSON, .docx, .txt). The live executable system lives entirely in 09_Computational_Modeling/, a Python (3.10) scientific pipeline. Compute flow: a centralized paths.py is the single source of truth resolving the MitoMAMMAL genome-scale model (Whole_Cell_Modeling/mitomammal/6_universal_mito_model.xml, a git submodule) and results/ output dirs. decay_utils.py runs pFBA on the COBRApy model to get signed baseline fluxes, then applies time-stepped, GPR-aware protein decay (AND-clause=min of subunit decay factors, OR=summed isozyme pooling via MitoMAMMAL's efflux_method) to scale reaction bounds, producing a 'capacity envelope' over time as nuclear-encoded proteins decay on literature half-lives (mt-encoded genes exempt). composite_utils.py bridges that FBA capacity envelope into a Beard-2005 biophysical OXPHOS ODE (ode_utils.py, SciPy LSODA) via FBA_ODE_REACTION_MAP, treating decay fractions as Vmax multipliers, and integrates ΔΨm/ATP/NADH trajectories to derive a 'transit window'. Scripts are organized by generation/phase: scripts/archive_v1 (deprecated), scripts/experiments_v2 (FBA-centric), scripts/investigation_phases (phase_a..phase_k forensic/validation), and scripts/composite (FBA+ODE coupling); each writes versioned outputs under results/ and is documented in LAB_NOTEBOOK.md and docs/investigation/ audit threads.",
  "provisional_intent": "PROVISIONAL: An independent-researcher R&D program (lead Miguel Ingram, per README.md:103) to engineer autonomous/programmable extracellular mitochondria, whose tractable near-term aim is computationally predicting the 'transit window' — how long an extracted mitochondrion keeps producing ATP/ΔΨm before reuptake viability is lost — packaged toward a q-bio Chicago 2026 conference abstract (README.md:11-23).",
  "components": [
    {
      "name": "01_Vision_and_Strategy",
      "role": "Thesis, 4-layer long-range vision, and assumption/strategy audits (README.md:46)"
    },
    {
      "name": "02_Methodology",
      "role": "Literature search, screening, and ranking methodology incl. BSHR_Loop (INDEX.md:25-33)"
    },
    {
      "name": "03_Study_Registry",
      "role": "studies.csv — 114 screened papers (1955-2024) with inclusion probabilities (README.md:48)"
    },
    {
      "name": "04_Source_Literature / 05_Extracted_Data",
      "role": "Source-paper summaries plus 3 tiers of AI extraction (Structured_JSON, PDF_Metadata, Protocol_Summaries) (INDEX.md:44-60)"
    },
    {
      "name": "06_Synthesis",
      "role": "Cross-paper comparative analyses and consolidated protocols (INDEX.md:62-69)"
    },
    {
      "name": "07_Lab_Manual / 08_Experimental_Work",
      "role": "Bench-ready isolation manual and planned/completed wet-lab experiments E1-E8 (INDEX.md:71-88)"
    },
    {
      "name": "09_Computational_Modeling",
      "role": "The active executable pipeline: time-stepped FBA + ODE transit-window modeling (README.md:11-21)"
    },
    {
      "name": "paths.py",
      "role": "Single source of truth for model/results/docs paths and sys.path bootstrap (paths.py:1-11)"
    },
    {
      "name": "decay_utils.py",
      "role": "GPR-aware FBA protein-decay capacity-envelope engine imported by all experiments (decay_utils.py:1-10)"
    },
    {
      "name": "ode_utils.py",
      "role": "Beard-2005 OXPHOS ODE integration library (SciPy LSODA) for ΔΨm/ATP dynamics (s1_files.json ode_utils note)"
    },
    {
      "name": "composite_utils.py",
      "role": "FBA->ODE coupling: maps decay fractions to ODE Vmax multipliers and drives composite simulations (composite_utils.py:1-31)"
    },
    {
      "name": "scripts/{archive_v1,experiments_v2,investigation_phases,composite}",
      "role": "Generationally/phase-organized experiment entry points writing versioned results/ outputs (paths.py:60-65)"
    },
    {
      "name": "Whole_Cell_Modeling submodules",
      "role": "External MitoMAMMAL (primary) and Human-GEM (cross-check) genome-scale models as git submodules (.gitmodules; README.md:74)"
    },
    {
      "name": "results/ + docs/ + LAB_NOTEBOOK.md",
      "role": "Versioned simulation outputs and self-audited investigation/conference-planning documentation trail (README.md:21)"
    }
  ],
  "denominator": 319
}
```

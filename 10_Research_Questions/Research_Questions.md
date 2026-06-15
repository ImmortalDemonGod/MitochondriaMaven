# Mitochondria Maven — Core Research Questions

Source: Personal notebooks, transcribed via Otter.ai (April 2026)

## Questions

### RQ1. How do you preserve mitochondria over long periods of time?
- **Status:** ELEVATED PRIORITY — reframed as transit survivability (April 2026)
- **Literature:** Storage protocols in 06_Synthesis/Consolidated_Protocols.txt; -80C buffer storage (250 mM sucrose, 10 mM Tris-HCl pH 7.4, 0.1 mM EDTA) documented in 07_Lab_Manual/
- **Reframe:** Preservation is not about long-term storage — it's about extending the **functional transit window** between extraction and cellular reuptake. Once a mitochondrion is internalized by a target cell, nuclear import machinery resumes and protein stock is replenished. The engineering target is transit survivability, not permanent autonomy.
- **Computational approach:** Time-stepped FBA modeling of ATP decay post-extraction, constrained by published ETC protein half-lives. Identifies which proteins degrade fastest and which interventions (antioxidants, cold chain, substrate supplementation, EV encapsulation) extend the transit window.
- **Connection to q-bio 2026:** This is now the PRIMARY research question driving the q-bio abstract.
- **Gaps:** ETC protein half-life data needed; mitophagy reuptake viability threshold not quantified; blood/ECF substrate concentration constraints for FBA not compiled

### RQ2. How autonomous can you reasonably make mitochondria?
- **Status:** Reframed — full autonomy may not be necessary (April 2026)
- **Literature:** Extracellular mitochondria confirmed in blood (Stephens et al. 2020); limited by nuclear-encoded protein dependence (~1,500 proteins imported vs ~37 encoded by mtDNA)
- **Reframe:** The assumption audit (Strategy_Critique_and_Assumptions_2026-04-21.md) revealed that full autonomy faces hard biological limits (protein turnover, evolutionary gene transfer, immune recognition). However, full autonomy is NOT required if reuptake occurs within the transit window. The question becomes: "what is the minimum autonomy needed for clinical utility?" rather than "how fully autonomous can we make them?"
- **Gaps:** The MitoMAMMAL knockdown experiment will quantify steady-state ATP under mt-genome-only conditions. Time-stepped modeling will show how quickly function degrades. Both inform the feasibility boundary.

### RQ3. Can plants uptake mitochondria and at what rate of ATP?
- **Status:** Unexplored
- **Literature:** Plant extraction protocols exist (rice, Arabidopsis, chickpea, pea) but no cross-kingdom transfer studies found
- **Gaps:** Entirely open research area

### RQ4. What are the mitochondria-to-biosynthesis rates?
- **Status:** Partially addressed
- **Literature:** ATP synthesis rates measured across protocols; bioenergetic characterization in multiple organisms
- **Gaps:** Comprehensive biosynthesis rate data not compiled; missing systematic comparison across organisms/conditions

### RQ5. How do I extract mitochondria at scale?
- **Status:** Active — protocol optimization done (Taguchi arrays, 2024 lab work)
- **Literature:** 93 extraction method papers reviewed; combined_content summaries with yield data
- **Lab work:** Successful extraction achieved; physical lab notebook with day-by-day protocols exists
- **Gaps:** Scaling beyond bench-top; automation; cost reduction; microfluidic approaches

### RQ6. What is the maximum mitochondrial density (intracellular and extracellular)?
- **Status:** Partially addressed
- **Literature:** Intracellular density varies by tissue type; extracellular mitochondria confirmed in blood
- **Gaps:** Maximum achievable extracellular density unknown; no engineering studies on density limits

### RQ7. What are the imported materials from the cell to the mitochondria?
- **Status:** Partially addressed
- **Literature:** Pyruvate, acetyl-CoA, NADH (via malate-aspartate shuttle); ~1,500 nuclear-encoded proteins
- **Gaps:** Complete import map not compiled; implications for autonomous operation not fully analyzed

### RQ8. How can you transfer mitochondria from one organism to another?
- **Status:** Well-covered in literature
- **Literature:** Tunneling nanotubes, extracellular vesicles, gap junctions, microinjection, FluidFM, magnetomitotransfer, MitoCeption, photothermal nanoblades, Mitopunch
- **Gaps:** Cross-species transfer efficiency; immunological barriers; long-term integration

### RQ9. What are the best yeast strains to extract mitochondria from?
- **Status:** Partially addressed
- **Literature:** S. cerevisiae protocols detailed in lab manual and literature; Pichia pastoris also covered
- **Lab work:** Yeast extraction was the focus of 2024 lab work
- **Gaps:** Systematic strain comparison not found; yield-per-strain data not compiled

### RQ10. How can I leverage computational modeling to answer these questions?
- **Status:** Early stage
- **Literature:** Synth3a whole-cell modeling work (related project); Lux3 lab computational paper on Synth3a
- **Gaps:** No modeling integrated into this project yet; connection to Synth3a needs formalization

## Mapping to 8 Literature Categories

| Research Question | Primary Category | Secondary Category |
|---|---|---|
| RQ1 (Preservation) | Mitochondrial Lab Protocols | Extraction/Isolation Techniques |
| RQ2 (Autonomy) | Fundamental Mitochondria Knowledge | Regulation and Dynamics |
| RQ3 (Plant uptake) | Mitochondrial Dynamics and Interactions | Case Studies |
| RQ4 (Biosynthesis rates) | Fundamental Mitochondria Knowledge | Lab Protocols |
| RQ5 (Scale extraction) | Extraction/Isolation Techniques | Lab Protocols |
| RQ6 (Max density) | Fundamental Mitochondria Knowledge | Dynamics and Interactions |
| RQ7 (Imported materials) | Fundamental Mitochondria Knowledge | Regulation and Dynamics |
| RQ8 (Transfer) | Mitochondrial Dynamics and Interactions | Case Studies |
| RQ9 (Yeast strains) | Extraction/Isolation Techniques | Lab Protocols |
| RQ10 (Modeling) | Genomics and Bioinformatics | Synthetic Biology |

## Mapping to 8 Planned Experiments

| Experiment | Related RQ |
|---|---|
| E1. Optimize max mitochondrial volume after isolation | RQ5, RQ6 |
| E2. Test if F0-ATP synthase rotor responds to red light | RQ4 |
| E3. Mitochondrial senescent cell detection | RQ2 |
| E4. Test transplant ability | RQ8 |
| E5. Test autonomy | RQ2, RQ7 |
| E6. Performance enhancement — rapid division signaling | RQ6 |
| E7. Insert PGC-1α and PPARγ into yeast mitochondria | RQ9, RQ2 |
| E8. Decrease cost of ATP production | RQ4, RQ5 |

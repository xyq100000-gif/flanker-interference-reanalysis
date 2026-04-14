# Flanker Interference Reanalysis

This repository documents a reproducible reanalysis of a small-sample Eriksen flanker dataset. The project reorganizes a raw spreadsheet export into block-level and subject-level datasets, reproduces the original repeated-measures ANOVA, and extends the workflow with a block-level mixed-effects model and descriptive error checks.

The emphasis is methodological rather than claim-oriented: the repository focuses on data restructuring, repeated-measures inference, hierarchical thinking, transparent limitations, and reproducible reporting.

## Research Question

How do arrow load and flanker consistency affect the congruency effect in an Eriksen flanker task?

The reanalysis examines a 2×2 within-subject design with two experimental factors:

- **Arrow load**: low (5 arrows) vs high (7 arrows)
- **Flanker consistency**: consistent vs inconsistent

The outcome of interest is the **congruency effect in milliseconds**, defined as the difference between incongruent and congruent reaction times.

## Data Structure

The repository preserves both the original spreadsheet export and the reconstructed analysis-ready datasets.

### Raw data

- `data/raw/flanker_block_export.csv`  
  Original spreadsheet-style export retained for provenance.

- `data/raw/flanker_subject_summary_original.csv`  
  Original subject-condition summary file used as a validation target.

### Processed data

- `data/processed/flanker_block_level.csv`  
  Reconstructed block-level dataset with 240 rows:
  - 12 participants
  - 5 repeated observations per condition
  - 4 within-subject conditions

- `data/processed/flanker_subject_summary.csv`  
  Reconstructed subject-level summary with 48 rows:
  - 12 participants
  - 4 within-subject conditions

The processed summary matches the original summary exactly.

## Analysis Workflow

The workflow proceeds in four steps:

1. **Parse the original export** into a tidy block-level dataset.
2. **Reconstruct subject-level summaries** and validate them against the original summary file.
3. **Reproduce the repeated-measures ANOVA** reported in the original analysis.
4. **Extend the analysis** with a block-level mixed-effects model and descriptive error checks.

## Main Findings

### 1. Validation of reconstructed summaries

The reconstructed subject-level summary reproduces the original summary exactly:

- 48 out of 48 rows matched
- Maximum absolute difference: **0 ms**

### 2. Repeated-measures ANOVA

The subject-level repeated-measures ANOVA produced the following results:

- **Arrow load**: F(1, 11) = 4.80, p = 0.051, partial eta squared = 0.304
- **Flanker consistency**: F(1, 11) = 67.56, p < 0.001, partial eta squared = 0.860
- **Interaction**: F(1, 11) = 2.82, p = 0.121, partial eta squared = 0.204

The strongest and most stable signal is the main effect of flanker consistency.

### 3. Condition means

Mean congruency effects by condition:

- Low load / Inconsistent: **33.48 ms**
- Low load / Consistent: **66.02 ms**
- High load / Inconsistent: **35.02 ms**
- High load / Consistent: **82.50 ms**

These condition means indicate substantially larger congruency effects under consistent flankers.

### 4. Within-load contrasts

Pairwise contrasts comparing consistent vs inconsistent flankers within each load condition:

- **Low load**: +32.54 ms, t(11) = 4.19, Holm-adjusted p = 0.0015
- **High load**: +47.48 ms, t(11) = 9.19, Holm-adjusted p < 0.001

### 5. Block-level mixed-effects model

Using the reconstructed 240-row block-level dataset, the mixed-effects model showed:

- A strong consistency effect under low load
- Little evidence for a main effect of arrow load on its own
- No clear evidence for the interaction

The block-level reanalysis therefore supports the same broad interpretation as the subject-level ANOVA: **flanker consistency is the dominant effect in this dataset**.

### 6. Error patterns

Error counts are included as a descriptive secondary outcome. Two participants have missing low-load error entries in the original export, so error analyses should be interpreted cautiously.

The error summaries suggest that accuracy should be reported alongside reaction-time effects rather than ignored.

## Figures and Tables

The repository includes:

- condition mean plots with 95% confidence intervals
- participant-level trajectory plots
- block-level distribution plots
- descriptive error-pattern plots
- ANOVA, contrast, mixed-model, and validation tables

See `results/figures/` and `results/tables/` for outputs.

## Repository Structure

```text
flanker-interference-reanalysis/
├── data/
│   ├── raw/
│   │   ├── flanker_block_export.csv
│   │   └── flanker_subject_summary_original.csv
│   └── processed/
│       ├── flanker_block_level.csv
│       └── flanker_subject_summary.csv
├── docs/
│   ├── attribution.md
│   ├── data_dictionary.md
│   ├── limitations.md
│   └── study_design.md
├── results/
│   ├── figures/
│   ├── tables/
│   └── analysis_summary.md
├── scripts/
│   ├── 01_parse_raw_export.py
│   ├── 02_validate_reconstructed_summary.py
│   ├── 03_reproduce_rm_anova.py
│   ├── 04_block_level_mixed_model.py
│   ├── 05_error_analysis.py
│   ├── 06_make_figures.py
│   └── utils.py
├── README.md
└── requirements.txt

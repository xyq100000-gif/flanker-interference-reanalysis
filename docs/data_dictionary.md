# Data Dictionary

## Raw file

`data/raw/flanker_block_export.csv`

This is the original spreadsheet export from the classroom experiment. It is intentionally preserved in its original wide format for provenance.

## Processed files

### `data/processed/flanker_block_level.csv`

Each row represents one within-condition repetition exported by the task software for a participant.

Columns:

- `participant_id`: anonymized participant identifier (1-12)
- `replicate_id`: repetition index within participant and condition (1-5)
- `arrow_load`: `low` (5 arrows) or `high` (7 arrows)
- `flanker_consistency`: `consistent` or `inconsistent`
- `rt_congruent_ms`: mean reaction time for congruent trials
- `rt_incongruent_ms`: mean reaction time for incongruent trials
- `congruency_effect_ms`: `rt_incongruent_ms - rt_congruent_ms`
- `error_count`: exported error count for that repetition

### `data/processed/flanker_subject_summary.csv`

Subject-level averages reconstructed from the block-level file.

Columns:

- `participant_id`
- `arrow_load`
- `flanker_consistency`
- `mean_rt_congruent_ms`
- `mean_rt_incongruent_ms`
- `mean_congruency_effect_ms`
- `mean_error_count`

## Validation file

`results/tables/validation_against_original_summary.csv`

This file verifies that the reconstructed subject-level means match the original summary file exactly.

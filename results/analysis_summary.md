# Rerun Summary

## What was rerun

I reconstructed the raw spreadsheet into a block-level dataset (240 rows) and a subject-level summary dataset (48 rows), then reran the main analyses.

## Validation

- Reconstructed summary rows matched the original summary file exactly: 48 / 48
- Maximum absolute difference: 0 ms

## Subject-level repeated-measures ANOVA

| Effect | F | df | p | partial eta squared |
|---|---:|---:|---:|---:|
| Arrow load | 4.80 | (1, 11) | 0.051 | 0.304 |
| Flanker consistency | 67.56 | (1, 11) | < .001 | 0.860 |
| Interaction | 2.82 | (1, 11) | 0.121 | 0.204 |

Interpretation: the consistency effect is very strong, the arrow-load main effect is borderline, and the interaction is not clearly supported.

## Condition means

| Condition | Mean congruency effect (ms) |
|---|---:|
| Low / Inconsistent | 33.48 |
| Low / Consistent | 66.02 |
| High / Inconsistent | 35.02 |
| High / Consistent | 82.50 |

## Within-load contrasts

| Contrast | Estimate (ms) | t | p (Holm) |
|---|---:|---:|---:|
| Low: consistent - inconsistent | 32.54 | 4.19 | 0.0015 |
| High: consistent - inconsistent | 47.48 | 9.19 | 0.0000 |

Interpretation: the consistency contrast is strong under both load conditions.

## Block-level mixed-effects model

The block-level model yields the same qualitative message:

- consistency effect at low load: 32.54 ms, p < .001
- arrow-load effect at the inconsistent condition: 1.54 ms, p = 0.832
- interaction: 14.94 ms, p = 0.146

Interpretation: the strongest and most stable signal is the consistency effect, not a clean interaction.

## Error analysis

Error fields are missing for participants 5 and 6 in the low-load conditions, so the error module should remain descriptive.

Mean error counts:

| Condition | Mean errors |
|---|---:|
| Low / Inconsistent | 1.50 |
| Low / Consistent | 2.39 |
| High / Inconsistent | 1.35 |
| High / Consistent | 1.78 |

Across complete subject-condition means, congruency effect and error count are positively associated (r = 0.46, p = 0.002; n = 44). That is a good reason to keep accuracy in the public-facing version of the project.

from __future__ import annotations

import pandas as pd
from scipy import stats

from utils import (
    ensure_output_dirs,
    reconstruct_block_level,
    make_subject_summary,
    RESULTS_TABLES_DIR,
)


def main() -> None:
    ensure_output_dirs()

    summary_df = make_subject_summary(reconstruct_block_level())

    error_summary = (
        summary_df.groupby(["arrow_load", "flanker_consistency"])
        .agg(
            mean_error_count=("mean_error_count", "mean"),
            sd_error_count=("mean_error_count", "std"),
            n_nonmissing=("mean_error_count", lambda x: x.notna().sum()),
        )
        .reset_index()
    )
    error_summary.to_csv(RESULTS_TABLES_DIR / "error_summary.csv", index=False)

    missing_rows = summary_df.loc[
        summary_df["mean_error_count"].isna(),
        ["participant_id", "arrow_load", "flanker_consistency"],
    ]
    missing_rows.to_csv(RESULTS_TABLES_DIR / "missing_error_rows.csv", index=False)

    complete = summary_df.dropna(subset=["mean_error_count"])
    r_value, p_value = stats.pearsonr(
        complete["mean_congruency_effect_ms"], complete["mean_error_count"]
    )
    pd.DataFrame(
        [
            {
                "measure_x": "mean_congruency_effect_ms",
                "measure_y": "mean_error_count",
                "pearson_r": r_value,
                "p_value": p_value,
                "n": len(complete),
            }
        ]
    ).to_csv(RESULTS_TABLES_DIR / "effect_error_correlation.csv", index=False)

    rt_summary = (
        summary_df.groupby(["arrow_load", "flanker_consistency"])
        .agg(
            mean_rt_congruent_ms=("mean_rt_congruent_ms", "mean"),
            mean_rt_incongruent_ms=("mean_rt_incongruent_ms", "mean"),
            mean_congruency_effect_ms=("mean_congruency_effect_ms", "mean"),
        )
        .reset_index()
    )
    rt_summary.to_csv(RESULTS_TABLES_DIR / "rt_summary_by_condition.csv", index=False)

    print("Saved error summaries, missingness table, correlation table, and RT summaries.")


if __name__ == "__main__":
    main()

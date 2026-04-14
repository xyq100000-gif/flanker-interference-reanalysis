from __future__ import annotations

import pandas as pd

from utils import (
    ensure_output_dirs,
    reconstruct_block_level,
    make_subject_summary,
    RAW_DIR,
    RESULTS_TABLES_DIR,
)


def main() -> None:
    ensure_output_dirs()

    summary_df = make_subject_summary(reconstruct_block_level())
    original = pd.read_csv(RAW_DIR / "flanker_subject_summary_original.csv").rename(
        columns={
            "subject": "participant_id",
            "arrow_num": "arrow_load",
            "consistent": "flanker_consistency",
            "effects(ms)": "original_mean_congruency_effect_ms",
        }
    )

    merged = summary_df.merge(
        original[
            [
                "participant_id",
                "arrow_load",
                "flanker_consistency",
                "original_mean_congruency_effect_ms",
            ]
        ],
        on=["participant_id", "arrow_load", "flanker_consistency"],
        how="outer",
        indicator=True,
    )

    merged["reconstructed_mean_congruency_effect_ms"] = merged[
        "mean_congruency_effect_ms"
    ]
    merged["difference_ms"] = (
        merged["reconstructed_mean_congruency_effect_ms"]
        - merged["original_mean_congruency_effect_ms"]
    )

    out = merged[
        [
            "participant_id",
            "arrow_load",
            "flanker_consistency",
            "reconstructed_mean_congruency_effect_ms",
            "original_mean_congruency_effect_ms",
            "difference_ms",
            "_merge",
        ]
    ]

    out.to_csv(RESULTS_TABLES_DIR / "validation_against_original_summary.csv", index=False)

    max_abs_diff = out["difference_ms"].abs().max()
    if max_abs_diff == 0 and (out["_merge"] == "both").all():
        print("Validation passed: reconstructed summary matches the original summary exactly.")
    else:
        print("Validation found differences. Inspect results/tables/validation_against_original_summary.csv")


if __name__ == "__main__":
    main()

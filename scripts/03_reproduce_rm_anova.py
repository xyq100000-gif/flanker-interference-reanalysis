from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.anova import AnovaRM

from utils import (
    ensure_output_dirs,
    reconstruct_block_level,
    make_subject_summary,
    RESULTS_TABLES_DIR,
)


def main() -> None:
    ensure_output_dirs()

    summary_df = make_subject_summary(reconstruct_block_level())

    aov = AnovaRM(
        summary_df,
        depvar="mean_congruency_effect_ms",
        subject="participant_id",
        within=["arrow_load", "flanker_consistency"],
    ).fit()

    anova_table = aov.anova_table.reset_index().rename(
        columns={
            "index": "effect",
            "F Value": "F_value",
            "Num DF": "df_num",
            "Den DF": "df_den",
            "Pr > F": "p_value",
        }
    )
    anova_table["partial_eta_sq"] = (
        anova_table["F_value"] * anova_table["df_num"]
    ) / (anova_table["F_value"] * anova_table["df_num"] + anova_table["df_den"])
    anova_table.to_csv(RESULTS_TABLES_DIR / "rm_anova_results.csv", index=False)

    condition_means = (
        summary_df.groupby(["arrow_load", "flanker_consistency"])["mean_congruency_effect_ms"]
        .agg(["mean", "std", "count"])
        .reset_index()
        .rename(
            columns={
                "mean": "mean_congruency_effect_ms",
                "std": "sd_congruency_effect_ms",
                "count": "n",
            }
        )
    )
    condition_means["se_congruency_effect_ms"] = (
        condition_means["sd_congruency_effect_ms"] / np.sqrt(condition_means["n"])
    )
    condition_means.to_csv(RESULTS_TABLES_DIR / "condition_means.csv", index=False)

    pivot = summary_df.pivot_table(
        index="participant_id",
        columns=["arrow_load", "flanker_consistency"],
        values="mean_congruency_effect_ms",
    )

    pairwise_rows = []
    raw_p_values = []

    for arrow_load in ["low", "high"]:
        consistent = pivot[(arrow_load, "consistent")]
        inconsistent = pivot[(arrow_load, "inconsistent")]
        t_stat, p_value = stats.ttest_rel(consistent, inconsistent)
        diff = (consistent - inconsistent).mean()
        se = stats.sem(consistent - inconsistent)
        ci_low, ci_high = stats.t.interval(
            0.95,
            len(consistent) - 1,
            loc=diff,
            scale=se,
        )

        pairwise_rows.append(
            {
                "contrast": f"{arrow_load}: consistent - inconsistent",
                "estimate_ms": diff,
                "t_value": t_stat,
                "df": len(consistent) - 1,
                "p_raw": p_value,
                "ci_low": ci_low,
                "ci_high": ci_high,
            }
        )
        raw_p_values.append(p_value)

    order = np.argsort(raw_p_values)
    adjusted = [None] * len(raw_p_values)
    running_max = 0.0
    m = len(raw_p_values)

    for rank, idx in enumerate(order):
        adjusted_p = (m - rank) * raw_p_values[idx]
        running_max = max(running_max, adjusted_p)
        adjusted[idx] = min(running_max, 1.0)

    for row, p_holm in zip(pairwise_rows, adjusted):
        row["p_holm"] = p_holm

    pd.DataFrame(pairwise_rows).to_csv(
        RESULTS_TABLES_DIR / "pairwise_contrasts.csv", index=False
    )

    print("Saved ANOVA table, condition means, and Holm-adjusted pairwise contrasts.")


if __name__ == "__main__":
    main()

from __future__ import annotations

import pandas as pd
import statsmodels.formula.api as smf

from utils import ensure_output_dirs, reconstruct_block_level, RESULTS_TABLES_DIR


def main() -> None:
    ensure_output_dirs()

    block_df = reconstruct_block_level()
    block_df["arrow_load"] = pd.Categorical(block_df["arrow_load"], categories=["low", "high"])
    block_df["flanker_consistency"] = pd.Categorical(
        block_df["flanker_consistency"], categories=["inconsistent", "consistent"]
    )

    model = smf.mixedlm(
        "congruency_effect_ms ~ C(arrow_load, Treatment('low')) * C(flanker_consistency, Treatment('inconsistent'))",
        block_df,
        groups=block_df["participant_id"],
    )
    fit = model.fit(reml=True, method="powell", maxiter=200, disp=False)

    conf_int = fit.conf_int()

    rows = [
        {
            "term": "Intercept (low, inconsistent)",
            "estimate": fit.params["Intercept"],
            "std_error": fit.bse["Intercept"],
            "z_value": fit.tvalues["Intercept"],
            "p_value": fit.pvalues["Intercept"],
            "ci_low": conf_int.loc["Intercept", 0],
            "ci_high": conf_int.loc["Intercept", 1],
        },
        {
            "term": "arrow_load[T.high]",
            "estimate": fit.params["C(arrow_load, Treatment('low'))[T.high]"],
            "std_error": fit.bse["C(arrow_load, Treatment('low'))[T.high]"],
            "z_value": fit.tvalues["C(arrow_load, Treatment('low'))[T.high]"],
            "p_value": fit.pvalues["C(arrow_load, Treatment('low'))[T.high]"],
            "ci_low": conf_int.loc["C(arrow_load, Treatment('low'))[T.high]", 0],
            "ci_high": conf_int.loc["C(arrow_load, Treatment('low'))[T.high]", 1],
        },
        {
            "term": "flanker_consistency[T.consistent]",
            "estimate": fit.params[
                "C(flanker_consistency, Treatment('inconsistent'))[T.consistent]"
            ],
            "std_error": fit.bse[
                "C(flanker_consistency, Treatment('inconsistent'))[T.consistent]"
            ],
            "z_value": fit.tvalues[
                "C(flanker_consistency, Treatment('inconsistent'))[T.consistent]"
            ],
            "p_value": fit.pvalues[
                "C(flanker_consistency, Treatment('inconsistent'))[T.consistent]"
            ],
            "ci_low": conf_int.loc[
                "C(flanker_consistency, Treatment('inconsistent'))[T.consistent]", 0
            ],
            "ci_high": conf_int.loc[
                "C(flanker_consistency, Treatment('inconsistent'))[T.consistent]", 1
            ],
        },
        {
            "term": "arrow_load[T.high]:flanker_consistency[T.consistent]",
            "estimate": fit.params[
                "C(arrow_load, Treatment('low'))[T.high]:C(flanker_consistency, Treatment('inconsistent'))[T.consistent]"
            ],
            "std_error": fit.bse[
                "C(arrow_load, Treatment('low'))[T.high]:C(flanker_consistency, Treatment('inconsistent'))[T.consistent]"
            ],
            "z_value": fit.tvalues[
                "C(arrow_load, Treatment('low'))[T.high]:C(flanker_consistency, Treatment('inconsistent'))[T.consistent]"
            ],
            "p_value": fit.pvalues[
                "C(arrow_load, Treatment('low'))[T.high]:C(flanker_consistency, Treatment('inconsistent'))[T.consistent]"
            ],
            "ci_low": conf_int.loc[
                "C(arrow_load, Treatment('low'))[T.high]:C(flanker_consistency, Treatment('inconsistent'))[T.consistent]",
                0,
            ],
            "ci_high": conf_int.loc[
                "C(arrow_load, Treatment('low'))[T.high]:C(flanker_consistency, Treatment('inconsistent'))[T.consistent]",
                1,
            ],
        },
        {
            "term": "random_intercept_variance",
            "estimate": fit.cov_re.iloc[0, 0],
            "std_error": None,
            "z_value": None,
            "p_value": None,
            "ci_low": None,
            "ci_high": None,
        },
        {
            "term": "residual_variance",
            "estimate": fit.scale,
            "std_error": None,
            "z_value": None,
            "p_value": None,
            "ci_low": None,
            "ci_high": None,
        },
    ]

    pd.DataFrame(rows).to_csv(
        RESULTS_TABLES_DIR / "block_level_mixed_model_coefficients.csv", index=False
    )

    with open(RESULTS_TABLES_DIR / "block_level_mixed_model_summary.txt", "w", encoding="utf-8") as f:
        f.write(str(fit.summary()))

    print("Saved block-level mixed-model coefficients and text summary.")


if __name__ == "__main__":
    main()

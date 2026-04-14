from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from utils import (
    ensure_output_dirs,
    reconstruct_block_level,
    make_subject_summary,
    RESULTS_FIGURES_DIR,
)


def main() -> None:
    ensure_output_dirs()

    block_df = reconstruct_block_level()
    summary_df = make_subject_summary(block_df)

    # Figure 1: condition means with 95% CI
    cond = (
        summary_df.groupby(["arrow_load", "flanker_consistency"])["mean_congruency_effect_ms"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    cond["se"] = cond["std"] / np.sqrt(cond["count"])
    cond["ci95"] = 1.96 * cond["se"]

    x_positions = {"inconsistent": 0, "consistent": 1}
    fig, ax = plt.subplots(figsize=(7, 5))

    for arrow_load in ["low", "high"]:
        sub = cond[cond["arrow_load"] == arrow_load].copy()
        xs = [x_positions[x] for x in sub["flanker_consistency"]]
        ax.errorbar(
            xs,
            sub["mean"],
            yerr=sub["ci95"],
            marker="o",
            linewidth=2,
            capsize=4,
            label=arrow_load,
        )

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Inconsistent", "Consistent"])
    ax.set_ylabel("Mean congruency effect (ms)")
    ax.set_xlabel("Flanker consistency")
    ax.set_title("Condition means with 95% CIs")
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.legend(title="Arrow load")
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES_DIR / "condition_means_95ci.png", dpi=300)
    plt.close(fig)

    # Figure 2: subject trajectories
    order = [
        ("low", "inconsistent"),
        ("low", "consistent"),
        ("high", "inconsistent"),
        ("high", "consistent"),
    ]
    label_map = {
        ("low", "inconsistent"): "Low/Inconsistent",
        ("low", "consistent"): "Low/Consistent",
        ("high", "inconsistent"): "High/Inconsistent",
        ("high", "consistent"): "High/Consistent",
    }

    wide = (
        summary_df.assign(condition=lambda d: list(zip(d["arrow_load"], d["flanker_consistency"])))
        .pivot_table(index="participant_id", columns="condition", values="mean_congruency_effect_ms")
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    xs = list(range(len(order)))
    for participant_id, row in wide.iterrows():
        ys = [row[c] for c in order]
        ax.plot(xs, ys, marker="o", alpha=0.5)

    ax.set_xticks(xs)
    ax.set_xticklabels([label_map[c] for c in order], rotation=20)
    ax.set_ylabel("Mean congruency effect (ms)")
    ax.set_title("Participant-level trajectories")
    ax.axhline(0, linestyle="--", linewidth=1)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES_DIR / "participant_trajectories.png", dpi=300)
    plt.close(fig)

    # Figure 3: block-level distributions
    block_df = block_df.copy()
    block_df["condition_label"] = (
        block_df["arrow_load"].str.capitalize()
        + "/"
        + block_df["flanker_consistency"].str.capitalize()
    )
    order_labels = [
        "Low/Inconsistent",
        "Low/Consistent",
        "High/Inconsistent",
        "High/Consistent",
    ]
    data = [block_df.loc[block_df["condition_label"] == label, "congruency_effect_ms"] for label in order_labels]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(data, labels=order_labels)
    ax.set_ylabel("Block-level congruency effect (ms)")
    ax.set_title("Block-level distributions by condition")
    ax.axhline(0, linestyle="--", linewidth=1)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES_DIR / "block_level_distributions.png", dpi=300)
    plt.close(fig)

    # Figure 4: error summary
    error_summary = (
        summary_df.groupby(["arrow_load", "flanker_consistency"])["mean_error_count"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    error_summary["se"] = error_summary["std"] / np.sqrt(error_summary["count"])

    fig, ax = plt.subplots(figsize=(7, 5))
    for arrow_load in ["low", "high"]:
        sub = error_summary[error_summary["arrow_load"] == arrow_load].copy()
        xs = [x_positions[x] for x in sub["flanker_consistency"]]
        ax.errorbar(
            xs,
            sub["mean"],
            yerr=sub["se"],
            marker="o",
            linewidth=2,
            capsize=4,
            label=arrow_load,
        )

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Inconsistent", "Consistent"])
    ax.set_ylabel("Mean error count")
    ax.set_xlabel("Flanker consistency")
    ax.set_title("Error patterns (descriptive)")
    ax.legend(title="Arrow load")
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES_DIR / "error_patterns.png", dpi=300)
    plt.close(fig)

    print("Saved four figures to results/figures.")


if __name__ == "__main__":
    main()

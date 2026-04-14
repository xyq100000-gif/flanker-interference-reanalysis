from __future__ import annotations

from pathlib import Path
import re
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
RESULTS_FIGURES_DIR = REPO_ROOT / "results" / "figures"


CONDITIONS = [
    ("low", "consistent", 2, 3, 4, 5, 6),
    ("low", "inconsistent", 7, 8, 9, 10, 11),
    ("high", "consistent", 12, 13, 14, 15, 16),
    ("high", "inconsistent", 17, 18, 19, 20, 21),
]


def load_raw_export() -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / "flanker_block_export.csv", header=None)


def reconstruct_block_level() -> pd.DataFrame:
    raw = load_raw_export()
    records: list[dict] = []
    participant: int | None = None
    replicate = 0

    for _, row in raw.iterrows():
        first_cell = row[0]

        if isinstance(first_cell, str) and first_cell.strip():
            match = re.search(r"(\d+)", first_cell)
            if match:
                participant = int(match.group(1))
                replicate = 0

        if (
            participant is not None
            and pd.notna(row[2])
            and not (isinstance(row[2], str) and "compatible" in row[2])
        ):
            replicate += 1

            for arrow_load, consistency, c_comp, c_incomp, c_effect, c_error, _c_avg in CONDITIONS:
                records.append(
                    {
                        "participant_id": participant,
                        "replicate_id": replicate,
                        "arrow_load": arrow_load,
                        "flanker_consistency": consistency,
                        "rt_congruent_ms": pd.to_numeric(row[c_comp], errors="coerce"),
                        "rt_incongruent_ms": pd.to_numeric(row[c_incomp], errors="coerce"),
                        "congruency_effect_ms": pd.to_numeric(row[c_effect], errors="coerce"),
                        "error_count": pd.to_numeric(row[c_error], errors="coerce"),
                    }
                )

    block_df = pd.DataFrame.from_records(records)
    return block_df


def make_subject_summary(block_df: pd.DataFrame) -> pd.DataFrame:
    summary_df = (
        block_df.groupby(
            ["participant_id", "arrow_load", "flanker_consistency"], as_index=False
        )
        .agg(
            mean_rt_congruent_ms=("rt_congruent_ms", "mean"),
            mean_rt_incongruent_ms=("rt_incongruent_ms", "mean"),
            mean_congruency_effect_ms=("congruency_effect_ms", "mean"),
            mean_error_count=("error_count", "mean"),
        )
    )
    return summary_df


def ensure_output_dirs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

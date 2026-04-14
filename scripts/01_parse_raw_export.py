from __future__ import annotations

from utils import ensure_output_dirs, reconstruct_block_level, make_subject_summary, PROCESSED_DIR


def main() -> None:
    ensure_output_dirs()

    block_df = reconstruct_block_level()
    summary_df = make_subject_summary(block_df)

    block_df.to_csv(PROCESSED_DIR / "flanker_block_level.csv", index=False)
    summary_df.to_csv(PROCESSED_DIR / "flanker_subject_summary.csv", index=False)

    print(f"Saved {len(block_df)} block-level rows.")
    print(f"Saved {len(summary_df)} subject-level summary rows.")


if __name__ == "__main__":
    main()

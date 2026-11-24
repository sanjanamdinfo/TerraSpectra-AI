import pandas as pd
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def preprocess_metadata(sensor):
    print(f"\n===== {sensor} METADATA PREPROCESSING =====")

    raw_file = RAW_DIR / f"{sensor}_data.csv"

    # Read original metadata
    df = pd.read_csv(
        raw_file,
        sep=";",
        encoding="cp1252",
        header=3
    )

    print("Original rows:", len(df))

    # Retain actual plant records only
    df = df.dropna(
        subset=["Pot [2]", "Genotype [3]", "Treatment [4]"]
    ).copy()

    # Rename identification columns
    df = df.rename(columns={
        "Pot [2]": "Pot",
        "Genotype [3]": "Genotype",
        "Treatment [4]": "Treatment"
    })

    # Save cleaned metadata
    output_file = PROCESSED_DIR / f"{sensor}_cleaned.csv"

    df.to_csv(output_file, index=False)

    print("Cleaned rows:", len(df))
    print("Columns:", len(df.columns))
    print("\nTreatment distribution:")
    print(df["Treatment"].value_counts())

    print("Missing values:", df.isna().sum().sum())
    print("Saved:", output_file)


def main():
    for sensor in ["VNIR", "SWIR"]:
        preprocess_metadata(sensor)

    print("\nBoth metadata datasets processed successfully!")


if __name__ == "__main__":
    main()
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data/raw/Data_description.csv"
OUTPUT_DIR = ROOT / "data/processed"
IMAGE_DIR = ROOT / "docs/images"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    df = pd.read_csv(
        INPUT_FILE,
        sep=";",
        encoding="cp1252",
        skiprows=2,
        usecols=range(6)
    )

    df = df.dropna(subset=["Pot [1]", "Treatment [5]"]).copy()

    df["Pot [1]"] = pd.to_numeric(df["Pot [1]"])
    df["Leaf [3]"] = pd.to_numeric(df["Leaf [3]"])
    df["Confidence level [6]"] = pd.to_numeric(
        df["Confidence level [6]"]
    )

    return df


def save_plot(filename):
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()
    print("Generated:", filename)


def main():
    df = load_data()

    print("SAMPLE-LEVEL EDA")
    print("=" * 50)
    print("Total leaf records:", len(df))
    print("Unique pots:", df["Pot [1]"].nunique())
    print("Unique genotypes:", df["Genotype [4]"].nunique())

    # 1. Treatment distribution
    treatment_counts = df["Treatment [5]"].value_counts()

    plt.figure(figsize=(7, 5))
    treatment_counts.plot(kind="bar")
    plt.title("Leaf Distribution by Treatment")
    plt.xlabel("Treatment")
    plt.ylabel("Number of Leaf Records")
    plt.xticks(rotation=0)
    save_plot("sample_eda_treatment.png")

    # 2. Genotype distribution
    genotype_counts = df["Genotype [4]"].value_counts()

    plt.figure(figsize=(7, 5))
    genotype_counts.plot(kind="bar")
    plt.title("Leaf Distribution by Genotype")
    plt.xlabel("Genotype")
    plt.ylabel("Number of Leaf Records")
    plt.xticks(rotation=0)
    save_plot("sample_eda_genotype.png")

    # 3. Side distribution
    side_counts = df["Side [2]"].value_counts()

    plt.figure(figsize=(7, 5))
    side_counts.plot(kind="bar")
    plt.title("Leaf Distribution by Pot Side")
    plt.xlabel("Pot Side")
    plt.ylabel("Number of Leaf Records")
    plt.xticks(rotation=0)
    save_plot("sample_eda_side.png")

    # 4. Infection confidence distribution
    confidence_counts = df["Confidence level [6]"].value_counts().sort_index()

    plt.figure(figsize=(7, 5))
    confidence_counts.plot(kind="bar")
    plt.title("Infection Confidence Distribution")
    plt.xlabel("Confidence Level (1 = High, 2 = Low)")
    plt.ylabel("Number of Leaf Records")
    plt.xticks(rotation=0)
    save_plot("sample_eda_confidence.png")

    # 5. Leaf count per pot
    leaves_per_pot = df.groupby("Pot [1]").size()

    plt.figure(figsize=(12, 5))
    leaves_per_pot.plot(kind="bar")
    plt.title("Number of Leaf Records per Pot")
    plt.xlabel("Pot Number")
    plt.ylabel("Number of Leaf Records")
    plt.xticks(rotation=90)
    save_plot("sample_eda_leaves_per_pot.png")

    # Save summary tables
    summary = pd.DataFrame({
        "Metric": [
            "Total leaf records",
            "Unique pots",
            "Unique genotypes",
            "Unique pot sides",
            "High-confidence records",
            "Low-confidence records",
            "Duplicate pot-side-leaf records",
            "Missing values"
        ],
        "Value": [
            len(df),
            df["Pot [1]"].nunique(),
            df["Genotype [4]"].nunique(),
            df["Side [2]"].nunique(),
            (df["Confidence level [6]"] == 1).sum(),
            (df["Confidence level [6]"] == 2).sum(),
            df.duplicated(
                ["Pot [1]", "Side [2]", "Leaf [3]"]
            ).sum(),
            int(df.isnull().sum().sum())
        ]
    })

    summary.to_csv(
        OUTPUT_DIR / "sample_eda_summary.csv",
        index=False
    )

    leaves_per_pot.rename(
        "Leaf_Count"
    ).to_csv(
        OUTPUT_DIR / "sample_eda_leaves_per_pot.csv"
    )

    print("\nEDA SUMMARY")
    print(summary.to_string(index=False))

    print("\nEDA completed successfully.")


if __name__ == "__main__":
    main()

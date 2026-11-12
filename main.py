import pandas as pd

# Load cleaned datasets
swir = pd.read_csv("data/processed/SWIR_cleaned.csv")
vnir = pd.read_csv("data/processed/VNIR_cleaned.csv")

def prepare_data(df, name):

    # Remove rows without sample identification
    df = df.dropna(
        subset=["Pot", "Genotype", "Treatment"]
    ).copy()

    # Remove rows without treatment labels
    df = df[
        df["Treatment"].isin(
            ["Infected", "Non-infected"]
        )
    ]

    print(f"\n===== {name} PREPARED DATA =====")
    print("Total valid samples:", len(df))
    print("\nTreatment distribution:")
    print(df["Treatment"].value_counts())

    print("\nGenotype distribution:")
    print(df["Genotype"].value_counts())

    return df


swir_prepared = prepare_data(swir, "SWIR")
vnir_prepared = prepare_data(vnir, "VNIR")

# Save prepared datasets
swir_prepared.to_csv(
    "data/processed/SWIR_prepared.csv",
    index=False
)

vnir_prepared.to_csv(
    "data/processed/VNIR_prepared.csv",
    index=False
)

print("\nPrepared datasets saved successfully!")
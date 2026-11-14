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
# =====================================
# PREPARED DATASET STRUCTURE INSPECTION
# =====================================

print("\n===== SWIR DATASET INSPECTION =====")

print("\nSWIR shape:")
print(swir_prepared.shape)

print("\nSWIR column names:")
print(swir_prepared.columns.tolist())

print("\nSWIR first 5 rows:")
print(swir_prepared.head())

print("\n===== VNIR DATASET INSPECTION =====")

print("\nVNIR shape:")
print(vnir_prepared.shape)

print("\nVNIR column names:")
print(vnir_prepared.columns.tolist())

print("\nVNIR first 5 rows:")
print(vnir_prepared.head())

# =====================================
# CORRECT DATA DESCRIPTION READING
# =====================================

description_corrected = pd.read_csv(
    "data/raw/Data_description.csv",
    sep=";",
    encoding="cp1252",
    header=2
)

print("\n===== CORRECTED DATA DESCRIPTION =====")

print("\nDataset shape:")
print(description_corrected.shape)

print("\nCorrect column names:")
print(description_corrected.columns.tolist())

print("\nFirst 10 records:")
print(description_corrected.head(10).to_string())

print("\nLast 10 records:")
print(description_corrected.tail(10).to_string())
# =====================================
# CORRECT DATA DESCRIPTION READING
# =====================================
# =====================================
# MISSING VALUE INSPECTION
# =====================================

print("\n===== SWIR MISSING VALUES =====")
print(swir_prepared.isnull().sum())

print("\nTotal SWIR missing values:")
print(swir_prepared.isnull().sum().sum())

print("\n===== VNIR MISSING VALUES =====")
print(vnir_prepared.isnull().sum())

print("\nTotal VNIR missing values:")
print(vnir_prepared.isnull().sum().sum())
# =====================================
# COMPLETELY EMPTY COLUMN INSPECTION
# =====================================

print("\n===== SWIR COMPLETELY EMPTY COLUMNS =====")
print(swir_prepared.columns[swir_prepared.isnull().all()].tolist())

print("\n===== VNIR COMPLETELY EMPTY COLUMNS =====")
print(vnir_prepared.columns[vnir_prepared.isnull().all()].tolist())
# =====================================
# MISSING VALUE PERCENTAGE
# =====================================

print("\n===== SWIR MISSING VALUE PERCENTAGE =====")

swir_missing_percentage = (
    swir_prepared.isnull().mean() * 100
)

print(swir_missing_percentage.round(2))


print("\n===== VNIR MISSING VALUE PERCENTAGE =====")

vnir_missing_percentage = (
    vnir_prepared.isnull().mean() * 100
)

print(vnir_missing_percentage.round(2))
# =====================================
# PREPARED DATA TYPE INSPECTION
# =====================================

print("\n===== SWIR DATA TYPES =====")
print(swir_prepared.dtypes)

print("\n===== SWIR FIRST SAMPLE RECORD =====")
print(swir_prepared.iloc[0].to_string())


print("\n===== VNIR DATA TYPES =====")
print(vnir_prepared.dtypes)

print("\n===== VNIR FIRST SAMPLE RECORD =====")
print(vnir_prepared.iloc[0].to_string())
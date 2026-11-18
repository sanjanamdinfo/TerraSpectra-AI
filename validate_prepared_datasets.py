import pandas as pd
import numpy as np
from pathlib import Path

# Project paths
DATA_DIR = Path("data/processed")

FILES = {
    "VNIR": DATA_DIR / "VNIR_prepared.csv",
    "SWIR": DATA_DIR / "SWIR_prepared.csv"
}

results = []

print("\n" + "=" * 65)
print("TERRASPECTRA-AI: PREPARED DATASET VALIDATION")
print("=" * 65)

# Validate each dataset
for sensor, file_path in FILES.items():

    # Check whether the file exists
    if not file_path.exists():
        print(f"\nFile not found: {file_path}")
        continue

    df = pd.read_csv(file_path)

    print(f"\n\n{'=' * 50}")
    print(f"{sensor} DATASET")
    print("=" * 50)

    # 1. Dataset dimensions
    print("\n1. Dataset Shape")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    # 2. Missing values
    missing_total = int(df.isnull().sum().sum())

    print("\n2. Missing Values")
    print("Total missing values:", missing_total)

    missing_by_column = df.isnull().sum()
    print("\nMissing values by column:")
    print(missing_by_column[missing_by_column > 0])

    # 3. Duplicate records
    duplicate_rows = int(df.duplicated().sum())
    duplicate_pots = int(df["Pot"].duplicated().sum())

    print("\n3. Duplicate Records")
    print("Duplicate rows:", duplicate_rows)
    print("Duplicate Pot IDs:", duplicate_pots)

    # 4. Treatment distribution
    treatment_counts = df["Treatment"].value_counts()

    print("\n4. Treatment Distribution")
    print(treatment_counts)

    # 5. Genotype distribution
    genotype_counts = df["Genotype"].value_counts()

    print("\n5. Genotype Distribution")
    print(genotype_counts)

    # 6. Treatment vs Genotype
    print("\n6. Treatment vs Genotype")
    print(pd.crosstab(df["Genotype"], df["Treatment"]))

    # 7. Infinite values
    numeric_df = df.select_dtypes(include=np.number)

    infinite_count = int(
        np.isinf(numeric_df.to_numpy()).sum()
    )

    print("\n7. Infinite Values")
    print("Total infinite values:", infinite_count)

    # 8. Completely empty columns
    empty_column_names = df.columns[df.isnull().all()].tolist()
    empty_columns = len(empty_column_names)

    print("\n8. Completely Empty Columns")
    print("Count:", empty_columns)
    print("Empty column names:", empty_column_names)

    # 9. Save validation results
    results.append({
        "Sensor": sensor,
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing_Values": missing_total,
        "Duplicate_Rows": duplicate_rows,
        "Duplicate_Pot_IDs": duplicate_pots,
        "Infinite_Values": infinite_count,
        "Completely_Empty_Columns": empty_columns,
        "Empty_Column_Names": ", ".join(empty_column_names)
    })


# 10. Save validation summary
if results:

    report = pd.DataFrame(results)

    output_file = DATA_DIR / "prepared_dataset_validation.csv"

    report.to_csv(output_file, index=False)

    print("\n\n" + "=" * 65)
    print("VALIDATION SUMMARY")
    print("=" * 65)

    print(report.to_string(index=False))

    print("\nValidation report saved to:")
    print(output_file)

    print("\nDataset validation completed successfully!")

else:
    print("\nNo datasets were available for validation.")

import csv
from pathlib import Path
from collections import defaultdict
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_dataset(filename, sensor):

    file_path = RAW_DIR / filename

    print(f"\n{'=' * 55}")
    print(f"ANALYSING {sensor} DATA")
    print(f"{'=' * 55}")

    with open(file_path, "r", encoding="cp1252", newline="") as file:
        rows = list(csv.reader(file, delimiter=";"))

    # Locate the actual column header
    header_index = next(
        i for i, row in enumerate(rows)
        if row and row[0].strip().startswith("Pot")
    )

    date_row = rows[header_index - 1]
    header_row = rows[header_index]

    # Extract valid pot records
    data_rows = [
        row for row in rows[header_index + 1:]
        if row and row[0].strip().isdigit()
    ]

    print("Total pot records:", len(data_rows))

    # Identify observation dates and corresponding G/D columns
    date_columns = []

    for col in range(3, len(header_row), 2):

        if col >= len(date_row):
            continue

        date = date_row[col].strip()

        if date:
            date_columns.append((date, col, col + 1))

    print("Observation dates:", len(date_columns))

    summary = defaultdict(lambda: {
        "Total_Pot_Records": 0,
        "Numeric_Entries": 0,
        "Total_Leaves_Recorded": 0,
        "Empty_Cells": 0,
        "Technical_NA": 0,
        "Unexpected_Values": 0
    })

    group_summary = defaultdict(lambda: {
        "Total_Pot_Records": 0,
        "Numeric_Entries": 0,
        "Total_Leaves_Recorded": 0,
        "Empty_Cells": 0,
        "Technical_NA": 0,
        "Unexpected_Values": 0
    })

    for row in data_rows:

        genotype = row[1].strip()
        treatment = row[2].strip()

        for date, g_col, d_col in date_columns:

            for side, col in [("G", g_col), ("D", d_col)]:

                value = row[col].strip() if col < len(row) else ""

                keys = [
                    (sensor, date, side),
                    (sensor, date, side, treatment, genotype)
                ]

                for key, target in zip(
                    keys, [summary, group_summary]
                ):

                    result = target[key]
                    result["Total_Pot_Records"] += 1

                    if value == "":
                        result["Empty_Cells"] += 1

                    elif value.upper() == "NA":
                        result["Technical_NA"] += 1

                    else:
                        try:
                            number = int(value)

                            if number < 0:
                                raise ValueError

                            result["Numeric_Entries"] += 1
                            result["Total_Leaves_Recorded"] += number

                        except ValueError:
                            result["Unexpected_Values"] += 1

    # Convert summaries to DataFrames
    summary_df = pd.DataFrame([
        {
            "Sensor": key[0],
            "Date_DPI": key[1],
            "Side": key[2],
            **values
        }
        for key, values in summary.items()
    ])

    group_df = pd.DataFrame([
        {
            "Sensor": key[0],
            "Date_DPI": key[1],
            "Side": key[2],
            "Treatment": key[3],
            "Genotype": key[4],
            **values
        }
        for key, values in group_summary.items()
    ])

    print("\nAcquisition Summary:")
    print(summary_df.to_string(index=False))

    print("\nMissing Data Summary:")
    print("Empty cells:", summary_df["Empty_Cells"].sum())
    print("Technical NA:", summary_df["Technical_NA"].sum())

    return summary_df, group_df


# Analyse both datasets
swir_summary, swir_groups = analyze_dataset(
    "SWIR_data.csv", "SWIR"
)

vnir_summary, vnir_groups = analyze_dataset(
    "VNIR_data.csv", "VNIR"
)

# Combine results
all_summary = pd.concat(
    [vnir_summary, swir_summary],
    ignore_index=True
)

all_groups = pd.concat(
    [vnir_groups, swir_groups],
    ignore_index=True
)

# Save results
all_summary.to_csv(
    OUTPUT_DIR / "acquisition_completeness_summary.csv",
    index=False
)

all_groups.to_csv(
    OUTPUT_DIR / "acquisition_completeness_by_group.csv",
    index=False
)

print("\n" + "=" * 55)
print("ACQUISITION ANALYSIS COMPLETED")
print("=" * 55)

print("\nGenerated files:")
print("1. acquisition_completeness_summary.csv")
print("2. acquisition_completeness_by_group.csv")
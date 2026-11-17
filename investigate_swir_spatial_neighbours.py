import os
import numpy as np
import pandas as pd

# --------------------------------------------------
# 1. FILE PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw", "SWIR_sample")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")

HDR_FILE = os.path.join(RAW_DIR, "01_D.hdr")
IMAGE_FILE = os.path.join(RAW_DIR, "01_D.hyspex")
COORD_FILE = os.path.join(RAW_DIR, "01_D_leaf1.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# 2. SWIR IMAGE INFORMATION
# --------------------------------------------------

LINES = 420
SAMPLES = 320
BANDS = 256
OFFSET = 1974272

# --------------------------------------------------
# 3. LOAD LEAF COORDINATES
# --------------------------------------------------

coordinates = pd.read_csv(COORD_FILE, header=None)
coordinates.columns = ["row", "col"]

leaf_pixels = set(
    zip(coordinates["row"], coordinates["col"])
)

print("\n===== COORDINATE INFORMATION =====")
print("Total leaf pixels:", len(leaf_pixels))

# --------------------------------------------------
# 4. LOAD SWIR IMAGE
# --------------------------------------------------

from spectral import open_image

img = open_image(HDR_FILE)
swir = img.load()

print("SWIR image shape:", swir.shape)
print("Interleave:", img.metadata.get("interleave"))

if swir.shape != (420, 320, 256):
    raise ValueError("Unexpected SWIR image dimensions.")
# --------------------------------------------------
# 5. SIX ZERO-VALUE MEASUREMENTS
# --------------------------------------------------

zero_pixels = [
    (149, 182, 248),
    (149, 290, 163),
    (149, 296, 165),
    (150, 158, 214),
    (150, 165, 13),
    (150, 290, 163)
]
# --------------------------------------------------
# 5A. VERIFY ZERO-VALUE MEASUREMENTS
# --------------------------------------------------

print("\n===== VERIFYING SIX ZERO POSITIONS =====")

for row, col, band in zero_pixels:
    value = int(swir[row, col, band])

    print(
        f"Row={row}, Column={col}, "
        f"Band={band}, Value={value}"
    )
# --------------------------------------------------
# 6. CHECK SPATIAL NEIGHBOURS
# --------------------------------------------------

results = []

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

print("\n===== VERIFYING SIX ZERO POSITIONS =====")

for row, col, band in zero_pixels:

    target_value = int(swir[row, col, band])

    print(
        f"Row={row}, Column={col}, "
        f"Band={band}, Value={target_value}"
    )

print("\n===== SPATIAL NEIGHBOUR ANALYSIS =====")

for row, col, band in zero_pixels:

    print(f"\nChecking row={row}, col={col}, band={band}")

    if (row, col) not in leaf_pixels:
        print("WARNING: Target coordinate not found in leaf mask.")
        continue

    target_value = int(swir[row, col, band])

    print("Target pixel value:", target_value)

    for dr, dc in directions:

        neighbour_row = row + dr
        neighbour_col = col + dc

        if (neighbour_row, neighbour_col) not in leaf_pixels:
            continue

        value = int(swir[neighbour_row, neighbour_col, band])

        results.append({
            "target_row": row,
            "target_col": col,
            "band": band,
            "neighbour_row": neighbour_row,
            "neighbour_col": neighbour_col,
            "direction_row": dr,
            "direction_col": dc,
            "neighbour_value": value,
            "neighbour_is_zero": value == 0
        })

        print(
            f"Neighbour ({neighbour_row}, {neighbour_col}) "
            f"Value: {value}"
        )
# --------------------------------------------------
# 7. SAVE RESULTS
# --------------------------------------------------

results_df = pd.DataFrame(results)

output_file = os.path.join(
    OUTPUT_DIR,
    "SWIR_spatial_neighbour_analysis.csv"
)

results_df.to_csv(output_file, index=False)

# --------------------------------------------------
# 8. SUMMARY
# --------------------------------------------------

print("\n===== SPATIAL NEIGHBOUR INVESTIGATION =====")

print("Zero measurements checked:", len(zero_pixels))
print("Neighbour observations:", len(results_df))

if not results_df.empty:

    print(
        "Zero-valued neighbours:",
        results_df["neighbour_is_zero"].sum()
    )

    print(
        "Non-zero neighbours:",
        (~results_df["neighbour_is_zero"]).sum()
    )

    print("\nResults by target pixel:")

    print(
        results_df.groupby(
            ["target_row", "target_col", "band"]
        )["neighbour_value"].agg(
            ["count", "min", "max", "mean"]
        )
    )

print("\nResults saved to:")
print(output_file)

print("\nInvestigation completed.")
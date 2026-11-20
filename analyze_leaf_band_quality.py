import numpy as np
import pandas as pd
from spectral import open_image

# Load SWIR image
img = open_image("data/raw/SWIR_sample/01_D.hdr")
data = img.load()

# Load leaf coordinates
coords = pd.read_csv(
    "data/raw/SWIR_sample/01_D_leaf1.csv",
    header=None
)

leaf_coords = set(map(tuple, coords.to_numpy()))

zero_pixels = [
    (149, 182, 248),
    (149, 290, 163),
    (149, 296, 165),
    (150, 158, 214),
    (150, 165, 13),
    (150, 290, 163)
]

print("===== LEAF-SPECIFIC BAND QUALITY =====")

for row, col, band in zero_pixels:

    neighbour_values = []

    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):

            if (r, c) == (row, col):
                continue

            if (r, c) in leaf_coords:
                neighbour_values.append(
                    int(data[r, c, band])
                )

    leaf_band_values = np.array([
        data[r, c, band]
        for r, c in leaf_coords
    ])

    print(f"\nPixel: ({row}, {col})")
    print("Band:", band)
    print("Target value:", int(data[row, col, band]))

    print("Leaf neighbours:", neighbour_values)

    print(
        "Leaf neighbour count:",
        len(neighbour_values)
    )

    print(
        "Zero values across leaf in this band:",
        np.count_nonzero(leaf_band_values == 0)
    )

    print(
        "Total leaf pixels:",
        len(leaf_band_values)
    )

    print(
        "Leaf band median:",
        round(float(np.median(leaf_band_values)), 2)
    )

print("\nLeaf-specific validation completed.")
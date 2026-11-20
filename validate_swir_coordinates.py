import pandas as pd
import numpy as np
from spectral import open_image

# Load SWIR image
img = open_image("data/raw/SWIR_sample/01_D.hdr")
data = img.load()

# Load leaf coordinates
coords = pd.read_csv(
    "data/raw/SWIR_sample/01_D_leaf1.csv",
    header=None
)

leaf_coordinates = set(
    map(tuple, coords.to_numpy())
)

# Six previously identified pixels
zero_pixels = [
    (149, 182, 248),
    (149, 290, 163),
    (149, 296, 165),
    (150, 158, 214),
    (150, 165, 13),
    (150, 290, 163)
]

print("===== SWIR COORDINATE VALIDATION =====")

for row, col, band in zero_pixels:

    value = int(data[row, col, band])

    is_leaf = (row, col) in leaf_coordinates

    spectrum = data[row, col, :]

    print(f"\nPixel: ({row}, {col})")
    print("Band:", band)
    print("Measurement:", value)
    print("Belongs to leaf:", is_leaf)
    print("Zero bands:", np.count_nonzero(spectrum == 0))
    print("Ignore-value bands:", np.count_nonzero(spectrum == 16383))

print("\n===== VALIDATION COMPLETED =====")
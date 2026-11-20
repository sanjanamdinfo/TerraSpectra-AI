import numpy as np
import pandas as pd
from spectral import open_image

# Load SWIR image
img = open_image("data/raw/SWIR_sample/01_D.hdr")
data = img.load()

print("Image shape:", data.shape)

# Load leaf coordinates
coords = pd.read_csv(
    "data/raw/SWIR_sample/01_D_leaf1.csv",
    header=None
)

coordinates = coords.to_numpy(dtype=int)

# Extract and flatten each leaf spectrum
leaf_spectra = np.stack([
    np.asarray(data[row, col, :]).reshape(-1)
    for row, col in coordinates
])

print("\n===== COMPLETE SWIR BAND QUALITY ANALYSIS =====")

print("Leaf spectra shape:", leaf_spectra.shape)
print("Total leaf pixels:", leaf_spectra.shape[0])
print("Total spectral bands:", leaf_spectra.shape[1])

# Verify dimensions
if leaf_spectra.shape[1] != 256:
    raise ValueError("Expected 256 spectral bands. Check image indexing.")

# Band-wise analysis
zero_counts = np.count_nonzero(leaf_spectra == 0, axis=0)

ignore_counts = np.count_nonzero(
    leaf_spectra == 16383,
    axis=0
)

print("\n===== BAND-WISE QUALITY =====")

for band in range(leaf_spectra.shape[1]):

    if zero_counts[band] > 0 or ignore_counts[band] > 0:

        print(
            f"Band {band}: "
            f"Zeros={zero_counts[band]}, "
            f"Ignore values={ignore_counts[band]}"
        )

print("\n===== SUMMARY =====")

print(
    "Total zero measurements:",
    np.count_nonzero(leaf_spectra == 0)
)

print(
    "Total ignore measurements:",
    np.count_nonzero(leaf_spectra == 16383)
)

print(
    "Bands containing zeros:",
    np.count_nonzero(zero_counts)
)

print(
    "Bands containing ignore values:",
    np.count_nonzero(ignore_counts)
)

print("\nAnalysis completed successfully.")
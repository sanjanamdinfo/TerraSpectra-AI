import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spectral import open_image

# File paths
HDR_PATH = "data/raw/SWIR_sample/01_D.hdr"
CSV_PATH = "data/raw/SWIR_sample/01_D_leaf1.csv"

# Load hyperspectral image
print("Loading SWIR image...")

img = open_image(HDR_PATH)
data = img.load()

print("Image shape:", data.shape)

# Create a 2D image using mean across spectral bands
background = np.mean(data, axis=2)

# Load leaf coordinates
coordinates = pd.read_csv(CSV_PATH, header=None)

x = coordinates[0]
y = coordinates[1]

# Create two visual comparisons
fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# Orientation 1: X = column, Y = row
axes[0].imshow(background, cmap="gray", origin="upper")
axes[0].scatter(x, y, s=2, c="red")

axes[0].set_title("Orientation 1: X = Column, Y = Row")
axes[0].set_xlabel("Image Column")
axes[0].set_ylabel("Image Row")

# Orientation 2: X = row, Y = column
axes[1].imshow(background, cmap="gray", origin="upper")
axes[1].scatter(y, x, s=2, c="red")

axes[1].set_title("Orientation 2: X = Row, Y = Column")
axes[1].set_xlabel("Image Column")
axes[1].set_ylabel("Image Row")

plt.tight_layout()

plt.savefig(
    "data/processed/SWIR_coordinate_orientation_comparison.png",
    dpi=300
)

plt.show()

print("\nCoordinate comparison completed.")
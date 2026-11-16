import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spectral import open_image

# Load SWIR image
img = open_image("data/raw/SWIR_sample/01_D.hdr")
data = img.load()

# Load coordinates
coordinates = pd.read_csv(
    "data/raw/SWIR_sample/01_D_leaf1.csv",
    header=None
)

# Corrected provisional mapping
rows = coordinates[0].to_numpy()
cols = coordinates[1].to_numpy()

# Extract leaf spectra
leaf_spectra = data[rows, cols, :]

print("Image shape:", data.shape)
print("Coordinate count:", len(coordinates))
print("Leaf spectra shape:", leaf_spectra.shape)

# Visualize coordinates
background = np.mean(data, axis=2)

plt.figure(figsize=(12, 7))
plt.imshow(background, cmap="gray", origin="upper")
plt.scatter(cols, rows, s=2, c="red")

plt.title("SWIR Leaf 1 - Provisional Coordinate Mapping")
plt.xlabel("Image Column")
plt.ylabel("Image Row")

plt.tight_layout()

plt.savefig(
    "data/processed/SWIR_leaf1_coordinate_verification.png",
    dpi=300
)

plt.show()
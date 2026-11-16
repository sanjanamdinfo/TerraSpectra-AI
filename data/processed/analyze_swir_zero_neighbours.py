import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spectral import open_image

# Load image
img = open_image("data/raw/SWIR_sample/01_D.hdr")
data = img.load()

# Load coordinates
coordinates = pd.read_csv(
    "data/raw/SWIR_sample/01_D_leaf1.csv",
    header=None
)

rows = coordinates[0].to_numpy()
cols = coordinates[1].to_numpy()

# Extract spectra
leaf_spectra = data[rows, cols, :]

# Find zero measurements
pixel_indices, band_indices = np.where(leaf_spectra == 0)

wavelengths = np.asarray(
    img.metadata["wavelength"],
    dtype=float
)

results = []

# Investigate neighbouring bands
for pixel, band in zip(pixel_indices, band_indices):

    for neighbour_band in range(
        max(0, band - 2),
        min(leaf_spectra.shape[1], band + 3)
    ):

        results.append({
            "Pixel_Index": pixel,
            "Image_Row": rows[pixel],
            "Image_Column": cols[pixel],
            "Zero_Band": band,
            "Neighbour_Band": neighbour_band,
            "Wavelength_nm": wavelengths[neighbour_band],
            "Spectral_Value": leaf_spectra[
                pixel, neighbour_band
            ],
            "Is_Zero_Band": neighbour_band == band
        })

# Create DataFrame
df = pd.DataFrame(results)

# Save results
df.to_csv(
    "data/processed/SWIR_zero_neighbour_analysis.csv",
    index=False
)

print("\n========== ZERO NEIGHBOUR ANALYSIS ==========")

print(df.to_string(index=False))

# Plot neighbouring spectral values
plt.figure(figsize=(12, 6))

for pixel, group in df.groupby("Pixel_Index"):

    plt.plot(
        group["Neighbour_Band"],
        group["Spectral_Value"],
        marker="o",
        label=f"Pixel {pixel}"
    )

plt.title("SWIR Spectral Values Around Zero Measurements")
plt.xlabel("Spectral Band Index")
plt.ylabel("Raw Spectral Value")
plt.legend(fontsize=8)
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "data/processed/SWIR_zero_neighbour_analysis.png",
    dpi=300
)

plt.close()

print("\nNeighbouring band investigation completed!")
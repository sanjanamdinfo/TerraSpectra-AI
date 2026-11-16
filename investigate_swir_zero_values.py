
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spectral import open_image
import os

# ------------------------------------------
# 1. Load SWIR hyperspectral image
# ------------------------------------------

print("Loading SWIR image...")

img = open_image("data/raw/SWIR_sample/01_D.hdr")
data = img.load()

# ------------------------------------------
# 2. Load leaf coordinates
# ------------------------------------------

coordinates = pd.read_csv(
    "data/raw/SWIR_sample/01_D_leaf1.csv",
    header=None
)

# Provisional coordinate mapping
rows = coordinates[0].to_numpy()
cols = coordinates[1].to_numpy()

# Check coordinate boundaries
if (
    np.any(rows < 0) or np.any(rows >= data.shape[0])
    or np.any(cols < 0) or np.any(cols >= data.shape[1])
):
    raise ValueError("Some coordinates are outside the image boundaries.")

# ------------------------------------------
# 3. Extract leaf spectra
# ------------------------------------------

leaf_spectra = data[rows, cols, :]

print("\n========== SWIR ZERO VALUE INVESTIGATION ==========")

print("Image shape:", data.shape)
print("Leaf spectra shape:", leaf_spectra.shape)

# ------------------------------------------
# 4. Identify zero values
# ------------------------------------------

zero_positions = np.where(leaf_spectra == 0)

pixel_indices = zero_positions[0]
band_indices = zero_positions[1]

total_zeros = len(pixel_indices)

print("\nTotal zero measurements:", total_zeros)
print("Total leaf pixels:", len(leaf_spectra))
print("Total spectral bands:", leaf_spectra.shape[1])

if total_zeros == 0:
    print("\nNo zero measurements found.")

else:

    # ------------------------------------------
    # 5. Create zero-value details
    # ------------------------------------------

    zero_details = pd.DataFrame({
        "Pixel_Index": pixel_indices,
        "Image_Row": rows[pixel_indices],
        "Image_Column": cols[pixel_indices],
        "Band_Index": band_indices,
        "Zero_Value": 0
    })

    # Add wavelength information if available
    wavelengths = img.metadata.get("wavelength")

    if wavelengths is not None:
        zero_details["Wavelength_nm"] = np.asarray(
            wavelengths, dtype=float
        )[band_indices]

    zero_details.to_csv(
        "data/processed/SWIR_zero_value_details.csv",
        index=False
    )

    print("\nZero-value details:")
    print(zero_details.to_string(index=False))

    # ------------------------------------------
    # 6. Count zero values per band
    # ------------------------------------------

    zero_counts = np.bincount(
        band_indices,
        minlength=leaf_spectra.shape[1]
    )

    zero_band_df = pd.DataFrame({
        "Band_Index": np.arange(leaf_spectra.shape[1]),
        "Zero_Count": zero_counts
    })

    if wavelengths is not None:
        zero_band_df["Wavelength_nm"] = np.asarray(
            wavelengths, dtype=float
        )

    zero_band_df.to_csv(
        "data/processed/SWIR_zero_values_per_band.csv",
        index=False
    )

    print("\nBands containing zero values:")
    print(zero_band_df[zero_band_df["Zero_Count"] > 0])

    # ------------------------------------------
    # 7. Visualize zero-value distribution
    # ------------------------------------------

    background = np.mean(data, axis=2)

    plt.figure(figsize=(12, 7))

    plt.imshow(
        background,
        cmap="gray",
        origin="upper"
    )

    plt.scatter(
        cols,
        rows,
        s=2,
        c="blue",
        label="Leaf pixels"
    )

    plt.scatter(
        cols[pixel_indices],
        rows[pixel_indices],
        s=35,
        c="red",
        label="Zero-value pixels"
    )

    plt.title("SWIR Leaf 1 - Zero-Value Pixel Locations")
    plt.xlabel("Image Column")
    plt.ylabel("Image Row")
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "data/processed/SWIR_zero_value_locations.png",
        dpi=300
    )

    plt.close()

    # ------------------------------------------
    # 8. Plot zero values per spectral band
    # ------------------------------------------

    plt.figure(figsize=(12, 5))

    plt.bar(
        zero_band_df["Band_Index"],
        zero_band_df["Zero_Count"]
    )

    plt.title("SWIR Zero Values Across Spectral Bands")
    plt.xlabel("Spectral Band Index")
    plt.ylabel("Number of Zero Measurements")

    plt.tight_layout()

    plt.savefig(
        "data/processed/SWIR_zero_values_per_band.png",
        dpi=300
    )

    plt.close()

print("\nInvestigation completed successfully!")
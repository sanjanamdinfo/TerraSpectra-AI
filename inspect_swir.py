import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spectral import envi


# ==========================================
# 1. LOAD SWIR HYPERSPECTRAL IMAGE
# ==========================================

header_path = "data/raw/SWIR_sample/01_D.hdr"
image_path = "data/raw/SWIR_sample/01_D.hyspex"

img = envi.open(header_path, image_path)

print("===== SWIR IMAGE INFORMATION =====")

print("Image dimensions:", img.shape)
print("Number of wavelength bands:", img.shape[2])

wavelengths = np.array(img.metadata["wavelength"], dtype=float)

print(
    "Wavelength range:",
    wavelengths[0],
    "to",
    wavelengths[-1],
    "nm"
)


# ==========================================
# 2. LOAD SPECTRAL DATA
# ==========================================

data = img.load()

print("\n===== SPECTRAL DATA INSPECTION =====")

print("Data shape:", data.shape)
print("Data type:", data.dtype)
print("Minimum value:", np.min(data))
print("Maximum value:", np.max(data))
print("Mean value:", np.mean(data))

ignore_value = int(img.metadata["data ignore value"])

print("Ignore value:", ignore_value)
print("Ignored pixels:", np.sum(data == ignore_value))


# ==========================================
# 3. DATA QUALITY CHECK
# ==========================================

print("\n===== DATA QUALITY CHECK =====")

print("Total values:", data.size)
print("Zero values:", np.sum(data == 0))
print("Maximum values (65535):", np.sum(data == 65535))
print("NaN values:", np.sum(np.isnan(data)))
print("Infinite values:", np.sum(np.isinf(data)))


# ==========================================
# 4. VALUE DISTRIBUTION
# ==========================================

print("\n===== VALUE DISTRIBUTION =====")

print("25th percentile:", np.percentile(data, 25))
print("50th percentile:", np.percentile(data, 50))
print("75th percentile:", np.percentile(data, 75))
print("95th percentile:", np.percentile(data, 95))


# ==========================================
# 5. LOAD LEAF COORDINATES
# ==========================================

leaf_path = "data/raw/SWIR_sample/01_D_leaf1.csv"

leaf_df = pd.read_csv(
    leaf_path,
    header=None,
    names=["X", "Y"]
)

print("\n===== LEAF COORDINATE INFORMATION =====")

print("Shape:", leaf_df.shape)

print("\nFirst 10 coordinates:")

print(leaf_df.head(10).to_string(index=False))


# ==========================================
# 6. COORDINATE VALIDATION
# ==========================================

print("\n===== LEAF COORDINATE CHECK =====")

print("X minimum:", leaf_df["X"].min())
print("X maximum:", leaf_df["X"].max())

print("Y minimum:", leaf_df["Y"].min())
print("Y maximum:", leaf_df["Y"].max())

print("Duplicate coordinates:", leaf_df.duplicated().sum())


# Check whether coordinates fit image dimensions

print("\n===== IMAGE BOUNDARY VALIDATION =====")

print("Image rows:", data.shape[0])
print("Image columns:", data.shape[1])

orientation_1_valid = (
    leaf_df["X"].between(0, data.shape[1] - 1).all()
    and leaf_df["Y"].between(0, data.shape[0] - 1).all()
)

orientation_2_valid = (
    leaf_df["X"].between(0, data.shape[0] - 1).all()
    and leaf_df["Y"].between(0, data.shape[1] - 1).all()
)

print("X = columns, Y = rows valid:", orientation_1_valid)
print("X = rows, Y = columns valid:", orientation_2_valid)


# ==========================================
# 7. VISUALISE LEAF COORDINATES
# ==========================================

print("\n===== GENERATING LEAF VISUALISATION =====")

band = data[:, :, 100]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))


# Orientation 1

axes[0].imshow(band, cmap="gray")

axes[0].scatter(
    leaf_df["X"],
    leaf_df["Y"],
    s=1
)

axes[0].set_title("X = Columns, Y = Rows")

axes[0].set_xlabel("Image Columns")
axes[0].set_ylabel("Image Rows")


# Orientation 2

axes[1].imshow(band, cmap="gray")

axes[1].scatter(
    leaf_df["Y"],
    leaf_df["X"],
    s=1
)

axes[1].set_title("X = Rows, Y = Columns")

axes[1].set_xlabel("Image Columns")
axes[1].set_ylabel("Image Rows")


plt.tight_layout()

plt.savefig(
    "data/processed/SWIR_leaf_coordinate_check.png",
    dpi=200,
    bbox_inches="tight"
)

plt.savefig(
    "data/processed/SWIR_leaf_coordinate_check.png",
    dpi=300,
    bbox_inches="tight"
)

print("\n===== SWIR INSPECTION COMPLETED =====")
# ==========================================
# 8. EXTRACT LEAF SPECTRAL INFORMATION
# ==========================================

print("\n===== LEAF SPECTRAL EXTRACTION =====")

rows = leaf_df["X"].to_numpy(dtype=int)
columns = leaf_df["Y"].to_numpy(dtype=int)

# Extract all 256 spectral bands for leaf pixels
leaf_spectra = data[rows, columns, :]

print("Extracted spectral data shape:", leaf_spectra.shape)

print("Number of leaf pixels:", leaf_spectra.shape[0])

print("Number of wavelength bands:", leaf_spectra.shape[1])

print("Mean spectral value:", np.mean(leaf_spectra))

print("Minimum spectral value:", np.min(leaf_spectra))

print("Maximum spectral value:", np.max(leaf_spectra))

# Check invalid values
print("NaN values:", np.isnan(leaf_spectra).sum())

print("Infinite values:", np.isinf(leaf_spectra).sum())

print("\n===== LEAF SPECTRAL EXTRACTION COMPLETED =====")
# ==========================================
# 9. LEAF SPECTRAL DATA QUALITY ANALYSIS
# ==========================================

print("\n===== LEAF SPECTRAL QUALITY ANALYSIS =====")

# Count zero values
zero_count = np.sum(leaf_spectra == 0)

# Count maximum values
max_count = np.sum(leaf_spectra == 65535)

# Count ignore values
ignore_count = np.sum(leaf_spectra == ignore_value)

# Count affected pixels
pixels_with_zero = np.sum(np.any(leaf_spectra == 0, axis=1))

pixels_with_max = np.sum(
    np.any(leaf_spectra == 65535, axis=1)
)

# Count affected wavelength bands
bands_with_max = np.sum(
    np.any(leaf_spectra == 65535, axis=0)
)

print("Total zero measurements:", zero_count)

print("Total maximum measurements:", max_count)

print("Ignore-value measurements:", ignore_count)

print("Pixels containing zero values:", pixels_with_zero)

print("Pixels containing maximum values:", pixels_with_max)

print("Wavelength bands containing maximum values:", bands_with_max)

print("\n===== QUALITY ANALYSIS COMPLETED =====")
# ==========================================
# 10. IDENTIFY AFFECTED WAVELENGTH BANDS
# ==========================================

print("\n===== AFFECTED WAVELENGTH ANALYSIS =====")

zero_per_band = np.sum(leaf_spectra == 0, axis=0)

max_per_band = np.sum(leaf_spectra == 65535, axis=0)

affected_bands = np.where(max_per_band > 0)[0]

print("Number of affected bands:", len(affected_bands))

print("\nAffected wavelength details:")

for band_index in affected_bands:

    print(
        "Band:", band_index,
        "| Wavelength:", wavelengths[band_index], "nm",
        "| Maximum values:", max_per_band[band_index],
        "| Zero values:", zero_per_band[band_index]
    )

print("\n===== WAVELENGTH ANALYSIS COMPLETED =====")
# ==========================================
# 11. IDENTIFY MAXIMUM-VALUE PIXEL LOCATIONS
# ==========================================

print("\n===== MAXIMUM-VALUE PIXEL LOCATIONS =====")

# Find positions of maximum values
max_positions = np.argwhere(leaf_spectra == 65535)

print("Total maximum-value positions:", len(max_positions))

print("\nFirst 20 affected measurements:")

for pixel_index, band_index in max_positions[:20]:

    print(
        "Leaf pixel:", pixel_index,
        "| X:", leaf_df.iloc[pixel_index]["X"],
        "| Y:", leaf_df.iloc[pixel_index]["Y"],
        "| Band:", band_index,
        "| Wavelength:", wavelengths[band_index], "nm"
    )

print("\n===== AFFECTED PIXEL ANALYSIS COMPLETED =====")
# ==========================================
# 12. MAXIMUM VALUE DISTRIBUTION ANALYSIS
# ==========================================

print("\n===== MAXIMUM VALUE DISTRIBUTION =====")

# Count maximum values in each wavelength band
max_counts = np.sum(leaf_spectra == 65535, axis=0)

# Display only affected bands
for band_index, count in enumerate(max_counts):

    if count > 0:

        print(
            f"Band {band_index} | "
            f"Wavelength: {wavelengths[band_index]:.2f} nm | "
            f"Maximum values: {count}"
        )

# Calculate percentage of affected leaf pixels
affected_pixels = np.any(leaf_spectra == 65535, axis=1)

print("\nTotal affected leaf pixels:", np.sum(affected_pixels))

print(
    "Percentage of affected leaf pixels:",
    round(np.mean(affected_pixels) * 100, 2), "%"
)

print("\n===== DISTRIBUTION ANALYSIS COMPLETED =====")
# ==========================================
# 13. VISUALISE MAXIMUM-VALUE LOCATIONS
# ==========================================

print("\n===== MAXIMUM VALUE LOCATION VISUALISATION =====")

# Find maximum-value positions
max_positions = np.argwhere(leaf_spectra == 65535)

# Get corresponding coordinates
affected_x = leaf_df.iloc[max_positions[:, 0]]["X"].to_numpy()
affected_y = leaf_df.iloc[max_positions[:, 0]]["Y"].to_numpy()

# Get corresponding wavelength band numbers
affected_bands = max_positions[:, 1]

# Create plot
plt.figure(figsize=(12, 6))

scatter = plt.scatter(
    affected_y,
    affected_x,
    c=affected_bands,
    cmap="viridis",
    s=35
)

plt.colorbar(scatter, label="Wavelength Band Index")

plt.xlabel("Y Coordinate (Image Columns)")
plt.ylabel("X Coordinate (Image Rows)")

plt.title("Spatial Distribution of Maximum Spectral Values")

plt.grid(True)

plt.savefig(
    "data/processed/SWIR_maximum_value_locations.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Total affected measurements:", len(max_positions))
print("Plot saved successfully.")

print("\n===== VISUALISATION COMPLETED =====")
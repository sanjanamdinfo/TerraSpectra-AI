import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spectral import envi


# ==========================================
# CREATE PROCESSED DATA FOLDER
# ==========================================

os.makedirs("data/processed", exist_ok=True)


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
print("Ignored values:", np.sum(data == ignore_value))


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
    dpi=300,
    bbox_inches="tight"
)

print("Leaf coordinate figure saved successfully.")

plt.show()


# ==========================================
# 8. EXTRACT LEAF SPECTRAL INFORMATION
# ==========================================

print("\n===== LEAF SPECTRAL EXTRACTION =====")

rows = leaf_df["X"].to_numpy(dtype=int)
columns = leaf_df["Y"].to_numpy(dtype=int)

# Extract all 256 spectral bands for leaf pixels

leaf_spectra = data[rows, columns, :]
# ==========================================
# SAVE LEAF SPECTRAL DATASET
# ==========================================

wavelength_columns = [
    f"{wavelength:.2f}_nm" for wavelength in wavelengths
]

spectral_df = pd.DataFrame(
    leaf_spectra,
    columns=wavelength_columns
)

# Add pixel identification and original coordinates
spectral_df.insert(0, "Y", leaf_df["Y"].to_numpy())
spectral_df.insert(0, "X", leaf_df["X"].to_numpy())
spectral_df.insert(0, "Pixel_ID", np.arange(1, len(leaf_df) + 1))

# Save extracted spectral dataset
output_path = "data/processed/SWIR_leaf_spectral_data.csv"

spectral_df.to_csv(output_path, index=False)

print("Spectral dataset saved:", output_path)
print("Spectral dataset shape:", spectral_df.shape)

print("Extracted spectral data shape:", leaf_spectra.shape)

print("Number of leaf pixels:", leaf_spectra.shape[0])

print("Number of wavelength bands:", leaf_spectra.shape[1])

print("Mean spectral value:", np.mean(leaf_spectra))

print("Minimum spectral value:", np.min(leaf_spectra))

print("Maximum spectral value:", np.max(leaf_spectra))

print("NaN values:", np.isnan(leaf_spectra).sum())

print("Infinite values:", np.isinf(leaf_spectra).sum())

print("\n===== LEAF SPECTRAL EXTRACTION COMPLETED =====")


# ==========================================
# 9. LEAF SPECTRAL DATA QUALITY ANALYSIS
# ==========================================

print("\n===== LEAF SPECTRAL QUALITY ANALYSIS =====")

zero_count = np.sum(leaf_spectra == 0)

max_count = np.sum(leaf_spectra == 65535)

ignore_count = np.sum(leaf_spectra == ignore_value)

pixels_with_zero = np.sum(
    np.any(leaf_spectra == 0, axis=1)
)

pixels_with_max = np.sum(
    np.any(leaf_spectra == 65535, axis=1)
)

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

max_counts = np.sum(leaf_spectra == 65535, axis=0)

for band_index, count in enumerate(max_counts):

    if count > 0:

        print(
            f"Band {band_index} | "
            f"Wavelength: {wavelengths[band_index]:.2f} nm | "
            f"Maximum values: {count}"
        )


affected_pixels = np.any(
    leaf_spectra == 65535,
    axis=1
)

print("\nTotal affected leaf pixels:", np.sum(affected_pixels))

print(
    "Percentage of affected leaf pixels:",
    round(np.mean(affected_pixels) * 100, 2),
    "%"
)

print("\n===== DISTRIBUTION ANALYSIS COMPLETED =====")


# ==========================================
# 13. VISUALISE MAXIMUM-VALUE LOCATIONS
# ==========================================

print("\n===== MAXIMUM VALUE LOCATION VISUALISATION =====")

max_positions = np.argwhere(leaf_spectra == 65535)

affected_x = leaf_df.iloc[
    max_positions[:, 0]
]["X"].to_numpy()

affected_y = leaf_df.iloc[
    max_positions[:, 0]
]["Y"].to_numpy()

affected_bands = max_positions[:, 1]


plt.figure(figsize=(12, 6))

scatter = plt.scatter(
    affected_y,
    affected_x,
    c=affected_bands,
    cmap="viridis",
    s=35
)

plt.colorbar(
    scatter,
    label="Wavelength Band Index"
)

plt.xlabel("Y Coordinate (Image Columns)")
plt.ylabel("X Coordinate (Image Rows)")

plt.title("Spatial Distribution of Maximum Spectral Values")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "data/processed/SWIR_maximum_value_locations.png",
    dpi=300,
    bbox_inches="tight"
)

print("Maximum-value location figure saved successfully.")

plt.show()

print("Total affected measurements:", len(max_positions))

print("\n===== VISUALISATION COMPLETED =====")


# ==========================================
# 14. NEIGHBOURING WAVELENGTH INVESTIGATION
# ==========================================

print("\n===== NEIGHBOURING WAVELENGTH INVESTIGATION =====")

affected_pixel_indices = np.unique(
    max_positions[:, 0]
)

print("Total affected pixels:", len(affected_pixel_indices))


print("\n===== AFFECTED PIXEL DETAILS =====")

for pixel_index in affected_pixel_indices[:20]:

    x = leaf_df.iloc[pixel_index]["X"]
    y = leaf_df.iloc[pixel_index]["Y"]

    affected_pixel_bands = max_positions[
        max_positions[:, 0] == pixel_index, 1
    ]

    print(
        f"Pixel: {pixel_index} | "
        f"X: {x} | "
        f"Y: {y} | "
        f"Affected bands: {affected_pixel_bands.tolist()}"
    )


print("\n===== NEIGHBOURING BAND STATISTICS =====")

affected_band_indices = np.unique(
    max_positions[:, 1]
)

for band in affected_band_indices:

    pixel_indices = np.unique(
        max_positions[
            max_positions[:, 1] == band, 0
        ]
    )

    print("\n--------------------------------")

    print(f"Affected Band: {band}")

    print(f"Wavelength: {wavelengths[band]:.2f} nm")

    for offset in [-2, -1, 1, 2]:

        neighbour = band + offset

        if 0 <= neighbour < len(wavelengths):

            values = leaf_spectra[
                pixel_indices,
                neighbour
            ]

            print(
                f"Neighbour Band: {neighbour} | "
                f"Wavelength: {wavelengths[neighbour]:.2f} nm | "
                f"Minimum: {values.min():.2f} | "
                f"Maximum: {values.max():.2f} | "
                f"Mean: {values.mean():.2f}"
            )


print("\n===== INVESTIGATION COMPLETED =====")


# ==========================================
# 15. MAXIMUM VALUE COMPARISON
# INSIDE AND OUTSIDE THE LEAF REGION
# ==========================================

print("\n===== MAXIMUM VALUE COMPARISON =====")

MAX_VALUE = 65535

# Create a mask for the leaf region

leaf_mask = np.zeros(
    data.shape[:2],
    dtype=bool
)

leaf_mask[rows, columns] = True


# Count maximum values in the complete image

whole_image_max = np.sum(
    data == MAX_VALUE
)


# Count maximum values inside the leaf region

leaf_max = np.sum(
    leaf_spectra == MAX_VALUE
)


# Count maximum values outside the leaf region

outside_max = whole_image_max - leaf_max


print("\n===== MAXIMUM VALUE SUMMARY =====")

print("Whole image maximum values:", whole_image_max)

print("Leaf region maximum values:", leaf_max)

print("Outside leaf region maximum values:", outside_max)


if whole_image_max > 0:

    print(
        "Percentage of maximum values inside leaf region:",
        round((leaf_max / whole_image_max) * 100, 2),
        "%"
    )


# Compare maximum values for every wavelength band

whole_band_counts = np.sum(
    data == MAX_VALUE,
    axis=(0, 1)
)

leaf_band_counts = np.sum(
    leaf_spectra == MAX_VALUE,
    axis=0
)

outside_band_counts = (
    whole_band_counts - leaf_band_counts
)


band_comparison = pd.DataFrame({

    "Band": np.arange(len(wavelengths)),

    "Wavelength_nm": wavelengths,

    "Whole_Image_Maximums": whole_band_counts,

    "Leaf_Maximums": leaf_band_counts,

    "Outside_Leaf_Maximums": outside_band_counts

})


print("\n===== TOP BANDS WITH MAXIMUM VALUES =====")

print(
    band_comparison[
        band_comparison["Whole_Image_Maximums"] > 0
    ].to_string(index=False)
)


# Save comparison results

comparison_csv_path = (
    "data/processed/SWIR_maximum_value_comparison.csv"
)

band_comparison.to_csv(
    comparison_csv_path,
    index=False
)

print("\nComparison CSV saved:", comparison_csv_path)


# Visualise maximum values across wavelength bands

plt.figure(figsize=(14, 6))

plt.plot(
    wavelengths,
    whole_band_counts,
    label="Whole Image",
    marker="o",
    markersize=3
)

plt.plot(
    wavelengths,
    leaf_band_counts,
    label="Leaf Region",
    marker="x",
    markersize=4
)

plt.xlabel("Wavelength (nm)")

plt.ylabel("Number of Maximum Values (65535)")

plt.title(
    "Maximum Value Distribution: Whole Image vs Leaf Region"
)

plt.legend()

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "data/processed/SWIR_maximum_value_band_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

print("Comparison figure saved successfully.")

plt.show()

print("\n===== SECTION 15 COMPLETED =====")

# ==========================================
# 16. SPATIAL DISTRIBUTION OF MAXIMUM VALUES
# ==========================================

print("\n===== SPATIAL MAXIMUM VALUE INVESTIGATION =====")

MAX_VALUE = 65535

# Confirm image dimensions
print("SWIR image shape:", data.shape)

if data.ndim != 3:
    raise ValueError(
        f"Expected 3D SWIR image, received shape {data.shape}"
    )

selected_bands = [
    74, 82, 87,
    90, 92, 104,
    121, 125, 255
]

# Create figure

fig, axes = plt.subplots(
    3,
    3,
    figsize=(16, 14)
)

axes = axes.flatten()

for i, band in enumerate(selected_bands):

    # Extract one spectral band
    band_data = np.asarray(data[:, :, band]).squeeze()

    print(f"\nProcessing Band {band}")
    print("Band data shape:", band_data.shape)

    # Validate image dimensions
    if band_data.ndim != 2:
        raise ValueError(
            f"Band {band} is not 2D: {band_data.shape}"
        )

    # Find maximum-value locations
    mask = band_data == MAX_VALUE

    row_positions, column_positions = np.where(mask)

    print("Maximum value count:", len(row_positions))

    # Plot maximum-value locations
    axes[i].scatter(
        column_positions,
        row_positions,
        s=5
    )

    axes[i].set_title(
        f"Band {band}\n"
        f"{wavelengths[band]:.2f} nm\n"
        f"Count: {len(row_positions)}"
    )

    axes[i].set_xlabel("Image Column")
    axes[i].set_ylabel("Image Row")

    axes[i].set_xlim(0, data.shape[1])
    axes[i].set_ylim(data.shape[0], 0)

    axes[i].grid(True, alpha=0.2)

plt.suptitle(
    "Spatial Distribution of Maximum Values (65535)",
    fontsize=16
)

plt.tight_layout()

spatial_plot_path = (
    "data/processed/SWIR_spatial_maximum_distribution.png"
)

plt.savefig(
    spatial_plot_path,
    dpi=300,
    bbox_inches="tight"
)

print("\nSpatial distribution figure saved:", spatial_plot_path)

plt.show()


# ==========================================
# OVERALL SPATIAL HEATMAP
# ==========================================

print("\n===== GENERATING OVERALL SPATIAL HEATMAP =====")

# Count maximum values across all wavelength bands
# for each image pixel

maximum_pixel_counts = np.sum(
    data == MAX_VALUE,
    axis=2
)

plt.figure(figsize=(12, 7))

plt.imshow(
    maximum_pixel_counts,
    cmap="hot",
    origin="upper",
    aspect="auto"
)

plt.colorbar(
    label="Number of Maximum Values Across Bands"
)

plt.title(
    "Overall Spatial Distribution of Maximum Values"
)

plt.xlabel("Image Column")
plt.ylabel("Image Row")

plt.tight_layout()

heatmap_path = (
    "data/processed/SWIR_overall_maximum_heatmap.png"
)

plt.savefig(
    heatmap_path,
    dpi=300,
    bbox_inches="tight"
)

print("Overall heatmap saved:", heatmap_path)

plt.show()

print("\n===== SECTION 16 COMPLETED =====")

print("\n===== ALL SWIR INSPECTION SECTIONS COMPLETED SUCCESSFULLY =====")
# ==========================================
# 17. COLUMN-WISE MAXIMUM VALUE INVESTIGATION
# ==========================================

print("\n===== COLUMN-WISE MAXIMUM VALUE INVESTIGATION =====")

MAX_VALUE = 65535

# Count maximum values in each image column
column_maximum_counts = np.sum(
    data == MAX_VALUE,
    axis=(0, 2)
)

# Create DataFrame
column_analysis = pd.DataFrame({
    "Image_Column": np.arange(data.shape[1]),
    "Maximum_Value_Count": column_maximum_counts
})

# Sort columns by maximum-value count
column_analysis_sorted = column_analysis.sort_values(
    by="Maximum_Value_Count",
    ascending=False
)

print("\nTop 15 columns containing maximum values:")
print(column_analysis_sorted.head(15).to_string(index=False))

# Save CSV
column_csv_path = "data/processed/SWIR_column_maximum_analysis.csv"

column_analysis.to_csv(
    column_csv_path,
    index=False
)

print("\nColumn analysis saved:", column_csv_path)

# Plot column-wise maximum values
plt.figure(figsize=(14, 6))

plt.bar(
    column_analysis["Image_Column"],
    column_analysis["Maximum_Value_Count"]
)

plt.title("Column-wise Distribution of Maximum Values (65535)")
plt.xlabel("Image Column")
plt.ylabel("Number of Maximum Values")

plt.tight_layout()

column_plot_path = (
    "data/processed/SWIR_column_maximum_distribution.png"
)

plt.savefig(
    column_plot_path,
    dpi=300,
    bbox_inches="tight"
)

print("Column distribution plot saved:", column_plot_path)

plt.show()

print("\n===== SECTION 17 COMPLETED =====")
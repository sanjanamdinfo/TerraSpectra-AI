import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_FILE = "data/processed/SWIR_leaf_spectral_data_qc.csv"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# LOAD DATASET
# ==========================================

print("\n===== EXPLAINABLE SPECTRAL ANALYSIS =====")

df = pd.read_csv(INPUT_FILE)

metadata_columns = ["Pixel_ID", "X", "Y"]

wavelength_columns = [
    col for col in df.columns
    if col not in metadata_columns
]

X = df[wavelength_columns].to_numpy(dtype=float)

print("\nDataset shape:", df.shape)
print("Number of pixels:", X.shape[0])
print("Number of wavelengths:", X.shape[1])

if not np.isfinite(X).all():
    raise ValueError("Dataset contains missing or infinite values.")

# Preserve sample identification
metadata = df[metadata_columns].copy()


# ==========================================
# SNV PREPROCESSING
# ==========================================

print("\n===== SNV PREPROCESSING =====")

row_means = X.mean(axis=1, keepdims=True)
row_stds = X.std(axis=1, keepdims=True)

if np.any(row_stds == 0):
    raise ValueError("Some pixel spectra have zero standard deviation.")

X_snv = (X - row_means) / row_stds

print("SNV transformation completed.")
print("SNV shape:", X_snv.shape)


# ==========================================
# ANALYSIS FUNCTION
# ==========================================

def perform_pca(data, method):

    print(f"\n===== {method} PCA =====")

    # Standardize each wavelength feature
    if method == "Standard":
        processed_data = StandardScaler().fit_transform(data)
    else:
        processed_data = data

    # Full PCA for explained variance
    pca = PCA()
    scores = pca.fit_transform(processed_data)

    explained = pca.explained_variance_ratio_ * 100
    cumulative = np.cumsum(explained)

    print("PC1 variance:", round(explained[0], 3), "%")
    print("PC2 variance:", round(explained[1], 3), "%")
    print("PC3 variance:", round(explained[2], 3), "%")

    print(
        "Components for 90% variance:",
        np.searchsorted(cumulative, 90) + 1
    )

    # ======================================
    # SAVE EXPLAINED VARIANCE
    # ======================================

    variance_df = pd.DataFrame({
        "Component": [
            f"PC{i+1}" for i in range(len(explained))
        ],
        "Explained_Variance_Percent": explained,
        "Cumulative_Variance_Percent": cumulative
    })

    variance_df.to_csv(
        f"{OUTPUT_DIR}/{method}_PCA_explained_variance.csv",
        index=False
    )

    # ======================================
    # SAVE WAVELENGTH IMPORTANCE
    # ======================================

    loadings = pca.components_[0]

    importance_df = pd.DataFrame({
        "Wavelength_nm": [
            float(col.replace("_nm", ""))
            for col in wavelength_columns
        ],
        "PC1_Loading": loadings,
        "Importance": np.abs(loadings)
    })

    importance_df = importance_df.sort_values(
        "Importance",
        ascending=False
    )

    importance_df.to_csv(
        f"{OUTPUT_DIR}/{method}_PC1_wavelength_importance.csv",
        index=False
    )

    print("\nTop 10 important wavelengths:")
    print(importance_df.head(10).to_string(index=False))

    # ======================================
    # SAVE PIXEL PCA SCORES
    # ======================================

    scores_df = metadata.copy()

    for i in range(3):
        scores_df[f"PC{i+1}_Score"] = scores[:, i]

    scores_df.to_csv(
        f"{OUTPUT_DIR}/{method}_PCA_pixel_scores.csv",
        index=False
    )

    # ======================================
    # SCREE PLOT
    # ======================================

    plt.figure(figsize=(9, 5))

    plt.plot(
        range(1, len(explained) + 1),
        explained,
        marker="o"
    )

    plt.xlabel("Principal Component")
    plt.ylabel("Explained Variance (%)")
    plt.title(f"{method} PCA Scree Plot")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{method}_PCA_scree_plot.png",
        dpi=300
    )

    plt.close()

    # ======================================
    # CUMULATIVE VARIANCE PLOT
    # ======================================

    plt.figure(figsize=(9, 5))

    plt.plot(
        range(1, len(cumulative) + 1),
        cumulative,
        marker="."
    )

    plt.axhline(
        90,
        linestyle="--",
        label="90% variance"
    )

    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Variance (%)")
    plt.title(f"{method} PCA Cumulative Variance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{method}_PCA_cumulative_variance.png",
        dpi=300
    )

    plt.close()

    # ======================================
    # PC1 WAVELENGTH IMPORTANCE PLOT
    # ======================================

    plot_df = importance_df.sort_values("Wavelength_nm")

    plt.figure(figsize=(12, 5))

    plt.plot(
        plot_df["Wavelength_nm"],
        plot_df["Importance"]
    )

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Absolute PC1 Loading")
    plt.title(f"{method} PCA - Wavelength Importance")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{method}_PC1_loading_profile.png",
        dpi=300
    )

    plt.close()

    print(f"\n{method} PCA analysis completed.")

    return importance_df, explained


# ==========================================
# RUN BOTH ANALYSES
# ==========================================

standard_importance, standard_variance = perform_pca(
    X,
    "Standard"
)

snv_importance, snv_variance = perform_pca(
    X_snv,
    "SNV"
)


# ==========================================
# COMPARE WAVELENGTH IMPORTANCE
# ==========================================

print("\n===== WAVELENGTH IMPORTANCE COMPARISON =====")

comparison = standard_importance[
    ["Wavelength_nm", "Importance"]
].merge(
    snv_importance[
        ["Wavelength_nm", "Importance"]
    ],
    on="Wavelength_nm",
    suffixes=("_Standard", "_SNV")
)

correlation = comparison[
    ["Importance_Standard", "Importance_SNV"]
].corr().iloc[0, 1]

print(
    "Absolute PC1 loading correlation:",
    round(correlation, 4)
)

comparison.to_csv(
    f"{OUTPUT_DIR}/wavelength_importance_comparison.csv",
    index=False
)


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n======================================")
print("EXPLAINABLE ANALYSIS COMPLETED")
print("======================================")

print("Standard PCA PC1:", round(standard_variance[0], 3), "%")
print("SNV PCA PC1:", round(snv_variance[0], 3), "%")

print("\nResults saved in:", OUTPUT_DIR)
import pandas as pd
import matplotlib.pyplot as plt

# Load wavelength importance results
df = pd.read_csv(
    "data/processed/wavelength_importance_comparison.csv"
)

# =====================================
# GRAPH 1: COMPLETE WAVELENGTH COMPARISON
# =====================================

df = df.sort_values("Wavelength_nm")

plt.figure(figsize=(13, 6))

plt.plot(
    df["Wavelength_nm"],
    df["Importance_Standard"],
    label="Standard PCA"
)

plt.plot(
    df["Wavelength_nm"],
    df["Importance_SNV"],
    label="SNV-PCA"
)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Absolute PC1 Loading")
plt.title("Wavelength Importance: Standard PCA vs SNV-PCA")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "data/processed/wavelength_importance_comparison.png",
    dpi=300
)

plt.close()


# =====================================
# GRAPH 2: TOP 20 WAVELENGTHS
# =====================================

standard = pd.read_csv(
    "data/processed/Standard_PC1_wavelength_importance.csv"
).head(20)

snv = pd.read_csv(
    "data/processed/SNV_PC1_wavelength_importance.csv"
).head(20)

fig, axes = plt.subplots(1, 2, figsize=(15, 8))

axes[0].barh(
    standard["Wavelength_nm"].astype(str),
    standard["Importance"]
)

axes[0].invert_yaxis()
axes[0].set_title("Standard PCA - Top 20")
axes[0].set_xlabel("Absolute PC1 Loading")
axes[0].set_ylabel("Wavelength (nm)")

axes[1].barh(
    snv["Wavelength_nm"].astype(str),
    snv["Importance"]
)

axes[1].invert_yaxis()
axes[1].set_title("SNV-PCA - Top 20")
axes[1].set_xlabel("Absolute PC1 Loading")
axes[1].set_ylabel("Wavelength (nm)")

plt.tight_layout()

plt.savefig(
    "data/processed/top20_wavelength_comparison.png",
    dpi=300
)

plt.close()

print("Wavelength comparison visualizations generated successfully.")
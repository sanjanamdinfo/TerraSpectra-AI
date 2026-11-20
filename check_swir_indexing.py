import pandas as pd
from spectral import open_image

# Load image
img = open_image("data/raw/SWIR_sample/01_D.hdr")
data = img.load()

print("Image shape:", data.shape)
print("Interleave:", img.metadata.get("interleave"))

# Six previously identified zero measurements
zero_pixels = [
    (149, 182, 248),
    (149, 290, 163),
    (149, 296, 165),
    (150, 158, 214),
    (150, 165, 13),
    (150, 290, 163)
]

print("\n===== INDEXING DIAGNOSTIC =====")

for row, col, band in zero_pixels:

    print(f"\nPixel: row={row}, col={col}, band={band}")

    # Test possible array-axis interpretations
    if row < data.shape[0] and band < data.shape[1] and col < data.shape[2]:
        print(
            "BIL-style [row, band, column]:",
            int(data[row, band, col])
        )

    if row < data.shape[0] and col < data.shape[1] and band < data.shape[2]:
        print(
            "[row, column, band]:",
            int(data[row, col, band])
        )

print("\nDiagnostic completed.")
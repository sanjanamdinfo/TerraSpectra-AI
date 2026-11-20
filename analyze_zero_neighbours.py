import numpy as np
from spectral import open_image

img = open_image("data/raw/SWIR_sample/01_D.hdr")
data = img.load()

zero_pixels = [
    (149, 182, 248),
    (149, 290, 163),
    (149, 296, 165),
    (150, 158, 214),
    (150, 165, 13),
    (150, 290, 163)
]

print("===== NEIGHBOURING PIXEL ANALYSIS =====")

for row, col, band in zero_pixels:

    print(f"\nPixel: ({row}, {col}), Band: {band}")

    neighbours = []

    for r in range(max(0, row - 1), min(data.shape[0], row + 2)):
        for c in range(max(0, col - 1), min(data.shape[1], col + 2)):

            if r == row and c == col:
                continue

            value = int(data[r, c, band])

            neighbours.append(value)

    print("Neighbour values:", neighbours)

    print("Neighbour mean:", round(np.mean(neighbours), 2))
    print("Neighbour median:", round(np.median(neighbours), 2))

print("\nAnalysis completed.")
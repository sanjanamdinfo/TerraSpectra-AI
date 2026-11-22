# Daily Progress - November 21, 2026

## Project
TerraSpectra-AI: Hyperspectral Crop Disease Forecasting

## Objective
Inspect and validate the prepared VNIR and SWIR datasets.

## Completed Work

1. Inspected the VNIR cleaned dataset.
2. Inspected the VNIR prepared dataset.
3. Reviewed the preprocessing logic in `main.py`.
4. Reviewed the existing `validate_prepared_datasets.py` script.
5. Executed prepared dataset validation for VNIR and SWIR.
6. Verified treatment and genotype distributions.
7. Checked missing values, duplicate records, duplicate Pot IDs, and infinite values.
8. Generated the prepared dataset validation report.

## Validation Results

| Metric | VNIR | SWIR |
|---|---:|---:|
| Samples | 48 | 48 |
| Columns | 39 | 39 |
| Missing values | 553 | 553 |
| Duplicate rows | 0 | 0 |
| Duplicate Pot IDs | 0 | 0 |
| Infinite values | 0 | 0 |
| Completely empty columns | 3 | 3 |

## Sample Distribution

- Infected: 24
- Non-infected: 24
- EPO_67: 24
- EPO_68: 24

Both datasets have equal treatment and genotype distributions.

## Observations

The following acquisition columns contain no recorded values:

- DPI_18_D
- DPI_19_D
- DPI_20_D

The missing acquisition values require interpretation using the original acquisition records.

The validation covers prepared metadata tables, not the actual hyperspectral image measurements.

## Files Inspected

- `main.py`
- `validate_prepared_datasets.py`
- `data/processed/VNIR_cleaned.csv`
- `data/processed/VNIR_prepared.csv`
- `data/processed/SWIR_prepared.csv`

## Generated Report

- `data/processed/prepared_dataset_validation.csv`

## Git Status

- Branch: `main`
- Working tree was clean after validation.
- No existing preprocessing code was modified.

## Next Steps

1. Investigate the missing acquisition values.
2. Review the original acquisition records.
3. Continue the planned hyperspectral data investigation.
---

# Daily Progress - November 22, 2026

## Objective

Investigate missing acquisition values in the prepared VNIR and SWIR datasets using the original dataset records and documentation.

## Initial Status

- Repository checked.
- Main branch synchronized with GitHub.
- Working tree clean.

## Work Status

- Missing acquisition investigation started.

## Next Steps

1. Inspect original dataset documentation.
2. Investigate missing acquisition records.
3. Document findings based on available evidence.
# Daily Progress - November 22, 2026

## Objective

Investigate missing acquisition values in the prepared VNIR and SWIR datasets using the original acquisition records and dataset documentation.

## Work Completed

### 1. Original Dataset Inspection
- Inspected the original `VNIR_data.csv` and `SWIR_data.csv` files.
- Used `cp1252` encoding to read the original CSV files correctly.
- Confirmed that both datasets contain 48 pot records and 18 acquisition dates.

### 2. Missing Acquisition Investigation
- Checked DPI 18, DPI 19 and DPI 20 on side D in both original datasets.
- Confirmed that these columns are empty for all 48 pots.
- Verified that these empty cells are also present in the original records.

### 3. Technical Malfunction Investigation
Identified the following explicit `NA` entries:

| Dataset | Pot | Genotype | Treatment | DPI | Side | Status |
|---|---|---|---|---|---|---|
| VNIR | 47 | EPO_67 | Non-infected | 10 | G | Technical malfunction |
| SWIR | 23 | EPO_67 | Non-infected | 10 | G | Technical malfunction |

### 4. Documentation Verification
The original dataset documentation specifies:
- Empty cells indicate no HSI acquisition due to sampling.
- `NA` indicates missing data due to a technical malfunction.

## Conclusion

The investigation confirmed that the three entirely empty acquisition columns in both prepared datasets originate from the original acquisition records. The identified technical-malfunction entries were also verified in the original files.

No raw datasets or preprocessing code were modified during this investigation.

## Next Steps

1. Review the implications of the confirmed missing acquisition values.
2. Continue the hyperspectral data investigation based on the available project data.
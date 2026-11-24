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
# Daily Progress - November 23, 2026

## Objective

Validate the prepared VNIR and SWIR datasets and investigate differences between the two sensor datasets.

## Work Completed

### 1. Prepared Dataset Validation
- Compared the prepared VNIR and SWIR datasets.
- Confirmed that both datasets contain 48 pot records and 39 columns.
- Verified that there are no duplicate Pot IDs.
- Confirmed that Pot IDs, genotype information and treatment labels match between the datasets.

### 2. VNIR and SWIR Differences
- Identified 12 different acquisition-count cells between the prepared datasets.
- Investigated the differences in Pots 13, 20, 23, 25 and 47.
- Compared the identified records with the original raw VNIR and SWIR datasets.
- Confirmed that the differences were already present in the original source records.

### 3. Cleaned-to-Prepared Dataset Validation
- Reproduced the filtering performed by the preparation pipeline.
- Compared the expected results against the saved prepared datasets.
- Validated dataset dimensions, column names, Pot IDs, genotype, treatment, acquisition counts and missing-value patterns.
- Confirmed exact content matches for both VNIR and SWIR after normalizing Pot IDs.

## Conclusion

Both prepared datasets correctly preserve the corresponding cleaned datasets after the preparation filtering.

The identified VNIR and SWIR acquisition-count differences originate from the original raw records. No preprocessing code or dataset modifications were required during this investigation.

# Daily Progress - November 24, 2026

## Objective

Investigate and correct the VNIR and SWIR metadata preprocessing workflow and validate the cleaned and prepared datasets.

## Work Completed

### 1. Original Dataset Investigation
- Investigated the seven additional blank and explanatory rows in both cleaned metadata datasets.
- Examined the original Git commit and identified that the original raw-to-cleaned preprocessing script was missing.
- Verified that both raw datasets contain 48 actual plant records.

### 2. Metadata Preprocessing Implementation
- Created `src/metadata_preprocessing.py`.
- Implemented reproducible preprocessing for both VNIR and SWIR metadata.
- Removed blank and explanatory rows using Pot, Genotype and Treatment identification fields.
- Preserved legitimate missing acquisition values.
- Generated corrected cleaned datasets containing 48 plant records and 39 columns each.

### 3. Prepared Dataset Regeneration
- Executed `main.py` to regenerate the prepared VNIR and SWIR datasets.
- Confirmed 24 infected and 24 non-infected samples in each dataset.
- Confirmed 24 samples each for genotypes EPO_67 and EPO_68.

### 4. Final Dataset Validation
Compared both cleaned datasets against their corresponding original raw datasets.

| Validation | VNIR | SWIR |
|---|---|---|
| Shape matches | PASS | PASS |
| Column names match | PASS | PASS |
| Exact content matches | PASS | PASS |
| Missing-value patterns match | PASS | PASS |

## Conclusion

Successfully implemented a reproducible metadata preprocessing script for VNIR and SWIR datasets.

Both cleaned datasets now contain exactly 48 valid plant records. All original acquisition values and missing-value patterns are preserved.

Final validation confirmed exact content matches between the cleaned datasets and their corresponding raw source records.

## Next Steps

1. Continue hyperspectral spectral data preparation.
2. Proceed with the next stages of the existing project workflow.
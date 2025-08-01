# Project Phase-II Report

**Team36**

- Minh Nguyen – minhn2
- Jiaqing Mo - jiaqing7  
- Haitham Shahin - hshahin2

---

## 1. Description of Data Cleaning Performed

### Short descriptions of cleaning steps performed

1. Trimmed all string columns (e.g., place, location, sponsor)
1. Used mass edits in event and occasion columns to standardize similar values 
1. Converted id, dish_count, page_count to numbers, date to date type
1. Added date_timeless (formatted date string), place_cleaned (cleaned for reconciliation)
1. Used Wikidata reconciliation to map place_cleaned to geographic entities
1. Used OpenCage API to fill in missing country when Wikidata failed
1. Combined Wikidata and OpenCage results into country_merged
1. Removed unnecessary/duplicate columns: language, keywords, location_type, temp reconciliation columns

### Rationale

#### Trimmed all string columns (e.g., place, location, sponsor)

Removed inconsistent spacing and invisible characters that cause grouping/filtering issues. Cleaned 557 records with unnecessary whitespace. It's useful for U1 and ensures accurate grouping of locations and venues.

#### Used mass edits in event and occasion columns to standardize similar values

Mass edited using clustering to unify case/punctuation/variants like “DINNER TO HONOR” → “DINNER”. Standardized categories for analysis and filtering. Not required for U1 but helpful if controlling for meal types

#### Converted id, dish_count, page_count to numbers, date to date type

Enables proper filtering, sorting, and aggregation. It's useful for U1 and allows counts per menu and dish aggregation.

#### Added date_timeless (formatted date string), place_cleaned (cleaned for reconciliation)

Helps downstream systems that don’t parse date objects; cleans for lookup. It's essential for tracking price changes over time for U1.

#### Used Wikidata reconciliation to map place_cleaned to geographic entities, Used OpenCage API to fill in missing country when Wikidata failed, Combined Wikidata and OpenCage results into country_merged

Enriches data with country info, essential for filtering by region, Improves completeness of country data. For U1, it's essential to increase the number of known currency by country and compare prices by country or region with the same currency.


#### Removed unnecessary/duplicate columns: language, keywords, location_type, temp reconciliation columns

Reduced noise in the dataset

## 2. Document data quality changes

### Results quantification

Menu Table:
| Column                 | Cells Changed | Notes                                 |
| ---------------------- | ------------- | ------------------------------------- |
| `event`                | \~11,800      | Standardized with mass edits          |
| `occasion`             | \~5,300       | Cleaned up punctuation and categories |
| `place_cleaned`        | \~1,659       | Removed unwanted characters           |
| `dish_count`           | 17,545        | Converted to number                   |
| `page_count`           | 17,545        | Converted to number                   |
| `id`                   | 17,545        | Converted to number                   |
| `date`                 | 16,959        | Converted to date                     |
| `date_timeless`        | 16,959        | Derived ISO string                    |
| `location`             | 555           | Whitespace normalized                 |
| `country` via Wikidata | 2,790         | Filled via reconciliation             |
| `country` via OpenCage | 4,340         | Filled via API fallback               |
| `country_merged`       | 6,563         | Combined Wikidata and geocode values  |



Integrity Constraint (IC) Violation Reduction:


Denial Constraint:
Constraint:
If location is valid, then currency should not be null
(∀ x: x.location.isValid → not isNull(x.currency))

Before Cleaning:
currency is blank (11089 records) or invalid (like cents) → can't reliably group

After Cleaning:
we have less unknown currency records by merging the country column and currency column, down to 5885 unknown currency/country records.



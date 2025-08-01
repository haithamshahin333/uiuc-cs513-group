# Dish Dataset Data Cleansing Report

### Short Description of Cleansing Steps Performed

1) Remove IC-Violations from the Dish dataset where the Dish ID is not found in the MenuItem dataset
2) Clean invalid date values for the first_appeared and last_appeared columns
3) Remove invalid pricing records where the lowest_price and the highest_price are either null or both $0
4) Standarize the Dish name column by trimming whitespace, removing quotes, and applying all names to be lowercase
5) Drop the unused 'description' column

### Rationale Per Step and Overall Analysis

For each step in the data cleansing, you can look within the `dish_data_analysis.ipynb` to see the background commands run with Python Pandas. The sections in the code are marked with the same headers used below.

#### Remove IC Violations Between the Dish dataset and the MenuItem Dataset
##### Section 1
The MenuItem dataset has a link back to the Dish dataset through the Dish ID. This is what links a given dish to a particular menu, which is necessary for the main use case since the goal is to understand how the dish price changes over time and location of the menu on which it appears.

Therefore, it is necessary to ensure that any dish analyzed has a corresponding location on a menu. If it does not, it should not be part of the analysis.

As shown in Section 1 of the dish analysis notebook, there were 9,262 dishes that were not within the MenuItems dataset (~2.19% of the Dish records). These records will need to be removed from the Dish dataset for the use case analysis.

#### Clean Invalid Date Values for the first_appeared and last_appeared columns
##### Section 2
Since the goal of the analysis is to analyze dish price over time, the years provided for the first_appeared and last_appeared columns should be logical both in terms of value and consistency.

Specifically, the first_appeared date we would not expect to be less than the year 1500 (the data dictionary did not provide a clear date as to when initial data was collected) and the last_appeared year should not be beyond the current year of 2025.

Additionally, the first_appeared date should not be greater than the last_appeared date for a given dish.

As shown in Section 2 of the dish analysis notebook, the following results demonstrate that data quality issues exist.

First Appeared Check Results:
- Future years (>2025): 11
- Extreme years (<1500): 55492

Last Appeared Check Results:
- Future years (>2025): 179
- Extreme years (<1500): 55321

Logical Issues Check Results:
- First > Last: 6

#### Remove Invalid Pricing Records
##### Section 3
The goal of the analysis is to understand how pricing changes over time for a given dish.
Therefore, the lowest_price and highest_price for a given dish must fall within an expected logical range. Additionally, it is necessary for these values to not be null or $0.

As shown in Section 3, the following results show that there are over 50% of records where both the lowest_price and highest_price are $0. This implies that the price of the dish was not populated and may be a proxy for null, so these records should be cleaned and removed.

- Records with both prices missing: 29100
- Records with lowest price missing but highest price present: 0
- Records with highest price missing but lowest price present: 0
- Records with both prices zero: 218014
- Percentage of records with both prices zero: 51.49162606253705%

#### Standardize the Dish Name Column
##### Section 4
Since the dish name is something that will explain the price variability and adds context to the dish ID being analyzed, it is necessary to standardize the dish name and clean the text value for things like whitespace, potential extra quotes, and making the case of the text normalized.

As shown in section 4, there are inconsistencies in the name field that need to be cleaned.

- Name Completeness: 423397/423397 (100.0%)
- Unique Names: 423363 (potential duplicates: 34)
- All Upper Case: 16491
- All Lower Case: 11513
- Mixed Case: 395393 (potential case standardization needed to make all lowercase)
- Dishes with quotes in name: 6860

#### Drop Empty/Null Data
##### Section 5
As shown in section 5 in the analysis, empty/null records and columns were identified. It was shown that the description column in the dataset was null for every record, rendering it meaningless for the dataset and safe to drop altogether.

Additionally, records had missing data for either the lowest_price or highest_price columns. These will be cleansed with the pricing cleaning section.

- Null values in 'name': 0 (0.0%)
- Empty values in 'name': 0 (0.0%)
- Null values in 'description': 423397 (100.0%)
- Empty values in 'description': 0 (0.0%)

# Document Data Quality Changes

The data cleansing script is `dish_data_cleaning.py`. Each step corresponds and prints the data changes below:

### Step 1 - Removing IC Violations:
- Violations of the IC-Constraint where the Dish ID exists in MenuItem: 9262

### Step 2 - Clean Invalid Years:
-   First appeared > 2025: 11
-   First appeared < 1500: 50773
-   Last appeared > 2025: 179
-   Last appeared < 1500: 50602
-   First > Last (logical error): 6

Removed 50954 records with invalid years

### Step 3 - Remove Invalid Pricing:
- Null lowest_price: 28068
- Null highest_price: 28068
- Both prices = $0: 167404
- Lowest > Highest (logical error): 0

Removed 199,865 records with invalid prices

### Step 4 - Standardize Dish Names
Name quality issues found:
- Names with quotes: 1,183
- Names with multiple spaces: 2,188
- Names with leading/trailing spaces: 3,978
- Standardized 163316 dish names (Unique names after: 145880)

### Step 5 - Drop Description Column
The description column is dropped to make the dataframe smaller in size.

### Summary of Data Cleaning Steps
- Original records: 423397
- Final records: 163316
- Total records removed: 260081 (61.42721842620519%)
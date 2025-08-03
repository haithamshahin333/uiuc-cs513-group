# MenuPage Dataset Data Cleansing Report

### Short Description of Cleansing Steps Performed

The MenuPage dataset is not relevant to the use case analysis of analyzing dish price data variability over time and location, but will still be cleaned for the potential of follow-on analysis if one obtains the pictures for the Menu Pages or whats to better understand the page an item exists on.

1) Check IC-Violations such that the menu_id in the MenuPage dataset should link back to a valid Menu in the Menu dataset
2) Clean the page_number field for null or negative values

# Rationale Per Step and Overall Analysis

For each step in the data cleansing, you can look within the `menupage_data_analysis.ipynb` to see the background commands run with Python Pandas. The sections in the code are marked with the same headers used below.

#### Check IC Violations Between the MenuPage dataset and Menu Dataset
##### Section 1
A key IC Constraint in the MenuPage dataset is ensuring that each MenuPage record can be linked back to its parent Menu through the menu_id column. Without this link, a record in the MenuPage would be invalid since it is meant to reference a page within a given menu. Records that do not link back to a Menu should be removed from the dataset.

As shown in Section 1 of the menupage_data_analysis notebook, the following report back the number of IC violations and records that need to be cleaned within the MenuPage dataset:

- Total unique menu IDs in MenuPage: 19816
- Total valid menu IDs in Menu table: 17545
- MenuPage records with invalid menu IDs: 2271
- Total MenuPage records: 66937
- Records with invalid menu_id: 5803
- Violation percentage: 8.669345802769769%

#### Clean the page_number columns
##### Section 2

A key attribute within the MenuPage dataset is the page number itself. This represents the page number within the parent menu that is being described. If this number if negative, 0, or null, then the page number itself does not make logical sense as it would not represent a page number within a menu.

As shown in Section 2, there are no records with a negative or 0 value for page_number, but there are 1202 records with a null page number, rendering them as invalid for any analysis:

- Null page_number values: 1202 (1.79571836204192%)
- Negative page_number values: 0 (0.0%)
- Zero page_number values: 0 (0.0%)

# Document Data Quality Changes

The data cleansing script is `menupage_data_cleaning.py`. Each step corresponds and prints the data changes below:

### Step 1 - Removing IC Violations
- Violations of the IC-Constraint where MenuPage menu_id exists in Menu: 2271
- Removed 5803 MenuPage records with invalid menu_id

### Step 2 - Clean Page Number
- Null page_number values: 945
- Removed 945 records with invalid page numbers

### Summary of Data Cleaning Steps
- Original records: 66937
- Final records: 60189
- Total records removed: 6748
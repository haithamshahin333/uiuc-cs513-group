# Project Phase-II Report

**Team36**

- Minh Nguyen – minhn2
- Jiaqing Mo - jiaqing7  
- Haitham Shahin - hshahin2

---

## 1. Description of Data Cleaning Performed

### Short descriptions of cleaning steps performed

1. Remove rows with missing, empty, non-numerical or negative price.
1. Fill in missing high_price column with data from price column.
1. Remove non-numerical value in high-price column.
1. Remove rows in which price is greater than high_price.
1. Remove rows with empty id, menu_page_id, created_at, updated_at, xpos or ypos
1. Remove rows in with non-numerical xpos or ypos
1. Remove rows with non-existent menu_page_id or dish_id

### Rationale

#### Remove missing, empty, non-numerical or negative price

Remove rows with missing, empty, non-numerical or negative price. This is essential for understanding the scope of missing data is critical for U1. According to our SQL analysis, there are 445,916 such rows. This is obviously violating constraints for price column so we filter out these rows.

#### Fill in missing high_price column

After filtering out missing price, we fill in missing high_price column with data from price column. According definition from menus.nypl.org, the high_price is the highest price of the item on the menu. Thus, by definition, we can copy value from price column to fill in the missing high_price value. Our SQL analysis exposes 1,240,821 such rows. This transformation will make cleaning up for U1 much more straight-forward.

#### Remove non-numerical value in high-price column

Remove non-numerical value in high-price column. High-price column is float, so it can't be non-numerical.

#### Filter rows in which price is greater than high_price

We continue to filter rows in which price is greater than high_price. According definition from menus.nypl.org, the high_price is the highest price of the item on the menu. Thus, we consider such rows invalid and remove them. This will help with the integrity of U1. According to our SQL analysis, there are 1274 such rows, which demands systematic filtering.

#### Remove rows with empty id, menu_page_id, created_at, updated_at, xpos or ypos

Remove rows with empty id, menu_page_id, created_at, updated_at, xpos or ypos. According to data constraints in the menus.nypl.org, these columns don't contain empty values. So any rows contain empty value must be invalid. This step will also improve integrity of the analysis in U1.

#### Remove rows in with non-numerical xpos or ypos

Remove rows in with non-numerical xpos or ypos. According to data constraints in the menus.nypl.org, these columns contain float values. So any rows contain non-numerical value must be invalid.

#### Remove rows with non-existent menu_page_id or dish_id

Remove rows with non-existent menu_page_id or dish_id. The dish_id and menu_page_id must obviously be valid. Removing invalid rows rules out the case where we have menu item that don't actually exist in a valid menu.

## 2. Document data quality changes

### Results quantification

1. Columns changed: `price`, high_price`.
1. Number of rows cleaned up: 445,916
1. Number of values filled in `high_price`: 1274

### Demonstration that data quality has been improved

| Violation / Need for improvement | Before cleaning | After cleaning |
|-----------|----------------|----------------|
| Rows with missing, empty, non-numerical or negative price | 445,916 (see querry 2) | 0 (see querry 9 ) |
| Rows with missing high price | 1,240,821 (see querry 3) | 0 (see querry 10 ) |
| Rows with price greater than high price | 1274 (see querry 5) | 0 (see querry 12 ) |

### Other validations (not demanded improvement)

1. Rows with non-numerical `high-price`: 0 (see query 4)
1. Rows with empty `id`, `menu_page_id`, `created_at`, `updated_at`, `xpos` or `ypos`: 0 (see query 6)
1. Rows in with non-numerical `xpos` or `ypos`: 0 (see query 7)

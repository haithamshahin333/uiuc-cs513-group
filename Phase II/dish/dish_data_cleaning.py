import pandas as pd
import numpy as np
import os

# @begin dish_data_cleaning_workflow
# @in dish_raw_csv_file
# @in menuitem_raw_csv_file  
# @out dish_cleaned_csv_file
def main():
    # @begin load_datasets
    # @in dish_raw_csv_file
    # @in menuitem_raw_csv_file
    # @out dish_df_original
    # @out menuitem_df
    print("Loading the Datasets")
    dish_df = pd.read_csv('data/raw/Dish.csv')
    menuitem_df = pd.read_csv('data/raw/MenuItem.csv')

    print(f"Original dish dataset: {len(dish_df)} records")
    print(f"Original columns: {list(dish_df.columns)}")
    # @end load_datasets
    
    # @begin remove_ic_violation_dishes
    # @in dish_df_original
    # @in menuitem_df
    # @out dish_df_clean_step1
    print("\n\n\nStep 1 - Remove IC Violations between Dish ID and MenuItem")
    # These do not meet the integrity constraints required for analysis
    dish_ids = set(dish_df['id'])
    menuitem_dish_ids = set(menuitem_df['dish_id'].dropna())
    unlinked_dish_ids = dish_ids - menuitem_dish_ids
    print(f"Violations of the IC-Constraint where the Dish ID exists in MenuItem: {len(unlinked_dish_ids)}")

    # Remove unlinked dishes
    before_unlinked_removal = len(dish_df)
    dish_df_clean = dish_df[dish_df['id'].isin(menuitem_dish_ids)].copy()
    after_unlinked_removal = len(dish_df_clean)
    unlinked_removed_count = before_unlinked_removal - after_unlinked_removal

    print(f"Removed {unlinked_removed_count} unlinked dishes")
    # @end remove_ic_violation_dishes
    
    # @begin clean_invalid_dates
    # @in dish_df_clean_step1
    # @param current_year
    # @param min_valid_year
    # @out dish_df_clean_step1_step2
    print("\n\n\nStep 2 - Clean Invalid Years")
    # Set current and min valid years
    current_year = 2025
    min_valid_year = 1500

    # Count invalid dates before cleaning
    invalid_future_first = (dish_df_clean['first_appeared'] > current_year).sum()
    invalid_ancient_first = (dish_df_clean['first_appeared'] < min_valid_year).sum()
    invalid_future_last = (dish_df_clean['last_appeared'] > current_year).sum()
    invalid_ancient_last = (dish_df_clean['last_appeared'] < min_valid_year).sum()
    invalid_logic = (dish_df_clean['first_appeared'] > dish_df_clean['last_appeared']).sum()

    print(f"Date validation issues found:")
    print(f"  First appeared > {current_year}: {invalid_future_first}")
    print(f"  First appeared < {min_valid_year}: {invalid_ancient_first}")
    print(f"  Last appeared > {current_year}: {invalid_future_last}")
    print(f"  Last appeared < {min_valid_year}: {invalid_ancient_last}")
    print(f"  First > Last (logical error): {invalid_logic}")

    # Apply date filters
    before_date_cleaning = len(dish_df_clean)
    date_filter = (
        (dish_df_clean['first_appeared'] >= min_valid_year) &
        (dish_df_clean['first_appeared'] <= current_year) &
        (dish_df_clean['last_appeared'] >= min_valid_year) &
        (dish_df_clean['last_appeared'] <= current_year) &
        (dish_df_clean['first_appeared'] <= dish_df_clean['last_appeared'])
    )

    dish_df_clean = dish_df_clean[date_filter].copy()
    after_date_cleaning = len(dish_df_clean)
    date_removed_count = before_date_cleaning - after_date_cleaning

    print(f"Removed {date_removed_count} records with invalid dates")
    # @end clean_invalid_dates
    
    # @begin remove_invalid_prices
    # @in dish_df_clean_step1_step2
    # @out dish_df_clean_step1_step2_step3
    print("\n\n\nStep 3 - Remove Invalid Pricing")
    # Count invalid prices before cleaning
    null_lowest = (dish_df_clean['lowest_price'].isnull()).sum()
    null_highest = (dish_df_clean['highest_price'].isnull()).sum()
    zero_both = ((dish_df_clean['lowest_price'] == 0) & (dish_df_clean['highest_price'] == 0)).sum()
    logic_error = (dish_df_clean['lowest_price'] > dish_df_clean['highest_price']).sum()

    print(f"Price validation issues found:")
    print(f"  Null lowest_price: {null_lowest}")
    print(f"  Null highest_price: {null_highest}")
    print(f"  Both prices = $0: {zero_both}")
    print(f"  Lowest > Highest (logical error): {logic_error}")

    # Apply price filters
    before_price_cleaning = len(dish_df_clean)
    price_filter = (
        (dish_df_clean['lowest_price'].notna()) &
        (dish_df_clean['highest_price'].notna()) &
        (dish_df_clean['lowest_price'] > 0) &
        (dish_df_clean['highest_price'] > 0) &
        (dish_df_clean['lowest_price'] <= dish_df_clean['highest_price'])
    )

    dish_df_clean = dish_df_clean[price_filter].copy()
    after_price_cleaning = len(dish_df_clean)
    price_removed_count = before_price_cleaning - after_price_cleaning

    print(f"Removed {price_removed_count:,} records with invalid prices")
    # @end remove_invalid_prices
    
    # @begin standardize_dish_names
    # @in dish_df_clean_step1_step2_step3
    # @out dish_df_clean_step1_step2_step3_step4
    print("\n\n\nStep 4 - Standardize Dish Name")
    # Count case variations before cleaning
    original_unique_names = dish_df_clean['name'].nunique()
    before_name_cleaning = len(dish_df_clean)

    # Check for various name quality issues
    names_with_quotes = dish_df_clean['name'].str.contains('"', na=False).sum()
    names_with_extra_spaces = dish_df_clean['name'].str.contains(r'\s{2,}', na=False).sum()
    names_with_leading_trailing_spaces = (dish_df_clean['name'] != dish_df_clean['name'].str.strip()).sum()

    print(f"Name quality issues found:")
    print(f"  Names with quotes: {names_with_quotes:,}")
    print(f"  Names with multiple spaces: {names_with_extra_spaces:,}")
    print(f"  Names with leading/trailing spaces: {names_with_leading_trailing_spaces:,}")

    # Standardize to lowercase case and clean whitespace
    dish_df_clean['name'] = dish_df_clean['name'].str.strip() 
    dish_df_clean['name'] = dish_df_clean['name'].str.replace(r'\s+', ' ', regex=True) 
    dish_df_clean['name'] = dish_df_clean['name'].str.lower()

    # Remove quotes that may interfere with analysis
    dish_df_clean['name'] = dish_df_clean['name'].str.replace('"', '', regex=False)

    # Calculate impact
    after_unique_names = dish_df_clean['name'].nunique()

    print(f"Standardized {before_name_cleaning} dish names")
    print(f"Unique names before: {original_unique_names}")
    print(f"Unique names after: {after_unique_names}")
    # @end standardize_dish_names
    
    # @begin drop_unused_columns
    # @in dish_df_clean_step1_step2_step3_step4
    # @out dish_df_clean_step1_step2_step3_step4_step5
    print("\n\n\nStep 5 - Drop Description Column")
    dish_df_clean = dish_df_clean.drop(columns=['description'])
    # @end drop_unused_columns
    
    # @begin write_cleaned_dataset
    # @in dish_df_clean_step1_step2_step3_step4_step5
    # @out dish_cleaned_csv_file
    print("Write Cleansed Dataset")
    # Create output directory if it doesn't exist
    output_dir = 'data/clean'
    os.makedirs(output_dir, exist_ok=True)

    # Write to CSV
    output_file = os.path.join(output_dir, 'Dish_cleaned.csv')
    dish_df_clean.to_csv(output_file, index=False)
    
    print(f"\n\n\nCleaned dataset written to: {output_file}")
    
    # Final summary
    print("\n\n\nFinal Summary of Cleaning Process")
    original_count = len(dish_df)
    final_count = len(dish_df_clean)
    total_removed = original_count - final_count
    reduction_percentage = (total_removed / original_count) * 100
    
    print(f"Original records: {original_count}")
    print(f"Final records: {final_count}")
    print(f"Total records removed: {total_removed} ({reduction_percentage}%)")
    print(f"Ready for analysis: Dataset cleaned and prepared for price/location analysis")
    # @end write_cleaned_dataset

# @end dish_data_cleaning_workflow

if __name__ == "__main__":
    main()
import pandas as pd
import numpy as np
import os

# @begin menupage_data_cleaning_workflow
# @in menupage_raw_csv_file
# @in menu_raw_csv_file  
# @out menupage_cleaned_csv_file
def main():
    # @begin load_datasets
    # @in menupage_raw_csv_file
    # @in menu_raw_csv_file
    # @out menupage_df_original
    # @out menu_df
    print("Loading the Datasets")
    menupage_df = pd.read_csv('data/raw/MenuPage.csv')
    menu_df = pd.read_csv('data/raw/Menu.csv')
    print(f"Original MenuPage dataset: {len(menupage_df)} records")
    # @end load_datasets

    # @begin remove_ic_violation_menupages
    # @in menupage_df_original
    # @in menu_df
    # @out menupage_df_clean_step1
    print("\n\n\nStep 1 - Remove IC Violations between MenuPage menu_id and Menu")
    menupage_menu_ids = set(menupage_df['menu_id'])
    valid_menu_ids = set(menu_df['id'])
    violating_menu_ids = menupage_menu_ids - valid_menu_ids
    print(f"Violations of the IC-Constraint where MenuPage menu_id exists in Menu: {len(violating_menu_ids)}")
    # Remove MenuPage records with invalid menu_ids
    before_ic_removal = len(menupage_df)
    menupage_df_clean = menupage_df[menupage_df['menu_id'].isin(valid_menu_ids)].copy()
    after_ic_removal = len(menupage_df_clean)
    ic_removed_count = before_ic_removal - after_ic_removal
    print(f"Removed {ic_removed_count} MenuPage records with invalid menu_id")
    # @end remove_ic_violation_menupages

    # @begin clean_invalid_page_numbers
    # @in menupage_df_clean_step1
    # @out menupage_df_clean_step1_step2
    print("\n\n\nStep 2 - Clean Invalid Page Numbers")
    # Count invalid page numbers before cleaning
    # As shown in the stats notebook, there are null page number values
    null_page_numbers = menupage_df_clean['page_number'].isnull().sum()
    print(f"Null page_number values: {null_page_numbers}")
    before_page_cleaning = len(menupage_df_clean)
    menupage_df_clean = menupage_df_clean[menupage_df_clean['page_number'].notna()].copy()
    after_page_cleaning = len(menupage_df_clean)
    page_removed_count = before_page_cleaning - after_page_cleaning
    print(f"Removed {page_removed_count} records with invalid page numbers")
    # @end clean_invalid_page_numbers
    
    # @begin write_cleaned_dataset
    # @in menupage_df_clean_step1_step2
    # @out menupage_cleaned_csv_file
    print("\n\n\nWrite Cleansed Dataset")
    output_dir = 'data/clean'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'MenuPage_cleaned.csv')
    menupage_df_clean.to_csv(output_file, index=False)
    
    print(f"Cleaned dataset written to: {output_file}")
    # @end write_cleaned_dataset
    
    # Final summary
    print("\n\n\nFinal Summary of Cleaning Process")
    original_count = len(menupage_df)
    final_count = len(menupage_df_clean)
    total_removed = original_count - final_count
    
    print(f"Original records: {original_count}")
    print(f"Final records: {final_count}")
    print(f"Total records removed: {total_removed}")
# @end menupage_data_cleaning_workflow

if __name__ == "__main__":
    main()


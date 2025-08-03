-- 1. Count total rows
SELECT 
    COUNT(*) as total_rows
FROM MenuItem;

-- 2. Count rows with invalid price values (null, blank, non-numerical or negative)
SELECT 
    COUNT(*) as invalid_price_count
FROM MenuItem 
WHERE price IS NULL 
  OR TRIM(CAST(price AS TEXT)) = ''
  OR CAST(price AS TEXT) NOT GLOB '[0-9]*'
  OR CAST(price AS TEXT) GLOB '*[^0-9.]*';

-- 3. Count rows with null or blank high_price values
SELECT 
    COUNT(*) as null_high_price_count
FROM MenuItem 
WHERE high_price IS NULL OR TRIM(CAST(high_price AS TEXT)) = '';

-- 4. Count rows with non-numerical high_price values (not empty but invalid format)
SELECT 
    COUNT(*) as non_numerical_high_price_count
FROM MenuItem 
WHERE high_price IS NOT NULL 
  AND TRIM(CAST(high_price AS TEXT)) != ''
  AND (CAST(high_price AS TEXT) NOT GLOB '[0-9]*'
       OR CAST(high_price AS TEXT) GLOB '*[^0-9.]*');

-- 5. Count rows where price > high_price (both must be numerical)
SELECT 
    COUNT(*) as bad_data_count
FROM MenuItem 
WHERE price IS NOT NULL 
  AND high_price IS NOT NULL 
  AND TRIM(CAST(price AS TEXT)) != ''
  AND TRIM(CAST(high_price AS TEXT)) != ''
  AND CAST(price AS TEXT) GLOB '[0-9]*'
  AND CAST(price AS TEXT) NOT GLOB '*[^0-9.]*'
  AND CAST(high_price AS TEXT) GLOB '[0-9]*'
  AND CAST(high_price AS TEXT) NOT GLOB '*[^0-9.]*'
  AND CAST(price AS REAL) > CAST(high_price AS REAL);

-- 6. Count rows with null or blank values in key columns
SELECT 
    COUNT(*) as missing_key_data_count
FROM MenuItem 
WHERE id IS NULL 
  OR TRIM(CAST(id AS TEXT)) = ''
  OR menu_page_id IS NULL 
  OR TRIM(CAST(menu_page_id AS TEXT)) = ''
  OR created_at IS NULL 
  OR TRIM(CAST(created_at AS TEXT)) = ''
  OR updated_at IS NULL 
  OR TRIM(CAST(updated_at AS TEXT)) = ''
  OR xpos IS NULL 
  OR TRIM(CAST(xpos AS TEXT)) = ''
  OR ypos IS NULL 
  OR TRIM(CAST(ypos AS TEXT)) = '';

-- 7. Count rows with non-numerical xpos or ypos values (not empty but invalid format)
SELECT 
    COUNT(*) as non_numerical_position_count
FROM MenuItem 
WHERE (xpos IS NOT NULL 
       AND TRIM(CAST(xpos AS TEXT)) != ''
       AND (CAST(xpos AS TEXT) NOT GLOB '[0-9]*'
            OR CAST(xpos AS TEXT) GLOB '*[^0-9.]*'))
   OR (ypos IS NOT NULL 
       AND TRIM(CAST(ypos AS TEXT)) != ''
       AND (CAST(ypos AS TEXT) NOT GLOB '[0-9]*'
            OR CAST(ypos AS TEXT) GLOB '*[^0-9.]*'));

-- 8. (After clean) Count total rows
SELECT 
    COUNT(*) as total_rows
FROM MenuItemClean;

-- 9. (After clean) Count rows with invalid price values (null, blank, non-numerical or negative)
SELECT 
    COUNT(*) as invalid_price_count
FROM MenuItemClean 
WHERE price IS NULL 
  OR TRIM(CAST(price AS TEXT)) = ''
  OR CAST(price AS TEXT) NOT GLOB '[0-9]*'
  OR CAST(price AS TEXT) GLOB '*[^0-9.]*';

-- 10. (After clean) Count rows with null or blank high_price values
SELECT 
    COUNT(*) as null_high_price_count
FROM MenuItemClean 
WHERE high_price IS NULL OR TRIM(CAST(high_price AS TEXT)) = '';

-- 11. (After clean) Count rows with non-numerical high_price values (not empty but invalid format)
SELECT 
    COUNT(*) as non_numerical_high_price_count
FROM MenuItemClean 
WHERE high_price IS NOT NULL 
  AND TRIM(CAST(high_price AS TEXT)) != ''
  AND (CAST(high_price AS TEXT) NOT GLOB '[0-9]*'
       OR CAST(high_price AS TEXT) GLOB '*[^0-9.]*');

-- 12. (After clean) Count rows where price > high_price (both must be numerical)
SELECT 
    COUNT(*) as bad_data_count
FROM MenuItemClean 
WHERE price IS NOT NULL 
  AND high_price IS NOT NULL 
  AND TRIM(CAST(price AS TEXT)) != ''
  AND TRIM(CAST(high_price AS TEXT)) != ''
  AND CAST(price AS TEXT) GLOB '[0-9]*'
  AND CAST(price AS TEXT) NOT GLOB '*[^0-9.]*'
  AND CAST(high_price AS TEXT) GLOB '[0-9]*'
  AND CAST(high_price AS TEXT) NOT GLOB '*[^0-9.]*'
  AND CAST(price AS REAL) > CAST(high_price AS REAL);

-- 13. (After clean) Count rows with null or blank values in key columns
SELECT 
    COUNT(*) as missing_key_data_count
FROM MenuItemClean 
WHERE id IS NULL 
  OR TRIM(CAST(id AS TEXT)) = ''
  OR menu_page_id IS NULL 
  OR TRIM(CAST(menu_page_id AS TEXT)) = ''
  OR created_at IS NULL 
  OR TRIM(CAST(created_at AS TEXT)) = ''
  OR updated_at IS NULL 
  OR TRIM(CAST(updated_at AS TEXT)) = ''
  OR xpos IS NULL 
  OR TRIM(CAST(xpos AS TEXT)) = ''
  OR ypos IS NULL 
  OR TRIM(CAST(ypos AS TEXT)) = '';

-- 14. (After clean) Count rows with non-numerical xpos or ypos values (not empty but invalid format)
SELECT 
    COUNT(*) as non_numerical_position_count
FROM MenuItemClean 
WHERE (xpos IS NOT NULL 
       AND TRIM(CAST(xpos AS TEXT)) != ''
       AND (CAST(xpos AS TEXT) NOT GLOB '[0-9]*'
            OR CAST(xpos AS TEXT) GLOB '*[^0-9.]*'))
   OR (ypos IS NOT NULL 
       AND TRIM(CAST(ypos AS TEXT)) != ''
       AND (CAST(ypos AS TEXT) NOT GLOB '[0-9]*'
            OR CAST(ypos AS TEXT) GLOB '*[^0-9.]*'));



-- queries

-- TOTAL COMPANIES TRACKED
SELECT count(*) 
    FROM `companies`;

-- RECENT TECH
SELECT symbol, name, sector, industry, ipo_year, last_sale, high_52_weeks, low_52_weeks 
    FROM `stocks`.`companies`
    WHERE 
        sector "Technology" 
        AND 
        ipo_year IN ("2017", "2016") 
    ORDER BY last_sale;

-- RECENT SECTORS IN LAST 2 YEARS
SELECT DISTINCT (`sector`), count(*)
    FROM `stocks`.`companies`
    WHERE `ipo_year` IN ("2017", "2016") 
    GROUP BY 1
    ORDER BY 2;


SELECT c.name, m.meta_type, m.meta_value, m.val_varchar 
    FROM stocks.companies c
    JOIN stocks.meta m
    ON c.id=m.entity_id AND m.entity_type='company';


SELECT c.name, c.sector, m.meta_type,  m.val_varchar 
    FROM stocks.companies c
        JOIN stocks.meta m
            ON c.id=m.entity_id AND m.entity_type='company'
    WHERE
        m.meta_key = 'wikipedia_url';

select * from stocks.meta;
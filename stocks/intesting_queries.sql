-- queries

-- TOTAL COMPANIES TRACKED
SELECT count(*) 
    FROM `companies`;

-- RECENT TECH
SELECT symbol, name, sector, industry, ipo_year, last_sale, high_52_weeks, low_52_weeks 
    FROM `stocks`.`companies`
    WHERE 
        sector="Technology" 
        AND 
        ipo_year IN ("2017", "2016") 
    ORDER BY last_sale;

-- RECENT SECTORS IN LAST 2 YEARS
SELECT DISTINCT (`sector`), count(*)
    FROM `stocks`.`companies`
    WHERE `ipo_year` IN ("2017", "2016") 
    GROUP BY 1
    ORDER BY 2;

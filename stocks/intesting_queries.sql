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


SELECT c.name, m.meta_key, m.val_varchar 
    FROM stocks.companies c
    JOIN stocks.meta m
    ON c.id=m.entity_id AND m.entity_type='company';


-- COMPANIES WITH WIKI URL
SELECT c.name, c.sector,  m.val_text, m.ts_update
    FROM stocks.companies c
        JOIN stocks.meta m
            ON c.id=m.entity_id AND m.entity_type='company'
    WHERE
        m.meta_key = 'wikipedia_url'
    ORDER BY m.ts_update DESC;

-- COMPANIES WITH WIKI SEARCH ERRORS

SELECT c.name, m.val_datetime, m.ts_update
    FROM stocks.companies c
        JOIN stocks.meta m
            ON c.id=m.entity_id AND m.entity_type='company'
    WHERE
        m.meta_key = 'daily'
    ORDER BY m.ts_update DESC;


-- compaies with meta
SELECT c.name, c.sector, m.meta_key, m.val_text, m.ts_update
    FROM stocks.companies c
        JOIN stocks.meta m
            ON c.id=m.entity_id AND m.entity_type='company'
    WHERE
        m.meta_key = 'dividend_stock'
    ORDER BY m.ts_update DESC;





-- Companies with high close avg price, min price and max close
select c.name, AVG(q.close), MIN(q.close), MAX(q.close)
    from companies c
    join quotes q
        on c.id = q.company_id
    join meta m
        ON 
            m.entity_id = c.id AND
            m.entity_type = 'company' AND
    group by 1
    order by 4 desc
    limit 50;
    

-- different types and counts of meta
select distinct meta_key, count(*) from meta group by 1 order by 2 desc;




-- QA daily

select distinct left(val_datetime, 10), count(*)
from meta 
where meta_key = "daily_google"
group by 1;





select distinct company_id, left(`date`, 10), count(*)
from stocks.quotes
where company_id =178
group by 1, 2;
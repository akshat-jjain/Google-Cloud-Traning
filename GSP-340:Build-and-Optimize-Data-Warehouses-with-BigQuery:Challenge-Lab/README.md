# Build and Optimize Data Warehouses with BigQuery: Challenge Lab
### Task 1 :- 
``` sql
CREATE OR REPLACE TABLE covid_165.oxford_policy_tracker_474 PARTITION BY date OPTIONS( partition_expiration_days=360, description="oxford_policy_tracker table in the COVID 19 Government Response public dataset with  an expiry time set to 360 days." ) AS SELECT * FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker` WHERE alpha_3_code NOT IN ('GBR', 'BRA', 'CAN','USA')
```
### Task 2 :- 
``` sql
ALTER TABLE covid_165.oxford_policy_tracker_474
ADD COLUMN IF NOT EXISTS population INT64,
ADD COLUMN IF NOT EXISTS country_area FLOAT64,
ADD COLUMN IF NOT EXISTS mobility STRUCT<avg_retail FLOAT64,
avg_grocery FLOAT64,
avg_parks FLOAT64,
avg_transit FLOAT64,
avg_workplace FLOAT64,
avg_residential FLOAT64>
```
### Task 3 :- 
``` sql
CREATE OR REPLACE TABLE covid_165.pop_data_2019 AS SELECT country_territory_code, pop_data_2019 FROM `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide` GROUP BY country_territory_code,  pop_data_2019 ORDER BY country_territory_code;

UPDATE `covid_165.oxford_policy_tracker_474` t0
SET population = t1.pop_data_2019
FROM `covid_800.pop_data_2019` t1
WHERE CONCAT(t0.alpha_3_code) = CONCAT(t1.country_territory_code);
```
### Task 4 :- 
``` sql
UPDATE `covid_165.oxford_policy_tracker_474` t0 SET t0.country_area = t1.country_area FROM `bigquery-public-data.census_bureau_international.country_names_area` t1 WHERE t0.country_name = t1.country_name;
```
### Task 5 :- 
``` sql
UPDATE `covid_165.oxford_policy_tracker_474` t0 SET t0.mobility.avg_retail      = t1.avg_retail, t0.mobility.avg_grocery     = t1.avg_grocery,
t0.mobility.avg_parks       = t1.avg_parks,
t0.mobility.avg_transit     = t1.avg_transit, t0.mobility.avg_workplace   = t1.avg_workplace, t0.mobility.avg_residential = t1.avg_residential
FROM ( SELECT country_region, date, AVG(retail_and_recreation_percent_change_from_baseline) as avg_retail, AVG(grocery_and_pharmacy_percent_change_from_baseline)  as avg_grocery, AVG(parks_percent_change_from_baseline) as avg_parks, AVG(transit_stations_percent_change_from_baseline) as avg_transit, AVG(workplaces_percent_change_from_baseline) as avg_workplace, AVG(residential_percent_change_from_baseline)  as avg_residential FROM `bigquery-public-data.covid19_google_mobility.mobility_report` GROUP BY country_region, date ) AS t1 WHERE CONCAT(t0.country_name, t0.date) = CONCAT(t1.country_region, t1.date)
```
### Task 6:- 
``` sql
SELECT country_name, population FROM `covid_165.oxford_policy_tracker_474` WHERE population is NULL;

SELECT country_name, country_area FROM `covid_165.oxford_policy_tracker_474` WHERE country_area IS NULL;

SELECT DISTINCT country_name FROM `covid_165.oxford_policy_tracker_474` WHERE population is NULL UNION ALL SELECT DISTINCT country_name FROM `covid_165.oxford_policy_tracker_474` WHERE country_area IS NULL ORDER BY country_name
```

# ☁ Engineer Data in Google Cloud: Challenge Lab | logbook

 
In this article, we will go through the lab GSP327 Engineer Data in Google Cloud: Challenge Lab, which is labeled as an expert-level exercise. You will practice the skills and knowledge to build a prediction model of taxi fares using machine learning with BigQuery.

## The challenge contains 3 required tasks:

- Clean your training data
- Create a BQML model called taxirides.fare_model
- Perform a batch prediction on new data

## Task 1: Clean your training data
In this task, you need to make a copy of `historical_taxi_rides_raw` to `taxi_training_data` in the given `taxirides` dataset in BigQuery.

> **Hints**: Refer to the lab **GSP426** Predict Taxi Fare with a BigQuery ML Forecasting Model on Qwiklabs

Make sure that:

- target column is called `fare_amount`
Data Cleaning Tasks:

- Keep rows for `trip_distance` > 0
- Remove rows for `fare_amount` > 2.5
- Ensure that the latitudes and longitudes are reasonable for the use case. ??
- Create a new column called `total_amount` from `tolls_amount` + `fare_amount`
- Sample the dataset < 1,000,000 rows
- Only copy fields that will be used in your model
<br>
Procedures:

1. In the Cloud Console, navigate to **Menu > BigQuery**.
2. Click on **More > Query settings** under the Query Editor.
3. Select **Set a destination table for query results** under Destination; Enter `taxi_training_data` as the Table name
4. Click **Save**
5. Run the following SQL query
``` sql
Select
  pickup_datetime,
  pickup_longitude AS pickuplon,
  pickup_latitude AS pickuplat,
  dropoff_longitude AS dropofflon,
  dropoff_latitude AS dropofflat,
  passenger_count AS passengers,
  ( tolls_amount + fare_amount ) AS fare_amount
FROM
  `taxirides.historical_taxi_rides_raw`
WHERE
  trip_distance > 0
  AND fare_amount >= 2.5
  AND pickup_longitude > -75
  AND pickup_longitude < -73
  AND dropoff_longitude > -75
  AND dropoff_longitude < -73
  AND pickup_latitude > 40
  AND pickup_latitude < 42
  AND dropoff_latitude > 40
  AND dropoff_latitude < 42
  AND passenger_count > 0
  AND RAND() < 999999 / 1031673361
```
## Task 2: Create a BQML model called `taxirides.fare_model`
In this task, you need to:

- Create a model called `taxirides.fare_model`
- Train the model with an RMSE < 10
> **Hints**: Refer to the lab **GSP426** Predict Taxi Fare with a BigQuery ML Forecasting Model on Qwiklabs

Create a model
Compose a new query with the given `ST_distance()` and `ST_GeogPoint()` functions in the Query Editor.

Make sure that:

- set `fare_amount` as the label
- train with the data in `taxirides.taxi_training_data`
The SQL query to create the BQML model can be coded to be:
``` sql
CREATE or REPLACE MODEL
  taxirides.fare_model OPTIONS (model_type='linear_reg',
    labels=['fare_amount']) AS
WITH
  taxitrips AS (
  SELECT
    *,
    ST_Distance(ST_GeogPoint(pickuplon, pickuplat), ST_GeogPoint(dropofflon, dropofflat)) AS euclidean
  FROM
    `taxirides.taxi_training_data` )
  SELECT
    *
  FROM
    taxitrips
 ```
Click **Run** and the machine learning process will take about 2 minutes.

Evaluate model performance
After the training completed, you can evaluate the **Root Mean Square Error (RMSE)** of the prediction model using the following query.
``` sql
#standardSQL
SELECT
  SQRT(mean_squared_error) AS rmse
FROM
  ML.EVALUATE(MODEL taxirides.fare_model,
    (
    WITH
      taxitrips AS (
      SELECT
        *,
        ST_Distance(ST_GeogPoint(pickuplon, pickuplat), ST_GeogPoint(dropofflon, dropofflat)) AS euclidean
      FROM
        `taxirides.taxi_training_data` )
      SELECT
        *
      FROM
        taxitrips ))
```

## Task 3: Perform a batch prediction on new data
In this task, you need to use the BQML model to predict the taxi fares of the data given in the `taxirides.report_prediction_data` table.


Make sure that:

- store your results in a table called `2015_fare_amount_predictions`.
<br>
Procedures:

1. Select **Set a destination table for query results under** Destination; Enter `2015_fare_amount_predictions` as the Table name
2. Click **Save**
3. Run the following SQL query.
``` sql
#standardSQL
SELECT
  *
FROM
  ML.PREDICT(MODEL `taxirides.fare_model`,
    (
    WITH
      taxitrips AS (
      SELECT
        *,
        ST_Distance(ST_GeogPoint(pickuplon, pickuplat)   , ST_GeogPoint(dropofflon, dropofflat)) AS    euclidean
      FROM
        `taxirides.report_prediction_data` )
    SELECT
      *
    FROM
      taxitrips ))
``` 

### Congratulations! You completed this challenge lab.

# Demonstration Video

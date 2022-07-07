# Create ML Models with BigQuery ML: Challenge Lab

This article will go through the lab to Create ML Models with BigQuery ML: Challenge Lab. In the previous, lab you will get familiar with Getting Started with BQML, Predict Visitor Purchases with a Classification Model in BQML, Predict Taxi Fare with a BigQuery ML Forecasting Model, Bracketology with Google Machine Learning, and Implement a Helpdesk Chatbot with Dialogflow & BigQuery ML.
### The challenge contains 5 required tasks.
1. Create a dataset to store your machine learning models.
2. Create a forecasting BigQuery machine learning model.
3. Create the second machine learning model.
4. Evaluate the two machine learning models.
5. Use the subscriber type machine learning model to predict average trip durations.
# Challenge Scenario

One of the projects you are working on needs to provide analysis based on real-world data that will help in the selection of new bicycle models for public bike share systems. Your role in this project is to develop and evaluate machine learning models that can predict average trip durations for bike schemes using the public data from Austin’s public bike share scheme to train and evaluate your models.
Two of the senior data scientists in your team have different theories on what factors are important in determining the duration of a bike-share trip and you have been asked to prioritize these to start. The first data scientist maintains that the key factors are the start station, the location of the start station, the day of the week, and the hour the trip started. While the second data scientist argues that this is an over-complication and the key factors are simply start station, subscriber type, and the hour the trip started.<br>
You have been asked to develop a machine learning model based on each of these input features. Given the fact that stay-at-home orders were in place for Austin during parts of 2020 as a result of COVID-19, you will be working on data from previous years. You have been instructed to train your models on data from 2018 and then evaluate them against data from 2019 based on Mean Absolute Error and the square root of Mean Squared Error.
You can access the public data for the Austin bike share scheme in your project by opening this link to the Austin bike share dataset in the browser tab for your lab.
As a final step, you must create and run a query that uses the model that includes subscriber type as a feature, to predict the average trip duration for all trips from the busiest bike-sharing station in 2019 (based on the number of trips per station in 2019) where the subscriber type is ‘Single Trip’.

## TASK 1: Create a dataset to store your machine learning models

### Steps:-

1. This dataset will be used to store our BQML models.
2. In the GCP Console go to **Navigation Menu >BigQuery**.
3. Click on Create Dataset.
4. Write the name of the Dataset you want I have Used `bike`.
5. Click on Create Dataset.

> Replace `EVALUTION_YEAR` And `TRAINING_YEAR` With Your Ones

## TASK 2: Create a forecasting BigQuery machine learning model

### Steps :

1. This task asks us to train a model-based.
2. Copy and paste the following code to the Query editor and then click Run.

``` sql
CREATE OR REPLACE MODEL bike.location_model
OPTIONS
  (model_type='linear_reg', labels=['duration_minutes']) AS
SELECT
    start_station_name,
    EXTRACT(HOUR FROM start_time) AS start_hour,
    EXTRACT(DAYOFWEEK FROM start_time) AS day_of_week,
    start_station_name AS location,
    duration_minutes
FROM
    `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
JOIN
    `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
ON
    trips.start_station_name = stations.name
WHERE
    EXTRACT(YEAR FROM start_time) = TRAINING_YEAR
    AND duration_minutes > 0
```

3. The query should return the starting station name, the hour the trip started, the weekday of the trip, and the address of the start station.


## TASK 3: Create the second machine learning model

### Steps :-

1. Similar to the second task, this task requires you to train a second model.
2. Click on compose new query and then copy and paste the following query into the BigQuery Query editor.

``` sql
CREATE OR REPLACE MODEL bike.subscriber_model
OPTIONS
  (model_type='linear_reg', labels=['duration_minutes']) AS
SELECT
    start_station_name,
    EXTRACT(HOUR FROM start_time) AS start_hour,
    subscriber_type,
    duration_minutes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
WHERE EXTRACT(YEAR FROM start_time) = TRAINING_YEAR
```

3. The query should return to predict the trip duration for bike trips.


## TASK 4: Evaluate the two machine learning models

### Steps:-

1. Click on compose new query and then copy and paste the following query into the BigQuery Query editor.

``` sql
-- Evaluation metrics for location_model
SELECT
  SQRT(mean_squared_error) AS rmse,
  mean_absolute_error
FROM
  ML.EVALUATE(MODEL bike.location_model, (
  SELECT
    start_station_name,
    EXTRACT(HOUR FROM start_time) AS start_hour,
    EXTRACT(DAYOFWEEK FROM start_time) AS day_of_week,
    start_station_name As location,
    duration_minutes
  FROM
    `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
  JOIN
   `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON
    trips.start_station_name = stations.name
  WHERE EXTRACT(YEAR FROM start_time) = EVALUTION_YEAR)
)
```

2. Click on compose new query and then copy and paste the following query into the BigQuery Query editor.

``` sql
-- Evaluation metrics for subscriber_model
SELECT
  SQRT(mean_squared_error) AS rmse,
  mean_absolute_error
FROM
  ML.EVALUATE(MODEL bike.subscriber_model, (
  SELECT
    start_station_name,
    EXTRACT(HOUR FROM start_time) AS start_hour,
    subscriber_type,
    duration_minutes
  FROM
    `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
  WHERE
    EXTRACT(YEAR FROM start_time) = EVALUTION_YEAR)
)
```

3. The query should return both the Mean Absolute Error and the Root Mean Square Error of the Model.

## TASK 5: Use the subscriber type machine learning model to predict average trip durations

### Steps:-
1. In this task, we are required to calculate the average predicted trip time for the busiest station.
2. Click on compose new query and then copy and paste the following query into the BigQuery Query editor.

``` sql
SELECT
  start_station_name,
  COUNT(*) AS trips
FROM
  `bigquery-public-data.austin_bikeshare.bikeshare_trips`
WHERE
  EXTRACT(YEAR FROM start_time) = EVALUTION_YEAR
GROUP BY
  start_station_name
ORDER BY
  trips DESC
```


3. Click on compose new query and then copy and paste the following query into the BigQuery Query editor.
4. The query should return the busiest station

``` sql
SELECT AVG(predicted_duration_minutes) AS average_predicted_trip_length
FROM ML.predict(MODEL bike.subscriber_model, (
SELECT
    start_station_name,
    EXTRACT(HOUR FROM start_time) AS start_hour,
    subscriber_type,
    duration_minutes
FROM
  `bigquery-public-data.austin_bikeshare.bikeshare_trips`
WHERE 
  EXTRACT(YEAR FROM start_time) = EVALUTION_YEAR
  AND subscriber_type = 'Single Trip'
  AND start_station_name = '21st & Speedway @PCL'))
```

5. The query should return the average trip time.



# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13

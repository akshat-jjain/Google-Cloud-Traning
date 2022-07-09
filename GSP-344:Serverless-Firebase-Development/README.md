# Serverless Firebase Development: Challenge Lab


### Overview
In a challenge lab you’re given a scenario and a set of tasks. Instead of following step-by-step instructions, you will use the skills learned from the labs in the quest to figure out how to complete the tasks on your own! An automated scoring system (shown on this page) will provide feedback on whether you have completed your tasks correctly.<br>

When you take a challenge lab, you will not be taught new Google Cloud concepts. You are expected to extend your learned skills, like changing default values and reading and researching error messages to fix your own mistakes.<br>

To score 100% you must successfully complete all tasks within the time period!<br>

This lab is recommended for students who are enrolled in the Serverless Firebase Development quest. Are you ready for the challenge?

### Provision the environment
- Link to the project:
``` bash
  gcloud config set project $(gcloud projects list --format='value(PROJECT_ID)' --filter='qwiklabs-gcp')
```
- Clone the repo:
``` bash
  git clone https://github.com/rosera/pet-theory.git
```
- Replace with your `DATASET_SERVICE_NAME`
``` bash
export DATASET_SERVICE_NAME=DATASET_SERVICE_NAME
```
- Replace with your `FRONTEND_STAGING_SERVICE`
``` bash
export FRONTEND_STAGING_SERVICE=FRONTEND_STAGING_SERVICE
```
- Replace with your `FRONTEND_PRODUCTION_SERVICE`
``` bash
export FRONTEND_PRODUCTION_SERVICE=FRONTEND_PRODUCTION_SERVICE
```

### Task 1: Create a Firestore database
- Navigation > Firestore
- Select `Native Mode` in Cloud Firestore
- Select `Nam5 (United States)` in Location
- Click Create Database.


### Task 2: Populate the Database
``` bash
cd pet-theory/lab06/firebase-import-csv/solution
npm install
node index.js netflix_titles_original.csv
```
### Task 3: Create a REST API
``` bash
cd ~/pet-theory/lab06/firebase-rest-api/solution-01
npm install
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/rest-api:0.1
gcloud beta run deploy $DATASET_SERVICE_NAME --image gcr.io/$GOOGLE_CLOUD_PROJECT/rest-api:0.1 --allow-unauthenticated
```
### Task 4: Firestore API access

``` bash
cd ~/pet-theory/lab06/firebase-rest-api/solution-02
npm install
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/rest-api:0.2
gcloud beta run deploy $DATASET_SERVICE_NAME --image gcr.io/$GOOGLE_CLOUD_PROJECT/rest-api:0.2 --allow-unauthenticated
```
- Replace with your `SERVICE_URL`
``` bash
SERVICE_URL=<copy url from your netflix-dataset-service>
curl -X GET $SERVICE_URL/2019
```

### Task 5: Deploy the Staging Frontend

- Paste Your Service Url at line 5 and uncomment it by removing slashes and comment line 4 by adding slashes
- Don't Remove `/2020` in  Service URL 
``` bash
cd ~/pet-theory/lab06/firebase-frontend/public
nano app.js
```

``` bash
npm install
cd ~/pet-theory/lab06/firebase-frontend
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/frontend-staging:0.1
gcloud beta run deploy $FRONTEND_STAGING_SERVICE --image gcr.io/$GOOGLE_CLOUD_PROJECT/frontend-staging:0.1
```
### Task 6: Deploy the Production Frontend
``` bash
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/frontend-production:0.1
gcloud beta run deploy $FRONTEND_PRODUCTION_SERVICE --image gcr.io/$GOOGLE_CLOUD_PROJECT/frontend-production:0.1
```

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13
- YouTube Channel: https://youtube.com/channel/UCQUEgfYbcz7pv36NoAv7S-Q/

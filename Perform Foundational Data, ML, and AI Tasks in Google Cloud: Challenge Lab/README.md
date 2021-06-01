# ☁ Perform Foundational Data, ML, and AI Tasks in Google Cloud: Challenge Lab | logbook

 
In this article, we will go through the lab GSP323 Perform Foundational Data, ML, and AI Tasks in Google Cloud: Challenge Lab, which is labeled as an expert-level exercise. You will practice the skills and knowledge for running Dataflow, Dataproc, and Dataprep as well as Google Cloud Speech API.

 **The challenge contains 4 required tasks:**


# Task 1: Run a simple Dataflow job
In this task, you have to transfer the data in a CSV file to BigQuery using Dataflow via Pub/Sub. First of all, you need to create a BigQuery dataset called `lab` and a Cloud Storage bucket called with your project ID.


## 1.1 Created a BigQuery dataset called `lab`
1. In the Cloud Console, click on **Navigation Menu > BigQuery.**
2. Select your project in the left pane.
3. Click **CREATE DATASET.**
4. Enter `lab` in the Dataset ID, then click **Create dataset**.
5. (Optional) Run ```gsutil cp gs://cloud-training/gsp323/lab.schema .``` in the Cloud Shell to download the schema file.
6. View the schema by running `cat lab.schema.`
7. Go back to the Cloud Console, select the new dataset **lab** and click **Create Table**.
8. In the Create table dialog, select **Google Cloud Storage** from the dropdown in the Source section.
9. Copy `gs://cloud-training/gsp323/lab.csv` to Select file from GCS bucket.
10. Enter `customers` to “Table name” in the Destination section.
11. Enable **Edit as text** and copy the JSON data from the `lab.schema` file to the textarea in the Schema section.
12. Click `Create table`.

## 1.2 Create a Cloud Storage bucket
1. In the Cloud Console, click on **Navigation Menu > Storage**.
2. Click **CREATE BUCKET**.
3. Copy your GCP Project ID to Name your bucket.
4. Click **CREATE**.

## 1.3 Create a Dataflow job
1. In the Cloud Console, click on **Navigation Menu > Dataflow**.
2. Click **CREATE JOB FROM TEMPLATE**.
3. In Create job from template, give an arbitrary job name.
4. From the dropdown under Dataflow template, select **Text Files on Cloud Storage Pub/Sub** under “Process Data in Bulk (batch)”. (DO **NOT** select the item under “Process Data Continuously (stream)”).
5. Under the Required parameters, enter the following values:

Field |	Value
------|------
JavaScript UDF path in Cloud Storage |	`gs://cloud-training/gsp323/lab.js`
JSON path |	`gs://cloud-training/gsp323/lab.schema`
JavaScript UDF name |	`transform`
BigQuery output table	| `YOUR_PROJECT:lab.customers`
Cloud Storage input path |	`gs://cloud-training/gsp323/lab.csv`
Temporary BigQuery directory |	`gs://YOUR_PROJECT/bigquery_temp`
Temporary location |	`gs://YOUR_PROJECT/temp`

**Replace** `YOUR_PROJECT` with your project ID.

6. Click RUN JOB.

# Task 2: Run a simple Dataproc job
### Create a Dataproc cluster
1. In the Cloud Console, click on **Navigation Menu > Dataproc > Clusters**.
2. Click **CREATE CLUSTER**.
3. Make sure the cluster is going to create in the region `us-central1`.
4. Click **Create**.
5. After the cluster has been created, click the **SSH** button in the row of the master instance.
6. In the SSH console, run the following command:
```
hdfs dfs -cp gs://cloud-training/gsp323/data.txt /data.txt
```
7. Close the SSH window and go back to the Cloud Console.
8. Click **SUBMIT JOB** on the cluster details page.
9. Select Spark from the dropdown of “Job type”.
10. Copy `org.apache.spark.examples.SparkPageRank` to “Main class or jar”.
11. Copy `file:///usr/lib/spark/examples/jars/spark-examples.jar` to “Jar files”.
12. Enter `/data.txt` to “Arguments”.
13. Click **CREATE**.
# Task 3: Run a simple Dataprep job
### Import runs.csv to Dataprep
1. In the Cloud Console, click on **Navigation menu > Dataprep**.
2. After entering the home page of Cloud Dataprep, click the **Import Data** button.
3. In the Import Data page, select **GCS** in the left pane.
4. Click on the pencil icon under Choose a file or folder.
5. Copy below code and paste it to the textbox, and click the **Go** button next to it.
```
gs://cloud-training/gsp323/runs.csv 
```
6. After showing the preview of runs.csv in the right pane, click on the **Import & Wrangle button**.
### Transform data in Dataprep
1. After launching the Dataperop Transformer, scroll right to the end and select **column10**.
2. In the Details pane, click **FAILURE** under Unique Values to show the context menu.
3. Select **Delete rows with selected values** to Remove all rows with the state of “FAILURE”.
4. Click the downward arrow next to **column9**, choose **Filter rows > On column value > Contains**.
5. In the Filter rows pane, enter the regex pattern `/(^0$|^0\.0$)/` to “Pattern to match”.
6. Select **Delete matching rows** under the Action section, then click the **Add** button.
7. Rename the columns to be:

- runid
- userid
- labid
- lab_title
- start
- end
- time
- score
- state
8. Confirm the recipe. It should like the screenshot below.
9. Click Run Job.


# Task 4: AI
### Use Google Cloud Speech API to analyze the audio file
1. In the Cloud Console, click on **Navigation menu > APIs & Services > Credentials**.
2. In the Credentials page, click on **+ CREATE CREDENTIALS > API key**.
3. Copy the API key to the clipboard, then click **RESTRICT KEY**.
4. Open the Cloud Shell, store the API key as an environment variable by running the following command:
```
export API_KEY=<YOUR-API-KEY>
```
> Replace <YOUR-API-KEY> with the copied key value.

5. In the Cloud Shell, create a JSON file called `gsc-request.json`.
6. Save the following codes to the file.
```
{
  "config": {
      "encoding":"FLAC",
      "languageCode": "en-US"
  },
  "audio": {
      "uri":"gs://cloud-training/gsp323/task4.flac"
  }
}
```
7. Use the following `curl` command to submit the request to Google Cloud Speech API and store the response to a file called `task4-gcs.result`.
```
curl -s -X POST -H "Content-Type: application/json" --data-binary @gsc-request.json \
"https://speech.googleapis.com/v1/speech:recognize?key=${API_KEY}" > task4-gcs.result
```
8. Upload the resulted file to Cloud Storage by running:
```
gsutil cp task4-gcs.result gs://<YOUR-PROJECT_ID>-marking/task4-gcs.result
```
> Replace <YOUR-PROJECT_ID> with your project ID.

### Use the Cloud Natural Language API to analyze the sentence
1. In the Cloud Shell, run the following command to use the Cloud Natural Language API to analyze the given sentence.

```
gcloud ml language analyze-entities --content="Old Norse texts portray Odin as one-eyed and long-bearded, frequently wielding a spear named Gungnir and wearing a cloak and a broad hat." > task4-cnl.result
```
2. Upload the resulted file to Cloud Storage by running:
```
gsutil cp task4-cnl.result gs://<YOUR-PROJECT_ID>-marking/task4-cnl.result
```
> Replace <YOUR-PROJECT_ID> with your project ID.

### Use Google Video Intelligence and detect all text on the video
1. In the Cloud Shell, create a JSON file called `gvi-request.json`.
2. Save the following codes to the file.
```
{
   "inputUri":"gs://spls/gsp154/video/train.mp4",
   "features": [
       "LABEL_DETECTION"
   ]
}
  ```
3. Go back to the Cloud Console, click on **Navigation menu > APIs & Services > Credentials**.
4. Click the service account named with “Qwiklabs User Service Account” to view the details.
5. Click **ADD KEY > Create new key**.
6. Choose **JSON** and click **CREATE** to download the Private key file to your computer.
7. Upload the file to the Cloud Shell environment.
8. Rename the uploaded file to `key.json`.
9. Run the following commands to create a token.
```
gcloud auth activate-service-account --key-file key.json
export TOKEN=$(gcloud auth print-access-token)
```
10. Run the following command to use theGoogle Video Intelligence and detect all text on the video.
```
curl -s -H 'Content-Type: application/json' \
   -H 'Authorization: Bearer '$(gcloud auth print-access-token)'' \
   'https://videointelligence.googleapis.com/v1/videos:annotate' \
   -d @gvi-request.json > task4-gvi.result
```
11. Upload the resulted file to Cloud Storage by running:
```
gsutil cp task4-gvi.result gs://<YOUR-PROJECT_ID>-marking/task4-gvi.result
```
> Replace <YOUR-PROJECT_ID> with your project ID.



### Congratulations! You completed this challenge lab.

# Demonstration Video

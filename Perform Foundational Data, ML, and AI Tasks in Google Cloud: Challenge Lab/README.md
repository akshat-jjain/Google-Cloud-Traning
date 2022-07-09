# ☁ Perform Foundational Data, ML, and AI Tasks in Google Cloud: Challenge Lab | logbook

 
In this article, we will go through the lab GSP323 Perform Foundational Data, ML, and AI Tasks in Google Cloud: Challenge Lab, which is labeled as an expert-level exercise. You will practice the skills and knowledge for running Dataflow, Dataproc, and Dataprep as well as Google Cloud Speech API.

 **The challenge contains 4 required tasks:**

### Task 1: Run a simple Dataflow job
In this task, you have to transfer the data in a CSV file to BigQuery using Dataflow via Pub/Sub. First of all, you need to create a BigQuery dataset called `lab` and a Cloud Storage bucket called with your project ID.


#### 1.1 Created a BigQuery dataset
1. In the Cloud Console, click on **Navigation Menu > BigQuery.**
2. Select your project in the left pane.
3. Click **CREATE DATASET.**
4. Enter `dataset_name` in the Dataset ID, then click **Create dataset**.
5. Run `gsutil cp gs://cloud-training/gsp323/lab.schema .`in the Cloud Shell to download the schema file.
6. View the schema by running `cat lab.schema.` And Copy the schema
7. Go back to the Cloud Console, select the new dataset **lab** and click **Create Table**.
8. In the Create table dialog, select **Google Cloud Storage** from the dropdown in the Source section.
9. Copy `cloud-training/gsp323/lab.csv` to Select file from GCS bucket.
10. Enter `customers` to “Table name” in the Destination section.
11. Enable **Edit as text** and copy the JSON data from the `lab.schema` file to the textarea in the Schema section.
12. Click `Create table`.

#### 1.2 Create a Cloud Storage bucket
1. In the Cloud Console, click on **Navigation Menu > Storage**.
2. Click **CREATE BUCKET**.
3. Copy your Bucket Name from panel.
4. Click **CREATE**.

#### 1.3 Create a Dataflow job
1. In the Cloud Console, click on **Navigation Menu > Dataflow**.
2. Click **CREATE JOB FROM TEMPLATE**.
3. In Create job from template, give an arbitrary job name.
4. From the dropdown under Dataflow template, select **Text Files on Cloud Storage BigQuery** under “Process Data in Bulk (batch)”. (DO **NOT** select the item under “Process Data Continuously (stream)”).
5. Under the Required parameters, enter the following values:

Field |	Value
------|------
JavaScript UDF path in Cloud Storage |	`gs://cloud-training/gsp323/lab.js`
JSON path |	`gs://cloud-training/gsp323/lab.schema`
JavaScript UDF name |	`transform`
BigQuery output table	| `Use As per your lab`
Cloud Storage input path |	`gs://cloud-training/gsp323/lab.csv`
Temporary BigQuery directory |	`Use As per your lab`
Temporary location |	`Use As per your lab`

6. Click RUN JOB.

### Task 2: Run a simple Dataproc job
#### Create a Dataproc cluster
1. In the Cloud Console, click on **Navigation Menu > Dataproc > Clusters**.
2. Click **CREATE CLUSTER**.
3. Make sure the cluster is going to create in the region `Use As per your lab`.
4. Click **Create**.
5. After the cluster has been created, click the **SSH** button in the row of the master instance.
6. In the SSH console, run the following command:
``` bash
hdfs dfs -cp gs://cloud-training/gsp323/data.txt /data.txt
```
7. Close the SSH window and go back to the Cloud Console.
8. Click **SUBMIT JOB** on the cluster details page.
9. Select Spark from the dropdown of “Job type”.
10. Copy `org.apache.spark.examples.SparkPageRank` to “Main class or jar”.
11. Copy `file:///usr/lib/spark/examples/jars/spark-examples.jar` to “Jar files”.
12. Enter `/data.txt` to “Arguments”.
13. Click **CREATE**.
### Task 3: Run a simple Dataprep job
#### Import runs.csv to Dataprep
1. In the Cloud Console, click on **Navigation menu > Dataprep**.
2. After entering the home page of Cloud Dataprep, click the **Import Data** button.
3. In the Import Data page, select **GCS** in the left pane.
4. Click on the pencil icon under Choose a file or folder.
5. Copy below code and paste it to the textbox, and click the **Go** button next to it.
``` bash
gs://cloud-training/gsp323/runs.csv 
```
6. After showing the preview of runs.csv in the right pane, click on the **Import & Wrangle button**.
#### Transform data in Dataprep
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

8. Confirm the recipe.And Add it
9. Click Run Job.


### Task 4: AI

``` bash
gcloud iam service-accounts create my-natlang-sa \
  --display-name "my natural language service account"
gcloud iam service-accounts keys create ~/key.json \
  --iam-account my-natlang-sa@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com
```
#### Task:4.1 Google Cloud Speech API
``` bash
wget https://raw.githubusercontent.com/guys-in-the-cloud/cloud-skill-boosts/main/Challenge-labs/Perform%20Foundational%20Data%2C%20ML%2C%20and%20AI%20Tasks%20in%20Google%20Cloud%3A%20Challenge%20Lab/speech-request.json
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json \
"https://speech.googleapis.com/v1/speech:recognize?key=${API_KEY}" > result.json
```
- Replace with your first bucket url
``` bash
gsutil cp speech.json <enter first bucket url>
```

#### Task:4.2 Cloud Natural Language API

``` bash
gcloud ml language analyze-entities --content="Old Norse texts portray Odin as one-eyed and long-bearded, frequently wielding a spear named Gungnir and wearing a cloak and a broad hat." > language.json
```
- Replace with your second bucket url
``` bash
gsutil cp language.json <enter second bucket url>
```

#### Task:4.3 Google Video Intelligence

``` bash 
wget https://github.com/guys-in-the-cloud/cloud-skill-boosts/blob/main/Challenge-labs/Perform%20Foundational%20Data%2C%20ML%2C%20and%20AI%20Tasks%20in%20Google%20Cloud:%20Challenge%20Lab/video-intelligence-request.json
curl -s -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$(gcloud auth print-access-token)'' \
    'https://videointelligence.googleapis.com/v1/videos:annotate' \
    -d @video-intelligence-request.json  > video.json
```
- Replace with your third bucket url
``` bash
 gsutil cp video.json <enter third bucket url>
```
# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshat_jjain

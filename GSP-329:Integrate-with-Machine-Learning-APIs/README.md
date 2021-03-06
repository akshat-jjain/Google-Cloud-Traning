# Integrate with Machine Learning APIs: Challenge Lab

<div align="center"><img src="https://github.com/akshat-jjain/Qwiklabs/blob/a287500a564441cba2f5d90eb47fa4e9620fa4e2/Integrate%20with%20Machine%20Learning%20APIs/Screenshot%20(18).png" align="center" alt="Integrate with Machine Learning APIs: Challenge Lab">
</div>
<br>

### Basic Steps :
![Credentials](https://user-images.githubusercontent.com/56213740/119262455-f1ec2280-bbf8-11eb-862b-2591945d5a25.png)
  * Login to Cloud Console using given credentials.
  * Open Google Cloud Shell.

<br>

## TASK 1 : 

> REPLACE BIGQUERY ROLE IN BELOW COMMAND
``` bash
export BIGQUERY_ROLE=BIGQUERY_ROLE
```
> REPLACE STORAGE ROLE IN BELOW COMMAND
``` bash
export STORAGE_ROLE=STORAGE_ROLE
```

``` bash
export SANAME=challenge
gcloud iam service-accounts create $SANAME

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID --member=serviceAccount:$SANAME@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com --role=$BIGQUERY_ROLE

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID --member=serviceAccount:$SANAME@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com --role=$STORAGE_ROLE
gcloud iam service-accounts keys create sa-key.json --iam-account $SANAME@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com
```
<br>

## TASK 2:
``` bash
export GOOGLE_APPLICATION_CREDENTIALS=${PWD}/sa-key.json
gsutil cp gs://$DEVSHELL_PROJECT_ID/analyze-images-v2.py .

```
<br>

- [x] Task 1 and 2 are Completed

<br>

## TASK 3:

  * Now go to **open editor** Button 
  ![Open Editor](https://user-images.githubusercontent.com/56213740/119262467-fca6b780-bbf8-11eb-9715-7d6d260205e5.png)
  ![Open Editor in new Tab](https://user-images.githubusercontent.com/56213740/119262466-fadcf400-bbf8-11eb-8875-95a4d34402e0.png)
  * Open `analyze-image.py` file in Editor
  * Remove whole code and paste below code

> Replace Locale as per your lab instructions at 2 places (line no 94 and 103)

``` python
# Dataset: image_classification_dataset
# Table name: image_text_detail
import os
import sys
# Import Google Cloud Library modules
from google.cloud import storage, bigquery, language, vision, translate_v2

if ('GOOGLE_APPLICATION_CREDENTIALS' in os.environ):
    if (not os.path.exists(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])):
        print ("The GOOGLE_APPLICATION_CREDENTIALS file does not exist.\n")
        exit()
else:
    print ("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not defined.\n")
    exit()

if len(sys.argv)<3:
    print('You must provide parameters for the Google Cloud project ID and Storage bucket')
    print ('python3 '+sys.argv[0]+ '[PROJECT_NAME] [BUCKET_NAME]')
    exit()

project_name = sys.argv[1]
bucket_name = sys.argv[2]

# Set up our GCS, BigQuery, and Natural Language clients

storage_client = storage.Client()
bq_client = bigquery.Client(project=project_name)
nl_client = language.LanguageServiceClient()

# Set up client objects for the vision and translate_v2 API Libraries

vision_client = vision.ImageAnnotatorClient()
translate_client = translate_v2.Client()

# Setup the BigQuery dataset and table objects

dataset_ref = bq_client.dataset('image_classification_dataset')
dataset = bigquery.Dataset(dataset_ref)
table_ref = dataset.table('image_text_detail')
table = bq_client.get_table(table_ref)

# Create an array to store results data to be inserted into the BigQuery table

rows_for_bq = []

# Get a list of the files in the Cloud Storage Bucket

files = storage_client.bucket(bucket_name).list_blobs()
bucket = storage_client.bucket(bucket_name)
print('Processing image files from GCS. This will take a few minutes..')

# Process files from Cloud Storage and save the result to send to BigQuery

for file in files:    
    if file.name.endswith('jpg') or  file.name.endswith('png'):
        file_content = file.download_as_string()

        # TBD: Create a Vision API image object called image_object 
        # Ref: https://googleapis.dev/python/vision/latest/gapic/v1/types.html#google.cloud.vision_v1.types.Image

        from google.cloud import vision_v1
        import io

        client = vision.ImageAnnotatorClient()

        # TBD: Detect text in the image and save the response data into an object called response
        # Ref: https://googleapis.dev/python/vision/latest/gapic/v1/api.html#google.cloud.vision_v1.ImageAnnotatorClient.document_text_detection

        image = vision_v1.types.Image(content=file_content)
        response = client.text_detection(image=image)    

        # Save the text content found by the vision API into a variable called text_data

        text_data = response.text_annotations[0].description

        # Save the text detection response data in <filename>.txt to cloud storage

        file_name = file.name.split('.')[0] + '.txt'
        blob = bucket.blob(file_name)

        # Upload the contents of the text_data string variable to the Cloud Storage file 

        blob.upload_from_string(text_data, content_type='text/plain')

        # Extract the description and locale data from the response file
        # into variables called desc and locale
        # using response object properties e.g. response.text_annotations[0].description

        desc = response.text_annotations[0].description
        locale = response.text_annotations[0].locale

        # if the locale is English (en) save the description as the translated_txt

        if locale == 'LOCALE': # REPLACE LOCALE HERE
            translated_text = desc
        else:
            # TBD: For non EN locales pass the description data to the translation API
            # ref: https://googleapis.dev/python/translation/latest/client.html#google.cloud.translate_v2.client.Client.translate
            # Set the target_language locale to 'en')

            from google.cloud import translate_v2 as translate
            client = translate.Client()
            translation = translate_client.translate(text_data, target_language='LOCALE') # REPLACE LOCALE HERE
            translated_text = translation['translatedText']
        print(translated_text)
        
        # if there is response data save the original text read from the image, 
        # the locale, translated text, and filename

        if len(response.text_annotations) > 0:
            rows_for_bq.append((desc, locale, translated_text, file.name))

print('Writing Vision API image data to BigQuery...')

# Write original text, locale and translated text to BQ
# TBD: When the script is working uncomment the next line to upload results to BigQuery

errors = bq_client.insert_rows(table, rows_for_bq)
assert errors == []
```
 * Save All Files `ctrl + s`
 * Go Back to Terminal
 ![Open Terminal](https://user-images.githubusercontent.com/56213740/119262469-fd3f4e00-bbf8-11eb-8cdd-05d4d1fe7551.png)

<br>

- [x] Task 3 Completed
<br>

>Note:Run Task 4 commands and then Check 

<br>

## TASK 4 :

<br>

``` bash
python3 analyze-images-v2.py $DEVSHELL_PROJECT_ID $DEVSHELL_PROJECT_ID
```

<br>

- [x] Task 4 Completed

<br>

## TASK 5 :

<br>

  * Now go to Big Query
  * Click Compose New Query
  * Paste Below Query
  * Run This Query
  
  <br>

``` sql
SELECT locale,COUNT(locale) as lcount FROM image_classification_dataset.image_text_detail GROUP BY locale ORDER BY lcount DESC
```

<br>

- [x] Task 5 Completed

<br>

![Lab Completed](https://user-images.githubusercontent.com/56213740/119262464-f9133080-bbf8-11eb-9f1d-14286ca48f02.png)

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13
- YouTube Channel: https://youtube.com/channel/UCQUEgfYbcz7pv36NoAv7S-Q/


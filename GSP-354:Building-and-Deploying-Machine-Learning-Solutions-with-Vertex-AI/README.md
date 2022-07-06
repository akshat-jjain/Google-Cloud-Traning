# GSP-354 : Building and Deploying Machine Learning Solutions with Vertex AI
### Overview
- TODO: fill in PROJECT_ID
- TODO: Create a globally unique Google Cloud Storage bucket for artifact storage.

- TODO: Add a hub.KerasLayer for BERT text preprocessing using the hparams dict.
- Name the layer 'preprocessing' and store in the variable preprocessor.
- TODO: Add a trainable hub.KerasLayer for BERT text encoding using the hparams dict.
- Name the layer 'BERT_encoder' and store in the variable encoder.
- TODO: Save your BERT sentiment classifier locally.
- Hint: Save it to './bert-sentiment-classifier-local'. Note the key name in model.save().
- TODO: create a Docker Artifact Registry using the gcloud CLI. Note the required respository-format and location flags.
- Documentation link: https://cloud.google.com/sdk/gcloud/reference/artifacts/repositories/create
- TODO: use Cloud Build to build and submit your custom model container to your Artifact Registry.
> Documentation link: https://cloud.google.com/sdk/gcloud/reference/builds/submit
> Hint: make sure the config flag is pointed at {MODEL_DIR}/cloudbuild.yaml defined above and you include your model directory.
- TODO: change this to your name.
- TODO: fill in the remaining arguments from the pipeline constructor.
- TODO: Generate online predictions using your Vertex Endpoint.
- TODO: write a movie review to test your model e.g. "The Dark Knight is the best Batman movie!"
- TODO: use your Endpoint to return prediction for your test_review.
### Task - 3: Import dataset
- TODO: fill in PROJECT_ID
``` bash
PROJECT_ID = "<PROJECT_ID>"
```
- TODO: Create a globally unique Google Cloud Storage bucket for artifact storage.
``` bash
GCS_BUCKET = f"gs://<PROJECT_ID>-vertex-challenge-lab"
```

### Task - 4: Build and train model
- TODO: Add a hub.KerasLayer for BERT text preprocessing using the hparams dict.
- Name the layer 'preprocessing' and store in the variable preprocessor.
``` bash
preprocessor = hub.KerasLayer(hparams['tfhub-bert-preprocessor'],name='preprocessing')
```

- TODO: Add a trainable hub.KerasLayer for BERT text encoding using the hparams dict.
- Name the layer 'BERT_encoder' and store in the variable encoder.
``` bash
encoder = hub.KerasLayer(hparams['tfhub-bert-encoder'], trainable=True, name='BERT_encoder')
```
- TODO: Save your BERT sentiment classifier locally.
> Hint: Save it to `'./bert-sentiment-classifier-local'`. Note the key name in `model.save()`.
``` bash
"model-dir": "./bert-sentiment-classifier-local"
```
### Task 5: Create artifact registry for custom container images
- TODO: create a Docker Artifact Registry using the gcloud CLI. Note the required respository-format and location flags.
- Documentation link: https://cloud.google.com/sdk/gcloud/reference/artifacts/repositories/create
``` bash
!gcloud artifacts repositories create {ARTIFACT_REGISTRY} \
--repository-format=docker \
--location={REGION} \
--description="Artifact registry for ML custom training images for sentiment classification"
```
- TODO: use Cloud Build to build and submit your custom model container to your Artifact Registry.
- Documentation link: https://cloud.google.com/sdk/gcloud/reference/builds/submit
> Hint: make sure the config flag is pointed at {MODEL_DIR}/cloudbuild.yaml defined above and you include your model directory.
``` bash
!gcloud builds submit {MODEL_DIR} --timeout=20m --config {MODEL_DIR}/cloudbuild.yaml
```
### Task 6: Define a pipeline using the KFP V2 SDK
- TODO: change this to your name.
``` bash
USER = "qwiklabsdemo"
```
- TODO: fill in the remaining arguments from the pipeline constructor.
``` bash
display_name=display_name,
    container_uri=container_uri,
    model_serving_container_image_uri=model_serving_container_image_uri,
    base_output_dir=GCS_BASE_OUTPUT_DIR,
```
- TODO: Generate online predictions using your Vertex Endpoint.
``` bash
endpoint = vertexai.Endpoint(
endpoint_name=ENDPOINT_NAME,
project=PROJECT_ID,
location=REGION
)
```
- TODO: write a movie review to test your model e.g. "The Dark Knight is the best Batman movie!"
``` bash
test_review = "The Dark Knight is the best Batman movie!"
```
- TODO: use your Endpoint to return prediction for your test_review.
``` bash
prediction = endpoint.predict([test_review])
```
# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13

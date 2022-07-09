# Explore Machine Learning Models with Explainable AI: Challenge Lab

In this article, we will go through the lab to Explore Machine Learning Models with Explainable AI: Challenge Lab. In the previous, lab you will get familiar with AI Platform: Qwik Start, Using the What-If Tool with Image Recognition Models, Identifying Bias in Mortgage Data using Cloud AI Platform and the What-if Tool, and Compare Cloud AI Platform Models using the What-If Tool to Identify Potential Bias.
#### The challenge contains 4 required tasks
- Start a JupyterLab Notebook Instance.
- Download the Challenge Notebook.
- Build and Train your Models.
- Deploy Model to AI Platform.

### Challenge scenario
You are a curious coder who wants to explore biases in public datasets using the What-If Tool. You decide to pull some mortgage data to train a couple of machine learning models to predict whether an applicant will be granted a loan. You specifically want to investigate how the two models perform when they are trained on different proportions of males and females in the datasets and visualize their differences in the What-If Tool.
#### What-If Tool
The What-If Tool is a visual interface designed to help you understand your data sets and the output of your machine learning models. You can run with minimal code from many different platforms, including Jupyter Notebooks, Kollab, TensorBoard, and Cloud AI Platform Notebooks.
## 1.Start a JupyterLab Notebook instance
- In the GCP Console go to Navigation Menu >AI Platform, then to Notebooks.
- On the Notebook instances page, click New Instance.
- In the Customize instance menu, select the latest version of TensorFlow without GPUs.
- In the New notebook instance dialog, accept the default options and click Create.
- In the AI Platform console will display your instance name, followed by Open Jupyterlab.
- Click Open JupyterLab. Your notebook is now set up.

## 2.Download the Challenge Notebook

- In your notebook, click the terminal.
- Clone the repository.
``` bash
git clone https://github.com/GoogleCloudPlatform/training-data-analyst
```

- Go to the enclosing folder: `training-data-analyst/quests/dei`.
- Open the notebook file `what-if-tool-challenge.ipynb`.
- Download and import the dataset `hmda_2017_ny_all-records_labels` by running the first to the eighth cells.


## 3.Build and train your models

- In the second cell of the Train your 1st model on the whole dataset section, add the following lines to create the model.
``` IPython Notebook
model = Sequential()
model.add(layers.Dense(8, input_dim=input_size))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='sgd', loss='mse')
model.fit(train_data, train_labels, batch_size=32, epochs=10)
```

- Copy the code for training the second model.
- Modify model to `limited_model` as well as `train_data`, `train_labels` to `limited_train_data`, `limited_train_labels`

``` IPython Notebook
limited_model = Sequential()
limited_model.add(layers.Dense(8, input_dim=input_size))
limited_model.add(layers.Dense(1, activation='sigmoid'))
limited_model.compile(optimizer='sgd', loss='mse')
limited_model.fit(limited_train_data, limited_train_labels, batch_size=32, epochs=10)
```
- Run the cells.


## 4.Deploy the models to AI Platform

- First, create a storage bucket to store your Models in. (Unique Bucket Name)
- Replace the values of GCP_PROJECT and MODEL_BUCKET with your project ID and a unique bucket name.
- Change the Model Name and replace it with `complete_model` and `limited_model`.
- Run all three cells.
- Confirm the created Bucket and the Upload model files in the Cloud Storage.
``` bash
# 1. Create an AI Platform model resource for your COMPLETE model.

!gcloud ai-platform models create $MODEL_NAME --regions $REGION
# Now create a version.
!gcloud ai-platform versions create $VERSION_NAME \
--model=$MODEL_NAME \
--framework='TENSORFLOW' \
--runtime-version=1.14 \
--origin=$MODEL_BUCKET/saved_complete_model/ \
--staging-bucket=$MODEL_BUCKET \
--python-version=3.5

# 2. Create your second AI Platform model: limited_model

!gcloud ai-platform models create $LIM_MODEL_NAME --regions $REGION
# Now create a version. 
!gcloud ai-platform versions create $VERSION_NAME \
--model=$LIM_MODEL_NAME \
--framework='TENSORFLOW' \
--runtime-version=1.14 \
--origin=$MODEL_BUCKET/saved_limited_model/ \
--staging-bucket=$MODEL_BUCKET \
--python-version=3.5
```

## (OPTIONAL) 5.Use the What-If Tool to explore biases

- After your models are deployed to the AI Platform, you can use the following code to explore them in the What-If Tool in the notebook. We’ve created custom prediction functions `custom_predict` and `bad_custom_predict` that get the class predictions from the models.
```
config_builder = (WitConfigBuilder(     examples_for_wit[:num_datapoints],feature_names=column_names)     .set_custom_predict_fn(bad_custom_predict)     .set_target_feature('loan_granted')     
.set_label_vocab(['denied', 'accepted'])     
.set_compare_custom_predict_fn(custom_predict)     .set_model_name('limited')   
.set_compare_model_name('complete'))
```

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13
- YouTube Channel: https://youtube.com/channel/UCQUEgfYbcz7pv36NoAv7S-Q/

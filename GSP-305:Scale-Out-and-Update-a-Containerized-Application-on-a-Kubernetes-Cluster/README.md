# Scale Out and Update a Containerized Application on a Kubernetes Cluster

This article will go through the lab to Scale-Out and Update a Containerized Application on a Kubernetes Cluster. This lab is similar to Build and Deploy a Docker Image to a Kubernetes Cluster.
## The challenge contains 4 required tasks.
1. Check that there is a tagged image in gcr.io for echo-app:v2.
2. Echo-app:v2 is running on the Kubernetes cluster.
3. The Kubernetes cluster deployment reports 2 replicas.
4. The application must respond to web requests with V2.0.0.
# Challenge Scenario
You are taking over ownership of a test environment and have been given an updated version of a containerized test application to deploy. Your systems’ architecture team has started adopting a containerized microservice architecture. You are responsible for managing the containerized test web applications. You will first deploy the initial version of a test application, called echo-app to a Kubernetes cluster called echo-cluster in a deployment called echo-web.
Before you get started, open the navigation menu and select Cloud Storage. The last steps in the Deployment Manager script used to set up your environment create a bucket.
Refresh the Storage browser until you see your bucket. You can move on once your Console resembles the following:

Check to make sure your GKE cluster has been created before continuing. Open the navigation menu and select Kubernetes Engine > Clusters.
Continue when you see a green checkmark next to echo-cluster:

To deploy your first version of the application, run the following commands in Cloud Shell to get up and running:
``` bash
gcloud container clusters get-credentials echo-cluster --zone=us-central1-a
kubectl create deployment echo-web --image=gcr.io/qwiklabs-resources/echo-app:v1
kubectl expose deployment echo-web --type=LoadBalancer --port 80 --target-port 8000
```

1. Check that there is a tagged image in gcr.io for echo-app:v2
   - The echo-web.tar.gz file has already been copied to a Google Cloud Storage bucket called gs://[PROJECT_ID] during the lab provision. Navigate to Storage, confirm the file exists in the bucket. Then, click the file name and copy the URL of the file from its detail page.
   - Go to Cloud shell and write commands.
   ``` bash
    gsutil cp gs://sureskills-ql/challenge-labs/ch04-kubernetes-app-deployment/echo-web.tar.gz . 
    tar -xvf echo-web.tar.gz
   ```
   - In the GCP Console go to Cloud Shell copy and paste the command.
   - It will tag image in gcr.io for echo-app:v2
   ``` bash
    gcloud builds submit --tag gcr.io/$DEVSHELL_PROJECT_ID/echo-app:v2 .
   ```
   - In the GCP Console go to Cloud Shell copy and paste the command.
   - Configuration as follow:
     - Cluster Name: echo-cluster
     - Zone: us-central1-a
   ``` bash
    gcloud container clusters get-credentials echo-cluster --zone us-central1-a 
   ```
2. Echo-app:v2 is running on the Kubernetes cluster
   - In the GCP Console go to Cloud Shell copy and paste the command.
   - It will create an application image with a v1 tag that has been pushed to the gcr.io repository
   ``` bash
    kubectl create deployment echo-web --image=gcr.io/qwiklabs-resources/echo-app:v1 
    kubectl expose deployment echo-web --type=LoadBalancer --port 80 --target-port 8000
   ```
3. The Kubernetes cluster deployment reports 2 replicas.
   - In the GCP Console go to Cloud Shell copy and paste the command.
    ``` bash
    kubectl scale deploy echo-web --replicas=2
    ```
4. The application must respond to web requests with V2.0.0
   - In the GCP Console go to Cloud Shell copy and paste the command.
    ``` bash
    kubectl edit deploy echo-web
    ```
Change the image version ‘v1’ to ‘v2’ by pressing “i”.
Save by esc -> Esc → “:wq”.



# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13
- YouTube Channel: https://youtube.com/channel/UCQUEgfYbcz7pv36NoAv7S-Q/

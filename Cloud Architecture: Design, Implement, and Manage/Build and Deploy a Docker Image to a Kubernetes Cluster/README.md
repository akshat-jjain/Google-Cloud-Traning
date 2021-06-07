# ☁ Build and Deploy a Docker Image to a Kubernetes Cluster | logbook
 
Containerization with Docker and Kubernetes (K8s) is an emerging application architecture for deploying, scaling and managing distributed applications. The challenge lab GSP304 “Build and Deploy a Docker Image to a Kubernetes Cluster“ is a test to assess the essential professional skills in deploying your application on GKE.

## Brief Introduction of Challenge Scenario

1. Use the sample application and Docker configuration to build a Docker image, and push the image to the gcr.io repository with a `v1` tag.
2. A new Kubernetes cluster called `echo-cluster` exists.
3. The application called `echo-app` has been deployed to the cluster. 
4. The service called `echo-web` exists that responds to requests like Echo-app.

# Create a Kubernetes Cluster
In the web console, navigate to **Kubernetes Engine > Clusters**. Click **Create a cluster** with:

- Cluster name: echo-cluster
- Num of Nodes: 2
- Machine type: N1-standard-2
- Zone: us-central1-a


I recommend starting from preparing the hardware because the process takes time. You can continue doing the steps in the next section. The cluster should be ready, when you finish building and pushing the docker image to Container Registry.

# Build a Docker Image of Sample Application
If you do not remember how to build a docker image on GCP, I recommend you revise the lab “Introduction to Docker“ before you start.

1. (Optional) While the provisioning of lab resources, you may click the link below the timer to download the given archive called `echo-web.tar.gz`. You may spend some time to study the contained files in your local storage.
2. The `echo-web.tar.gz` file has already been copied to a Google Cloud Storage bucket called `gs://[PROJECT_ID]` during the lab provision. Navigate to **Storage**, confirm the file exists in the bucket. Then, click the file name and copy the URL of the file from its detail page.
3. Open a Cloud Shell, use the following commands to copy and unzip `echo-web.tar.gz` to the shell environment:
```
export PROJECT_ID=$(gcloud info --format='value(config.project)')
gsutil cp gs://${PROJECT_ID}/echo-web.tar.gz .
tar -xvzf echo-web.tar.gz
gcloud builds submit --tag gcr.io/$DEVSHELL_PROJECT_ID/echo-app:v1 .
```
4. Build a docker image of the sample application with a tag called `v1`, and push the image to Google Container Registry,
```
docker build -t echo-app:v1 .
docker tag echo-app:v1 gcr.io/${PROJECT_ID}/echo-app:v1
docker push gcr.io/${PROJECT_ID}/echo-app:v1
```
5. In the web console, navigate to **Container Registry > Images** to confirm the docker image has been pushed to the cloud repositories.

Next, you need to deploy the application to the Kubernetes Cluster. There are two ways to do this: (1) deploy using web console, and (2) deploy using Cloud Shell. You can choose either way to finish the lab.

# Deploy the Application to the Kubernetes Cluster Using Cloud Shell
You can deploy the application using cloud shell instead. After creating your cluster, you need to get authentication credentials to interact with the cluster.

To authenticate the cluster run the following command,
```
gcloud container clusters get-credentials echo-cluster
```
Run the following `kubectl run` command in Cloud Shell to create a new Deployment `echo-app` from the echo-app container image with opening TCP port 8000:
```
kubectl run echo-app --image=gcr.io/${PROJECT_ID}/echo-app:v1 --port 8000
```
Now create a Kubernetes Service, which is a Kubernetes resource that lets you expose your application (that responds on **port 8000**) to external traffic that responds to normal web requests on **port 80**, by running the following `kubectl expose` command:
```
kubectl expose deployment echo-app --name echo-web \
   --type LoadBalancer --port 80 --target-port 8000
```
Inspect the `echo-web` Service by running kubectl get:
```
kubectl get service echo-web
```
Copy and open the IP address of the external endpoints in a new tab of your browser, the sample application should look like:

# Congratulations! You should accomplish the lab

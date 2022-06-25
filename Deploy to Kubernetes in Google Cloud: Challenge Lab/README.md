# ☁ Deploy to Kubernetes in Google Cloud: Challenge Lab | logbook

In this article, we will go through the lab GSP318 Deploy to Kubernetes in Google Cloud: Challenge Lab, which is an expert-level exercise (formerly known as Kubernetes in Google Cloud: Challenge Lab) on Qwiklabs. You will practice the skills and knowledge for configuring Docker images and containers and deploying fully-fledged Kubernetes Engine applications.

#### The challenge contains 4 required tasks:

- Create a Docker image and store the Dockerfile
- Test the created Docker image
- Push the Docker image in the Google Container Repository
- Create and expose a deployment in Kubernetes
- Increase the replicas from 1 to [Replica Count]
- Update the deployment with a new version of valkyrie-app
- Create a pipeline in Jenkins to deploy your app
## Task 1: Create a Docker image and store the Dockerfile
> Hint: Refer procedures and modify the codes in the lab GSP055 Introduction to Docker

- First of all, you have to run the following command in Cloud Shell.
```
source <(gsutil cat gs://cloud-training/gsp318/marking/setup_marking_v2.sh)
```
It installs the marking scripts, which use to check your progress.
- Then, run the commands below to clone the valkyrie-app source code repository to the Cloud Shell. (Remember to replace YOUR_PROJECT_ID with your Project ID)
```
export PROJECT=$YOUR_PROJECT_ID
gcloud source repos clone valkyrie-app --project=$PROJECT
```
- Create a Dockerfile under the valkyrie-app directory and add the configuration to the file. Copy the given codes from the lab page to the following snippet, and then run the commands in the Cloud Shell.
```
cd valkyrie-app
cat > Dockerfile <<EOF  
FROM golang:1.10
WORKDIR /go/src/app
COPY source .
RUN go install -v
ENTRYPOINT ["app","-single=true","-port=8080"]
EOF
```
- Build the image with the following command:
- Replace `[Image Name]` with `Image Name` And `[Tag name]` with `Tag name`
```
docker build -t [Image Name]:[Tag name] .
```
- Run `docker images` to look at the images you built.

Before clicking Check my progress on the lab page, don’t forget to run the following commands to execute the marking script:
```
cd ~/marking
./step1_v2.sh
```
## Task 2: Test the created Docker image
> Hint: Refer procedures and modify the codes in the lab GSP055 Introduction to Docker

The lab instruction requires you to run the docker image built in Task 1 and show the running application by Web Preview on port 8080. Based on the requirements, the docker command will be:

- In the Cloud Shell, go back to the valkyrie-app directory, and run the below command.
- Replace `[Image Name]` with `Image Name` and `[Image with tag]` with `Image with tag`
```
docker run -p 8080:8080 --name [Image name] [Image with tag] &
```
- Click Web Preview to see the running app.
- After that, open a new Cloud Shell to run the step2_v2.sh marking script.
```
cd ~/marking
./step2_v2.sh
```

## Task 3: Push the Docker image in the Container Repository
> Hint: Refer procedures and modify the codes in the lab GSP055 Introduction to Docker

In this task, you will push the Docker image valkyrie-app:v0.0.1 into the Container Registry with a tag `gcr.io/YOUR_PROJECT_ID/valkyrie-app:v0.0.1.`


Thus, you should format the docker commands as below.
> Replace `[Image with tag]` with `Image with tag`
```
docker tag [Image with tag] gcr.io/$PROJECT/[Image with tag]
docker images
docker push gcr.io/$PROJECT/[Image with Tag]
```
After pushing the container, the [Image name] repository will appear in the Cloud Console as shown in the image below.


Push the Docker image of valkyrie-app in the Google Container Repository
## Task 4: Create and expose a deployment in Kubernetes
> Hint: Refer procedures in the labs GSP100 Kubernetes Engine: Qwik Start and GSP021 Orchestrating the Cloud with Kubernetes for steps 1-2 and steps 3-4, respectively.

- In the Cloud Shell, go to the `valkyrie-app` subdirectory.
- Get authentication credentials for the cluster

```
gcloud container clusters get-credentials valkyrie-dev --region us-east1-d
```

- Use a text editor to modify `deployment.yaml` and replace `IMAGE_HERE` with `gcr.io/YOUR_PROJECT_ID/valkyrie-dev:[Tag name] `
```
cd valkyrie-app
gcloud container clusters get-credentials valkyrie-dev --zone us-east1-d
kubectl create -f k8s/deployment.yaml
kubectl create -f k8s/service.yaml
```
## Task 5: Update the deployment with a new version of valkyrie-app
   
> Hint: Refer the skills in lab GSP053 Managing Deployments Using Kubernetes Engine or my previous article Qwiklabs/Logbook: Scale Out and Update a Containerized Application on a Kubernetes Cluster

- Replace `[Replicas count]` with `Replicas count`
```
kubectl scale deployment valkyrie-dev --replicas [Replicas count]
```

- Go back to the `valkyrie-app` directory in the Cloud Shell.
- Merge the branch called kurt-dev into master using the following git command:
```
git merge origin/kurt-dev
```
- Build and push the new version with tagged `[Updated Version]`:
```
docker build -t valkyrie-dev:[Updated Version] .
docker tag valkyrie-dev:[Updated Version] gcr.io/$PROJECT/valkyrie-dev:[Updated Version]
docker images
docker push gcr.io/$PROJECT/valkyrie-dev:[Updated Version]
```
- Trigger a rolling update by running the following command:
> Replace `[Updated Version]` with `Updated Version` and `[PROJECT_ID]` with `PROJECT_ID`
```
kubectl set image deployment valkyrie-dev backend=gcr.io/$PROJECT_ID/valkyrie-dev:[Updated Version] frontend=gcr.io/$PROJECT_ID/valkyrie-dev:[Updated Version]
```

## Task 6: Create a pipeline in Jenkins to deploy your app
> Hint: Refer procedures in the labs GSP051 Continuous Delivery with Jenkins in Kubernetes Engine

In this task, you will need to:

- Connect to Jenkins
- Adding your service account credentials
- Creating a Jenkins job
- Modifying the pipeline definition
- Modify the site
- Kick off Deployment
- Get the password with the following command:
```
printf $(kubectl get secret cd-jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo
```

- If there is another running container, use the docker commands below to kill it:
```
docker ps
docker container kill $(docker ps -aq)
```
- Connect to the Jenkins console using the commands below:
```
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/component=jenkins-master" -l "app.kubernetes.io/instance=cd" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward $POD_NAME 8080:8080 >> /dev/null &
```
- Click on the Web Preview button in cloud shell, then click “Preview on port 8080” to connect to the Jenkins console.
- Username: `admin`
- In the Jenkins user interface, click `Credentials` in the left navigation.
- Click `Jenkins`
- Click `Global credentials (unrestricted)`.
- Click `Add Credentials` in the left navigation.
- Select `Google Service Account from metadata` from the Kind drop-down and click OK.
- Create a pipeline job that points to your */master branch on your source code.
- Click `Jenkins > New Item` in the left navigation:
- Name the project `valkyrie-app`, then choose the `Pipeline` option and click OK.
- On the next page, in the `Pipeline` section, click `Pipeline script from SCM` and select `git` in SCM  .
- Paste the HTTPS clone URL of your `sample-app` repo in Cloud Source Repositories 
```
https://source.developers.google.com/p/YOUR_PROJECT_ID/r/valkyrie-app 
```
into the Project Repository field. 
- Remember to replace YOUR_PROJECT_ID with your GCP Project ID.
- From the  `Credentials` drop-down, select the name of the credentials you created when adding your service account in the previous steps.
- Open `Jenkinsfile` file in a text editor, and replace `YOUR_PROJECT` with your `GCP project ID`.
- Open `source/html.go` file in a text editor, and change the color of headings from `green` to `orange`.
- Commit and push the changes:
```
git config --global user.email "you@example.com"
git config --global user.name "student"
git add *
git commit -m 'green to orange'
git push origin master
```
Finally, manually trigger the build in the Jenkins console

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13

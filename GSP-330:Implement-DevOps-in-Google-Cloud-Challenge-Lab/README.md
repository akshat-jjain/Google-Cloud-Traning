# Implement DevOps in Google Cloud: Challenge Lab
In this article, we will go through the lab to Implement DevOps in Google Cloud. You will practice the skills in implementing a continuous deployment pipeline using the Jenkins build and deployment automation tool.

The challenge contains 4 required tasks

- Check Jenkins pipeline has been configured.
- Check that Jenkins has deployed a development pipeline.
- Check that Jenkins has deployed a canary pipeline.
- Check that Jenkins has merged a canary pipeline with production.
Some Jooli Inc. standards you should follow:

- Create all resources in the us-east1 region and us-east1-b zone, unless otherwise directed.
- Use the project VPCs.
- Naming is normally team-resource, e.g. an instance could be named kraken-webserver1.
- Allocate cost effective resource sizes. Projects are monitored and excessive resource use will result in the containing project’s termination (and possibly yours), so beware. This is the guidance the monitoring team is willing to share; unless directed, use n1-standard-1.

### 1.Configure a Jenkins pipeline for continuous deployment to Kubernetes Engine.
In this step you have to Clone the repository, Checking a Kubernetes cluster, Install and Setup Helm, Configure and Install Jenkins, Connect to Jenkins, Deploying the Application, Creating the Jenkins Pipeline, Adding your service account credentials, and Creating the Jenkins job.

#### Clone the repository
- To get set up, open a new session in Cloud Shell and run the following command to set your zone `us-east1-d`.
```
gcloud config set compute/zone us-east1-d
```
- Then clone the lab’s sample code.
```
git clone https://source.developers.google.com/p/$DEVSHELL_PROJECT_ID/r/sample-app
```
#### Checking a Kubernetes cluster.
- In the GCP Console go to `Navigation Menu >Kubernetes Engine > Clusters`
- Then Check cluster named `jenkins-cd`.

Now, get the credentials for your cluster.
```
gcloud container clusters get-credentials jenkins-cd --zone us-east1-b --project $DEVSHELL_PROJECT_ID
```
Kubernetes Engine uses these credentials to access your newly provisioned cluster confirm that you can connect to it by running the following command.
```
kubectl cluster-info
```
- Navigate to Source Repositories, click on `sample-app` and review the Jenkins file in the root of that repository.
#### Install and Setup Helm.
You will use Helm to install Jenkins from the Charts repository. Helm is a package manager that makes it easy to configure and deploy Kubernetes applications. Once you have Jenkins installed, you’ll be able to set up your CI/CD pipeline.
```
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo add stable https://charts.helm.sh/stable
```
- Ensure the repo is up to date.
```
helm repo update
```
#### Configure and Install Jenkins.
- Use git to clone the lab’s sample code.
```
git clone https://github.com/GoogleCloudPlatform/continuous-deployment-on-kubernetes.git
```
- Change to the following directory.
```
cd continuous-deployment-on-kubernetes
```
-  To configure and install Jenkins, run the following command to deploy with the Helm CLI.
```
helm install cd stable/jenkins -f jenkins/values.yaml --version 1.2.2 --wait
```
- Once that command completes ensure the Jenkins pod goes to the Running state and the container is in the READY state.
```
kubectl get pods
```

- Run the following command to setup port forwarding to the Jenkins UI from the Cloud Shell.
```
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/component=jenkins-master" -l "app.kubernetes.io/instance=cd" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward $POD_NAME 8080:8080 >> /dev/null &
```
- Now, check that the Jenkins Service was created properly.
```
kubectl get svc
```
#### Connect to Jenkins
- The Jenkins chart will automatically create an `admin password` for you. To retrieve it, run.
```
printf $(kubectl get secret cd-jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo
```
- To get to the Jenkins user interface, click on the `Web Preview` button in cloud shell, then click `Preview on port 8080`
- You should now be able to log in with username `admin` and your auto-generated password.

#### Deploying the Application.
- In Google Cloud Shell, navigate to the sample application directory.

```
cd ~/sample-app
```
- Create the Kubernetes namespace to logically isolate the deployment.
```
kubectl create ns production 
```
Create the production and canary deployments, and the services using the kubectl apply commands.
```
kubectl apply -f k8s/production -n production
kubectl apply -f k8s/canary -n production
kubectl apply -f k8s/services -n production
```
- Retrieve the external IP for the production services.
```
kubectl get service gceme-frontend -n production
```
#### Creating the Jenkins Pipeline
Initialize the sample-app directory as its own Git repository.
```
git init
git config credential.helper gcloud.sh
```
- Run the following command.
```
git remote add origin https://source.developers.google.com/p/$DEVSHELL_PROJECT_ID/r/default
```
Set the username and email address for your Git commits. Replace `[EMAIL_ADDRESS]` with your Git email address and `[USERNAME]` with your Git username.
```
git config --global user.email "student-03-932c4d0605b8@qwiklabs.net"
git config --global user.name "[YOUR_USERNAME]"
```
-  Add, commit, and push the files.
```
git add .
git commit -m "Initial commit"
git push origin master
```
#### Adding your service account credentials
Configure your credentials to allow Jenkins to access the code repository. Jenkins will use your cluster’s service account credentials in order to download code from the Cloud Source Repositories.

-  In the Jenkins user interface, click `Manage Jenkins` in the left navigation then click `Manage Credentials`.
-  Click `Jenkins`.
-  Click `Global credentials (unrestricted)`.
-  Click `Add Credentials` in the left navigation.
-  Select `Google Service Account from metadata` from the Kind drop-down and click OK.


The global credentials has been added. The name of the credential is the Project ID found in the CONNECTION DETAILS section of the lab.

####  Creating the Jenkins job.

Navigate to your Jenkins user interface and follow these steps to configure a Pipeline job.

- Click `New Item` in the left navigation.
- Name the project `sample-app`, then choose the `Multibranch Pipeline` option and click OK.
- On the next page, in the Branch Sources section, click `Add Source` and select `git`.
- Paste the HTTPS clone URL of your `sample-app` repo in Cloud Source Repositories into the Project Repository field. 
> Replace `[PROJECT_ID]` with your Project ID.
```
https://source.developers.google.com/p/[PROJECT_ID]/r/sample-app
```

- Select the service account for your `GCP project` from the Credentials dropdown list.
- Under `Scan Multibranch Pipeline Triggers` section, check the `Periodically if not otherwise` run box and set the Interval value to `1 minute`.
- Click `Save` leaving all other options with their defaults.

### 2.Push an update to the application to a development branch.
In this task, you need to Modify the site.

- Create a development branch and push it to the Git server.
```
git checkout -b new-feature
```
- Now Open `html.go`
```
vi html.go
```
- Then Start the editor. `i`
- Change the two instances of `<div class="card blue">` with `Your Colour`
```
<div class="card Colour">
```
- Save the `html.go` file: press `Esc` then. `:wq`
- Now Open `main.go`
```
vi main.go
```
- Then Start the editor. `i`
- The version is defined in this line.
```
const version string = "1.0.0"
```
- Update it to the `Your Version`
```
const version string = "Version"
```
- Save the main.go file one more time: Esc then. `:wq`
- Commit and push your changes.
```
git config --global user.email "[EMAIL_ADDRESS]"
git config --global user.name "[USERNAME]"
git add Jenkinsfile html.go main.go
git commit -m "Version 2.0.0"
git push origin new-feature
```
### 3.Push a Canary deployment to the production namespace.
In this task, you need to create a new branch called canary, merge the development branch with it, and push that to the repository.

- Now Go to the SSH window, run the following command to create a canary branch in the sample-app directory.
```
git checkout -b canary
```
- Merge the change from the development branch.
```
git merge new-feature
```
- Now Push the canary to the Git server.
```
git push origin canary
```
### 4.Promote the Canary Deployment to production.
In this task, you need to MERGE and PUSH it to the Git Server.

- Now Go to the SSH window, run the following commands to merge the canary branch and push it to the Git server.
```
git checkout master
git merge canary
git push origin master
```
- In Jenkins, you should see the master pipeline has kicked off.
-  You can check the service URL to ensure that all of the traffic is being served by your new version, 2.0.0.
```
export FRONTEND_SERVICE_IP=$(kubectl get -o \ jsonpath="{.status.loadBalancer.ingress[0].ip}" --namespace=production services gceme-frontend)
```

# Demonstration Video

[![Watch the video](https://img.youtube.com/vi/lLDrmbOMtto/maxresdefault.jpg)](https://youtu.be/lLDrmbOMtto)

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13
- YouTube Channel: https://youtube.com/channel/UCQUEgfYbcz7pv36NoAv7S-Q/


Thank you stay safe, stay healthy.

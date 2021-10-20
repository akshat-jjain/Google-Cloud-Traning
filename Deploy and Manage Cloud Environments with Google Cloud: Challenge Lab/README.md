# Deploy and Manage Cloud Environments with Google Cloud: Challenge Lab

In this article, we will go through the lab to Deploy and Manage Cloud Environments with Google Cloud. In the previous, lab you will get familiar with Deploy and Manage Docker containers using kubectl, Deployment Manager, Continuous Delivery Pipelines with Spinnaker, and Kubernetes Engine, Multiple VPC Networks, and Site Reliability Troubleshooting with Cloud Monitoring APM.
#### The challenge contains 3 required tasks
- Create the Production Environment
- Setup the Admin instance
- Verify the Spinnaker deployment
#### Some Jooli Inc. standards you should follow:
- Create all resources in the us-east1 region and us-east1-b zone, unless otherwise directed.
- Use the project VPCs.
- Naming is normally a team-resource, e.g. an instance could be named kraken-webserver1.
- Allocate cost-effective resource sizes. Projects are monitored and excessive resource use will result in the containing project’s termination (and possibly yours), so beware. This is the guidance the monitoring team is willing to share; unless directed, use n1-standard-1.

## 1. Create the production environment
The first step is to create a production environment.
   - In the GCP Console go to Navigation Menu >Compute Engine > VM Instance.
   - Click the SSH button to access the jumphost instance.
   - In the SSH window, go to the cd /work/dm directory.
   - Use an editor to open the configuration file prod-network.yaml, and replace `SET_REGION` to `us-east1`
   - Copy and Paste the following command.  
   ```
   sed -i s/SET_REGION/us-east1/g prod-network.yaml
   gcloud deployment-manager deployments create prod-network --config=prod-network.yaml
   ```
   - Now create a Kubernetes cluster in the new network
   ```
   gcloud config set compute/zone us-east1-b
   gcloud container clusters create kraken-prod \
   --num-nodes 2 \
   --network kraken-prod-vpc \
   --subnetwork kraken-prod-subnet
   ```
   - Checking Credentials of kraken-pod
   ```
   gcloud container clusters get-credentials kraken-prod
   ```
   
   - Go to Directory
   ```
   cd /work/k8s
   for F in $(ls *.yaml); do kubectl create -f $F; done
   ```
   > Note: All commands written in SSH

## 2.Setup the Admin instance
In this step Create kraken-admin and Monitoring workspace.
Create kraken-admin through this command :
```
gcloud config set compute/zone us-east1-b
gcloud compute instances create kraken-admin --network-interface="subnet=kraken-mgmt-subnet" --network-interface="subnet=kraken-prod-subnet"
```
Create a Monitoring workspace

- In the GCP Console go to Navigation Menu > Monitoring> Alerting.
- Click Create Policy.
- Click Add Condition, and then set up the Metrics with the following parameters:

| Fields        	| Options                                                         	|
|---------------	|-----------------------------------------------------------------	|
| Resource Type 	| GCE VM Instance                                                 	|
| Metric        	| CPU Utilization compute.googleapis.com/instance/cpu/utilization 	|
| Filter        	| Choose instance id and paste the value copied from kraken-admin 	|
| Threshold     	| 50 for 1 minute                                                	  |

- Click ADD
- Then add an email in the Notification setting.
- Click Save

# 3.Verify the Spinnaker deployment
In this step the lab manual suggests you use Cloud Shell and kubectl to port forward the spin-deck pod from port 9000 to 8080.
- In the GCP Console go to Navigation Menu >Kubernetes Engine > Services & Ingress
- Go to spin-deck.
- Click Port Forward.
- Cloud Shell will open with the port forwarding command.
- Click on the web preview icon on cloud shell open port 8080.
- Clone your source code repository and commit it by following the command.
> Note: Commands written in cloud Shell.
```
gcloud config set compute/zone us-east1-b
gcloud source repos clone sample-app
cd sample-app
touch a
git config --global user.email "$(gcloud config get-value account)"
git config --global user.name "Student"
git commit -a -m "change"
git tag v1.0.1
git push --tags
```
# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshat_jjain

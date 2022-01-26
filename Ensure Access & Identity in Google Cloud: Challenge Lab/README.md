# Ensure Access & Identity in Google Cloud: Challenge Lab

# Prerequisite

- Create file `role-definition.yaml`
```
nano role-definition.yaml
```
- Replace `[Custom Security Role]` with your `Role`
- Paste below code in the editor
```
title: "[Custom Security Role]"
description: "Add and update objects in Google Cloud Storage buckets"
includedPermissions:
- storage.buckets.get
- storage.objects.get
- storage.objects.list
- storage.objects.update
- storage.objects.create
```
- Press `CTRL-O` ENTER `CTRL-X` 
# Task 1: Create a custom security role

> Note: Replace `[Custom Security Role]` with your `Role`
```
gcloud iam roles create [Custom Security Role] \
   --project $DEVSHELL_PROJECT_ID \
   --file role-definition.yaml
```
# Task 2: Create a service account

> Note: Replace `[Service Account]` with your `Service Account`
```
gcloud iam service-accounts create [Security Account] \
   --display-name "Orca Private Cluster Service Account"
```
# Task 3: Bind a custom security role to a service account

> Note: Replace `[Service Account]` with your `Service Account` And Replace `[Custom Security Role]` with your `Role`
```
gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
   --member serviceAccount:[Service Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com \
   --role roles/monitoring.viewer

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
   --member serviceAccount:[Service Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com \
   --role roles/monitoring.metricWriter

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
   --member serviceAccount:[Service Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com \
   --role roles/logging.logWriter
  
gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
   --member serviceAccount:[Service Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com \
   --role projects/$DEVSHELL_PROJECT_ID/roles/[Custom Security Role]
```

# Task 4: Create and configure a new Kubernetes Engine private cluster

```
JUMPHOST_IP=$(gcloud compute instances describe orca-jumphost \
  --format='get(networkInterfaces[0].networkIP)')
```
```
SUBNET_IP_RANGE="10.142.0.0/28"
```
> Note: Replace `[Cluster Name]` with your `Cluster Name` and `[Service Account]` with your `Service Account`

```
gcloud beta container clusters create [Cluster Name] \
   --network orca-build-vpc \
   --subnetwork orca-build-subnet \
   --service-account [Security Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com \
   --enable-master-authorized-networks \
   --master-authorized-networks $JUMPHOST_IP/32 \
   --enable-private-nodes \
   --master-ipv4-cidr $SUBNET_IP_RANGE \
   --enable-ip-alias \
   --enable-private-endpoint
```
# Task 5: Deploy an application to a private Kubernetes Engine cluster

> Note: Run Commands in SSH window of `orca-jumphost`
> And Replace `[Cluster Name]` with your `Cluster Name`
```
gcloud container clusters get-credentials [Cluster Name] --internal-ip --zone=us-east1-b
kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0
```

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshat_jjain

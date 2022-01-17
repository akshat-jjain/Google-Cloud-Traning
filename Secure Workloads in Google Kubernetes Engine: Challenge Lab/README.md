# Secure Workloads in Google Kubernetes Engine: Challenge Lab

# Task 0: Download the necessary files
Run the following to download all the files for this lab:
```
gsutil -m cp gs://cloud-training/gsp335/* .
```

# Task 1: Setup Cluster

You need to create a Kubernetes cluster with the following values:

- name: [Cluster Name]
- zone: Us-central1-c
- machine-type: n1-standard-4
- number of nodes: 2
- enable network policy

Run the following gcloud command will create a cluster called kraken-cluster with the required specifications:
```
gcloud container clusters create [Cluster Name] \
   --zone us-central1-c \
   --machine-type n1-standard-4 \
   --num-nodes 2 \
   --enable-network-policy
```

# Task 2: Setup WordPress
This task involves the following three subtasks:

- Setup the Cloud SQL database and database username and password
- Create a service account for access to your WordPress database from your WordPress instances
- Create the WordPress deployment and service

You can perform the first two subtasks simultaneously, while you are creating the cluster in Task 1. It usually takes more time on GCP to create a Cloud SQL instance, compared to a Kubernetes cluster. Both the Cloud SQL and the cluster will be ready when you are going to conduct the rest of the tasks.
### Setup the Cloud SQL database and database username and password
#### Create a Cloud SQL instance
You can create the Cloud SQL instance using either Cloud Console or Cloud Shell. In production, I will suggest you go for the Cloud Console because you can better look at all the configurations. But in this lab, you can simply run the following command to create a default MySQL instance in the region **us-central1**:
```
gcloud sql instances create [Cloud SQL Instance] --region us-central1
```
It usually requires 5 - 10 minutes to process.
> Run below command or Do it Manually
```
gcloud sql databases create wordpress --instance [Cloud SQL Instance] --charset utf8 --collation utf8_general_ci

gcloud sql users create wordpress --host % --instance [Cloud SQL Instance] --password [Password]
```

***OR***
### Create a database for WordPress
- In the Cloud Console, click on **Navigation Menu > SQL**.
- Once the Cloud SQL instance is ready, select the `Databases` tab on the left panel.
- Click **CREATE DATABASE**.
- Enter `wordpress` as the database name.
- Click Create.
### Create a user for accessing the Cloud SQL
- In the **Cloud SQL** page, select the **Users** tab on the left panel.
- Click *ADD USER ACCOUNT.
- Enter `wordpress` as the User name.
- Enter a password that you can remember.
- Select **Allow any host (%)** for the name of the Host.
- Click **Add**.

### Create a service account for access to your WordPress database from your WordPress instances
Now you need a service account with binding the role `roles/cloudsql.client` and save its credentials as a JSON file. In the Cloud Shell, run the following commands:
```
gcloud iam service-accounts create [Service Account]

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
   --member="[Service Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com" \
   --role="roles/cloudsql.client"

gcloud iam service-accounts keys create key.json --iam-account=[Service Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com
```

# Task 3: Setup Ingress with TLS

# Task 4: Set up Network Policy

# Task 5: Setup Binary Authorization

# Task 6: Setup Pod Security Policy

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshat_jjain

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
   --member="serviceAccount:[Service Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com" \
   --role="roles/cloudsql.client"

gcloud iam service-accounts keys create key.json --iam-account=[Service Account]@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com
```
After that, save the service account file as a secret in your Kubernetes cluster using the command provided in the official lab instruction.
```
kubectl create secret generic cloudsql-instance-credentials --from-file key.json
```
Also, the WordPress database username and password as well.
```
kubectl create secret generic cloudsql-db-credentials \
   --from-literal username=wordpress \
   --from-literal password='[Password]'
```

### Create the WordPress deployment and service
Run the following to create a persistent volume for your WordPress application:
```
kubectl create -f volume.yaml
```
Go to the overview page of your Cloud SQL instance, and copy the `Connection name`.
Open `wordpress.yaml` with your favorite editor, and replace **INSTANCE_CONNECTION_NAME** (in line 61) with the Connection name of your Cloud SQL instance.
Save the file changes, and run the following to apply the file to create the WordPress environment in the cluster.
```
kubectl apply -f wordpress.yaml
```
To verify the deployment, navigate to the Kubernetes Engine page in the Cloud Console. Now you should see `wordpress` in the Workloads tab as well as the Services tab.
# Task 3: Setup Ingress with TLS

In this challenge lab, please note that you have to install the same nginx-ingress version, which is used in lab GSP181. Otherwise, you will not able to create nginx-ingress-controller for continuing the lab.

### Set up nginx-ingress environment
The nginx-ingress will be installed using Helm. A recent, stable version of Helm should be pre-installed on your Cloud Shell. Run `helm version` to check which version you are using and also ensure that Helm is installed:
```
helm version
```
Run the following to add the chart repository and ensure the chart list is up to date:
```
helm repo add stable https://charts.helm.sh/stable
helm repo update
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
Go ahead and use the following helm command to install stable nginx-ingress:
```
helm install nginx-ingress stable/nginx-ingress --set rbac.create=true
```
Wait until the load balancer gets deployed and exposes an external IP. You get to monitor the nginx-ingress-controller service by running the following command:
```
kubectl get service nginx-ingress-controller -w
```
### Set up your DNS record
Once the service obtained an external IP address, press **Ctrl + C** to stop the previous command. You can now continue to set up your DNS record.

A shell script called add_ip.sh is provided, and you have downloaded it to the Cloud Shell at the beginning of the lab. Execute it by running this command:
```
. add_ip.sh
```
### Set up cert-manager.io

Run the following commands to deploy the `cert-manager`:
```
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v0.16.0/cert-manager.yaml

kubectl create clusterrolebinding cluster-admin-binding \
   --clusterrole=cluster-admin \
   --user=$(gcloud config get-value core/account)
```
Navigate to the Kubernetes Engine page in the Cloud Console
Edit `issuer.yaml` and set the email address(line no 10).
Save the file changes and run the following to apply them to setup the letsencrypt prod issuer:
```
kubectl apply -f issuer.yaml
```
Configure `nginx-ingress` to use an encrypted certificate for your site
Edit `ingress.yaml` and set your **YOUR_LAB_USERNAME.labdns.xyz** DNS record to lines 11 and 14 like this:
Save the file changes and run the following:
```
kubectl apply -f ingress.yaml
```
Open your domain name `https://YOUR_LAB_USERNAME.labdns.xyz` with HTTPS in a new tab.

# Task 4: Set up Network Policy

Open the `network-policy.yaml` in an editor. You should see there are already two network policies. The first one is to deny all ingress from the internet and the second one is to allow the traffic from `ngnix-ingress` to `wordpress`.

You need to add one more network policy to allow ingress traffic from the internet into `nginx-ingress`. Use the second network policy as a template to compose a new policy. Change values of `name` and `spec` to the configuration like this:
```
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
   name: allow-world-to-nginx-ingress
   namespace: default
spec:
   podSelector:
      matchLabels:
         app: nginx-ingress
   policyTypes:
   - Ingress
   ingress:
   - {}
```
Append the new policy to the `network-policy.yaml`, and save the file.
Run the following to apply the configuration file:
```
kubectl apply -f network-policy.yaml
```

# Task 5: Setup Binary Authorization
### Configure Binary Authorization Policy
- In the Cloud Console, navigate to **Security > Binary Authorization**.
- Enable the **Binary Authorization API**.
- On the Binary Authorization page, click on **EDIT POLICY**.
- Select *Disallow all images* for the **Default rule**.
- Scroll down to Images exempt from this policy, click **ADD IMAGE PATTERN**.
- Paste `docker.io/library/wordpress:latest` to the textbox, and click **DONE**.
- Repeat the above two steps to add the following image paths:
   - us.gcr.io/k8s-artifacts-prod/ingress-nginx/*
   - gcr.io/cloudsql-docker/*
   - quay.io/jetstack/*
- Click SAVE POLICY.

### Enable Binary Authorization in Google Kubernetes Engine
- Navigate to **Kubernetes Engine > Clusters**.
- Click your cluster name to view its detail page.
- Click on the pencil icon for Binary authorization under the **Security** section.
- Check Enable **Binary Authorization** in the dialog.
- Click **SAVE CHANGES**.

Your cluster will start updating its binary authorization settings. Wait until the update finish.
# Task 6: Setup Pod Security Policy
The challenge lab provides the following Pod Security Policy demo files for you to use:

- psp-restrictive.yaml
- psp-role.yaml
- psp-use.yaml

Running the following command to deploy each file:
```
kubectl apply -f <filename.yaml>
```

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13
- YouTube Channel: https://youtube.com/channel/UCQUEgfYbcz7pv36NoAv7S-Q/

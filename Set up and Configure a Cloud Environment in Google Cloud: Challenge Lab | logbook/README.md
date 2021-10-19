# ☁ Set up and Configure a Cloud Environment in Google Cloud: Challenge Lab | logbook

In this article, we will go through the lab GSP321 Set up and Configure a Cloud Environment in Google Cloud: Challenge Lab, which is an expert-level exercise on Qwiklabs. You will practice the skills and knowledge to deploy VPCs for development and production, a Kubernetes cluster, and a Cloud SQL instance for a WordPress site.


#### The challenge contains 9 required tasks:

- Create development VPC manually
- Create production VPC using Deployment Manager
- Create bastion host
- Create and configure Cloud SQL Instance
- Create Kubernetes cluster
- Prepare the Kubernetes cluster
- Create a WordPress deployment
- Enable monitoring
- Provide access for an additional engineer

## Task 1: Create development VPC manually

Make sure you create all resources in the `us-east1` region and `us-east1-b` zone.

1. In the Google Cloud Console, navigate to **VPC network > VPC networks**
2. Click on **Create VPC network**.
3. Enter `griffin-dev-vpc` to the **Name** field.
4. Select **Custom** for the Subnet creation mode.
5. Add `griffin-dev-wp` subnet with the following parameters:

| Field             	| Value             	|
|--------------------|--------------------|
| Name:             	| `griffin-dev-wp`  	|
| Region:           	| `us-east1`        	|
| IP address range: 	| `192.168.16.0/20` 	|

6. Click **+ Add subnet** and add `griffin-dev-mgmt` subnet with the following parameters

| Field             | Value              |
|-------------------|--------------------|
| Name:             | `griffin-dev-mgmt` |
| Region:           | `us-east1`         |
| IP address range: | `192.168.32.0/20`  |
7. Click Create.

## Task 2: Create production VPC using Deployment Manager

1. Copy the Deployment Manager configuration files to Cloud Shell using the following command:

```
gsutil cp -r gs://cloud-training/gsp321/dm ~/
```
2. Edit `prod-network.yaml` configuration file
```
cd dm
edit prod-network.yaml
```
3. Replace `SET_REGION` with `us-east1` in the editor, and then save the change.
4. Go back to the Cloud Shell, use the following command to create the production VPC network with the configuration files:
```
gcloud deployment-manager deployments create griffin-prod --config prod-network.yaml
```
5. Go back to the Cloud Console, navigate to Deployment Manager to confirm the deployment.

## Task 3: Create bastion host
1. In the Cloud Console, navigate to **Compute Engine > VM instances**.
2. Click **Create**.
3. Use the following parameters to create the bastion host:

 | Field   	| Value          	|
 |---------	|----------------	|
 | Name:   	| griffin-dev-db 	|
 | Region: 	| us-east1       	|

4. Expand the **Management, security, disks, networking, sole tenancy** section.
5. In the **Networking** tab, add `bastion` to the Network tags.
6. Click **Add network interface**, make sure that you set up two Network interfaces,
   - griffin-dev-mgmt
   - griffin-prod-mgmt
7. Click Create.
8. Navigate to **VPC network > Firewall**.
9. Click **CREATE FIREWALL RULE**.
10. Configure the rule with the following parameters:

| Field                	| Value                 	|
|----------------------	|-----------------------	|
| Name:                	| allow-bastion-dev-ssh 	|
| Network:             	| griffin-dev-vpc       	|
| Targets:             	| bastion               	|
| Source IP ranges:    	| 192.168.32.0/20       	|
| Protocols and ports: 	| tcp: 22               	|

11. Click **CREATE**.
12. Click **CREATE FIREWALL RULE** again.
13. Configure another rule with the following parameters:

| Field                	| Value                  	|
|----------------------	|------------------------	|
| Name:                	| allow-bastion-prod-ssh 	|
| Network:             	| griffin-prod-vpc       	|
| Targets:             	| bastion                	|
| Source IP ranges:    	| 192.168.48.0/20        	|
| Protocols and ports: 	| tcp: 22                	|

14. Click **CREATE**.

OR 
```
gcloud compute --project=qwiklabs-gcp-01-240538d99502 firewall-rules create allow-bastion-prod-ssh --direction=INGRESS --priority=1000 --network=griffin-prod-vpc --action=ALLOW --rules=tcp:22 --source-ranges=192.168.48.0/20 --target-tags=bastion
```

## Task 4: Create and configure Cloud SQL Instance
In the Cloud Console, navigate to SQL.
Click CREATE INSTANCE.
Click Choose MySQL.
Use the following parameters to create the instance:

| Field          	| Value          	|
|----------------	|----------------	|
| Name:          	| griffin-dev-db 	|
| Region:        	| us-east1       	|
| Zone:          	| us-east1-b     	|
| Root password: 	| e.g. 12345678  	|
| Path           	| /              	|

Note: In real practice, you must set a strong password.

Click Create.
Click the griffin-dev-db in the SQL pane after it has been created.
Under Connect to this instance, click on Connect using Cloud Shell.
Go back to the Cloud Shell, run:
```
gcloud sql connect griffin-dev-db --user=root --quiet
```
Enter the Root password generated in Step 4.
In the SQL console, run the following query to create the wordpress database:
``` sql
CREATE DATABASE wordpress;
GRANT ALL PRIVILEGES ON wordpress.* TO "wp_user"@"%" IDENTIFIED BY "stormwind_rules";
FLUSH PRIVILEGES;
exit
```
## Task 5: Create Kubernetes cluster
Create a 2 node cluster (n1-standard-4) called griffin-dev, in the griffin-dev-wp subnet, and in the zone us-east1-b.


1. In the Cloud Console, navigate to Kubernetes Engine > Clusters.
2. Click Create cluster.
3. In the Cluster basics tab, configure:
   - Name: griffin-dev
   - Zone: us-east1-b
 
4. In the left pane, click default-pool under NODE POOLS and set
   - Number of nodes: 2
5. Click Nodes Under default-pool, and set
   - Machine type: n1-standard-4
7. Go to the Network tab, set
   - Network: griffin-dev-vpc
   - Node subnet: griffin-dev-wp
8. Networking settings for new Kubernetes cluster griffin-dev
9. Click CREATE.
or
```
gcloud beta container --project "qwiklabs-gcp-01-240538d99502" clusters create "griffin-dev" --zone "us-east1-b" --no-enable-basic-auth --cluster-version "1.20.10-gke.301" --release-channel "regular" --machine-type "n1-standard-4" --image-type "COS_CONTAINERD" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --max-pods-per-node "110" --num-nodes "2" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/qwiklabs-gcp-01-240538d99502/global/networks/griffin-dev-vpc" --subnetwork "projects/qwiklabs-gcp-01-240538d99502/regions/us-east1/subnetworks/griffin-dev-wp" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --enable-shielded-nodes --node-locations "us-east1-b"
```


## Task 6: Prepare the Kubernetes cluster
In the Cloud Shell, use the following command to copy the files for the Kubernetes:
```
gsutil cp -r gs://cloud-training/gsp321/wp-k8s ~/
```
Open `wp-k8s/wp-env.yaml` with the Cloud Shell Editor.
```
cd ~/wp-k8s
edit wp-env.yaml
```
Replace `username_goes_here` and `password_goes_here` to **`wp_user`** and **`stormwind_rules`**, respectively.
Save the file change.
After the Kubernetes cluster has been created, click on the Connect button.
Run the following command to connect the cluster:
```
gcloud container clusters get-credentials griffin-dev --zone=us-east1-b
```
Deploy the configuration to the cluster using:
```
kubectl apply -f wp-env.yaml
```
Use the command below to create the key, and then add the key to the Kubernetes environment:
```
gcloud iam service-accounts keys create key.json \
    --iam-account=cloud-sql-proxy@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
kubectl create secret generic cloudsql-instance-credentials \
    --from-file key.json
```
## Task 7: Create a WordPress deployment
Open `wp-k8s/wp-deployment.yaml` with the Cloud Shell Editor
```
cd ~/wp-k8s
edit wp-deployment.yaml
```
Replace `YOUR_SQL_INSTANCE` with `griffin-dev-db`’s Instance connection name.


Save the file change.
Go back to the Cloud Shell, run the following commands:
```
kubectl create -f wp-deployment.yaml
kubectl create -f wp-service.yaml
```
Copy the External endpoints of the deployed wordpress service and open it in your browser.


## Task 8: Enable monitoring
Go back to the Cloud Console, and navigate to Monitoring.
In the Monitoring console, click Uptime checks in the left pane.
Click CREATE UPTIME CHECK.
Configure using the following parameters:

| Field         	| Value                   	|
|---------------	|-------------------------	|
| Title         	| WordPress Uptime        	|
| Check Type    	| HTTP                    	|
| Resource Type 	| URL                     	|
| Hostname      	| YOUR-WORDPRESS_ENDPOINT 	|
| Path          	| /                       	|

new GCP uptime checks monitoring
Click TEST.
Click SAVE if there is no error.
## Task 9: Provide access for an additional engineer
In the Cloud Console, navigate to IAM & Admin > IAM.
Click +ADD.
In the Add members to … pane, copy and paste the second user account for the lab to the New members field.
In the Role dropdown, select Project > Editor.
Click SAVE.


Congratulations! You completed this challenge lab.

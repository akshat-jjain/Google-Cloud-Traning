# Build and Secure Networks in Google Cloud: Challenge Lab


In this article, we will go through the lab Build and Secure Networks in Google Cloud. In the previous, lab you will get familiar with User Authentication: Identity-Aware Proxy, Multiple VPC Networks,
VPC Networks Controlling Access, HTTP Load Balancer with Cloud Armor and Create an Internal Load Balancer.
#### The challenge contains 6 required tasks
- Remove the overly permissive rules.
- Start the bastion host instance.
- Create a firewall rule that allows SSH (tcp/22) from the IAP service and add network tag on bastion.
- Create a firewall rule that allows traffic on HTTP (tcp/80) to any address and add network tag on juice-shop.
- Create a firewall rule that allows traffic on SSH (tcp/22) from the acme-mgmt-subnet network address and add network tag on juice-shop.
- SSH to bastion host via IAP and juice-shop via bastion.


#### Some Jooli Inc. standards you should follow:
- Create all resources in the default region or zone, unless otherwise directed.
- Naming is normally a team-resource, e.g. an instance could be named kraken-webserver1
- Allocate cost-effective resource sizes. Projects are monitored and excessive resource use will result in the containing project’s termination (and possibly yours), so beware. This is the guidance the monitoring team is willing to share; unless directed use f1-micro for small Linux VMs and n1-standard-1 for Windows or other applications such as Kubernetes nodes.

## 1. Create the production environment
The first step is to create open-access firewall rules.

> Use this command or Do Manually
```
gcloud compute firewall-rules delete open-access
```

- In the GCP Console go to Navigation Menu >VPC Network > Firewall.
- Click on the box next to the rule named open-access.
- Then Click on Delete to remove.


## 2. Start the bastion host instance
In this step, you have a virtual machine and want to start.

> Use this command or Do Manually
```
gcloud compute instances start bastion
```

- In the GCP Console go to Navigation Menu >Compute Engine > VM Instance.
- Click on the box next to the instance named bastion.
- Click on Start to run the instance.


## 3. Create a firewall rule that allows SSH (tcp/22) from the IAP service and add network tag on bastion
In this step, you have to create a firewall rule that allows SSH (tcp/22) from the IAP service.

> Use this command or Do Manually
> Replace `SSH IAP network tag` with your SSH IAP network tag.
```
gcloud compute firewall-rules create SSH IAP network tag --allow=tcp:22 --source-ranges 35.235.240.0/20 --target-tags SSH IAP network tag --network acme-vpc
gcloud compute instances add-tags bastion --tags=SSH IAP network tag --zone=us-central1-b
```

- Add network tag on bastion VM.
- Go to the VM Instance page, click on the bastion instance and click the Edit option
- Now Add `SSH IAP network tag` to the Network tags field.
- At the end of the page click Save.
- Now you have to create a firewall for bastion
- In the GCP Console go to Navigation Menu >VPC Network > Firewall.
- Click Create firewall rule.
- Configure the following settings:

| Field                	| Value                                	|
|----------------------	|--------------------------------------	|
| Name                 	| e.g. `SSH IAP network tag`            |
| Direction of traffic 	| Ingress                              	|
| Targets              	| Specified target tags                	|
| Target tags          	| `SSH IAP network tag`                	|
| Source IP ranges     	| 35.235.240.0/20                      	|
| Protocols and ports  	| Select TCP and enter 22 to allow SSH 	|


## 4. Create a firewall rule that allows traffic on HTTP (tcp/80) to any address and add network tag on juice-shop
In this step, you have to create a firewall rule that allows traffic on HTTP (tcp/80) to any address.
> Use this command or Do Manually
> Replace `HTTP network tag` with your HTTP network tag
```
gcloud compute firewall-rules create HTTP network tag --allow=tcp:80 --source-ranges 0.0.0.0/0 --target-tags HTTP network tag --network acme-vpc
gcloud compute instances add-tags juice-shop --tags=HTTP network tag --zone=us-central1-b
```
- In the GCP Console go to Navigation Menu >VPC Network > Firewall.
- Click Create firewall rule.
- Configure the following settings:

| Field                	| Value                                 	|
|----------------------	|---------------------------------------	|
| Name                 	| e.g. `HTTP network tag`               	|
| Direction of traffic 	| Ingress                               	|
| Targets              	| Specified target tags                 	|
| Target tags          	| `HTTP network tag`                      |
| Source IP ranges     	| 0.0.0.0/0                             	|
| Protocols and ports  	| Select TCP and enter 80 to allow HTTP 	|

- Add network tag on juice-shop VM.
- Go to the VM Instance page, click on the juice-shop instance and click the Edit option
- Now Add `HTTP network tag` to the Network tags field.
- At the end of the page click Save.


## 5. Create a firewall rule that allows traffic on SSH (tcp/22) from acme-mgmt-subnet network address and add network tag on juice-shop
In this step, you have to create a firewall rule that allows traffic on SSH (tcp/22) from acme-mgmt-subnet network address.
> Use this command or Do Manually
> Replace `SSH internal network tag` with your SSH internal network tag
```
gcloud compute firewall-rules create SSH internal network tag --allow=tcp:22 --source-ranges 192.168.10.0/24 --target-tags SSH internal network tag --network acme-vpc
gcloud compute instances add-tags juice-shop --tags=SSH internal network tags --zone=us-central1-b
```
- In the GCP Console go to Navigation Menu >VPC Network.
- Copy the IP address of the aceme-mgmt-subnet.
- In the GCP Console go to Navigation Menu >VPC Network > Firewall> Firewall Rules.
- Click Create firewall rule.
- Configure the following settings:

| Field                	| Value                                      	|
|----------------------	|--------------------------------------------	|
| Name                 	| e.g. `SSH internal network tag`          	  |
| Direction of traffic 	| Ingress                                    	|
| Targets              	| Specified target tags                      	|
| Target tags          	| `SSH internal network tag`                 	|
| Source IP ranges     	| IP address range of your aceme-mgmt-subnet 	|
| Protocols and ports  	| Select TCP and enter 22 to allow SSH       	|


## 6. SSH to bastion host via IAP and juice-shop via bastion
After configuring the firewall rules, try to verify the environment via the bastion.
- In the GCP Console go to Navigation Menu >Compute Engine > VM Instance.
- Copy the Internal IP of the `juice-shop` instance.
- Then click on the SSH button in the row of the `bastion` instance.
- From the SSH console, access the juice-shop from the bastion using the following command:
```
ssh <internal-IP-of-juice-shop>
```
> Note:Replace `<internal-IP-of-juice-shop>` with Internal IP


# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshat_jjain

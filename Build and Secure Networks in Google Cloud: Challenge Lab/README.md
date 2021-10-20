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
- In the GCP Console go to Navigation Menu >VPC Network > Firewall.
- Click on the box next to the rule named open-access.
- Then Click on Delete to remove.
## 2. Start the bastion host instance
In this step, you have a virtual machine and want to start.
- In the GCP Console go to Navigation Menu >Compute Engine > VM Instance.
- Click on the box next to the instance named bastion.
- Click on Start to run the instance.
## 3. Create a firewall rule that allows SSH (tcp/22) from the IAP service and add network tag on bastion
In this step, you have to create a firewall rule that allows SSH (tcp/22) from the IAP service.
- Add network tag on bastion VM.
- Go to the VM Instance page, click on the bastion instance and click the Edit option
- Now Add bastion to the Network tags field.
- At the end of the page click Save.
- Now you have to create a firewall for bastion
- In the GCP Console go to Navigation Menu >VPC Network > Firewall.
- Click Create firewall rule.
- Configure the following settings:
Field- Value
Name- e.g. allow-ssh-from-iap
Direction of traffic- Ingress
Targets- Specified target tags
Target tags-bastion
Source IP ranges- 35.235.240.0/20
Protocols and ports- Select TCP and enter 22 to allow SSH

## 4. Create a firewall rule that allows traffic on HTTP (tcp/80) to any address and add network tag on juice-shop
In this step, you have to create a firewall rule that allows traffic on HTTP (tcp/80) to any address.
- In the GCP Console go to Navigation Menu >VPC Network > Firewall.
- Click Create firewall rule.
- Configure the following settings:
Field- Value
Name- e.g. allow-http-ingress
Direction of traffic- Ingress
Targets- Specified target tags
Target tags-juice-shop
Source IP ranges-0.0.0.0/0
Protocols and ports- Select TCP and enter 80 to allow HTTP

- Add network tag on juice-shop VM.
- Go to the VM Instance page, click on the juice-shop instance and click the Edit option
- Now Add juice-shop to the Network tags field.
- At the end of the page click Save.
## 5. Create a firewall rule that allows traffic on SSH (tcp/22) from acme-mgmt-subnet network address and add network tag on juice-shop
In this step, you have to create a firewall rule that allows traffic on SSH (tcp/22) from acme-mgmt-subnet network address.
- In the GCP Console go to Navigation Menu >VPC Network.
- Copy the IP address of the aceme-mgmt-subnet.
- In the GCP Console go to Navigation Menu >VPC Network > Firewall> Firewall Rules.
- Click Create firewall rule.
- Configure the following settings:
Field- Value
Name- e.g.allow-ssh-from-mgmt-subnet
Direction of traffic- Ingress
Targets- Specified target tags
Target tags-bastion,juice-shop
Source IP ranges- IP address range of your aceme-mgmt-subnet
Protocols and ports- Select TCP and enter 22 to allow SSH.

## 6. SSH to bastion host via IAP and juice-shop via bastion
After configuring the firewall rules, try to verify the environment via the bastion.
- In the GCP Console go to Navigation Menu >Compute Engine > VM Instance.
- Copy the Internal IP of the juice-shop instance.
- Then click on the SSH button in the row of the bastion instance.
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

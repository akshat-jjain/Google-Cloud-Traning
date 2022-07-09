# Getting Started: Create and Manage Cloud Resources: Challenge Lab

In this article, we will go through the lab Getting Started: Create and Manage Cloud Resources. In the previous, lab you will get familiar with Google Cloud Platform, Virtual Machine, Kubernetes Engine, Load Balancer.


#### The challenge contains 3 required tasks
- Creating a Project Jumphost instance.
- Creating a Kubernetes Service Cluster.
- Creating the Web Server Frontend.

#### Some Jooli Inc. standards you should follow:
- Create all resources in the default region or zone, unless otherwise directed.
- Naming is normally team-resource, e.g. an instance could be named nucleus-webserver1
- Allocate cost-effective resource sizes. Projects are monitored and excessive resource use will result in the containing project’s termination (and possibly yours), so beware. This is the guidance the monitoring team is willing to share; unless directed use f1-micro for small Linux VMs and n1-standard-1 for Windows or other applications such as Kubernetes nodes.



## 1.Create a project Jumphost instance
The first step is to create a Jumphost instance
- In the GCP Console go to Navigation Menu >Compute Engine > VM Instance.

- Write the below parameters, check machine type, and Image type.
- The name of instance be `Instance Name`
- Region be Default Region
- Zone be Default Zone
- The machine type be f1-micro.
- Using the default image type (Debian Linux)
- Click **Create**

## 2.Create a Kubernetes service cluster
In this step, you have to create a Kubernetes Service Cluster
- Create the cluster in the us-east1 region.
- Using the Docker container hello-app (`gcr.io/google-samples/hello-app:2.0`) as a place holder.
- Open the app on port `Port Number`
- Activate Cloud Shell and write the following commands

> Note: Replace Port Number with your Port Number
``` bash
gcloud config set compute/zone us-east1-b
gcloud container clusters create nucleus-webserver1
gcloud container clusters get-credentials nucleus-webserver1
kubectl create deployment hello-app --image=gcr.io/google-samples/hello-app:2.0
kubectl expose deployment hello-app --type=LoadBalancer --port PortNumber
kubectl get service 
```


It will create a Kubernetes cluster
## 3.Setup an HTTP load balancer
In this step, you have to create a serve the site via Nginx web servers
- Activate the cloud shell and Copy and Paste the following commands

``` bash
cat << EOF > startup.sh
#! /bin/bash
apt-get update
apt-get install -y nginx
service nginx start
sed -i — ‘s/nginx/Google Cloud Platform — ‘“\$HOSTNAME”’/’ /var/www/html/index.nginx-debian.html
EOF
```

Now you have to perform the steps to HTTP(s) Load Balancer in front of two web servers

1. Creating an instance template:

``` bash
gcloud compute instance-templates create nginx-template \
--metadata-from-file startup-script=startup.sh
```

2. Creating a target pool:

``` bash
gcloud compute target-pools create nginx-pool
```

3. Creating a managed instance group:

``` bash
gcloud compute instance-groups managed create nginx-group \
--base-instance-name nginx \
--size 2 \
--template nginx-template \
--target-pool nginx-pool

gcloud compute instances list
```

4. Creating a firewall rule to allow traffic (80/tcp):

> Note: Replace FirewallName with Your Firewall Name

``` bash
gcloud compute firewall-rules create FirewallName --allow tcp:80

gcloud compute forwarding-rules create nginx-lb \
--region us-east1 \
--ports=80 \
--target-pool nginx-pool

gcloud compute forwarding-rules list
```

5. Creating a health check:

``` bash
gcloud compute http-health-checks create http-basic-check

gcloud compute instance-groups managed \
set-named-ports nginx-group \
--named-ports http:80
```

6. Creating a backend service and attach the managed instance group:

``` bash
gcloud compute backend-services create nginx-backend \
--protocol HTTP --http-health-checks http-basic-check --global

gcloud compute backend-services add-backend nginx-backend \
--instance-group nginx-group \
--instance-group-zone us-east1-b \
--global
```

7. Creating a URL map and target HTTP proxy to route requests to your URL map:

``` bash
gcloud compute url-maps create web-map \
--default-service nginx-backend

gcloud compute target-http-proxies create http-lb-proxy \
--url-map web-map
```

8. Creating a forwarding rule:

``` bash
gcloud compute forwarding-rules create http-content-rule \
--global \
--target-http-proxy http-lb-proxy \
--ports 80

gcloud compute forwarding-rules list
```

# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13
- YouTube Channel: https://youtube.com/channel/UCQUEgfYbcz7pv36NoAv7S-Q/


# Demonstration Video
[![Watch the video](https://img.youtube.com/vi/CjVlbv5GmKU/maxresdefault.jpg)](https://youtu.be/CjVlbv5GmKU)

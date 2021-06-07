# ☁ Google Cloud Essential Skills: Challenge Lab | logbook

# Task 1 - Create a VM instance
To create a Compute Engine instance, the easiest way is through the GCP web console. In the Console, navigate to Compute Engine > VM instances. When you create a new VN instance,

- Make sure you give the instance a name, called `apache`, and
- Select `Allow HTTP traffic` under the Firewall section.
- You can leave other fields with the default settings, then click **Create**.
> Check your progress: Created Compute Engine instance, called apache
 
# Task 2 - Install Apache and Overwrite Default Web Page
After the VM instance is really, you have to configure it as an Apache webserver. If you do not remember how to install Apache, I advise you to look up the command lines from the lab GSP212 “VPC Flow Logs - Analyzing Network Traffic“.


Keep inside the VM instances console, click **SSH** to launch a terminal, and connect to the `apache` instance. You will install the packages with the following command-lines.

In the SSH terminal, update the package index:
```
sudo apt-get update
```
Install the apache2 package:
```
sudo apt-get install apache2 -y
```

Copy the External IP of the instance to your web browser. You should see an Apache2 Debian Default Page if the web server is successfully installed.


Apache2 Debian Default Page


Finally, you have to overwrite the default web page to rendering with **“Hello World!”**:
```
echo '<!doctype html><html><body><h1>Hello World!</h1></body></html>' | sudo tee /var/www/html/index.html
```
Refresh the web page in your browser,

# Congratulations! You should accomplish the lab 

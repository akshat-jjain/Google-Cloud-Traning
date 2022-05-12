# ☁ Deploy a Compute Instance with a Remote Startup Script | logbook
 

# Brief Introduction of Challenge Scenario

1. Create a Google Cloud Storage bucket, and confirm that the bucket contains a file.
2. Create a Linux virtual machine that runs a remote startup script called install-web.sh from cloud storage.
3. Confirm that an HTTP access firewall rule exists with tag that applies to that virtual machine.
4. Confirm the web server can be connected using HTTP and get a non-error response.

# Download Sample Startup Script
First of all, find **Sample Startup Script** below the Start button and the timer of the lab. Then, download the startup script file to your computer. This lab requires a minute for provisioning lab resources. You may make use of this interval to download the file or take a drink.

Download sample startup script below the Qwiklabs start button and lab timer
# Upload the Startup Script to a Cloud Storage Bucket
1. In the web console, navigate to Storage.
2. Create a bucket with a unique bucket name.
3. Upload the `install-web.sh` file to the bucket.
4. Make the file publicly accessible (This ensures the file can be accessed by the VM instance deployed soon).
   1. Edit the file permissions in Cloud Storage using GCP web console
   2. Click the three dots icon at the right end of the filename. Choose *Edit permissions* in the dropdown menu.
   3. Add a new User, type **allUsers** to the name field, and choose Reader.
5. Click the filename and copy the URL, i.e. `gs://.../install-web.sh` for later use.

# Configure Metadata in Creating VM instance

1. Go to Compute Engine, create a new VM instance.
2. Select `Allow HTTP traffic` under the Firewall section.
3. Expand **Management, security, disks, networking, sole tenancy**.
4. In the Metadata section, add `startup-script-url` and paste the URL of the script file as the key value.
5. Click Create to create the instance.

# Inspect Instance Correctly Running Startup Script

1. Wait for the new VM instance startup.
2. Click the instance name to open its Details tab. Then, expand the Logs and click Serial port 1 (console).
3. The startup script automatically installs the Apache web server software while creating the VM instance. You should able to find the log events about downloading the startup script and installing the apache packages.
4. Open the external IP in your web browser. You should view the Apache default page if the startup script has been successfully executed.


# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13


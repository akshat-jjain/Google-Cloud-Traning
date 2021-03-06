# ☁ Configure a Firewall and a Startup Script with Deployment Manager | logbook

 
With the Google Cloud web console, you can easily configure and deploy many different GCP resources without any coding skills. I believe that there is no big deal for you, even a beginner, to finish the first and second labs of the Qwiklabs quest of “Cloud Architecture: Design, Implement, and Manage”. The web console assists in quick access to the GCP resources for testing and building small projects. If you are an amateur or hobbyist developer, just make use of the web console is pretty enough.

But if you aim to be a professional cloud engineer, you must know and apply some more advanced skills, such as creating and managing cloud resources with simple templates for a repeatable deployment process. The third lab of the challenge quest, GSP302 “Configure a Firewall and a Startup Script with Deployment Manager“, is to test your ability to define the resources of a basic apache web server. You need to know how to format and parameterize the resource properties in YAML as a Jinja2 configuration file. It is much harder than the previous labs. I recommend you revising the Qwiklabs quest called Deployment Manager, if you are not familiar with building custom templates.

# Brief Introduction of Challenge Scenario

1. Configure a deployment template and apply it to the Deployment Manager.
2. The deployment creates a VM instance with an embedded startup-script.
3. The VM instance that has a startup-script also has a tag called http.
4. Create a firewall rule that allows port 80 (HTTP) traffic and is applied using the tag http.
5. The virtual machine responds to web requests using the Apache web server, which should be installed by the startup script.
6. The Deployment manager includes startup script and firewall resources.

# Download the baseline Deployment Manager template

The lab gives a basic deployment manager template, containing with the `.jinja`, `.yaml` and `.jinja.schema` files as well as the sample startup script. In a cloud shell, use the following commands to download and unpack the files.

```
mkdir deployment_manager
cd deployment_manager
gsutil cp gs://spls/gsp302/* .
```
You can explore the files by opening a Cloud Shell code editor. The template for you to deploy a virtual machine

# Edit the Jinja Template
Open the `qwiklabs.jinja` file, you should see the following codes:
The template already includes the following configurations:

* Instance name: vm-test
* Zone: Read the value from the `qwiklabs.yaml`
* Machine Type: f1-micro
* Disks: Persistent, Debian-9
* Network Interfaces: Default Network with a public IP address
<br>
To fulfil the lab requirements, the template still does not have,

* metadata for embedding the startup script, and
* a tag called `http`.

# Add Firewall Rule for HTTP traffic
Firewall rules and VM instances are separated resources, so make sure to correctly space/indent the firewall configuration code to be part of the resource block. You may manually list and parameterize the configuration all by yourself, if you can. A more robust way to use the GCP web console to visually configure and generate a REST profile with creating the firewall.

Format the REST profile using a JSON to YAML converter, such as https://www.json2yaml.com/. You should obtain something similar to the following codes:

```
resources:
- type: compute.v1.instance
  name: vm-{{ env["deployment"] }}
  properties:
    zone: {{ properties["zone"] }}
    machineType: https://www.googleapis.com/compute/v1/projects/{{ env["project"] }}/zones/{{ properties["zone"] }}/machineTypes/f1-micro
    tags:
        items:
        - 'http'
    metadata:
      items:
      # For more ways to use startup scripts on an instance, see:
      #   https://cloud.google.com/compute/docs/startupscript
      - key: startup-script
        value: |
          #!/bin/bash
          apt-get update
          apt-get install -y apache2
    disks:
    - deviceName: boot
      type: PERSISTENT
      boot: true
      autoDelete: true
      initializeParams:
        diskName: disk-{{ env["deployment"] }}
        sourceImage: https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/family/debian-9
    networkInterfaces:
    - network: https://www.googleapis.com/compute/v1/projects/{{ env["project"] }}/global/networks/default
      # Access Config required to give the instance a public IP address
      accessConfigs:
      - name: External NAT
        type: ONE_TO_ONE_NAT
- type: compute.v1.firewall
  name: {{ env["project"] }}-allow-http
  properties:
    network: https://www.googleapis.com/compute/v1/projects/{{ env["project"] }}/global/networks/default
    sourceRanges: [0.0.0.0/0]
    targetTags: ['http']
    allowed:
    - IPProtocol: tcp
      ports: ['80']
```
**Save** the file change.

Open `qwiklabs.yaml`
Replace Code with this
```
imports:
- path: qwiklabs.jinja

resources:
- name: qwiklabs
  type: qwiklabs.jinja
  properties:
    zone: us-central1-a
```

# Apply the Deployment
It’s time to deploy the configuration file and see if the deployment works. Run the following `gcloud` command in Cloud Shell.
```
gcloud deployment-manager deployments create vm-test --config=qwiklabs.yaml
```
In the web console, navigate to **Deployment Manager** to monitor the progress. Also, go to **Compute Engine** and **VPC Network > Firewall** to verify the deployment results.


# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshat_jjain


# ☁ Configure Secure RDP using a Windows Bastion Host with Terraform on GCP | logbook
 
The topic “Configure Secure RDP using a Windows Bastion Host” is from a challenging lab that I took in Qwiklabs (here is the link to the lab). It was a tricky one that I failed and did a few times of retakes to accomplish it. If you face the same challenge, I hope this blog article would help you. I will share my codes with you for your reference.

Qwiklabs has over 400 hands-on labs and is a great online self-paced learning Google Cloud Platform (GCP). Most exercises in Qwiklabs provide clear step-by-step instructions for you to follow and finish the labs, except a few Advanced Challenge Labs. Those labs are not easy because they do not offer the “cookbook” steps. You have to figure out the solutions by yourself as the exercises for students who prepare for the Google Cloud Certified Professional Cloud Architect. The lab GSP303 “Configure Secure RDP using a Windows Bastion Host“ is one of the challenge exercises.

Brief Introduction of Challenge Scenario

1. Create a new non-default VPC called securenetwork.
2. Create a new non-default subnet within securenetwork.
3. Configure a firewall rule that allows TCP port 3389 traffic ( for RDP ) the internet to the bastion host called vm-bastionhost using network tags.
4. Create a Windows 2016 server instance vm-bastionhost with applying the above firewall rule.
5. Create a Windows 2016 server instance called vm-securehost that does not have a public IP-address.
6. The vm-securehost is running Microsoft IIS web server software.

vpc
creATE
name = securenetwork
new subnet:
name = secure-subnet
region = us-central1
ip range = 192.168.16.0/20
CREATE
------------------------------------
click on the vpc network you made
go to FIREWALL RULES
add firewall rule
name = secure-allow-rdp
target tags = rdp
source ip ranges = 0.0.0.0/0
check TCP = 3389
CREATE
--------------------------------------------------------------------
VM INSTANCES
create vm instance
name = vm-bastionhost
n1 standard 2
boot disk = windows server / windows server 2016 datacenter
boot disk type = standard persistent disk
szie = 150
allow http
networking
networking tags = rdp
network interface
network -> securenetwork (external ip = epipheral)
add network default (external ip = epipheral)
CREATE
--------------------------------------------------------------------
CREATE ANOTHER INSTANCE
NAME = vm-securehost
n1 standard 2
boot disk = windows server / windows server 2016 datacenter
boot disk type = standard persistent disk
szie = 150
networking tags = rdp
network interface
network -> securenetwork -> external ip -> none
add network default
CREATE

OPEN CLOUD SHELL
gcloud compute reset-windows-password vm-bastionhost --user app_admin --zone us-central1-a

go to start menu and type "remote desktop connection"
input ip addr from the cloud shell
connect
input username and password from cloud shell

minimize the screen and go to cloud shell

gcloud compute reset-windows-password vm-securehost --user app_admin2 --zone us-central1-a

add roles and features

next next next

click web server(IIS)
add feature
next next next install

since we had reset external ip for web server IIS ... we have to edit and remove its ip again
If your second last task is remaining go to vm-securehost and click on edit
Make these changes
network -> securenetwork -> external ip -> none
network default -> external ip -> none


# Congratulations! You completed this challenge lab.
Stay tuned till the next blog
##### If you Want to Connect with Me:

- Linkedin: https://www.linkedin.com/in/akshat-jjain
- Twitter: https://twitter.com/akshatjain_13


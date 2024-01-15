# Set up JFrog Artifactory Server

You will use JFrog Artifactory server for your next project. Below are the steps to set up the Artifactory server on an XLarge EC2 Instance using Docker, assuming you are using Amazon Linux 2.

## Table of Contents
- [JFrog System Requirements](#jfrog-system-requirements)
- [Launch an EC2 Instance](#launch-an-ec2-instance)
- [Connect to Your EC2 Instance](#connect-to-your-ec2-instance)
- [Update and Install Required Packages](#update-and-install-required-packages)
- [Download Artifactory Docker Image](#download-artifactory-docker-image)
- [Create Data Directory](#create-data-directory)
- [Start JFrog Artifactory Container](#start-jfrog-artifactory-container)
- [Run Artifactory as a Service](#run-artifactory-as-a-service)
- [Access Artifactory Web Interface](#access-artifactory-web-interface)
- [Default Username and Password for JFrog](#default-username-and-password-for-jfrog)
- [Configure Artifactory through the Web Interface](#configure-artifactory-through-the-web-interface)
- [Conclusion](#conclusion)

## JFrog System Requirements
Before starting the setup, ensure you have the following system requirements for the JFrog Artifactory server:
- 4 CPU
- 4GB Memory (RAM)

As a result, an XLarge EC2 Instance is recommended to meet these requirements.

### Launch an EC2 Instance
1. Log in to your AWS console.
2. Go to the EC2 dashboard.
3. Click "Launch Instance" and select an appropriate Amazon Machine Image (AMI) based on Amazon Linux 2.
4. Choose the instance type, configure the instance, and add storage as per your requirements.
5. Configure security groups to allow incoming traffic to Artifactory ports (e.g., HTTP/HTTPS).

### Connect to Your EC2 Instance
Once your EC2 instance is running, you need to connect to it via SSH using the key pair you selected while launching the instance.

### Update and Install Required Packages
Run the following commands to update and install the necessary packages on your EC2 instance:
```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
docker info
```

### Download Artifactory Docker Image
Pull the latest JFrog Artifactory Docker image using the following command:
```bash
sudo docker pull docker.bintray.io/jfrog/artifactory-oss:latest
docker images
```

### Create Data Directory
Create a data directory for Artifactory on the host system:
```bash
sudo mkdir -p /jfrog/artifactory
sudo chown -R 1030 /jfrog/
```

### Start JFrog Artifactory Container
Start the Artifactory container using the following command:
```bash
sudo docker run --name artifactory -d -p 8081:8081 -p 8082:8082 -v /jfrog/artifactory:/var/opt/jfrog/artifactory docker.bintray.io/jfrog/artifactory-oss:latest
```

### Run Artifactory as a Service
To run Artifactory as a service, create a systemd script for Artifactory:
```bash
sudo vi /etc/systemd/system/artifactory.service
```
Copy and paste the following code into the editor:
```plaintext
[Unit]
Description=Setup Systemd script for Artifactory Container
After=network.target

[Service]
Restart=always
ExecStartPre=-/usr/bin/docker kill artifactory
ExecStartPre=-/usr/bin/docker rm artifactory
ExecStart=sudo docker run --name artifactory -d -p 8081:8081 -p 8082:8082 -v /jfrog/artifactory:/var/opt/jfrog/artifactory docker.bintray.io/jfrog/artifactory-oss:latest

[Install]
WantedBy=multi-user.target
```
Save and exit from the editor (press `Esc`, type `:wq`, and hit `Enter`).

Run the following commands to enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start artifactory
sudo systemctl enable artifactory
sudo systemctl status artifactory
```

### Access Artifactory Web Interface
By default, Artifactory runs on port 8081. Ensure the security group associated with your EC2 instance allows incoming traffic on this port. Then, open your web browser and navigate to: `http://your-ec2-instance-public-ip:8081/artifactory/`. You should now see the Artifactory login page.

### Default Username and Password for JFrog
- Username: `admin`
- Password: `password`

### Configure Artifactory through the Web Interface
Follow the Artifactory setup wizard to complete the initial configuration. You will need to set up the admin user, license key (if applicable), and any additional settings.

## Conclusion
Congratulations! You have successfully set up JFrog Artifactory on an XLarge EC2 Instance using Docker. The server is now ready for use in your projects.


## Set up a GitLab server on an EC2 instance using Docker image:

1. Launch a new EC2 instance:
   - Log in to the AWS Management Console.
   - Go to the EC2 service.
   - Click on "Launch Instance" to create a new virtual machine.
   - Choose an appropriate Docker-compatible AMI. You can search for AMIs labeled as "Amazon Linux 2" or "Ubuntu" with Docker pre-installed.
   - Select an instance type based on your requirements and click "Next" to proceed.
   - Configure the instance details, such as the number of instances, network settings, and storage.
   - Add any additional tags or security groups as needed.
   - Review the configuration and click "Launch" to create the instance.
   - Choose or create a key pair to access the instance securely.
   - Once the instance is launched, note down the public IP or DNS name for future reference.

2. Connect to the EC2 instance using SSH:
   - Open a terminal or SSH client on your local machine.
   - Use the SSH key pair you selected during the instance setup to connect to the EC2 instance using its public IP or DNS name.
   - The SSH command typically looks like this: `ssh -i /path/to/private_key.pem ec2-user@public_ip_address`

3. Install Docker on the EC2 instance:
   - Update the package lists on the EC2 instance by running the following command:
     ```
     sudo apt update      # for Ubuntu
     ```
   - Install Docker by running the appropriate commands based on the operating system:
     ```
     sudo apt install docker.io     # for Ubuntu
     ```
   - Start the Docker service:
     ```
     sudo service docker start
     ```
   - Add the current user to the Docker group to run Docker commands without sudo (optional):
     ```
     sudo usermod -aG docker $USER
     ```

4. Pull the GitLab Docker image:
   - Run the following command to pull the GitLab Docker image from the official repository:
     ```
     sudo docker pull gitlab/gitlab-ce:latest
     ```

5. Run the Docker container with the GitLab image:
   - Start the GitLab container using the pulled Docker image:
     ```
     sudo docker run -d \
       --publish 443:443 --publish 80:80 --publish 22:22 \
       --name gitlab \
       --restart always \
       --volume /srv/gitlab/config:/etc/gitlab \
       --volume /srv/gitlab/logs:/var/log/gitlab \
       --volume /srv/gitlab/data:/var/opt/gitlab \
       gitlab/gitlab-ce:latest
     ```
     This command does the following:
     - Publishes ports 443 (HTTPS), 80 (HTTP), and 22 (SSH) from the container to the EC2 instance.
     - Sets the container name to "gitlab".
     - Specifies the restart policy to "always" so that the container automatically starts on system boot.
     - Mounts three volumes for GitLab configuration, logs, and data storage, respectively. Adjust the paths (`/srv/gitlab/`) according to your preference.

6. Wait for the GitLab container to start and access its web interface:
   - After running the Docker command, wait for a few minutes to allow GitLab to initialize and start.
   - Once the container is running, you can access the GitLab web interface using the EC2 instance's public IP or DNS name in a web browser.
   - Open your browser and enter `http://<EC2-instance-public-IP>` or `http://<EC2-instance-DNS-name>`.
   - GitLab's setup page should appear, and you can follow the on-screen instructions to configure GitLab, set up the initial admin account, and complete the installation.

That's it! You have now set up a GitLab server on an EC2 instance using a Docker image. You can access and use GitLab for your version control needs through the web interface or SSH.

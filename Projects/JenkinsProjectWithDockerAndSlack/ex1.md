```markdown
# Install Jenkins with Docker

## 1. Install Docker:
To install and configure Docker on Amazon Linux, you can follow these steps:

Update the package repository and packages:

```bash
sudo yum update -y
```

Install Docker dependencies:

```bash
sudo yum install -y docker
```

 Start the Docker service:

```bash
sudo service docker start
```

Enable Docker to start on boot:

```bash
sudo chkconfig docker on
```

Add the `ec2-user` to the `docker` group to allow running Docker commands without using `sudo`:

```bash
sudo usermod -a -G docker ec2-user
```


## 2. Pull Jenkins Docker Image:
```bash
sudo docker pull orchardup/jenkins
```

## 3. Create a `docker-compose.yml` File:
```yaml
version: '3'
services:
  jenkins:
    image: jenkins/jenkins:lts
    ports:
      - 8081:8080
    volumes:
      - jenkins_home:/var/jenkins_home
    restart: always
    networks:
      - jenkins_network

networks:
  jenkins_network:

volumes:
  jenkins_home:
```

## 4. Start the Jenkins Container:
```bash
sudo docker-compose up -d
```

## 5. Unlock Jenkins:
On the initial setup page, you will be prompted to enter an administrator password. This password is stored on the Jenkins server and can be found in the file system. Use the following command to access the password:
```bash
sudo docker exec -it <CONTAINER_ID> cat /var/jenkins_home/secrets/initialAdminPassword
```

## 6. Copy the Password and Paste it into the Jenkins Web Interface:
Use the password obtained from the previous step to unlock Jenkins.

## 7. Customize Jenkins:
Next, you can choose to install suggested plugins or select specific plugins based on your requirements. This step may take some time as Jenkins downloads and installs the selected plugins.

## 8. Create an Admin User:
After the plugin installation, you'll be prompted to set up an admin user account. Provide the required information, such as username, password, full name, and email address.

## 9. Save and Finish:
Once the admin user is created, click on the "Save and Finish" button to complete the setup.

## 10. Jenkins is Ready:
After the setup is completed, you'll see the Jenkins dashboard. From here, you can start creating projects, managing plugins, and configuring Jenkins according to your needs.

## Configuring Jenkins Agents with Docker

### Create a Jenkins SSH Credential
1. Go to your Jenkins dashboard.
2. Click on "Manage Jenkins" in the main menu and then click on the "Manage Credentials" button.
3. Select "Add Credentials" from the global item drop-down.
4. Fill in the form as follows:
   - Kind: SSH Username with private key
   - ID: jenkins
   - Description: The Jenkins SSH key
   - Username: jenkins
   - Private Key: Select "Enter directly" and paste the content of your private key file .pem
   - Passphrase: Fill your passphrase used to generate the SSH key pair (leave empty if you didn’t use one at the previous step)
5. Press the "Create" button.

### Setting up the agent1 on Jenkins
1. Go to your Jenkins dashboard.
2. Click on "Manage Jenkins" in the main menu.
3. Go to "Manage Nodes and clouds" in the side menu.
4. Click on "New Node" in the side menu.
5. Fill in the Node/agent name and select the type (e.g., Name: agent1, Type: Permanent Agent).
6. Fill in the fields:
   - Remote root directory (e.g., `/home/jenkins`)
   - Label (e.g., `agent1`)
   - Usage (e.g., `only build jobs with label expression…`)
   - Launch method (e.g., `Launch agents by SSH`)
   - Host (e.g., `localhost` or your IP address)
   - Credentials (e.g., `jenkins`)
   - Host Key verification Strategy (e.g., `Manually trusted key verification`)
7. Press the "Save" button, and the agent1 will be registered but offline for the time being. Click on it.

You should now see "This node is being launched." If that’s not the case, you can press the "Relaunch agent" button and wait a few seconds. You can now click on the "Log" button on the left, and you should receive the message: "Agent successfully connected and online" on the last log line.

### Delegating the first job to agent1
1. Go to your Jenkins dashboard.
2. Select "New Item" in the side menu.
3. Enter a name (e.g., "First Job to Agent1").
4. Select the "Freestyle project" and press "OK."
5. Check the option: "Restrict where this project can be run."
6. Fill the field: "label" with the agent1 label (e.g., `agent1`).
7. Now, select the option "Execute shell" in the Build section.
8. Add the command `echo $NODE_NAME` in the Command field of the "Execute shell" step, and the name of the agent will be printed inside the log when this job is run.
9. Press the "Save" button and then select the option "Build Now."
10. Wait a few seconds, and then go to the "Console Output" page. You should receive output similar to:
```
Started by user Admin User
Running as SYSTEM
Building remotely on agent1 in workspace /home/jenkins/workspace/First Job to Agent1
[First Job to Agent1] $ /bin/sh -xe /tmp/jenkins15623311211559049312.sh
+ echo $NODE_NAME
agent1
Finished: SUCCESS
```
```

Note: Please make sure to replace `<CONTAINER_ID>` with the actual ID of the Jenkins container. Also, update the file paths and settings as per your system configuration.

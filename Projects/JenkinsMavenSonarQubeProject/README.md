# Installing SonarQube on Ubuntu EC2 Instance

We'll be installing SonarQube inside Docker and using Docker Compose to spin up the SonarQube instance inside our Ubuntu instance.

## Table of Contents
- [Install Docker](#install-docker)
- [Install Docker Compose](#install-docker-compose)
- [Install SonarQube](#install-sonarqube)
- [Accessing SonarQube Dashboard](#accessing-sonarqube-dashboard)
- [Default Credentials](#default-credentials)

## Install Docker
Paste the below commands in your Ubuntu instance after connecting with it:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo usermod -aG docker ubuntu
sudo systemctl status docker
```
Press `CTRL+C` or `CTRL+Z` to exit from the above command.

## Install Docker Compose
Continue from the previous step and run these commands:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

## Install SonarQube
Run the following commands to install SonarQube:

```bash
sudo sysctl -w vm.max_map_count=262144
mkdir sonar
wget https://raw.githubusercontent.com/awstechguide/devops/master/docker-compose.yml
sudo su
cd sonar
docker-compose up
```

Once all the above commands are executed, SonarQube will be successfully installed and running.

## Accessing SonarQube Dashboard
SonarQube runs on Port 9000. To connect to the SonarQube Dashboard, use the public IP address of the Ubuntu instance with port 9000 at the end.

For example:
```
http://your-ec2-instance-public-ip:9000
```

## Default Credentials
The default credentials for SonarQube will be as follows:

- Username: admin
- Password: admin

Note: It is essential to change the default password for security reasons after logging in to SonarQube.




# Cloning and Pushing Java Project to GitLab

This guide will walk you through the steps to clone an open-source Java project (Calculator) from a GitHub repository and push the source code to a GitLab repository. Before proceeding, make sure you have Git installed on your system.

## Table of Contents
- [Clone the Java Project](#clone-the-java-project)
- [Push Source Code to GitLab](#push-source-code-to-gitlab)

## Clone the Java Project
To clone the open-source Java project (Calculator) from the provided GitHub repository, follow these steps:

1. Open a terminal or command prompt on your local machine.
2. Navigate to the directory where you want to clone the project. For example, if you want to clone it into a folder called "projects," use the following command to change to that directory:
   ```bash
   cd /path/to/projects
   ```
3. Clone the GitHub repository using the `git clone` command. The repository URL for the Calculator project is:
   ```bash
   git clone https://github.com/HouariZegai/Calculator.git
   ```
4. Wait for the cloning process to complete. The repository will be downloaded to your local machine in a folder named "Calculator."

## Push Source Code to GitLab
Before pushing the source code to your GitLab server, ensure you have access to the server and have the necessary permissions to create and push to repositories.

1. Create a new repository on your GitLab server. Log in to your GitLab account, navigate to the project's section, click on the "New Project" button, and follow the prompts to create a new empty repository.

2. In your terminal or command prompt, navigate to the "Calculator" project directory that you cloned in the previous step.

3. Add your GitLab repository as a remote origin. Replace `<your-gitlab-repo-url>` with the URL of your GitLab repository. You can find this URL on the GitLab project page under the "Clone" dropdown.
   ```bash
   git remote add origin <your-gitlab-repo-url>
   ```

4. Commit your changes. It's a good practice to create a new branch for your changes.
   ```bash
   git checkout -b feature-branch
   git add .
   git commit -m "Initial commit"
   ```

5. Push the code to the remote GitLab repository using the branch you created in the previous step.
   ```bash
   git push -u origin feature-branch
   ```

   Depending on your GitLab server's configuration, you might be prompted to enter your GitLab credentials (username and password) during the push process.

   If the current user does not have write permissions, you can try changing the ownership of the `.git` directory to the current user. Replace `<your-username>` with your actual username:
   ```bash


   sudo chown -R <your-username>:<your-username> .git
   ```
   This command changes the ownership of the `.git` directory and all its contents recursively to the specified user.

   After adjusting the permissions, try the `git push` command again:
   ```bash
   git push -u origin feature-branch
   ```

Now, the source code from the "Calculator" project is pushed to your GitLab repository under the branch "feature-branch" (you can choose any other branch name you prefer). You can continue with the next steps in the Jenkins pipeline to build, test, and analyze the Java application using SonarQube.



# Creating API Token and Configuring Jenkins Pipeline

This guide explains how to create an API token for your GitLab project and configure a Jenkins pipeline job to fetch code from the repository using the token.

## Table of Contents
- [Create an API Token](#create-an-api-token)
- [Create a New Jenkins Pipeline Job](#create-a-new-jenkins-pipeline-job)
- [Configure Jenkins Pipeline](#configure-jenkins-pipeline)

## Create an API Token
Follow these steps to create an API token for your GitLab project:

1. Go to the GitLab project's Access Tokens page.

2. Click on "Create a personal access token" to generate a new API token.

3. Provide a name for the token and select the desired expiration date.

4. Choose the scopes (permissions) for the token based on your needs. Be cautious about granting unnecessary permissions for security reasons.

5. Click on the "Create personal access token" button to generate the API token.

6. After the token is generated, copy and save it in a secure place. This is the only time you'll be able to see it, and losing the token will require generating a new one.

## Create a New Jenkins Pipeline Job
From the Jenkins dashboard:

1. Click on "New Item" to create a new pipeline job.

2. Enter a name for the job, choose "Pipeline," and click "OK."

## Configure Jenkins Pipeline
In the pipeline configuration, define the steps for the pipeline:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Fetch Code') {
            steps {
                // Clone the GitLab repository
                echo 'Fetching source code from GitLab...'
                git branch: 'feature-branch', credentialsId: 'Calculator', url: 'http://172.31.33.251/RoyBidani/calculator.git'
            }
        }
    }
}
```

In the pipeline configuration, replace the following placeholders:

- `feature-branch`: Replace this with the name of the branch you want to fetch code from.
- `Calculator`: Replace this with the ID of the credentials that store the API token. (To add credentials, go to Jenkins > Manage Jenkins > Manage Credentials)
- `http://172.31.33.251/RoyBidani/calculator.git`: Replace this with the URL of your GitLab repository.

This pipeline configuration will fetch the source code from the specified branch of the GitLab repository using the provided API token. You can continue to add more stages and steps to build, test, and deploy your project as needed.



# Using Maven for Build in Jenkins Pipeline

This guide explains how to use Maven to build a Java application in a Jenkins pipeline. We will also provide instructions on how to install Maven on the Jenkins slave (Amazon Linux) and modify the pipeline to include the Maven build stage.

## Table of Contents
- [Install Maven on Jenkins Slave](#install-maven-on-jenkins-slave)
- [Modify Jenkins Pipeline](#modify-jenkins-pipeline)

## Install Maven on Jenkins Slave
To install Maven on the Jenkins slave (Amazon Linux), follow these steps:

1. Connect to your Jenkins slave (Amazon Linux) using SSH.

2. Install Maven using the YUM package manager:
   ```bash
   sudo yum install maven -y
   ```

3. Verify the Maven installation by checking the version:
   ```bash
   mvn -version
   ```
   
   

   This command will display the installed Maven version along with other details.

## Modify Jenkins Pipeline
To include the Maven build stage in your Jenkins pipeline, modify the pipeline configuration as follows:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Fetch Code') {
            steps {
                // Clone the GitLab repository
                echo 'Fetching source code from GitLab...'
                git branch: 'feature-branch', credentialsId: 'Calculator', url: 'http://172.31.33.251/RoyBidani/calculator.git'
            }
        }
        stage('Build with Maven') {
            steps {
                // Build the Java application using Maven
                sh 'mvn clean package'
            }
        }
    }
}
```

In the modified pipeline configuration:

1. The `Fetch Code` stage remains unchanged and continues to fetch the source code from the specified branch of the GitLab repository using the provided API token.

2. A new stage `Build with Maven` is added. This stage uses the `sh` step to execute the Maven build command `mvn clean package`.

   Note: Ensure that the Jenkins slave has sufficient

 permissions to access the Maven repositories and download dependencies during the build process.

With these modifications, your Jenkins pipeline will now fetch the source code from GitLab and build the Java application using Maven. You can continue to add more stages and steps to test, package, and deploy your project as needed.



# Adding Testing Stage Using SonarQube to Jenkins Pipeline

To include a testing stage using SonarQube in your Jenkins pipeline, follow the steps below:

## Table of Contents
- [Install and Configure Jenkins](#install-and-configure-jenkins)
- [Install SonarQube Plugin](#install-sonarqube-plugin)
- [Generate SonarQube Token](#generate-sonarqube-token)
- [Configure SonarQube Server in Jenkins](#configure-sonarqube-server-in-jenkins)
- [Create Jenkins Pipeline](#create-jenkins-pipeline)
- [Add SonarQube Scanner Step](#add-sonarqube-scanner-step)
- [Run the Jenkins Pipeline](#run-the-jenkins-pipeline)
- [View SonarQube Reports](#view-sonarqube-reports)

## 1. Install and Configure Jenkins
Set up Jenkins on your local machine or on another EC2 instance if you don't have it installed already. You can follow the official Jenkins installation guide for this.

## 2. Install SonarQube Plugin
In Jenkins, go to "Manage Jenkins" > "Manage Plugins" > "Available" and search for "SonarQube Scanner." Install the plugin and restart Jenkins if prompted.

## 3. Generate SonarQube Token
To enable your pipeline to push code analysis results to SonarQube, you'll need to generate a SonarQube token. This token will act as the authentication mechanism between your CI/CD pipeline and SonarQube. Log in to your SonarQube server, go to "My Profile" > "Security" > "Generate Tokens," and create a new token with the required permissions.

## 4. Configure SonarQube Server in Jenkins
After installing the SonarQube Scanner plugin, navigate to "Manage Jenkins" > "Configure System." Scroll down to the "SonarQube servers" section and click on "Add SonarQube." Provide the necessary details, including the name, server URL, and SonarQube authentication token (generated in SonarQube).

## 5. Create Jenkins Pipeline
In Jenkins, go to "New Item" and create a "Pipeline" project. In the pipeline configuration, specify your version control system and other relevant settings.

## 6. Add SonarQube Scanner Step
In your Jenkinsfile (or scripted pipeline), add a stage for testing using SonarQube. Here's an example that includes the SonarQube scanning step:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // Your build steps go here
            }
        }
        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('MySonarQubeServer') {
                    sh 'mvn sonar:sonar'
                }
            }
        }
    }
}
```

In the above example, the `mvn sonar:sonar` command is used for scanning a Maven project. Adjust the command based on the build tool you are using.

after it we need to create a web hook.
in the sonar server create a web hook with the jenkin url and then add the next stage:

```groovy
        stage("Quality gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') { // Set a reasonable timeout duration
                waitForQualityGate abortPipeline: true
        }
    }
}
```

## 7. Run the Jenkins Pipeline
Save the Jenkinsfile and trigger the pipeline by clicking "Build Now." Jenkins will start the pipeline, which includes the SonarQube scan stage.

## 8. View SonarQube Reports
After the SonarQube scan completes, you can view the analysis results and code quality reports in your SonarQube server's dashboard.

Remember to adjust the pipeline and SonarQube configuration according to your specific project setup, such as adding environment variables, setting up build tools, etc.

**Note:** Make sure your Jenkins server and SonarQube server are properly configured to communicate with each other, and the required security settings are in place to protect sensitive information.


# Publishing Artifacts to Artifactory from Jenkins Pipeline

To publish artifacts to Artifactory from a Jenkins pipeline, follow these step-by-step instructions:

## Table of Contents
- [Step 1: Set up Artifactory Server in Jenkins](#step-1-set-up-artifactory-server-in-jenkins)
- [Step 2: Configure Jenkins Pipeline](#step-2-configure-jenkins-pipeline)
- [Step 3: Add Artifactory Publish Step](#step-3-add-artifactory-publish-step)
- [Step 4: Save and Run Pipeline](#step-4-save-and-run-pipeline)

### Step 1: Set up Artifactory Server in Jenkins
1. Open Jenkins and navigate to "Manage Jenkins" > "Configure System."
2. Scroll down to the "Artifactory" section.
3. Click on "Add Artifactory Server."
4. Fill in the details of your Artifactory server, including the URL, username, and password.
5. Click on "Test Connection" to ensure Jenkins can connect to the Artifactory server successfully.
6. Save the Artifactory configuration.

### Step 2: Configure Jenkins Pipeline
1. Open the Jenkinsfile for your pipeline or create a new one. Make sure it is set up correctly with stages for building your project.

### Step 3: Add Artifactory Publish Step
1. Inside your Jenkins pipeline, add a stage to publish the artifacts to Artifactory. Typically, this stage should come after the build stage.

```groovy
stage('Publish to Artifactory') {
    steps {
        script {
            def server = Artifactory.server 'Artifactory'
            def uploadSpec = """{
                "files": [
                    {
                        "pattern": "target/*.jar",
                        "target": "Calculator/"
                    }
                ]
            }"""
            server.upload uploadSpec
        }
    }
}
```

### Step 4: Save and Run Pipeline
1. Save the Jenkinsfile.
2. Trigger the pipeline to run either manually or through a webhook or schedule.

When the pipeline runs, it will build your project and then publish the artifacts (e.g., JAR files) to the specified repositories in Artifactory.

Make sure that your Jenkins pipeline has the necessary credentials and permissions to publish to Artifactory.



# Configuring Jenkins to Send Email with Pipeline Status

To configure Jenkins to send an email with the pipeline status using the built-in "E-mail Notification" feature, follow these steps:

## Table of Contents
- [Step 1: Configure Jenkins System](#step-1-configure-jenkins-system)
- [Step 2: Configure Email Password](#step-2-configure-email-password)
- [Step 3: E-mail Notification Settings](#step-3-e-mail-notification-settings)
- [Step 4: Test Configuration](#step-4-test-configuration)
- [Step 5: Configure Pipeline to Send Email](#step-5-configure-pipeline-to-send-email)
- [Step 6: Save and Apply Configuration](#step-6-save-and-apply-configuration)

### Step 1: Configure Jenkins System
1. Navigate to "Manage Jenkins" > "Configure System" from the Jenkins dashboard.

### Step 2: Configure Email Password
1. Go to Gmail or your email provider and manage your account settings.
2. In the security section, enable two-step authentication.
3. Scroll down to "Passwords to app" and generate a new password for Jenkins to use for email authentication. Save this password; it's important for later steps.

### Step 3: E-mail Notification Settings
1. In the "Configure System" page of Jenkins, scroll down to the "E-mail Notification" section.
2. Provide the following information:
   - **SMTP server**: The address of your SMTP server (e.g., smtp.gmail.com).
   - **Default user e-mail suffix**: Keep this blank.
   - **Use SMTP Authentication**: Check this option if your SMTP server requires authentication.
   - **User Name**: If using SMTP authentication, provide the username for your SMTP server.
   - **Password**: If using SMTP authentication, provide the password generated in Step 2.

3. Click "Advanced..." to expand more options:
   - **Use SSL**: Check this option if your SMTP server requires an SSL connection.
   - **Charset**: The character set for the email. Use UTF-8.

### Step 4: Test Configuration
1. Click on "Test Configuration" to verify that Jenkins can successfully connect to your SMTP server using the provided settings. You should receive a test email to the email address specified in the "System Admin e-mail address" field.

### Step 5: Configure Pipeline to Send Email
1. In your pipeline script, add the following code to send an email based on the pipeline status:

```groovy
post {
    success {
        script {
            def buildNumber = env.BUILD_NUMBER
            def buildUrl = env.BUILD_URL
            def commit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
            def branch = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()

            mail to: 'your-email@example.com',
                 subject: "Success pipeline - Build #${buildNumber}",
                 body: "The pipeline was successful.\n\n" +
                       "Build Number: ${buildNumber}\n" +
                       "Build URL: ${buildUrl}\n" +
                       "Git Commit: ${commit}\n" +
                       "Git Branch: ${branch}\n"
        }
    }
    failure {
        script {
            def buildNumber = env.BUILD_NUMBER
            def buildUrl = env.BUILD_URL
            def commit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
            def branch = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()

            mail to: 'your-email@example.com',
                 subject: "Failed pipeline - Build #${buildNumber}",
                 body: "The pipeline has failed.\n\n" +
                       "Build Number: ${buildNumber}\n" +
                       "Build URL: ${buildUrl}\n" +
                       "Git Commit: ${commit}\n" +
                       "Git Branch: ${branch}\n"
        }
    }
}
```

### Step 6: Save and Apply Configuration
1. After configuring the pipeline, save the changes in the Jenkinsfile and run the pipeline to trigger the email notification.

Now, whenever the pipeline runs, Jenkins will send an email to the specified email address with the status of the pipeline (e.g., Success, Failure, Unstable) along with a link to the Jenkins build page. Make sure that your Jenkins pipeline has the necessary credentials and permissions to send emails.


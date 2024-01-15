# Configuring Jenkins Pipeline to Build Docker Image, SonarQube Tests, and Upload to Artifactory

To configure Jenkins to automate building a Docker image, running SonarQube tests, and uploading the .jar file to Artifactory, follow these steps:

## Table of Contents
- [Step 1: Create a Dockerfile](#step-1-create-a-dockerfile)
- [Step 2: Configure Jenkins Pipeline](#step-2-configure-jenkins-pipeline)
- [Step 3: Edit the pom.xml File](#step-3-edit-the-pomxml-file)

### Step 1: Create a Dockerfile

Create a Dockerfile with the stages: a build stage using Maven and a SonarQube testing stage. The Dockerfile should look like this:

```Dockerfile
# Stage 1: Build stage using Maven
FROM maven:3.8.4-jdk-11 AS build

# Set the working directory to /app
WORKDIR /app

# Copy the pom.xml file to the container
COPY pom.xml .

# Resolve Maven dependencies and cache them for faster builds
RUN mvn dependency:go-offline

# Copy the entire project source code to the container
COPY . .

# Run SonarQube analysis on the code
RUN mvn sonar:sonar \
    -Dsonar.projectKey=com.houari:Calculator \
    -Dsonar.host.url=http://172.31.27.246:9000/ \
    -Dsonar.login=sqa_7b12bf33a113276c85ba69626c9194265bfae05e

# Build the executable JAR file
RUN mvn package

# Stage 2: Final stage using OpenJDK
FROM openjdk:11-jre-slim

# Set the working directory to /app
WORKDIR /app

# Copy the built JAR file from the build stage to the final container
COPY --from=build /app/target/Calculator-1.0-SNAPSHOT.jar .

# Set the command to run the application when the container starts
CMD ["java", "-jar", "Calculator-1.0-SNAPSHOT.jar"]
```

### Step 2: Configure Jenkins Pipeline

Create a Jenkins pipeline script to fetch files from the GitLab server, build the Docker image, convert it to a .jar file, and then upload the .jar file to Artifactory. The pipeline script should look like this:

```groovy
import org.jfrog.hudson.pipeline.common.types.ArtifactoryServer

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
        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                sh 'docker build -t calculator-1.0-snapshot .'
                // Convert the Docker image to .jar file
                sh 'docker save calculator-1.0-snapshot > calculator-1.0-snapshot.jar'
            }
        }
        stage('Publish Docker Image to Artifactory') {
            steps {
                script {
                    def server = Artifactory.server 'Artifactory'
                    def dockerImageName = 'calculator-1.0-snapshot'
                    def targetRepo = 'Calculator' 

                    def buildInfo = server.upload spec: """{
                        "files": [
                            {
                                "pattern": "target/*.jar",
                                "target": "Calculator/"
                            },
                            {
                                "pattern": "calculator-1.0-snapshot.jar",
                                "target": "Calculator/calculator-1.0-snapshot.jar"
                            }
                        ]
                    }"""
                    server.publishBuildInfo buildInfo
                }
            }
        }
        stage("Clean") {
            steps {
                deleteDir()
                // Remove <none> images
                sh 'docker rmi $(docker images -f "dangling=true" -q) || true'

                // Stop and remove all containers
                sh 'docker stop $(docker ps -a -q) || true'
                sh 'docker rm $(docker ps -a -q) || true'
            }
        }
    } 
    
    post {
        success {
            // Send email notification for successful pipeline
            mail to: 'your-email@example.com',
                 subject: "Success pipeline - Build #${env.BUILD_NUMBER}",
                 body: "The pipeline was successful.\n\n" +
                       "Build Number: ${env.BUILD_NUMBER}\n" +
                       "Build URL: ${env.BUILD_URL}\n"
        }
        failure {
            // Send email notification for failed pipeline
            mail to: 'your-email@example.com',
                 subject: "Failed pipeline - Build #${env.BUILD_NUMBER}",
                 body: "The pipeline has failed.\n\n" +
                       "Build Number: ${env.BUILD_NUMBER}\n" +
                       "Build URL: ${env.BUILD_URL}\n"
        }
    }
}
```

### Step 3: Edit the pom.xml File

Edit the pom.xml file and add the following lines to specify the target and add the SonarQube plugin:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.houari</groupId>
    <artifactId>Calculator</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <jackson-dataformat-yaml.version>2.14.2</jackson-dataformat-yaml.version>
        <junit-j

upiter-params.version>5.9.2</junit-jupiter-params.version>
        <!-- Set SonarQube plugin version -->
        <sonar-maven-plugin.version>3.9.0.2155</sonar-maven-plugin.version>
        <sonar.java.binaries>/app/target/sonar</sonar.java.binaries>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.fasterxml.jackson.dataformat</groupId>
            <artifactId>jackson-dataformat-yaml</artifactId>
            <version>${jackson-dataformat-yaml.version}</version>
        </dependency>

        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-params</artifactId>
            <version>${junit-jupiter-params.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Add SonarQube plugin -->
            <plugin>
                <groupId>org.sonarsource.scanner.maven</groupId>
                <artifactId>sonar-maven-plugin</artifactId>
                <version>${sonar-maven-plugin.version}</version>
            </plugin>
        </plugins>
    </build>
</project>
```

With these steps, your Jenkins pipeline will fetch code from GitLab, build the Docker image, run SonarQube tests, upload the .jar file to Artifactory, and finally clean up unnecessary images and containers. Additionally, email notifications will be sent for both successful and failed pipeline runs.

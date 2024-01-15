# GitHub Actions CI/CD Pipeline for Docker Deployment

This guide walks you through setting up a GitHub Actions CI/CD pipeline for building a Docker container, pushing it to DockerHub, and deploying it to a target instance using SSH. Ensure you have the necessary prerequisites in place.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Fork the Repository](#step-1-fork-the-repository)
3. [Step 2: Set Up GitHub Actions](#step-2-set-up-github-actions)
4. [Step 3: Configure DockerHub Secrets](#step-3-configure-dockerhub-secrets)
5. [Step 4: Create DockerFile](#step-4-create-dockerfile-at-the-root-directory)
6. [Step 5: Deploy the Docker Image on Another Instance with SSH](#step-5-deploy-the-docker-image-on-another-instance-with-ssh)
7. [Step 6: Run the Deployment Script in GitHub Actions](#step-6-run-the-deployment-script-in-github-actions)

---

## Prerequisites

Before you start, make sure you have the following in place:

- A GitHub account.
- A DockerHub account or another container registry of your choice.
- Docker installed locally.
- Git installed locally.

---

## Step 1: Fork the Repository

1. Go to the GitHub repository you want to fork: [https://github.com/jenkins-docs/simple-java-maven-app](https://github.com/jenkins-docs/simple-java-maven-app)
2. Click the "Fork" button in the upper-right corner to fork the repository to your GitHub account.

---

## Step 2: Set Up GitHub Actions

1. Go to your forked repository on GitHub.
2. Click on the "Actions" tab.
3. Click the "Set up a workflow yourself" link.
4. Create a new YAML file in the `.github/workflows` directory of your repository, for example, `.github/workflows/docker-build.yml`.

Here's a sample `docker-build.yml` file:

```yaml
name: Build and Deploy Docker Image

on:
  push:
    branches:
      - master

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Set up Java
        uses: actions/setup-java@v2
        with:
          java-version: '11'
          distribution: 'temurin'
          server-id: github
          settings-path: ${{ github.workspace }}

      - name: Bump version
        id: bump
        uses: mickem/gh-action-bump-maven-version@v1

      - name: Build Docker Image
        run: |
          docker build -t roybidani/simple-java-maven-app:latest .
          docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }}
          docker push roybidani/simple-java-maven-app:latest
```

---

## Step 3: Configure DockerHub Secrets

1. Go to your GitHub repository.
2. Click on "Settings" > "Secrets" > "New repository secret."
3. Add two secrets: `DOCKER_USERNAME` (your DockerHub username) and `DOCKER_PASSWORD` (your DockerHub password or access token).
4. Make sure `GITHUB_TOKEN` has the right permissions. In your repo, go to settings -> actions on the left side bar -> general -> at Workflow permissions set the right permissions.

---

## Step 4: Create DockerFile at the Root Directory

Create a `Dockerfile` at the root directory of your project. Here's an example:

```dockerfile
# Use the official maven image as the build environment
FROM maven:3.8-jdk-11 as build

# Set the working directory in the image
WORKDIR /app

# Copy the pom.xml and source code to the container
COPY pom.xml .
COPY src ./src/

# Package the application
RUN mvn clean package

# Use the official openjdk image as the runtime environment
FROM openjdk:11-jre-slim

# Set the working directory in the image
WORKDIR /app

# Copy the jar file from the build stage to the current stage
COPY --from=build /app/target/*.jar app.jar

# Specify the command to run on container start
CMD ["java", "-jar", "app.jar"]
```

---

## Step 5: Deploy the Docker Image on Another Instance with SSH

To deploy the Docker image on another instance using SSH, ensure you have access to the target instance, Docker installed, and SSH access. Here are the steps:

1. **Prepare the Target Instance:**
   - Ensure Docker is installed and running on the target instance.
   - Configure SSH access and have the necessary credentials (private key) to connect to the instance.

2. **Create a Deployment Script:**
   - Create a 'scripts' directory.
   - Write a script to connect to the target instance via SSH.
   - Pull the Docker image from your container registry (e.g., DockerHub).
   - Run a Docker container using the pulled image. Use Docker Compose or a simple `docker run` command based on your application's requirements.

Here's an example of a simple deployment script (`deployment-script.sh`) to get you started:

```bash
#!/bin/bash
# Define Docker image details
DOCKER_IMAGE="roybidani/simple-java-maven-app:latest"
# Pull the latest Docker image
docker pull $DOCKER_IMAGE
# Stop and remove the existing container (if it exists)
docker stop simple-java-maven-app || true
docker rm simple-java-maven-app || true
# Run the Docker container
docker run -d --name simple-java-maven-app -p 80:8080 $DOCKER_IMAGE
```

---

## Step 6: Run the Deployment Script in GitHub Actions

Execute the deployment script as a step in your GitHub Actions workflow by adding another step in your YAML file. Here's an example of how to do this:

```yaml
      - name: Deploy to EC2
        env:
          PRIVATE_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
        run: |
          echo "$PRIVATE_KEY" > deploy_key.pem
          chmod 600 deploy_key.pem
          scp -i deploy_key.pem -o StrictHostKeyChecking=no ./scripts/deployment-script.sh ec2-user@35.180.61.1:/tmp/
          # Change permissions of the deployment script on the remote server
          ssh -i deploy_key.pem -o StrictHostKeyChecking=no ec2-user@35.180.61.1 "chmod +x /tmp/deployment-script.sh"
          ssh -i deploy_key.pem -o StrictHostKeyChecking=no ec2-user@35.180.61.1 "/tmp/deployment-script.sh"
          rm -f deploy_key.pem
```

- Pass the private key secret as an environment variable for secure authentication with the target instance.
- Copy and execute the script on the remote server.

Make sure to replace `YOUR_PRIVATE_KEY_SECRET` with the name of the secret in your GitHub repository containing the SSH private key.

With these steps in place, your CI/CD pipeline will build the Docker image, push it to DockerHub, and then deploy it to your target instance using SSH as part of your GitHub Actions workflow.

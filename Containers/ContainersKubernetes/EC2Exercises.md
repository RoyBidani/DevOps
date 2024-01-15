
# Setting Up Docker and Kubernetes on AWS EC2

## Table of Contents

1. [Install Docker on EC2](#install-docker-on-ec2)
2. [Exercise 1: Install minikube and kubectl](#exercise-1-install-minikube-and-kubectl-locally)
3. [Exercise 2: Create a deployment](#exercise-2-create-a-deployment)
4. [Exercise 3: Display the created deployment](#exercise-3-display-the-created-deployment)
5. [Exercise 4: Display existing pods](#exercise-4-display-existing-pods)
6. [Exercise 5: Expose the application](#exercise-5-expose-the-application)
7. [Exercise 6: Connect to the service through the browser](#exercise-6-connect-to-the-service-through-the-browser)
8. [Exercise 7: Open the minikube dashboard](#exercise-7-open-the-minikube-dashboard)
9. [Exercise 8: Delete the 'test' service](#exercise-8-delete-the-test-service)
10. [Exercise 9: Deploy Python weather application using YAML](#exercise-9-deploy-your-python-weather-application-using-a-yaml-object-configuration-file)
11. [Exercise 10: Delete one of the pods](#exercise-10-delete-one-of-the-pods)
12. [Exercise 11: Manually scale your application](#exercise-11-manually-scale-your-application-to-three-replica-sets)
13. [Exercise 12: Display information about the service](#exercise-12-display-information-about-the-service)

---

## Install Docker on EC2

To follow the exercises below, ensure Docker is installed on your EC2 instance:

1. **Update Package Information:**
   Run the following command to update the package information on your instance:

   ```sh
   sudo yum update -y
   ```

2. **Install Docker:**
   Install Docker using the `yum` package manager:

   ```sh
   sudo yum install docker -y
   ```

3. **Start and Enable Docker:**
   After the installation is complete, start the Docker service and enable it to start on boot:

   ```sh
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

4. **Add User to Docker Group (Optional):**
   If you want to run Docker commands without using `sudo`, you can add your user to the `docker` group:

   ```sh
   sudo usermod -aG docker ec2-user
   ```

   Remember to log out and log back in for the group changes to take effect.

5. **Verify Docker Installation:**
   Check that Docker is running and accessible by running:

   ```sh
   docker --version
   ```

6. **Logout:**
   After completing installation and verification, log out of the EC2 instance:

   ```sh
   exit
   ```

Docker should now be installed and running on your Amazon Linux EC2 instance.

## Exercise 1: Install minikube and kubectl locally

Follow these steps to set up minikube and kubectl on your EC2 instance:

1. Open a terminal on your AWS EC2 instance.
2. Install necessary packages and dependencies:

```bash
sudo yum update -y
sudo yum install curl conntrack-tools -y
```

3. Install kubectl:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

4. Install minikube:

```bash
curl -LO "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube version
```

## Exercise 2: Create a deployment

1. Start minikube cluster:

```bash
minikube start
```

2. Create a deployment for a web application pod (nginx image):

```bash
kubectl create deployment test --image=roybidani/weather_app:app
```

## Exercise 3: Display the created deployment

```bash
kubectl get deployments
```

## Exercise 4: Display existing pods

```bash
kubectl get pods
```

## Exercise 5: Expose the application

```bash
kubectl expose deployment test --type=NodePort --port=8000
```

## Exercise 6: Connect to the service through the browser

To access the service from your local machine, find the external IP and port:

```bash
minikube service test --url
```

Copy the URL and paste it into your browser's address bar.

## Exercise 7: Open the minikube dashboard

```bash
minikube dashboard
```

## Exercise 8: Delete the 'test' service

```bash
kubectl delete service test
```


## Exercise 9: Deploy your Python weather application using a YAML object configuration file

1. Create a YAML file named `weather-app.yaml`.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: weather-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: weather-app
  template:
    metadata:
      labels:
        app: weather-app
    spec:
      containers:
      - name: web
        image: your-image-name:tag

---
apiVersion: v1
kind: Service
metadata:
  name: weather-app-service
spec:
  type: NodePort
  selector:
    app: weather-app
  ports:
    - port: 8000
      targetPort: 8000

```

2. Apply the configuration:

```bash
kubectl apply -f weather-app.yaml
```


## Exercise 10: Delete one of the pods

```bash
kubectl delete pod <pod-name>
```

## Exercise 11: Manually scale your application to three replica sets

```bash
kubectl scale deployment weather-app --replicas=3
```

## Exercise 12: Display information about the service

```bash
kubectl get service weather-app-service
```

These exercises cover setting up Docker, minikube, kubectl, deploying applications, and managing pods on your AWS EC2 instance.

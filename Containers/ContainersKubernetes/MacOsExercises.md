Certainly! Here's the content formatted as a `README.md` with a table of contents and improved wording:

# Kubernetes Exercises: Setting Up and Deploying Applications

## Table of Contents

1. [Exercise 1: Install minikube and kubectl locally](#exercise-1-install-minikube-and-kubectl-locally)
2. [Exercise 2: Create a deployment for a web application](#exercise-2-create-a-deployment-for-a-web-application)
3. [Exercise 3: Display the created deployment](#exercise-3-display-the-created-deployment)
4. [Exercise 4: Display existing pods](#exercise-4-display-existing-pods)
5. [Exercise 5: Expose your application](#exercise-5-expose-your-application)
6. [Exercise 6: Connect to the service through the browser](#exercise-6-connect-to-the-service-through-the-browser)
7. [Exercise 7: Open the minikube dashboard](#exercise-7-open-the-minikube-dashboard)
8. [Exercise 8: Delete the 'test' service](#exercise-8-delete-the-test-service)
9. [Exercise 9: Deploy your Python weather application](#exercise-9-deploy-your-python-weather-application)
10. [Exercise 10: Delete one of the pods](#exercise-10-delete-one-of-the-pods)
11. [Exercise 11: Manually scale your application](#exercise-11-manually-scale-your-application)
12. [Exercise 12: Display information about the service](#exercise-12-display-information-about-the-service)

---

## Exercise 1: Install minikube and kubectl locally

1. Open Terminal on your MacBook Pro.
2. Install Homebrew (if not already installed):

   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. Install Minikube and kubectl using Homebrew:

   ```sh
   brew install minikube kubectl
   ```

## Exercise 2: Create a deployment for a web application

1. Open Terminal.
2. Start Minikube (this might take a while):

   ```sh
   minikube start --driver=docker
   ```

3. Create a deployment named 'test' using kubectl (replace `your-image` with the actual container image):

   ```sh
   kubectl create deployment test --image=your-image
   ```

## Exercise 3: Display the created deployment

1. Display the deployment using kubectl:

   ```sh
   kubectl get deployment test
   ```

## Exercise 4: Display existing pods

1. Display the pods using kubectl:

   ```sh
   kubectl get pods
   ```

## Exercise 5: Expose your application

1. Expose the deployment as a NodePort service:

   ```sh
   kubectl expose deployment test --type=NodePort --port=8000
   ```

## Exercise 6: Connect to the service through the browser

1. Get the NodePort using kubectl:

   ```sh
   minikube service test
   ```

2. It will open the browser on the service.

## Exercise 7: Open the minikube dashboard

1. Open the Minikube dashboard using kubectl:

   ```sh
   minikube dashboard
   ```

## Exercise 8: Delete the 'test' service

1. Delete the service using kubectl:

   ```sh
   kubectl delete svc test
   ```

## Exercise 9: Deploy your Python weather application

1. Create a YAML file named `weather-app.yaml` with the provided content.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: weather-app
spec:
  type: NodePort
  selector:
    app: weather-app
  ports:
    - protocol: TCP
      port: 8000        # Corrected to port 8000
      targetPort: 8000

---
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
        - name: weather-app-container
          image: your-weather-app-image
          ports:
            - containerPort: 80
```

2. Apply the configuration:

   ```sh
   kubectl apply -f weather-app.yaml
   ```

## Exercise 10: Delete one of the pods

1. Delete one of the pods:

   ```sh
   kubectl get pods
   kubectl delete pod <pod-name>
   ```

   Kubernetes will automatically create a new pod to maintain the desired replica count.

## Exercise 11: Manually scale your application

1. Scale your deployment to three replicas:

   ```sh
   kubectl scale deployment weather-app --replicas=3
   ```

## Exercise 12: Display information about the service

1. Display information about the service using kubectl:

   ```sh
   kubectl describe svc weather-app
   ```

These exercises cover setting up Minikube, deploying applications, and managing pods using kubectl on your local environment.

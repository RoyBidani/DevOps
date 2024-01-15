### Part 1: Setting Up a Kubernetes Cluster and Jenkins master and agent:

**Terraform configuration to create a Jenkins master instance, a Jenkins agent instance, and three EC2 instances for Kubernetes cluster:**


```hcl
# Define the provider and AWS configuration
provider "aws" {
  region = "eu-west-3"  # Replace with your desired AWS region
}

# Create a security group for Jenkins instances with necessary ports open
resource "aws_security_group" "jenkins_security_group" {
  name_prefix = "jenkins-sg-"
  
  # Allow all trafic access for administrative purposes
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Add more ingress rules as needed
  
  # Allow all outbound traffic (from the instances to anywhere)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an EC2 instance for Jenkins master
resource "aws_instance" "jenkins_master_instance" {
  ami           = "ami-008bcc0a51a849165"  # Ubuntu 20.04 LTS (adjust to your region)
  instance_type = "t3a.medium"               # Adjust instance type as needed
  key_name      = "myKey"                 # Replace with your SSH key pair
  security_groups = [aws_security_group.jenkins_security_group.name]

  tags = {
    Name = "master-jenkins"  # Name tag for the Jenkins master instance
  }
}

# Create an EC2 instance for Jenkins agent
resource "aws_instance" "jenkins_agent_instance" {
  ami           = "ami-008bcc0a51a849165"  # Ubuntu 20.04 LTS (adjust to your region)
  instance_type = "t3a.medium"               # Adjust instance type as needed
  key_name      = "myKey"                 # Replace with your SSH key pair
  security_groups = [aws_security_group.jenkins_security_group.name]

  tags = {
    Name = "agent-jenkins"  # Name tag for the Jenkins agent instance
  }
}

# Create 2 EC2 instances for Kubernetes nodes
resource "aws_instance" "worker_instance" {
  count         = 2
  ami           = "ami-008bcc0a51a849165"  # Ubuntu 20.04 LTS (adjust to your region)
  instance_type = "t3a.medium"               # Adjust instance type as needed
  key_name      = "myKey"                 # Replace with your SSH key pair
  security_groups = [aws_security_group.jenkins_security_group.name]

  tags = {
    Name = "worker-${count.index + 1}"  # Name tag for the Jenkins nodes
  }
}

# Create master kubernetes
resource "aws_instance" "master_kubernetes_instance" {
  ami           = "ami-008bcc0a51a849165"  # Ubuntu 20.04 LTS (adjust to your region)
  instance_type = "t3a.medium"               # Adjust instance type as needed
  key_name      = "myKey"                 # Replace with your SSH key pair
  security_groups = [aws_security_group.jenkins_security_group.name]

  tags = {
    Name = "master_kubernetes"  # Name tag for the Jenkins nodes
  }
}

# Output the public IP addresses of the Jenkins instances
output "jenkins_master_public_ip" {
  value = aws_instance.jenkins_master_instance.public_ip
}

output "jenkins_agent_public_ip" {
  value = aws_instance.jenkins_agent_instance.public_ip
}

output "kubernetes_worker_instance_public_ips" {
  value = [for instance in aws_instance.worker_instance : instance.public_ip]
}

```

After saving this Terraform configuration to a `.tf` file, you can run the following commands to provision the infrastructure:

1. **Initialize Terraform:**

   ```bash
   terraform init
   ```

2. **Apply the configuration (provision resources):**

   ```bash
   terraform apply
   ```
### Part 2: Setting Up Jenkins master instance

**Install Jenkins with Docker**
in the EC2 instance:

   ```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
sudo docker pull orchardup/jenkins
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
   ```
              
**Create a docker-compose.yml File:**
```yml
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

**Start the Jenkins Container:**
```bash
sudo docker-compose up -d
```

### Part 3: set up Jenkins Agent with Java, Git, Docker and Jenkins Agent, and configure it to connect to your Jenkins Server:

**Update and Upgrade Packages**

Update the package list and upgrade the installed packages to their latest versions:

```bash
sudo apt update
sudo apt upgrade -y
```

**Install Docker**
```bash
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

**Install Java**

Install OpenJDK (Java Development Kit) 8, which is commonly used with Jenkins:

```bash
sudo apt install openjdk-8-jdk -y
```

**Install Git**

Install Git version control system:

```bash
sudo apt install git -y
```

**Install Jenkins Agent**

Jenkins Agent is typically called a "Jenkins Slave." To set up the Jenkins Slave (Agent), you'll need to obtain the agent.jar file from your Jenkins server. Follow these steps:
1. log in to the master instance

2. create a file named "jenkins-slave.pem" and paste the content of the key.pem

3. chmod 400 jenkins-slave.pem 
 
4. Log in to your Jenkins server via browser

5. Navigate to "Manage Jenkins" -> "Manage Nodes"

6. Click "New Node" to create a new Jenkins Slave.

7. Configure the Jenkins Slave with a name and choose the "Permanent Agent" option.

8. choose "Lunch agent by via ssh" and provide the key.pem and username

9. Click "Save" to create the agent.

10. On the agent configuration page,you see the logs eith the staus

Your Jenkins Agent should now be connected to your Jenkins server.



### Part 4: Set Up Kubernetes Cluster:

**Install Kubernetes Using kubeadm:**
   - SSH into the kubernetes nodes.
   - Install kubeadm, kubelet, and kubectl: 
```bash
sudo apt-get install -y apt-transport-https ca-certificates curl
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

**Initialize Kubernetes Master Node:**
   - On the master node, run `sudo kubeadm init`.
   - Follow the instructions to set up kubeconfig on your local machine.
   - and run it to gain access to the kubectl:
   ```bash
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ```

**Join Worker Nodes:**
   - On each worker node, run the `kubeadm join` command provided by the master node during initialization.



### Part 5: Jenkins Pipeline for Docker and Kubernetes


**Configure Jenkins Credentials**

1. In your Jenkins server, navigate to "Manage Jenkins" > "Manage Credentials."

2. Under "Stores scoped to Jenkins," click on "(global)."

3. Click on "Add Credentials" and add the following credentials:
   - Kind: Username with password
   - Scope: Global
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password
   - ID: docker-hub-creds

4. do the same with GitLab


***Create a New Jenkins Pipeline Job**

1. Log in to your Jenkins server.

2. Click on "New Item" to create a new pipeline job.

3. Provide a name for your job (e.g., "Docker-Build-Push-Pipeline") and select the "Pipeline" project type.

4. Scroll down to the "Pipeline" section and configure the following:

   - **Definition**: Choose "Pipeline script."

5. Save the job.


**Configure the Pipeline Script in Jenkins**

In this step, you'll configure the pipeline script directly in the Jenkins job configuration.

1. In your newly created Jenkins job configuration:

   - Scroll down to the "Pipeline" section.

   - In the "Script" text area, enter the following pipeline script:

```groovy
pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = credentials('docker-hub-creds')
    DOCKER_IMAGE_NAME = 'roybidani/weather_app:jenkins'
    KUBECONFIG_PATH = '/home/ubuntu/config' // Path to your kubeconfig file
  }
  stages {
      stage('Fetch Code') {
            steps {
                // Clone the GitLab repository
                echo 'Fetching source code from GitLab...'
                git branch: 'master', credentialsId: 'gitlab', url: 'https://gitlab.com/infinity1934640/weather'
            }
        }
    stage('Build') {
      steps {
        sh 'docker build -t $DOCKER_IMAGE_NAME .'
      }
    }
    stage('Login to Docker Hub') {
      steps {
        sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
      }
    }
    stage('Push to Docker Hub') {
      steps {
        sh "docker push $DOCKER_IMAGE_NAME"
      }
    }
    stage('Update Deployment.yml') {
      steps {
        script {
          // Replace the image name in deployment.yaml
          sh "sed -i 's#image: .*#image: $DOCKER_IMAGE_NAME#' deployment.yaml"
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        script {
          // Set the Kubernetes cluster context
          sh "kubectl --kubeconfig=$KUBECONFIG_PATH config use-context kubernetes-admin@kubernetes"
          // Deploy the updated deployment.yaml
          sh "kubectl --kubeconfig=$KUBECONFIG_PATH apply -f deployment.yaml"
        }
      }
    }
    stage('Deploy Ingress') {
      steps {
        script {
          // Apply the Ingress resource
          sh "kubectl --kubeconfig=$KUBECONFIG_PATH apply -f ingress.yaml"
        }
      }
    }
    stage('Clean Workspace') {
      steps {
        // Clean the working directory
        deleteDir()
      }
    }
  }
}


```
2. **Configure Docker Hub Credentials**

   In Jenkins, go to "Manage Jenkins" > "Manage Credentials" and add your Docker Hub credentials as "Username with password" credentials.

3. **Configure Kubernetes Credentials**
	
	**Locate kubeconfig File:**
   - On many systems, the default `kubeconfig` file is located at `~/.kube/config`.  copy its content to a file on the jenkins agent

	**Cluster Context Name:**
   - To find the name of the cluster context, you can use the `kubectl config get-contexts` command. Run the following command in master terminal:

     ```
     kubectl config get-contexts
     ```


**Make sure you have Deployment.yaml and ingress.yaml on the Git repository**

Deployment.yaml:
```yml
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
        image: roybidani/weather_app:latest
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: weather-app-service
spec:
  selector:
    app: weather-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000 # Adjust if your app listens on a different port

```

ingress.yaml:

```yml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: weather-app-ingress
spec:
  rules:
    - host: http://weather.io # Replace with your desired domain
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: weather-app-service
                port:
                  number: 80
                  
```

### Part 6: Jenkins Second Pipeline with Replicas

To create a Jenkins pipeline with a parameter for setting the number of replicas:

To use a parameter called `REPLICAS` to set the number of desired replicas in your Jenkins pipeline, you need to define and pass this parameter when triggering the pipeline job. Here's how you can modify your Jenkins pipeline to use the `REPLICAS` parameter:

1. Modify your Jenkins pipeline to use the `REPLICAS` parameter:

```groovy
pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = credentials('docker-hub-creds')
    DOCKER_IMAGE_NAME = 'roybidani/weather_app:jenkins'
    KUBECONFIG_PATH = '/home/ubuntu/config' // Path to your kubeconfig file
  }
  parameters {
    string(name: 'REPLICAS', defaultValue: '2', description: 'Number of desired replicas')
  }
  stages {
    stage('Fetch Code') {
      steps {
        // Clone the GitLab repository
        echo 'Fetching source code from GitLab...'
        git branch: 'master', credentialsId: 'gitlab', url: 'https://gitlab.com/infinity1934640/weather'
      }
    }
    stage('Build') {
      steps {
        sh 'docker build -t $DOCKER_IMAGE_NAME .'
      }
    }
    stage('Login to Docker Hub') {
      steps {
        sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
      }
    }
    stage('Push to Docker Hub') {
      steps {
        sh "docker push $DOCKER_IMAGE_NAME"
      }
    }
    stage('Update Deployment.yml') {
      steps {
        script {
          // Replace the image name and replicas in deployment.yaml
          sh "sed -i 's#image: .*#image: $DOCKER_IMAGE_NAME#; s#replicas: .*#replicas: $REPLICAS#' deployment.yaml"
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        script {
          // Set the Kubernetes cluster context
          sh "kubectl --kubeconfig=$KUBECONFIG_PATH config use-context kubernetes-admin@kubernetes"
          // Deploy the updated deployment.yaml
          sh "kubectl --kubeconfig=$KUBECONFIG_PATH apply -f deployment.yaml"
        }
      }
    }
    stage('Deploy Ingress') {
      steps {
        script {
          // Apply the Ingress resource
          sh "kubectl --kubeconfig=$KUBECONFIG_PATH apply -f ingress.yaml"
        }
      }
    }
    stage('Clean Workspace') {
      steps {
        // Clean the working directory
        deleteDir()
      }
    }
  }
}

```

Now, when you trigger the Jenkins job, you'll be prompted to provide the number of desired replicas as the `REPLICAS` parameter, and this value will be used to update the `replicas` field in your `deployment.yaml` during the pipeline execution.

---

You've now successfully set up your infrastructure, Jenkins, and Kubernetes cluster and created Jenkins pipelines for Docker and Kubernetes deployments. You can adapt these steps to suit your specific application and deployment requirements.

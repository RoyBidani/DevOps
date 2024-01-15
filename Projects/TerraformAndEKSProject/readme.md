# Infrastructure and Application Deployment Guide

This guide will help you set up an infrastructure using Terraform, provision an Amazon Elastic Kubernetes Service (EKS) cluster, create a Network Load Balancer (NLB), and deploy a Python REST API on the cluster. Below are the steps and explanations:

## Table of Contents
- [System Diagram](#system-diagram)
- [Infrastructure as Code with Terraform](#infrastructure-as-code-with-terraform)
   - [VPC](#vpc)
   - [EKS Cluster (`eks-cluster` directory)](#eks-cluster-eks-cluster-directory)
   - [Create a Load Balancer](#create-a-load-balancer)
- [Python REST API](#python-rest-api)

---

## System Diagram

Visualize your infrastructure and component relationships:

```
    +------------------------+
    |   Internet Gateway     |
    +------------------------+
              |
    +------------------------+
    |       NAT Gateway      |
    +------------------------+
              |
    +------------------------+
    |          VPC           |
    |(Virtual Private Cloud) |
    +------------------------+
       |          |          |
    +--+     +--------+     +--------+
    |  |     | Subnet |     | Subnet |
    |  |     |(Private)|    |(Public)|
    |  |     +--------+     +--------+
    |  |           |             |
    |  |     +--------+        +------------+
    |  |     | EKS Cluster|     | Load Balancer |
    |  |     +--------+        +------------+
    |  |          |
    |  |     +------------+
    |  |     | EC2 Nodes  |
    |  |     +------------+
    |  |
    |  |   +------------------+
    |  +---| Python REST API |
    |      +------------------+
    |
    +------------------------+
```

---

## Infrastructure as Code with Terraform

### VPC

In the `vpc` directory, you'll define your Virtual Private Cloud (VPC), subnets, routing tables, NAT gateways, and internet gateways using Terraform.

**`main.tf` - Define the VPC:**

```hcl
# Configure the AWS provider with your AWS region.
provider "aws" {
  region = "eu-west-3"
}

# Create an AWS VPC with a specific CIDR block, DNS support, and hostnames enabled.
resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "my-vpc"
  }
}

# Define private subnets using valid availability zones.
resource "aws_subnet" "private_subnet" {
  count = 2
  cidr_block          = "10.0.${count.index}.0/24"
  availability_zone   = "eu-west-3${element(["a", "b"], count.index)}"  # Use "a" and "b" for availability zones.
  vpc_id              = aws_vpc.my_vpc.id
  map_public_ip_on_launch = false
  tags = {
    Name = "private-subnet-${element(["a", "b"], count.index)}"
  }
}

# Define public subnets using valid availability zones.
resource "aws_subnet" "public_subnet" {
  count = 2
  cidr_block          = "10.0.${count.index + 10}.0/24"
  availability_zone   = "eu-west-3${element(["a", "b"], count.index + 2)}"  # Use "a" and "b" for availability zones.
  vpc_id              = aws_vpc.my_vpc.id
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-${element(["a", "b"], count.index)}"
  }
}

# Create an internet gateway and attach it to the VPC.
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
}

# Create NAT gateways (customize count and tags).
resource "aws_nat_gateway" "nat_gateway" {
  count         = 2
  allocation_id = aws_eip.nat_eip[count.index].id
  subnet_id     = aws_subnet.public_subnet[count.index].id
  tags = {
    Name = "nat-gateway-${count.index + 1}"
  }
}

# Create Elastic IPs for NAT gateways.
resource "aws_eip" "nat_eip" {
  count = 2
  domain   = "vpc"
}

# Define outputs to retrieve VPC and subnet information.
output "vpc_id" {
  value = aws_vpc.my_vpc.id
}

output "private_subnet_ids" {
  value = aws_subnet.private_subnet[*].id
}

output "public_subnet_ids" {
  value = aws_subnet.public_subnet[*].id
}
```

### EKS Cluster (`eks-cluster` directory)

In the `eks-cluster` directory, you'll configure your EKS cluster and worker node groups.

**`main.tf` - Define the EKS cluster and worker node groups:**

```hcl
provider "aws" {
  region = "eu-west-3"
}

# Create a new security group for worker nodes in the same VPC as EKS
resource "aws_security_group" "worker_node_sg" {
  name        = "my-eks-worker-node-sg"
  description = "Security group for EKS worker nodes"
  vpc_id      = "vpc-07643607954748c30"

  # Define ingress and egress rules as needed
  # Example: Allow incoming traffic from the EKS control plane security group
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    security_groups = [module.eks.cluster_security_group_id]
  }
  # Add more ingress and egress rules as needed
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-eks-cluster"
  cluster_version = "1.27"
  
   # Set the VPC ID to match your security group and subnets
  vpc_id = "vpc-07643607954748c30"  # Use the VPC ID of your EKS cluster

  # You can customize other module arguments here as needed

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
  
  control_plane_subnet_ids = []
  subnet_ids = [
    # Specify your existing subnet IDs directly here
    "subnet-03f311534ab9d6700",  # Private subnet 1
    "subnet-0e020e658062b9504",  # Private subnet 2
    "subnet-0879db60c99af8f08",  # Public subnet 1
    "subnet-050f988ea9549129c",  # Public subnet 2
    # Add more subnet IDs if needed
  ]
}

resource "aws_iam_role" "eks_node_role" {


  name = "eks-node-role"

  # Define IAM policies for nodes here

  # Define the trust policy allowing EC2 instances to assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach the AmazonEKSWorkerNodePolicy to the IAM role
resource "aws_iam_policy_attachment" "eks_node_policy_attachment" {
  name       = "eks-node-policy"  # Use a placeholder name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  roles      = [aws_iam_role.eks_node_role.name]
}

# Attach the AmazonEC2ContainerRegistryReadOnly policy to the IAM role
resource "aws_iam_policy_attachment" "ecr_readonly_policy_attachment" {
  name       = "ecr-readonly-policy"  # Use a placeholder name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  roles      = [aws_iam_role.eks_node_role.name]
}

resource "aws_iam_instance_profile" "eks_node_profile" {
  name = "eks-node-profile"
  role = aws_iam_role.eks_node_role.name
}

resource "aws_eks_node_group" "eks_nodes" {
  cluster_name             = module.eks.cluster_name
  node_group_name          = "eks-node-group"
  node_role_arn            = aws_iam_role.eks_node_role.arn

  # Specify your existing subnet IDs directly here
  subnet_ids = [
    "subnet-03f311534ab9d6700",  # Private subnet 1
    "subnet-0e020e658062b9504",  # Private subnet 2
    "subnet-0879db60c99af8f08",  # Public subnet 1
    "subnet-050f988ea9549129c",  # Public subnet 2
    # Add more subnet IDs if needed
  ]

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  # Set the security group for your worker nodes here
  remote_access {
    ec2_ssh_key = "myKey" # Replace with your SSH key name
    source_security_group_ids = [aws_security_group.worker_node_sg.id]
  }
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}
```

### Create a Load Balancer

To distribute traffic to your EKS cluster nodes, create an AWS Network Load Balancer (NLB).

**a. Create a new Terraform file for NLB configuration:**

Create a new Terraform file, e.g., `lb.tf`, in your `eks-cluster` directory:

```plaintext
project/
├── eks-cluster/
│   ├── main.tf
│   ├── lb.tf       # Create this file for NLB configuration
```

**b. Define the NLB resource in `lb.tf`:**

```hcl
resource "aws_lb" "my_nlb" {
  name               = "my-nlb"
  internal           = false # Set to true for internal NLB
  load_balancer_type = "network"
  subnets            = aws_subnet.public_subnet[*].id # Use your public subnets
}

resource "aws_lb_target_group" "my_target_group" {
  name     = "my-target-group"
  port     = 80
  protocol = "TCP"
  vpc_id   = aws_vpc.my_vpc.id
}

resource "aws_lb_listener" "my_listener" {
  load_balancer_arn = aws_lb.my_nlb.arn
  port              = 80
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_target_group.arn
  }
}

output "nlb_dns_name" {
  value = aws_lb.my_nlb.dns_name
}
```

---

## Python REST API

Follow these steps to deploy a Python REST API on your EKS cluster:

1. **Clone the Project:**

   In your local development environment, open a terminal, navigate to your desired directory, and run these commands to clone the "Hello World" Python REST API project:

   ```bash
   git clone https://github.com/alankrantas/hello-world-rest-apis.git
   cd hello-world-rest-apis/python_api
   ```

2. **Create `api-deployment.yaml` File:**

   Create a new file called `api-deployment.yaml`:

   ```bash
   touch api-deployment.yaml
   ```

   Open `api-deployment.yaml` and paste the following content:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: hello-world-api
   spec:
     replicas: 2  # Adjust the number of replicas as needed
     selector:
       matchLabels:
         app: hello-world-api
     template:
       metadata:
         labels:
           app: hello-world-api
       spec:
         containers:
         - name: hello-world-api
           image: alankrantas/hello-world-rest-api:latest  # Use the image from the repository
           ports:
           - containerPort: 5000
   ```

3. **Create `api-service.yaml` File:**

   Create another file called `api-service.yaml`:

   ```bash
   touch api-service.yaml
   ```

   Open `api-service.yaml` and paste the following content:

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: hello-world-api
   spec:
     selector:
       app: hello-world-api
     ports:
       - protocol: TCP
         port: 80
         targetPort: 5000
     type: ClusterIP  # Expose as a ClusterIP service within the cluster
   ```

4. **Apply Deployment and Service to EKS Cluster:**

   Apply the deployment and service to your AWS EKS cluster:

   ```bash
   kubectl apply -f api-deployment.yaml
   kubectl apply -f api-service.yaml
   ```

   This will deploy your Python REST API and create a Kubernetes Service to expose it within the cluster.

Now you have a fully deployed infrastructure with an EKS cluster and a Python REST API running on it. You can access the API using the DNS name provided by the NLB.

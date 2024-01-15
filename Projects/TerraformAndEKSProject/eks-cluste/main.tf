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





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



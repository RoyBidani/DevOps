### Table of Contents

1. [Exercise 1: Install Terraform on Ubuntu 22.04 ARM64](#exercise-1-install-terraform-on-ubuntu-2204-arm64)
2. [Exercise 2: Write Terraform code to install your weather app on Docker (on-premise)](#exercise-2-write-terraform-code-to-install-your-weather-app-on-docker-on-premise)
3. [Exercise 3: Create a new EC2 instance on your AWS account using Terraform, running Ubuntu](#exercise-3-create-a-new-ec2-instance-on-your-aws-account-using-terraform-running-ubuntu)
4. [Exercise 4: Create security groups for this instance with Terraform dynamic blocks](#exercise-4-create-security-groups-for-this-instance-with-terraform-dynamic-blocks)
5. [Exercise 5: Create an EC2 instance with the configuration of security groups by importing the module your labmate created in the previous exercise](#exercise-5-create-an-ec2-instance-with-the-configuration-of-security-groups-by-importing-the-module-your-labmate-created-in-the-previous-exercise)
6. [Exercise 6: Configure the remote backend for this infrastructure in $3](#exercise-6-configure-the-remote-backend-for-this-infrastructure-in-3)
7. [Exercise 7: Rename the EC2 instance as 'Infinity Terraform Test Server' using an input variable](#exercise-7-rename-the-ec2-instance-as-infinity-terraform-test-server-using-an-input-variable)
8. [Exercise 8: Using Terraform, create an EC2 server with your weather app on it](#exercise-8-using-terraform-create-an-ec2-server-with-your-weather-app-on-it)
9. [Exercise 9: Destroy the EC2 instance via Terraform](#exercise-9-destroy-the-ec2-instance-via-terraform)
10. [Exercise 10: Create an AWS VPC with specific components](#exercise-10-create-an-aws-vpc-with-specific-components)

---

## Exercise 1: Install Terraform on Ubuntu 22.04 ARM64

1. **Download Terraform**: Open a terminal and run the following commands to download the latest version of Terraform for ARM64.

   Install repository addition dependencies:

   ```bash
   sudo apt update
   sudo apt install software-properties-common gnupg2 curl
   ```

   Download Terraform:

   ```bash
   wget https://releases.hashicorp.com/terraform/1.0.11/terraform_1.0.11_linux_arm64.zip
   unzip terraform_1.0.11_linux_arm64.zip
   ```

   Import repository GPG key:

   ```bash
   curl https://apt.releases.hashicorp.com/gpg | gpg --dearmor > hashicorp.gpg
   sudo install -o root -g root -m 644 hashicorp.gpg /etc/apt/trusted.gpg.d/
   ```

   With the key imported, add the Hashicorp repository to your Ubuntu system:

   ```bash
   sudo apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
   ```

   Install Terraform on your Ubuntu Linux system:

   ```bash
   sudo apt install terraform
   ```

2. **Verify Installation**: To verify the installation, run:

   ```bash
   terraform --version
   ```

---

## Exercise 2: Write Terraform code to install your weather app on Docker (on-premise)

Here is an example `main.tf` file that can deploy your Python weather app using Docker:

```hcl
# Define the required Docker provider and its version
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

# Configure the Docker provider
provider "docker" {}

# Define a Docker image resource named "weather_app"
resource "docker_image" "weather_app" {
  # Specify the name of the Docker image to use
  name = "roybidani/weather_app:app"
}

# Define a Docker container resource named "weather_app"
resource "docker_container" "weather_app" {
  # Use the image ID of the "weather_app" Docker image
  image = docker_image.weather_app.image_id

  # Set the name of the Docker container
  name  = "weather_app_container"

  # Configure port mapping for the Docker container
  ports {
    internal = 8080   # Internal port within the container
    external = 8000   # External port on the host
  }
}
```

---

## Exercise 3: Create a new EC2 instance on your AWS account using Terraform, running Ubuntu

1. **Configure AWS Credentials**: Ensure you have your AWS credentials configured either by setting environment variables or using AWS CLI `aws configure`.

2. **Write Terraform Configuration**: Create a `.tf` file with the following content to define an EC2 instance running Ubuntu:

   ```hcl
   	# Define an AWS EC2 instance resource named "ubuntu_server"
   	resource "aws_instance" "ubuntu_server" {
     ami           = "ami-05b5a865c3579bbc4" # Ubuntu 20.04 LTS (replace with the current Ubuntu AMI ID for your region)
     instance_type = "t2.micro"

     # Add tags to the EC2 instance for easy identification
     tags = {
       Name = "UbuntuServer"
     }

     # Specify the SSH key pair to be used for authentication
     key_name = "myKey"

     # Specify the appropriate subnet ID from your VPC
     subnet_id = "subnet-0edf3cad61e2af405"
   }
   ```

3. **Initialize Terraform**: In the same directory as your `.tf` file, run:

   ```bash
   terraform init
   ```

4. **Apply the Configuration**: Run the following command to create the EC2 instance:

   ```bash
   terraform apply
   ```

---

## Exercise 4: Create security groups for this instance with Terraform dynamic blocks

To create security groups for an AWS EC2 instance using Terraform dynamic blocks with the specified rules and state locking using DynamoDB, you can follow the code below. I've added comments to explain each part of the configuration:

```hcl
# Configure the AWS provider with the desired region
provider "aws" {
  region = "eu-west-3"  # Replace with your desired AWS region
}

# Create a security group for inbound rules
resource "aws_security_group" "inbound_sg" {
  name        = "inbound-sg"
  description = "Security group for inbound rules"

  # Inbound rules
  dynamic "ingress" {
    for_each = [
      {
        description = "SSH from local IP",
        from_port   = 22,
        to_port     = 22,
        protocol    = "tcp",
        cidr_blocks = ["your_local_ip/32"]  # Replace with your local IP
      },
      {
        description = "HTTP from all IPs",
        from_port   = 80,
        to_port     = 80,
        protocol    = "tcp",
        cidr_blocks = ["0.0.0.0/0"]
      },
      {
        description = "HTTPS from all IPs",
        from_port   = 443,
        to_port     = 443,
        protocol    = "tcp",
        cidr_blocks = ["0.0.0.0/0"]
      }
    ]

    content {
      description     = ingress.value["description"]
      from_port       = ingress.value["from_port"]
      to_port         = ingress.value["to_port"]
      protocol        = ingress.value["protocol"]
      cidr_blocks     = ingress.value["cidr_blocks"]
    }
  }

  # Outbound rules (allow all traffic)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Enable state locking with DynamoDB
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"  # Replace with your S3 bucket name
    key            = "terraform.tfstate"
    region         = "us-east-1"  # Replace with the AWS region for your S3 bucket
    encrypt        = true
    dynamodb_table = "your-dynamodb-lock-table"  # Replace with your DynamoDB lock table name
  }
}
```

In this configuration:

1. We create an AWS security group named "inbound_sg" with dynamic ingress rules. It allows SSH from your local IP, and HTTP/HTTPS from all IPs.

2. For state locking with DynamoDB, configure the `terraform` backend with the appropriate S3 bucket and DynamoDB lock table. Replace `"your-terraform-state-bucket"`, `"your-dynamodb-lock-table"`, and `"us-east-1"` with your actual values.

After creating this Terraform configuration, you can run `terraform init`, `terraform plan`, and `terraform apply` to provision the security group and configure state locking.

---

## Exercise 5: Create an EC2 instance with the configuration of security groups by importing the module your labmate created in the previous exercise

1. **Create a module directory with the security group file (`sgModule/main.tf`):**

   ```hcl
   # Configure the AWS provider with the desired region
   provider "aws" {
     region = "eu-west-3"  # Replace with your desired AWS region
   }

   # Create a security group for inbound rules
   resource "aws_security_group" "inbound_sg" {
     name        = "inbound-sg"
     description = "Security group for inbound rules"

     # Inbound rules
     dynamic "ingress" {
       for_each = [
         {
           description = "SSH from from all IPs",
           from_port   = 22,
           to_port     = 22,
           protocol    = "tcp",
           cidr_blocks = ["0.0.0.0/0"]  # Replace with your local IP
         },
         {
           description = "HTTP from all IPs",
           from_port   = 80,
           to_port     = 80,
           protocol    = "tcp",
           cidr_blocks = ["0.0.0.0/0"]
         },
         {
           description = "HTTPS from all IPs",
           from_port   = 443,
           to_port     = 443,
           protocol    = "tcp",
           cidr_blocks = ["0.0.0.0/0"]
         }
       ]

       content {
         description     = ingress.value["description"]
         from_port       = ingress.value["from_port"]
         to_port         = ingress.value["to_port"]
         protocol        = ingress.value["protocol"]
         cidr_blocks     = ingress.value["cidr_blocks"]
       }
     }

     # Outbound rules (allow all traffic)
     egress {
       from_port   = 0
       to_port     = 0
       protocol    = "-1"
       cidr_blocks = ["0.0.0.0/0"]
     }
   }

   output "security_group_id" {
     value = aws_security_group.inbound_sg.id
   }
   ```

2. **Create a `main.tf` file with the content (in the root directory):**

   ```hcl
   # Enable state locking with DynamoDB
   terraform {
     backend "s3" {
       bucket         = "bidasbucket"  # Replace with your S3 bucket name
       key            = "terraform.tfstate"
       region         = "eu-west-3"  # Replace with the AWS region for your S3 bucket
       encrypt        = true
       dynamodb_table = "terraform_table"  # Replace with your DynamoDB lock table name
     }
   }

   module "sg" {
     source = "./sgModule"
   }

   resource "aws_instance" "ec2_instance" {
     ami           = "ami-05b5a865c3579bbc4" # Replace with the current Ubuntu AMI ID for your region
     instance_type = "t2.micro"

     # Add tags to the EC2 instance for easy identification
     tags = {
       Name = "UbuntuServer2"
     }

     # Specify the SSH key pair to be used for authentication
     key_name = "myKey"



     # Reference the security group ID from the module's output
     vpc_security_group_ids = [
       module.sg.security_group_id
     ]

     # Specify the appropriate subnet ID from your VPC
     subnet_id = "subnet-0edf3cad61e2af405"
   }
   ```

3. **Initialize Terraform**: In the same directory as your `.tf` file, run:

   ```bash
   terraform init
   ```

4. **Apply the Configuration**: Run the following command to create the EC2 instance:

   ```bash
   terraform apply
   ```

---

## Exercise 6: Configure the remote backend for this infrastructure in S3

To configure a remote backend (e.g., S3) for the infrastructure you created in Exercise 3, follow these steps:

1. **Create an S3 Bucket**: Create an S3 bucket in your AWS account to store the Terraform state file.

2. **Update Terraform Configuration**: Modify your Terraform configuration (the `.tf` file) to include the backend configuration. For example:

   ```hcl
   terraform {
     backend "s3" {
       bucket         = "your-s3-bucket-name"
       key            = "terraform.tfstate"
       region         = "us-east-1"  # Adjust to your desired region
     }
   }
   ```

3. **Initialize Terraform**: Run `terraform init` to initialize Terraform with the new backend configuration.

4. **Apply Configuration**: Run `terraform apply` to apply the configuration using the remote backend.

---

## Exercise 7: Rename the EC2 instance as 'Infinity Terraform Test Server' using an input variable

To rename the EC2 instance as 'Infinity Terraform Test Server' using an input variable in your Terraform configuration, follow these steps:

1. Define an Input Variable: In your Terraform configuration, you need to define an input variable for the instance name. Add the following block at the top of your `.tf` file:

   ```hcl
   variable "instance_name" {
     description = "Name for the EC2 instance"
     default     = "Infinity Terraform Test Server"
   }
   ```

   This block defines an input variable called `instance_name` with a default value of "Infinity Terraform Test Server." You can change the default value to whatever you prefer.

2. Update the EC2 Instance Resource: Locate the `aws_instance` resource block in your configuration (the `resource "aws_instance" "ec2_instance"` block). Within this block, modify the `tags` section to use the `var.instance_name` variable for the instance's Name tag:

   ```hcl
   tags = {
     Name = var.instance_name
   }
   ```

   Here, we are setting the Name tag of the EC2 instance to the value of the `var.instance_name` variable.

3. Apply the Configuration: After making these changes, run `terraform apply` to update the EC2 instance's Name tag to "Infinity Terraform Test Server."

You can also override the default value of `instance_name` by specifying it when you apply the Terraform configuration:

```bash
terraform apply -var "instance_name=YourCustomName"
```

Replace "YourCustomName" with the desired name for your EC2 instance if you want to override the default value.

Remember to save your Terraform configuration file after making these changes, and then you can apply the configuration to update the EC2 instance's Name tag.

---

## Exercise 8: Using Terraform, create an EC2 server with your weather app on it

1. **Create a `main.tf` file:**

   Here is an example of a `main.tf` file that deploys your Python weather app on an AWS EC2 instance:

   ```hcl
   provider "aws" {
     region = "eu-west-3" # Replace with your desired AWS region
   }

   # Look up the "inbound_sg" security group by name
   data "aws_security_group" "inbound_sg" {
     name = "inbound-sg" # Replace with the actual name of your security group
   }

   resource "aws_instance" "example" {
     ami           = "ami-05b5a865c3579bbc4" # Replace with your desired AMI ID
     instance_type = "t2.micro"

     # Shell script to run the Docker container with the image.
     user_data = file("script.sh")

     tags = {
       Name = "MyEC2Instance"
     }

     # Specify the SSH key pair to be used for authentication
     key_name = "myKey"

     # Reference the security group using the data source result
     vpc_security_group_ids = [data.aws_security_group.inbound_sg.id]

     # Specify the appropriate subnet ID from your VPC
     subnet_id = "subnet-0edf3cad61e2af405"
   }
   ```

2. **Create a `script.sh` file:**

   The `script.sh` file contains the shell script to set up Docker and run your Python weather app. Here's a basic example:

   ```bash
   #!/bin/bash
   for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do
     sudo apt-get remove $pkg
   done

   sudo apt-get update -y

   sudo apt-get install ca-certificates curl gnupg -y

   echo "deb [arch=\"$(dpkg --print-architecture)\" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg

   sudo apt-get update -y

   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

   sudo usermod -aG docker $USER

   newgrp docker

   docker run -d -p 80:8000 roybidani/weather_app:app
   ```

3. **Initialize Terraform**: In the same directory as your `.tf` file, run:

   ```bash
   terraform init
   ```

4. **Apply the Configuration**: Run the following command to create the EC2 instance and deploy your weather app:

   ```bash
   terraform apply
   ```

---

## Exercise 9: Destroy the EC2 instance via Terraform

Run the following command to destroy the EC2 instance you created earlier:

```bash
terraform destroy
```

---

## Exercise 10: Create an AWS VPC with specific components

To create an AWS VPC with Terraform that includes a public subnet, a private subnet, an Internet Gateway, and a routing table, you can use the following Terraform configuration. I've added comments to explain each part of the configuration:

```hcl
# Define the AWS provider and region
provider "aws" {
  region = "eu-west-3

"  # Replace with your desired AWS region
}

# Create a VPC
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"  # Replace with your desired VPC CIDR block
}

# Create an Internet Gateway
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
}

# Create a public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"  # Replace with your desired public subnet CIDR block
  availability_zone       = "eu-west-3a"   # Replace with your desired availability zone
  map_public_ip_on_launch = true
}

# Create a private subnet
resource "aws_subnet" "private_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.2.0/24"  # Replace with your desired private subnet CIDR block
  availability_zone       = "eu-west-3b"   # Replace with your desired availability zone
}

# Create a routing table for the public subnet
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.my_vpc.id
}

# Create a default route to the Internet Gateway in the public route table
resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.my_igw.id
}

# Associate the public subnet with the public route table
resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

# Output the VPC ID and Subnet IDs
output "vpc_id" {
  value = aws_vpc.my_vpc.id
}

output "public_subnet_id" {
  value = aws_subnet.public_subnet.id
}

output "private_subnet_id" {
  value = aws_subnet.private_subnet.id
}
```

This Terraform configuration does the following:

1. Creates a VPC with the specified CIDR block.
2. Creates an Internet Gateway and associates it with the VPC.
3. Creates a public subnet with a specified CIDR block, availability zone, and enables auto-assigning public IP addresses.
4. Creates a private subnet with a specified CIDR block and availability zone.
5. Creates a routing table for the public subnet.
6. Adds a default route to the Internet Gateway in the public route table.
7. Associates the public subnet with the public route table.
8. Outputs the VPC ID, public subnet ID, and private subnet ID.

After creating this Terraform configuration, run `terraform init` to initialize Terraform and `terraform apply` to create the AWS VPC and associated components.

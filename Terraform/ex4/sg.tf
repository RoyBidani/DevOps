

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
  description = "ID of the security group for the EC2 instance"
  value       = aws_security_group.inbound_sg.id
}


# Enable state locking with DynamoDB
#terraform {
 # backend "s3" {
  #  bucket         = "bidasbucket"  # Replace with your S3 bucket name
   # key            = "terraform.tfstate"
    #region         = "eu-west-3"  # Replace with the AWS region for your S3 bucket
    #encrypt        = true
    #dynamodb_table = "terraform_table"  # Replace with your DynamoDB lock table name
  #}
#}


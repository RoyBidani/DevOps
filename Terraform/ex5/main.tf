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






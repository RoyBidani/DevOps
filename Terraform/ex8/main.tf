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

  # shell script to run the Docker container with the image.
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




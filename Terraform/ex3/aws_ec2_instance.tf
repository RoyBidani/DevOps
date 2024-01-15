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

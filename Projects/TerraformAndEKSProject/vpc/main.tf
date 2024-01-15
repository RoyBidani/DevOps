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


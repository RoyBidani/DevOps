# Define the AWS provider and region
provider "aws" {
  region = "eu-west-3" # Replace with your desired AWS region
}

# Create a VPC
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16" # Replace with your desired VPC IP range
  enable_dns_support = true
  enable_dns_hostnames = true
}

# Create an Internet Gateway
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
}

# Create a public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "10.0.1.0/24" # Replace with your desired public subnet IP range
  availability_zone = "eu-west-3a" # Replace with the actual availability zone name
  map_public_ip_on_launch = true
}


# Create a private subnet
resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "10.0.2.0/24" # Replace with your desired private subnet IP range
  availability_zone = "eu-west-3a" # Replace with your desired availability zone
}

# Create a custom route table for the public subnet
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.my_vpc.id
}

# Create a route to the Internet Gateway for the public subnet
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


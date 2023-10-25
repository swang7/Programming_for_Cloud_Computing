terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-west-2"
}

# Our default security group to access
# the instances over SSH and HTTP
resource "aws_security_group" "default" {
  name        = "web_group"
  description = "Allow ssh and web access"

  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  ami               = var.ami
  availability_zone = "us-west-2a"
  instance_type     = "t2.micro"

  # The name of our SSH keypair you've created and downloaded
  # from the AWS console.
  key_name = var.key_name

  # Our Security group to allow HTTP and SSH access
  security_groups = [aws_security_group.default.name]

  tags = {
    Name = "aws_hw4_instance"
  }

  ebs_block_device {
    device_name = "/dev/xvdf"
    volume_type = "gp2"
    volume_size = 1
    delete_on_termination = true
  }

  # Run a remote provisioner on the instance after creating it.
  # In this case, we mount the ebs and write a file
  user_data = file("userdata.sh")
}

resource "aws_eip" "default" {
  instance = aws_instance.app_server.id
  domain   = "vpc"
}

 terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "notes-app-terraform-state-cherry"
    key    = "dev/terraform.tfstate"
    region = "ap-south-1"
  }
}

provider "aws" {
  region = "ap-south-1"
}

module "vpc" {
  source = "./modules/vpc"

  environment       = "dev"
  vpc_cidr          = "10.0.0.0/16"
  subnet_cidr       = "10.0.1.0/24"
  availability_zone = "ap-south-1a"
}

module "ec2" {
  source = "./modules/ec2"

  environment   = "dev"
  vpc_id        = module.vpc.vpc_id
  subnet_id     = module.vpc.subnet_id
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t2.micro"
}
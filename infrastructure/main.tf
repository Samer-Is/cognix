# COGNIX AI - AWS Infrastructure with Terraform
# Target: < $20/month using serverless architecture

terraform {
  required_version = ">= 1.5"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "cognix-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "cognix"
}

# Outputs
output "api_gateway_url" {
  description = "API Gateway URL"
  value       = aws_apigatewayv2_api.cognix_api.api_endpoint
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = aws_cognito_user_pool.cognix_pool.id
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.cognix_db.endpoint
}

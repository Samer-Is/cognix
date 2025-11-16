# AWS Cognito for user authentication

# User Pool
resource "aws_cognito_user_pool" "cognix_pool" {
  name = "${var.project_name}-users-${var.environment}"

  # Sign-in options
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  # Password policy
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = false
  }

  # Account recovery
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  # User attributes
  schema {
    name                = "email"
    attribute_data_type = "String"
    required            = true
    mutable             = true
  }

  schema {
    name                = "name"
    attribute_data_type = "String"
    required            = false
    mutable             = true
  }

  # Email configuration
  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  tags = {
    Name        = "COGNIX User Pool"
    Environment = var.environment
  }
}

# User Pool Client
resource "aws_cognito_user_pool_client" "cognix_client" {
  name         = "${var.project_name}-client"
  user_pool_id = aws_cognito_user_pool.cognix_pool.id

  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]

  # Token validity
  access_token_validity  = 1  # 1 hour
  id_token_validity      = 1  # 1 hour
  refresh_token_validity = 30 # 30 days

  token_validity_units {
    access_token  = "hours"
    id_token      = "hours"
    refresh_token = "days"
  }

  # Prevent user existence errors
  prevent_user_existence_errors = "ENABLED"
}

# User Pool Domain
resource "aws_cognito_user_pool_domain" "cognix_domain" {
  domain       = "${var.project_name}-${var.environment}"
  user_pool_id = aws_cognito_user_pool.cognix_pool.id
}

# Output Cognito details
output "cognito_user_pool_client_id" {
  description = "Cognito User Pool Client ID"
  value       = aws_cognito_user_pool_client.cognix_client.id
}

output "cognito_domain" {
  description = "Cognito Domain"
  value       = aws_cognito_user_pool_domain.cognix_domain.domain
}

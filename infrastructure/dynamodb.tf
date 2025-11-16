# DynamoDB Tables for user management and activity tracking

# Users table
resource "aws_dynamodb_table" "cognix_users" {
  name           = "${var.project_name}-users-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"  # Cost-effective for low traffic
  hash_key       = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  global_secondary_index {
    name            = "email-index"
    hash_key        = "email"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = false
  }

  tags = {
    Name        = "COGNIX Users"
    Environment = var.environment
  }
}

# Activity logs table
resource "aws_dynamodb_table" "cognix_activity" {
  name           = "${var.project_name}-activity-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "activity_id"
  range_key      = "timestamp"

  attribute {
    name = "activity_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name            = "user-index"
    hash_key        = "user_id"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true  # Auto-delete old logs
  }

  tags = {
    Name        = "COGNIX Activity Logs"
    Environment = var.environment
  }
}

# Agent memory table for conversation context
resource "aws_dynamodb_table" "cognix_memory" {
  name           = "${var.project_name}-agent-memory-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "session_id"

  attribute {
    name = "session_id"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name            = "user-sessions-index"
    hash_key        = "user_id"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Name        = "COGNIX Agent Memory"
    Environment = var.environment
  }
}

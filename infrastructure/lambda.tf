# AWS Lambda Functions

# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = {
    Name        = "COGNIX Lambda Role"
    Environment = var.environment
  }
}

# Attach policies to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:*",
          "s3:*",
          "secretsmanager:GetSecretValue",
          "rds:*"
        ]
        Resource = "*"
      }
    ]
  })
}

# Lambda Layer for dependencies
resource "aws_lambda_layer_version" "cognix_dependencies" {
  filename            = "lambda_layer.zip"  # Create this with dependencies
  layer_name          = "${var.project_name}-dependencies"
  compatible_runtimes = ["python3.11"]
  
  lifecycle {
    create_before_destroy = true
  }
}

# Main Chat Handler Lambda
resource "aws_lambda_function" "chat_handler" {
  filename      = "lambda_functions.zip"  # Package backend code
  function_name = "${var.project_name}-chat-handler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handlers.chat_handler.handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 512

  layers = [aws_lambda_layer_version.cognix_dependencies.arn]

  environment {
    variables = {
      ENVIRONMENT           = var.environment
      DYNAMODB_USERS_TABLE  = aws_dynamodb_table.cognix_users.name
      DYNAMODB_ACTIVITY_TABLE = aws_dynamodb_table.cognix_activity.name
      DYNAMODB_MEMORY_TABLE = aws_dynamodb_table.cognix_memory.name
      RDS_SECRET_ARN        = aws_secretsmanager_secret.db_password.arn
      S3_DATA_BUCKET        = aws_s3_bucket.cognix_data.bucket
      S3_UPLOADS_BUCKET     = aws_s3_bucket.cognix_uploads.bucket
    }
  }

  tags = {
    Name        = "COGNIX Chat Handler"
    Environment = var.environment
  }
}

# Data Query Lambda
resource "aws_lambda_function" "data_query" {
  filename      = "lambda_functions.zip"
  function_name = "${var.project_name}-data-query"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handlers.data_query.handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 512

  layers = [aws_lambda_layer_version.cognix_dependencies.arn]

  environment {
    variables = {
      ENVIRONMENT    = var.environment
      RDS_SECRET_ARN = aws_secretsmanager_secret.db_password.arn
    }
  }

  tags = {
    Name        = "COGNIX Data Query"
    Environment = var.environment
  }
}

# File Processor Lambda
resource "aws_lambda_function" "file_processor" {
  filename      = "lambda_functions.zip"
  function_name = "${var.project_name}-file-processor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handlers.file_processor.handler"
  runtime       = "python3.11"
  timeout       = 60
  memory_size   = 1024

  layers = [aws_lambda_layer_version.cognix_dependencies.arn]

  environment {
    variables = {
      ENVIRONMENT       = var.environment
      S3_UPLOADS_BUCKET = aws_s3_bucket.cognix_uploads.bucket
    }
  }

  tags = {
    Name        = "COGNIX File Processor"
    Environment = var.environment
  }
}

# S3 trigger for file processing
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.cognix_uploads.arn
}

resource "aws_s3_bucket_notification" "uploads_notification" {
  bucket = aws_s3_bucket.cognix_uploads.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.file_processor.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
}

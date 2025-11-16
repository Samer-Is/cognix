# CloudWatch for monitoring and logging

# Log Groups for Lambda functions
resource "aws_cloudwatch_log_group" "chat_handler_logs" {
  name              = "/aws/lambda/${aws_lambda_function.chat_handler.function_name}"
  retention_in_days = 7  # Cost optimization

  tags = {
    Name        = "COGNIX Chat Handler Logs"
    Environment = var.environment
  }
}

resource "aws_cloudwatch_log_group" "data_query_logs" {
  name              = "/aws/lambda/${aws_lambda_function.data_query.function_name}"
  retention_in_days = 7

  tags = {
    Name        = "COGNIX Data Query Logs"
    Environment = var.environment
  }
}

resource "aws_cloudwatch_log_group" "file_processor_logs" {
  name              = "/aws/lambda/${aws_lambda_function.file_processor.function_name}"
  retention_in_days = 7

  tags = {
    Name        = "COGNIX File Processor Logs"
    Environment = var.environment
  }
}

# Cost Alarm
resource "aws_cloudwatch_metric_alarm" "high_cost" {
  alarm_name          = "${var.project_name}-high-cost-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "EstimatedCharges"
  namespace           = "AWS/Billing"
  period              = "21600"  # 6 hours
  statistic           = "Maximum"
  threshold           = "20"     # $20
  alarm_description   = "Alert when costs exceed $20"
  
  dimensions = {
    Currency = "USD"
  }

  tags = {
    Name        = "COGNIX Cost Alarm"
    Environment = var.environment
  }
}

# Lambda Error Alarms
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${var.project_name}-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "Alert on Lambda errors"

  dimensions = {
    FunctionName = aws_lambda_function.chat_handler.function_name
  }

  tags = {
    Name        = "COGNIX Lambda Errors"
    Environment = var.environment
  }
}

# API Gateway 5XX Errors
resource "aws_cloudwatch_metric_alarm" "api_errors" {
  alarm_name          = "${var.project_name}-api-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "5XXError"
  namespace           = "AWS/ApiGateway"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "Alert on API Gateway 5XX errors"

  dimensions = {
    ApiName = aws_apigatewayv2_api.cognix_api.name
  }

  tags = {
    Name        = "COGNIX API Errors"
    Environment = var.environment
  }
}

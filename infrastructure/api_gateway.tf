# API Gateway for RESTful endpoints

# HTTP API (cheaper than REST API)
resource "aws_apigatewayv2_api" "cognix_api" {
  name          = "${var.project_name}-api-${var.environment}"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = ["*"]  # Restrict in production
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["*"]
    max_age       = 300
  }

  tags = {
    Name        = "COGNIX API"
    Environment = var.environment
  }
}

# Stage
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.cognix_api.id
  name        = "$default"
  auto_deploy = true

  tags = {
    Name        = "COGNIX API Default Stage"
    Environment = var.environment
  }
}

# Lambda integrations
resource "aws_apigatewayv2_integration" "chat_integration" {
  api_id           = aws_apigatewayv2_api.cognix_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.chat_handler.invoke_arn
  
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "query_integration" {
  api_id           = aws_apigatewayv2_api.cognix_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.data_query.invoke_arn
  
  payload_format_version = "2.0"
}

# Routes
resource "aws_apigatewayv2_route" "chat" {
  api_id    = aws_apigatewayv2_api.cognix_api.id
  route_key = "POST /api/chat"
  target    = "integrations/${aws_apigatewayv2_integration.chat_integration.id}"
}

resource "aws_apigatewayv2_route" "query" {
  api_id    = aws_apigatewayv2_api.cognix_api.id
  route_key = "POST /api/query"
  target    = "integrations/${aws_apigatewayv2_integration.query_integration.id}"
}

# Lambda permissions for API Gateway
resource "aws_lambda_permission" "chat_api_gw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chat_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.cognix_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "query_api_gw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_query.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.cognix_api.execution_arn}/*/*"
}

# Throttling settings (cost control)
resource "aws_apigatewayv2_stage" "throttling" {
  api_id      = aws_apigatewayv2_api.cognix_api.id
  name        = "prod"
  auto_deploy = true

  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }

  tags = {
    Name        = "COGNIX API Production Stage"
    Environment = var.environment
  }
}

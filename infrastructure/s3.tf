# S3 Buckets for data storage

# Data bucket for CSV files
resource "aws_s3_bucket" "cognix_data" {
  bucket = "${var.project_name}-data-${var.environment}"

  tags = {
    Name        = "COGNIX Data"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "data_versioning" {
  bucket = aws_s3_bucket.cognix_data.id

  versioning_configuration {
    status = "Disabled"  # Save costs
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lifecycle" {
  bucket = aws_s3_bucket.cognix_data.id

  rule {
    id     = "delete-old-files"
    status = "Enabled"

    expiration {
      days = 90  # Delete files older than 90 days
    }
  }
}

# Uploads bucket for RAG documents
resource "aws_s3_bucket" "cognix_uploads" {
  bucket = "${var.project_name}-uploads-${var.environment}"

  tags = {
    Name        = "COGNIX Uploads"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "uploads_versioning" {
  bucket = aws_s3_bucket.cognix_uploads.id

  versioning_configuration {
    status = "Disabled"
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "data_public_block" {
  bucket = aws_s3_bucket.cognix_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "uploads_public_block" {
  bucket = aws_s3_bucket.cognix_uploads.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

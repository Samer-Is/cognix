# RDS PostgreSQL Database (t3.micro for cost optimization)

# Security group for RDS
resource "aws_security_group" "rds_sg" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for COGNIX RDS"
  vpc_id      = aws_default_vpc.default.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restrict this in production
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "COGNIX RDS Security Group"
    Environment = var.environment
  }
}

# Default VPC (to save costs)
resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

# DB Subnet Group
resource "aws_db_subnet_group" "cognix_subnet" {
  name       = "${var.project_name}-db-subnet"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name        = "COGNIX DB Subnet Group"
    Environment = var.environment
  }
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [aws_default_vpc.default.id]
  }
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "cognix_db" {
  identifier             = "${var.project_name}-db-${var.environment}"
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = "db.t3.micro"  # ~$13/month
  allocated_storage      = 20             # 20GB
  storage_type           = "gp2"
  storage_encrypted      = true

  db_name  = "cognix"
  username = "cognixadmin"
  password = random_password.db_password.result

  db_subnet_group_name   = aws_db_subnet_group.cognix_subnet.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = true  # For development; disable in production

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  skip_final_snapshot       = true  # For development
  deletion_protection       = false # For development
  auto_minor_version_upgrade = true

  tags = {
    Name        = "COGNIX Database"
    Environment = var.environment
  }
}

# Random password for database
resource "random_password" "db_password" {
  length  = 16
  special = true
}

# Store password in Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "${var.project_name}-db-password-${var.environment}"

  tags = {
    Name        = "COGNIX DB Password"
    Environment = var.environment
  }
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    username = aws_db_instance.cognix_db.username
    password = random_password.db_password.result
    host     = aws_db_instance.cognix_db.address
    port     = aws_db_instance.cognix_db.port
    dbname   = aws_db_instance.cognix_db.db_name
  })
}

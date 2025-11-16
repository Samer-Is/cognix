# COGNIX AI - Development & Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or use Docker)
- AWS CLI configured
- Terraform 1.5+

### Local Development Setup

#### 1. Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup database (PostgreSQL)
# Create database: cognix
createdb cognix

# Run migrations
alembic upgrade head

# Start backend server
uvicorn main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/api/docs

#### 2. Frontend Setup

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### Environment Variables

Create `.env` file in project root (already created):
```
# AWS Configuration
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# AI API Keys
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cognix
```

## 🏗️ AWS Deployment

### Option 1: Full AWS Deployment with Terraform

```powershell
cd infrastructure

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply infrastructure (creates all AWS resources)
terraform apply

# Note the outputs:
# - API Gateway URL
# - Cognito User Pool ID
# - RDS Endpoint
```

### Option 2: Local Development with AWS Services

For development, you can use:
- Local PostgreSQL instead of RDS
- LocalStack for S3/DynamoDB simulation
- Direct API calls to Anthropic/OpenAI

## 📊 Data Generation

Generate realistic demo data for all 5 domains:

```powershell
cd backend
python scripts/generate_data.py --all

# Or generate specific domain:
python scripts/generate_data.py --domain telecom
python scripts/generate_data.py --domain banking
```

This creates CSV files and populates the database with sample data.

## 🧪 Testing

### Backend Tests
```powershell
cd backend
pytest tests/ -v --cov=.
```

### Frontend Tests
```powershell
cd frontend
npm run test
```

## 🔧 Project Structure

```
cognix/
├── backend/
│   ├── agents/              # Multi-agent system (5 agents)
│   │   ├── orchestrator.py  # LangGraph workflow
│   │   ├── welcoming_agent.py
│   │   ├── supervisor_agent.py
│   │   ├── data_manager_agent.py
│   │   ├── data_engineer_agent.py
│   │   └── analytics_expert_agent.py
│   ├── api/                 # FastAPI endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── chat.py          # Main chat endpoint
│   │   ├── domains.py       # Domain management
│   │   ├── insights.py      # Analytics insights
│   │   └── files.py         # File upload (RAG)
│   ├── database/            # Database models & schemas
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── connection.py    # DB connection
│   ├── services/            # Business logic
│   │   ├── analytics_service.py
│   │   └── rag_service.py
│   ├── utils/               # Utilities
│   │   └── config.py        # Configuration
│   ├── main.py              # FastAPI app entry
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── DomainSelector.tsx
│   │   │   └── AgentViewer.tsx
│   │   ├── pages/           # Page components
│   │   │   ├── ChatPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   └── DashboardPage.tsx
│   │   ├── services/        # API services
│   │   │   ├── api.ts
│   │   │   └── authService.ts
│   │   ├── stores/          # Zustand stores
│   │   │   ├── authStore.ts
│   │   │   └── domainStore.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── infrastructure/          # Terraform IaC
│   ├── main.tf              # Main configuration
│   ├── s3.tf                # S3 buckets
│   ├── dynamodb.tf          # DynamoDB tables
│   ├── rds.tf               # PostgreSQL RDS
│   ├── lambda.tf            # Lambda functions
│   ├── api_gateway.tf       # API Gateway
│   ├── cognito.tf           # User authentication
│   └── cloudwatch.tf        # Monitoring & logs
├── .env                     # Environment variables
├── .gitignore
└── README.md
```

## 🤖 AI Agents Architecture

### Agent Workflow (LangGraph)

```
User Query → Welcoming Agent → Can Handle?
                               ↓ No
                           Supervisor Agent
                               ↓
                    ┌──────────┼──────────┐
                    ↓          ↓          ↓
              Data Manager  Data Engineer  Analytics Expert
                    │          │          │
                    └──────────┼──────────┘
                               ↓
                          Supervisor (Finalize)
                               ↓
                           Response
```

### Agent Responsibilities:

1. **Welcoming Agent**: Greetings, navigation, platform help
2. **Supervisor Agent**: Orchestration, planning, validation
3. **Data Manager Agent**: Schema expertise, data relationships
4. **Data Engineer Agent**: Natural language to SQL, query execution
5. **Analytics Expert Agent**: Insights, visualizations, predictions

## 💰 Cost Breakdown

Target: < $20/month

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Lambda | 512MB, minimal invocations | $0-3 |
| API Gateway | HTTP API | $0-2 |
| RDS PostgreSQL | t3.micro, 20GB | $8-10 |
| DynamoDB | On-demand | $0-2 |
| S3 | Standard storage | $0-2 |
| Cognito | Free tier | $0 |
| CloudWatch | 7-day retention | $0-1 |
| **Total** | | **$8-20** |

## 🔐 Security Best Practices

1. **Never commit secrets**: Use `.env` files (already in .gitignore)
2. **Rotate API keys regularly**
3. **Use AWS Secrets Manager** in production
4. **Enable MFA** on AWS account
5. **Restrict S3 bucket access** (already configured)
6. **Use HTTPS only** (configured in API Gateway)
7. **Implement rate limiting** (configured)

## 📈 Scaling Considerations

When traffic grows beyond $20/month budget:

1. **Upgrade RDS**: t3.small or t3.medium
2. **Add ElastiCache**: For caching frequent queries
3. **Use Aurora Serverless**: Auto-scaling database
4. **Add CloudFront**: CDN for frontend
5. **Implement queuing**: SQS for async processing

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check database connection
psql -U postgres -d cognix -c "SELECT 1;"
```

### Frontend errors
```powershell
# Clear node_modules and reinstall
Remove-Item -Recurse -Force node_modules
npm install

# Clear vite cache
Remove-Item -Recurse -Force .vite
npm run dev
```

### AWS deployment issues
```powershell
# Check AWS credentials
aws sts get-caller-identity

# Verify Terraform state
terraform show

# Check logs
aws logs tail /aws/lambda/cognix-chat-handler --follow
```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Chat
- `POST /api/chat` - Send message to AI agents
- `GET /api/chat/history/{session_id}` - Get chat history
- `DELETE /api/chat/history/{session_id}` - Delete history

### Domains
- `GET /api/domains` - List all domains
- `GET /api/domains/{domain_name}` - Get domain info
- `POST /api/domains/select` - Select active domain
- `GET /api/domains/{domain_name}/schema` - Get schema

### Insights
- `POST /api/insights` - Generate automated insights

### Files
- `POST /api/files/upload` - Upload file for RAG
- `GET /api/files/list` - List uploaded files
- `DELETE /api/files/{file_id}` - Delete file

## 🎯 Next Steps

1. **Generate Demo Data**: Run data generation scripts
2. **Create First User**: Register through frontend
3. **Select Domain**: Choose from 5 domains
4. **Start Chatting**: Ask questions about your data
5. **View Agent Activity**: Watch AI agents collaborate

## 📞 Support

- GitHub Repository: https://github.com/Samer-Is/cognix
- Issues: https://github.com/Samer-Is/cognix/issues

## 📄 License

MIT License - See LICENSE file for details

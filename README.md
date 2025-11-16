# COGNIX AI

Intelligent Multi-Domain Data Analytics Platform with AI Agents

## Overview

COGNIX AI is an AI-powered analytics platform that provides intelligent business insights across multiple domains (Telecom, Banking, Digital Marketing, Healthcare, FMCG) through a conversational interface. The system features autonomous AI agents, predictive analytics, and real-time visualization capabilities.

## Architecture

- **Backend**: Python 3.11+ with FastAPI, LangGraph for multi-agent orchestration
- **Frontend**: React 18+ with TypeScript, Tailwind CSS, Recharts
- **Infrastructure**: AWS (Lambda, API Gateway, DynamoDB, RDS PostgreSQL, S3, Cognito)
- **AI**: Anthropic Claude API (claude-sonnet-4), OpenAI GPT-4

## Project Structure

```
cognix/
├── backend/                 # FastAPI backend
│   ├── agents/             # Multi-agent system
│   ├── api/                # API endpoints
│   ├── database/           # Database models and migrations
│   ├── services/           # Business logic
│   └── utils/              # Utilities
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   └── utils/         # Utilities
├── infrastructure/         # Terraform IaC
├── data/                   # CSV datasets and generators
└── docs/                   # Documentation
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- AWS CLI configured
- Terraform 1.5+

### Environment Variables
Create `.env` file in backend/ directory:
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
DATABASE_URL=postgresql://...
```

### Installation

1. **Backend Setup**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Frontend Setup**
```bash
cd frontend
npm install
```

3. **Infrastructure Deployment**
```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

## Development

### Run Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Run Frontend
```bash
cd frontend
npm run dev
```

## Features

- ✅ Multi-agent AI system with 5 specialized agents
- ✅ Natural language to SQL conversion
- ✅ Predictive analytics and anomaly detection
- ✅ Real-time agent interaction viewer
- ✅ Multi-domain support (5 industries)
- ✅ RAG for custom document uploads
- ✅ Interactive visualizations
- ✅ Conversation memory
- ✅ AWS serverless deployment (<$20/month)

## Cost Breakdown

- Lambda: $0-5/month
- RDS PostgreSQL (t3.micro): $0-8/month
- DynamoDB: $0-2/month
- S3: $0-2/month
- API Gateway: $0-3/month
- **Total**: <$20/month

## License

MIT

## Repository

https://github.com/Samer-Is/cognix

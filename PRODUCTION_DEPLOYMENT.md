# Cognix AI Platform - Production Deployment

## ✅ GitHub Repository
- **URL**: https://github.com/Samer-Is/cognix
- **Status**: Code published and up to date

## 🚀 Production Deployment (In Progress)

### Backend API Deployment
**Target**: AWS ECS with Fargate (containerized FastAPI)

**Deployment Steps**:
1. ✅ Remove PyTorch dependency causing DLL errors
2. ✅ Create Dockerfile for backend container
3. 🔄 Build and push Docker image to ECR
4. 🔄 Deploy to ECS Fargate cluster
5. ⏳ Configure load balancer for HTTPS access
6. ⏳ Connect to AWS resources (S3, DynamoDB, Cognito)

**Expected Production URL**: `https://api.cognix.[domain].com`

### Frontend Deployment
**Target**: AWS Amplify (automated React deployment)

**Deployment Steps**:
1. ⏳ Connect GitHub repository to Amplify
2. ⏳ Configure build settings
3. ⏳ Set environment variables (backend API URL)
4. ⏳ Deploy and get production URL

**Expected Production URL**: `https://main.[app-id].amplifyapp.com`

## 📦 AWS Infrastructure Status

### ✅ Deployed Resources
- **S3 Buckets**: cognix-uploads-dev, cognix-data-dev
- **DynamoDB Tables**: cognix-users-dev, cognix-activity-dev, cognix-agent-memory-dev
- **Cognito**: User Pool (us-east-1_n7x6ggn6Y)
- **API Gateway**: n3go6oxxi3 (to be connected to ECS)
- **CloudWatch**: Cost alarms and monitoring

### 🔄 In Progress
- **ECS Cluster**: Backend container deployment
- **Application Load Balancer**: HTTPS endpoint for backend
- **Amplify**: Frontend hosting and CI/CD

### ❌ Not Using
- **Lambda**: Using ECS instead (better for FastAPI)
- **RDS**: Using DynamoDB only (free tier, serverless)

## 💰 Estimated Costs
- **ECS Fargate**: ~$15-30/month (1 vCPU, 2GB RAM)
- **S3**: ~$1-5/month
- **DynamoDB**: Free tier (on-demand)
- **Amplify**: Free tier
- **Total**: ~$20-40/month

## 🎯 Next Steps
1. Deploy backend container to ECS
2. Configure load balancer and domain
3. Deploy frontend to Amplify
4. End-to-end testing
5. Provide production URLs to user

## 📝 Environment Variables Required

### Backend (.env)
```
AWS_ACCESS_KEY_ID=[from AWS credentials]
AWS_SECRET_ACCESS_KEY=[from AWS credentials]
AWS_REGION=us-east-1
S3_BUCKET=cognix-uploads-dev
DYNAMODB_TABLE_PREFIX=cognix
COGNITO_USER_POOL_ID=us-east-1_n7x6ggn6Y
COGNITO_CLIENT_ID=16hcotdh8jqpsa9fe60lioe7to
ANTHROPIC_API_KEY=[user's key]
OPENAI_API_KEY=[user's key]
```

### Frontend (.env)
```
REACT_APP_API_URL=https://api.cognix.[domain].com
REACT_APP_WS_URL=wss://api.cognix.[domain].com
```

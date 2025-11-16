# 🚀 COGNIX AI - Quick Start Guide

## Get Running in 5 Minutes

### Step 1: Install Dependencies

```powershell
# Run automated setup script
.\setup.ps1
```

This will:
- ✅ Check prerequisites (Python, Node.js, Git)
- ✅ Create Python virtual environment
- ✅ Install backend dependencies
- ✅ Install frontend dependencies
- ✅ Setup database (if PostgreSQL available)

### Step 2: Generate Demo Data

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python scripts/generate_data.py --all
```

This creates realistic data for all 5 domains.

### Step 3: Start Backend

```powershell
# In terminal 1
cd backend
uvicorn main:app --reload --port 8000
```

Backend API will run at: http://localhost:8000  
Swagger Docs: http://localhost:8000/api/docs

### Step 4: Start Frontend

```powershell
# In terminal 2
cd frontend
npm run dev
```

Frontend will run at: http://localhost:3000

### Step 5: Use the App

1. **Open** http://localhost:3000
2. **Register** a new account
3. **Select** a domain (Telecom, Banking, etc.)
4. **Start chatting** with COGNIX AI!
5. **Watch** the AI agents collaborate in real-time

---

## 🎯 Try These Queries

### Telecom Domain
```
"Show me the total number of active customers"
"What's the average call duration?"
"Which plan type is most popular?"
"Show customer churn trends"
```

### Banking Domain
```
"How many transactions happened this month?"
"What's the average account balance?"
"Show me fraud alerts"
"Analyze transaction patterns"
```

### Digital Marketing Domain
```
"What's our best performing campaign?"
"Calculate the average CTR"
"Show conversion rates by channel"
"Compare campaign ROI"
```

### Healthcare Domain
```
"How many appointments this week?"
"What's the bed occupancy rate?"
"Show patient demographics"
"Analyze appointment patterns"
```

### FMCG Domain
```
"What are our top selling products?"
"Show inventory levels"
"Calculate sales velocity"
"Analyze pricing trends"
```

---

## 🐛 Troubleshooting

### Backend won't start?
```powershell
# Check database is running
psql -U postgres -c "SELECT 1;"

# Check .env file has correct values
cat .env

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend errors?
```powershell
# Clear and reinstall
Remove-Item -Recurse -Force node_modules
npm install

# Clear cache
Remove-Item -Recurse -Force .vite
```

### Database connection issues?
```powershell
# Use Docker PostgreSQL
docker run --name cognix-postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=cognix `
  -p 5432:5432 `
  -d postgres:15
```

---

## 📚 Learn More

- **Full Guide**: See `DEPLOYMENT_GUIDE.md`
- **Project Summary**: See `PROJECT_SUMMARY.md`
- **API Docs**: http://localhost:8000/api/docs
- **GitHub**: https://github.com/Samer-Is/cognix

---

## 🎉 You're Ready!

COGNIX AI is now running locally. Explore the multi-agent system, try different domains, and watch AI agents collaborate to answer your questions!

**Need Help?** Check the troubleshooting section or open an issue on GitHub.

Happy analyzing! 📊✨

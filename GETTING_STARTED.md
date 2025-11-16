# 🚀 COGNIX AI - Quick Start Guide

## Option 1: Run with SQLite (No PostgreSQL Setup Required)

### 1. Update Database Configuration

Edit `backend/.env` and change:
```bash
# From:
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cognix

# To:
DATABASE_URL=sqlite+aiosqlite:///./cognix.db
```

### 2. Install SQLite Driver
```powershell
pip install aiosqlite
```

### 3. Start the Backend
```powershell
cd backend
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000
Swagger UI: http://localhost:8000/docs

### 4. Test the API
Open a new terminal:
```powershell
cd ..
python test_api.py
```

---

## Option 2: Full Setup with PostgreSQL

### 1. Install PostgreSQL

Download from: https://www.postgresql.org/download/windows/

Or use Chocolatey:
```powershell
choco install postgresql
```

### 2. Create Database
```powershell
psql -U postgres
CREATE DATABASE cognix;
\q
```

### 3. Initialize Database with Demo Data
```powershell
cd backend
python scripts/init_database.py
```

### 4. Start Backend
```powershell
uvicorn main:app --reload
```

### 5. Test
```powershell
cd ..
python test_api.py
```

---

## Frontend Setup (Optional)

### 1. Install Node.js
Download from: https://nodejs.org/

### 2. Install Dependencies
```powershell
cd frontend
npm install
```

### 3. Start Development Server
```powershell
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## Quick Test Without Frontend

Once the backend is running, you can:

1. **Visit Swagger UI**: http://localhost:8000/docs
2. **Run test script**: `python test_api.py`
3. **Use curl/httpx**: 
   ```powershell
   curl http://localhost:8000/health
   ```

---

## Troubleshooting

### Database Connection Error
- **Solution**: Use SQLite option (see Option 1 above)
- Check `DATABASE_URL` in `.env`

### Port Already in Use
```powershell
# Use different port
uvicorn main:app --reload --port 8001
```

### Missing Dependencies
```powershell
pip install -r requirements.txt
```

### API Key Errors
Check `.env` file has valid keys:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`

---

## Example Chat Queries

Once running, try these:

**Telecom Domain:**
- "Show me customers with high data usage"
- "What's the average call duration by plan type?"
- "Detect anomalies in customer behavior"

**Banking Domain:**
- "List top 10 accounts by balance"
- "Show transaction trends over time"
- "Identify accounts with suspicious activity"

**Marketing Domain:**
- "Compare campaign performance"
- "What's the average CTR by channel?"
- "Forecast campaign ROI"

**Healthcare Domain:**
- "Show appointment patterns"
- "Find patients with missed appointments"
- "Analyze wait times by doctor"

**FMCG Domain:**
- "Top selling products this month"
- "Inventory levels by warehouse"
- "Predict stock requirements"

---

## Project Structure

```
COGNEX_AI1/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── agents/              # 5 AI agents
│   ├── api/                 # REST endpoints
│   ├── database/            # Models & schemas
│   ├── services/            # Business logic
│   └── scripts/             # Utilities
├── frontend/
│   └── src/                 # React app
├── infrastructure/          # AWS Terraform
├── data/
│   └── generated/           # Demo CSV files
└── test_api.py             # API test script
```

---

## Next Steps

1. ✅ Run backend with SQLite
2. ✅ Test with `test_api.py`
3. ⚠️ Install Node.js for frontend
4. ⚠️ Configure AWS for production deployment

---

## Support

For issues:
1. Check logs: `tail -f backend/logs/app.log`
2. Verify environment: `cat backend/.env`
3. Test health: `curl http://localhost:8000/health`

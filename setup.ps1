# COGNIX AI - Complete Setup Script for Windows PowerShell
# This script sets up the entire project from scratch

Write-Host "🚀 COGNIX AI - Automated Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check Git
try {
    $gitVersion = git --version
    Write-Host "✅ Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found. Please install Git" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Setting up backend..." -ForegroundColor Yellow

# Backend Setup
if (Test-Path "backend/venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
} else {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv backend/venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& backend/venv/Scripts/Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install -r backend/requirements.txt --quiet

Write-Host "✅ Backend setup complete" -ForegroundColor Green

Write-Host ""
Write-Host "🎨 Setting up frontend..." -ForegroundColor Yellow

# Frontend Setup
Set-Location frontend

if (Test-Path "node_modules") {
    Write-Host "Node modules already installed" -ForegroundColor Yellow
} else {
    Write-Host "Installing npm dependencies..." -ForegroundColor Cyan
    npm install
}

Set-Location ..

Write-Host "✅ Frontend setup complete" -ForegroundColor Green

Write-Host ""
Write-Host "🗄️  Database setup..." -ForegroundColor Yellow

# Check if PostgreSQL is available
try {
    $pgVersion = psql --version
    Write-Host "✅ PostgreSQL: $pgVersion" -ForegroundColor Green
    
    Write-Host "Creating database..." -ForegroundColor Cyan
    # Create database if it doesn't exist
    $null = psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'cognix'" 2>&1
    if ($LASTEXITCODE -ne 0) {
        createdb -U postgres cognix
        Write-Host "✅ Database 'cognix' created" -ForegroundColor Green
    } else {
        Write-Host "Database 'cognix' already exists" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  PostgreSQL not found. You'll need to set up the database manually" -ForegroundColor Yellow
    Write-Host "   Or use Docker: docker run --name cognix-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Review .env file and add your API keys" -ForegroundColor White
Write-Host "2. Start backend: cd backend; uvicorn main:app --reload" -ForegroundColor White
Write-Host "3. Start frontend: cd frontend; npm run dev" -ForegroundColor White
Write-Host "4. Open browser: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation: See DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
Write-Host "🌐 GitHub: https://github.com/Samer-Is/cognix" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 Happy coding!" -ForegroundColor Magenta

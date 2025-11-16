"""
COGNIX AI - Main FastAPI Application
Multi-Domain Data Analytics Platform with AI Agents
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from api import chat, domains, auth, insights, files
from database.connection import engine, Base
from utils.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan manager"""
    logger.info("🚀 Starting COGNIX AI...")
    
    # Create database tables
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    yield
    
    logger.info("👋 Shutting down COGNIX AI...")
    await engine.dispose()


# Initialize FastAPI app
app = FastAPI(
    title="COGNIX AI",
    description="Intelligent Multi-Domain Data Analytics Platform with AI Agents",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "COGNIX AI",
        "version": "1.0.0",
        "environment": settings.environment
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to COGNIX AI",
        "description": "Intelligent Multi-Domain Data Analytics Platform",
        "docs": "/api/docs",
        "health": "/health"
    }


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(domains.router, prefix="/api/domains", tags=["Domains"])
app.include_router(insights.router, prefix="/api/insights", tags=["Insights"])
app.include_router(files.router, prefix="/api/files", tags=["Files"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )

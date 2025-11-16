"""
Simple database initialization for SQLite
Creates tables using SQLAlchemy models
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import engine, Base
from database.models import User, ActivityLog, SavedQuery, Alert, Conversation, UploadedFile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db():
    """Create all tables"""
    
    logger.info("=" * 60)
    logger.info("COGNIX AI - Database Initialization (SQLite)")
    logger.info("=" * 60)
    
    async with engine.begin() as conn:
        logger.info("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ All tables created successfully!")
    logger.info("=" * 60)
    
    # Show tables created
    tables = [
        "users",
        "activity_logs", 
        "saved_queries",
        "alerts",
        "conversations",
        "uploaded_files"
    ]
    
    logger.info("\n📋 Tables created:")
    for table in tables:
        logger.info(f"   ✓ {table}")
    
    logger.info("\n🎉 Database is ready to use!")
    logger.info("Start the server with: uvicorn main:app --reload")


if __name__ == "__main__":
    asyncio.run(init_db())

"""
Database connection and session management
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from utils.config import settings
import logging

logger = logging.getLogger(__name__)

# Create async engine
# Support both PostgreSQL and SQLite
db_url = settings.database_url

if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(
        db_url,
        echo=settings.debug,
        future=True,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
elif db_url.startswith("sqlite"):
    # SQLite configuration
    if not db_url.startswith("sqlite+aiosqlite"):
        db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")
    engine = create_async_engine(
        db_url,
        echo=settings.debug,
        future=True,
        connect_args={"check_same_thread": False}
    )
else:
    # Default PostgreSQL
    engine = create_async_engine(
        db_url,
        echo=settings.debug,
        future=True
    )

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

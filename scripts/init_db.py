"""
Script to initialize the database with the required tables.
"""

import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from infrastructure.db.models import Base
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db():
    """Initialize the database."""
    logger.info("Creating database tables...")

    # Create engine
    engine = create_async_engine(
        config.DATABASE_URL,
        echo=True,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

    logger.info("Database tables created!")


if __name__ == "__main__":
    asyncio.run(init_db())

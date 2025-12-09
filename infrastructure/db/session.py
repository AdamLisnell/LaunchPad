from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import config

# Create engine
engine = create_async_engine(
    config.DATABASE_URL,
    echo=config.ENVIRONMENT == "development",
    future=True,
)

# Create session factory
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Get a database session."""
    async with async_session_factory() as session:
        yield session

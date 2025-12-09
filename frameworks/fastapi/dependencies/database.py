from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.session import get_session

# Export session dependency
get_db_session = get_session

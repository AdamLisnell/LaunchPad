from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.ports.repositories.candidate_repository import CandidateRepository
from core.ports.repositories.job_repository import JobRepository
from core.ports.repositories.requirement_repository import RequirementRepository
from repository_factory import repository_factory
from infrastructure.db.database import get_db


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async for session in get_db():
        yield session


def get_candidate_repository(
    session: AsyncSession = Depends(get_db_session)
) -> CandidateRepository:
    """Get Candidate repository dependency."""
    return repository_factory.get(CandidateRepository, session=session)


def get_job_repository(
    session: AsyncSession = Depends(get_db_session)
) -> JobRepository:
    """Get Job repository dependency."""
    return repository_factory.get(JobRepository, session=session)


def get_requirement_repository(
    session: AsyncSession = Depends(get_db_session)
) -> RequirementRepository:
    """Get Requirement repository dependency."""
    return repository_factory.get(RequirementRepository, session=session)
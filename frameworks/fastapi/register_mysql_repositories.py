"""
Register MySQL repositories in the application.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.ports.repositories.candidate_repository import CandidateRepository
from core.ports.repositories.job_repository import JobRepository
from core.ports.repositories.requirement_repository import RequirementRepository

from adapters.repositories.mysql.mysql_candidate_repository import MySQLCandidateRepository
from adapters.repositories.mysql.mysql_job_repository import MySQLJobRepository
from adapters.repositories.mysql.mysql_requirement_repository import (
    MySQLRequirementRepository,
)

from frameworks.fastapi.dependencies.database import get_db_session
from repository_factory import repository_factory


def register_mysql_repositories():
    """Register MySQL repositories in the repository factory."""
    
    # Create factory functions
    def get_mysql_candidate_repository(
        session: AsyncSession = Depends(get_db_session),
    ) -> CandidateRepository:
        return MySQLCandidateRepository(session)

    def get_mysql_job_repository(
        session: AsyncSession = Depends(get_db_session),
    ) -> JobRepository:
        return MySQLJobRepository(session)

    def get_mysql_requirement_repository(
        session: AsyncSession = Depends(get_db_session),
    ) -> RequirementRepository:
        return MySQLRequirementRepository(session)

    # Register repositories
    repository_factory.register(
        CandidateRepository, get_mysql_candidate_repository, "mysql"
    )
    repository_factory.register(JobRepository, get_mysql_job_repository, "mysql")
    repository_factory.register(
        RequirementRepository, get_mysql_requirement_repository, "mysql"
    )
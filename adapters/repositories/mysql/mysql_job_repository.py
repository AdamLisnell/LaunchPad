from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from core.domain.job import Job
from core.ports.repositories.job_repository import JobRepository
from adapters.repositories.mysql.mysql_repository import MySQLRepository
from infrastructure.db.models import JobModel


class MySQLJobRepository(MySQLRepository[Job, JobModel], JobRepository):
    """MySQL implementation of Job repository."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, JobModel, Job)

    async def find_by_category(self, category: str) -> List[Job]:
        """Find jobs by category."""
        result = await self.session.execute(
            select(JobModel).where(JobModel.category == category)
        )
        models = result.scalars().all()
        return [model.to_domain() for model in models]

    async def find_available(self, current_date: Optional[date] = None) -> List[Job]:
        """Find jobs that are still available for application."""
        if current_date is None:
            current_date = date.today()
        result = await self.session.execute(
            select(JobModel).where(
                or_(
                    JobModel.application_end_date.is_(None),
                    JobModel.application_end_date >= current_date
                )
            )
        )
        models = result.scalars().all()
        return [model.to_domain() for model in models]
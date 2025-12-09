from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.domain.candidate import Candidate
from core.ports.repositories.candidate_repository import CandidateRepository
from adapters.repositories.mysql.mysql_repository import MySQLRepository
from infrastructure.db.models import CandidateModel


class MySQLCandidateRepository(MySQLRepository[Candidate, CandidateModel], CandidateRepository):
    """MySQL implementation of Candidate repository."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, CandidateModel, Candidate)

    async def find_by_location(self, location: str) -> List[Candidate]:
        """Find candidates by location."""
        result = await self.session.execute(
            select(CandidateModel).where(CandidateModel.location == location)
        )
        models = result.scalars().all()
        return [model.to_domain() for model in models]
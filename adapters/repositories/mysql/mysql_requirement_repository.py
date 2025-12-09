from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc

from core.domain.requirement import Requirement
from core.ports.repositories.requirement_repository import RequirementRepository
from adapters.repositories.mysql.mysql_repository import MySQLRepository
from infrastructure.db.models import RequirementModel


class MySQLRequirementRepository(
    MySQLRepository[Requirement, RequirementModel], RequirementRepository
):
    """MySQL implementation of Requirement repository."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, RequirementModel, Requirement)

    async def find_by_order(self) -> List[Requirement]:
        """Find requirements ordered by their order field."""
        result = await self.session.execute(
            select(RequirementModel).order_by(asc(RequirementModel.order))
        )
        models = result.scalars().all()
        return [model.to_domain() for model in models]
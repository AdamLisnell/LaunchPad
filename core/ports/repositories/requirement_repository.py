from typing import List, Optional

from core.domain.requirement import Requirement
from core.ports.repositories.base_repository import BaseRepository


class RequirementRepository(BaseRepository[Requirement]):
    """Repository interface for Requirement entities."""

    async def find_by_order(self) -> List[Requirement]:
        """Find requirements ordered by their order field."""
        pass

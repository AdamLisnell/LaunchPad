from typing import List, Optional

from core.domain.requirement import Requirement
from core.ports.repositories.requirement_repository import RequirementRepository
from adapters.repositories.memory.memory_repository import MemoryRepository


class MemoryRequirementRepository(MemoryRepository[Requirement], RequirementRepository):
    """Memory implementation of Requirement repository."""

    async def find_by_order(self) -> List[Requirement]:
        """Find requirements ordered by their order field."""
        return sorted(self._storage.values(), key=lambda q: q.order)
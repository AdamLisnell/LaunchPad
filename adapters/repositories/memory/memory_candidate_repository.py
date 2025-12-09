from typing import List, Optional

from core.domain.candidate import Candidate
from core.ports.repositories.candidate_repository import CandidateRepository
from adapters.repositories.memory.memory_repository import MemoryRepository


class MemoryCandidateRepository(MemoryRepository[Candidate], CandidateRepository):
    """Memory implementation of Candidate repository."""

    async def find_by_location(self, location: str) -> List[Candidate]:
        """Find candidates by location."""
        return [
            candidate for candidate in self._storage.values() if candidate.location == location
        ]
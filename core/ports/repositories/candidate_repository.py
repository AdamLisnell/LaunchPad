from typing import List, Optional

from core.domain.candidate import Candidate
from core.ports.repositories.base_repository import BaseRepository


class CandidateRepository(BaseRepository[Candidate]):
    """Repository interface for Candidate entities."""

    async def find_by_location(self, location: str) -> List[Candidate]:
        """Find candidates by location."""
        pass
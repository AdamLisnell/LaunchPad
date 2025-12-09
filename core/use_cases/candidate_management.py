from typing import List, Optional

from core.domain.candidate import Candidate
from core.ports.repositories.candidate_repository import CandidateRepository


class CandidateManagement:
    """Use case for managing candidates."""

    def __init__(self, candidate_repository: CandidateRepository):
        self.candidate_repository = candidate_repository

    async def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        """Get a Candidate by id."""
        return await self.candidate_repository.get(candidate_id)

    async def list_candidates(self, skip: int = 0, limit: int = 100) -> List[Candidate]:
        """List candidates with pagination."""
        return await self.candidate_repository.list(skip, limit)

    async def create_candidate(self, candidate: Candidate) -> Candidate:
        """Create a new Candidate."""
        return await self.candidate_repository.create(candidate)

    async def update_candidate(
        self, candidate_id: str, candidate: Candidate
    ) -> Optional[Candidate]:
        """Update a Candidate."""
        return await self.candidate_repository.update(candidate_id, candidate)

    async def delete_candidate(self, candidate_id: str) -> bool:
        """Delete a Candidate."""
        return await self.candidate_repository.delete(candidate_id)

    async def get_candidates_by_location(self, location: str) -> List[Candidate]:
        """Get candidates by location."""
        return await self.candidate_repository.find_by_location(location)
from typing import List, Optional

from core.domain.requirement import Requirement
from core.ports.repositories.requirement_repository import RequirementRepository


class RequirementManagement:
    """Use case for managing requirements."""

    def __init__(self, requirement_repository: RequirementRepository):
        self.requirement_repository = requirement_repository

    async def get_requirement(self, requirement_id: str) -> Optional[Requirement]:
        """Get a Requirement by id."""
        return await self.requirement_repository.get(requirement_id)

    async def list_requirements(self, skip: int = 0, limit: int = 100) -> List[Requirement]:
        """List requirements with pagination."""
        return await self.requirement_repository.list(skip, limit)

    async def create_requirement(self, requirement: Requirement) -> Requirement:
        """Create a new Requirement."""
        return await self.requirement_repository.create(requirement)

    async def update_requirement(
        self, requirement_id: str, requirement: Requirement
    ) -> Optional[Requirement]:
        """Update a Requirement."""
        return await self.requirement_repository.update(requirement_id, requirement)

    async def delete_requirement(self, requirement_id: str) -> bool:
        """Delete a Requirement."""
        return await self.requirement_repository.delete(requirement_id)

    async def get_ordered_requirements(self) -> List[Requirement]:
        """Get requirements ordered by their order field."""
        return await self.requirement_repository.find_by_order()
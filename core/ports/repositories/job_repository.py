from datetime import date
from typing import List, Optional

from core.domain.job import Job
from core.ports.repositories.base_repository import BaseRepository


class JobRepository(BaseRepository[Job]):
    """Repository interface for Job entities."""

    async def find_by_category(self, category: str) -> List[Job]:
        """Find jobs by category."""
        pass

    async def find_available(self, current_date: date = None) -> List[Job]:
        """Find jobs that are still available for application."""
        pass

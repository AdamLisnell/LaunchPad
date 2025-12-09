from datetime import date
from typing import List, Optional

from core.domain.job import Job
from core.ports.repositories.job_repository import JobRepository
from adapters.repositories.memory.memory_repository import MemoryRepository


class MemoryJobRepository(MemoryRepository[Job], JobRepository):
    """Memory implementation of Job repository."""

    async def find_by_category(self, category: str) -> List[Job]:
        """Find jobs by category."""
        return [job for job in self._storage.values() if job.category == category]

    async def find_available(self, current_date: Optional[date] = None) -> List[Job]:
        """Find jobs that are still available for application."""
        if current_date is None:
            current_date = date.today()
        return [
            job
            for job in self._storage.values()
            if job.application_end_date is None
            or job.application_end_date >= current_date
        ]
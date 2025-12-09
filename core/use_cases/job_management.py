from datetime import date
from typing import List, Optional

from core.domain.job import Job
from core.ports.repositories.job_repository import JobRepository


class JobManagement:
    """Use case for managing jobs."""

    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    async def get_job(self, job_id: str) -> Optional[Job]:
        """Get a Job by id."""
        return await self.job_repository.get(job_id)

    async def list_jobs(self, skip: int = 0, limit: int = 100) -> List[Job]:
        """List jobs with pagination."""
        return await self.job_repository.list(skip, limit)

    async def create_job(self, job: Job) -> Job:
        """Create a new Job."""
        return await self.job_repository.create(job)

    async def update_job(self, job_id: str, job: Job) -> Optional[Job]:
        """Update a Job."""
        return await self.job_repository.update(job_id, job)

    async def delete_job(self, job_id: str) -> bool:
        """Delete a Job."""
        return await self.job_repository.delete(job_id)

    async def get_jobs_by_category(self, category: str) -> List[Job]:
        """Get jobs by category."""
        return await self.job_repository.find_by_category(category)

    async def get_available_jobs(self) -> List[Job]:
        """Get available jobs."""
        return await self.job_repository.find_available()
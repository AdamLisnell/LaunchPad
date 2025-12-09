from fastapi import Depends

from core.use_cases.candidate_management import CandidateManagement
from core.use_cases.job_management import JobManagement
from core.use_cases.requirement_management import RequirementManagement
from core.use_cases.match_jobs import MatchJobs 
from core.ports.repositories.candidate_repository import CandidateRepository
from core.ports.repositories.job_repository import JobRepository 

from frameworks.fastapi.dependencies.repositories import (
    get_candidate_repository,
    get_job_repository,
    get_requirement_repository,
)


def get_candidate_management(
    candidate_repository=Depends(get_candidate_repository),
) -> CandidateManagement:
    """Get Candidate management use case dependency."""
    return CandidateManagement(candidate_repository)


def get_job_management(
    job_repository=Depends(get_job_repository),
) -> JobManagement:
    """Get Job management use case dependency."""
    return JobManagement(job_repository)


def get_requirement_management(
    requirement_repository=Depends(get_requirement_repository),
) -> RequirementManagement:
    """Get Requirement management use case dependency."""
    return RequirementManagement(requirement_repository)


def get_match_jobs(
    job_repo: JobRepository = Depends(get_job_repository),
    candidate_repo: CandidateRepository = Depends(get_candidate_repository),
) -> MatchJobs:
    from core.services.embedding_service import EmbeddingService
    embedding_service = EmbeddingService()
    return MatchJobs(job_repo, candidate_repo, embedding_service)
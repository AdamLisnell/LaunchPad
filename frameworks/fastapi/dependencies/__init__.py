from core.services.embedding_service import EmbeddingService

from frameworks.fastapi.dependencies.repositories import (
    get_candidate_repository,
    get_job_repository,
    get_requirement_repository,
)
from frameworks.fastapi.dependencies.use_cases import (
    get_candidate_management,
    get_job_management,
    get_requirement_management,
    get_match_jobs,
)
from frameworks.fastapi.dependencies.database import get_db_session


__all__ = [
    "get_candidate_repository",
    "get_job_repository",
    "get_requirement_repository",
    "get_candidate_management",
    "get_job_management",
    "get_requirement_management",
    "get_match_jobs",
    "get_db_session",
]
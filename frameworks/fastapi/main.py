import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import config
from frameworks.fastapi.routes import candidates, jobs, match, requirements

logger = logging.getLogger(__name__)


def register_memory_repositories(app: FastAPI):
    """Register memory repositories (data in RAM - resets on restart)."""
    from repository_factory import repository_factory
    from core.ports.repositories.candidate_repository import CandidateRepository
    from core.ports.repositories.job_repository import JobRepository
    from core.ports.repositories.requirement_repository import RequirementRepository
    from adapters.repositories.memory.memory_candidate_repository import MemoryCandidateRepository
    from adapters.repositories.memory.memory_job_repository import MemoryJobRepository
    from adapters.repositories.memory.memory_requirement_repository import MemoryRequirementRepository
    
    repository_factory.register(CandidateRepository, MemoryCandidateRepository)
    repository_factory.register(JobRepository, MemoryJobRepository)
    repository_factory.register(RequirementRepository, MemoryRequirementRepository)
    logger.info("✅ Using Memory repositories (data will reset on restart)")


def register_mysql_repositories(app: FastAPI):
    """Register MySQL repositories (data persists in MySQL database)."""
    from repository_factory import repository_factory
    from core.ports.repositories.candidate_repository import CandidateRepository
    from core.ports.repositories.job_repository import JobRepository
    from core.ports.repositories.requirement_repository import RequirementRepository
    from adapters.repositories.mysql.mysql_candidate_repository import MySQLCandidateRepository
    from adapters.repositories.mysql.mysql_job_repository import MySQLJobRepository
    from adapters.repositories.mysql.mysql_requirement_repository import MySQLRequirementRepository
    
    repository_factory.register(CandidateRepository, MySQLCandidateRepository)
    repository_factory.register(JobRepository, MySQLJobRepository)
    repository_factory.register(RequirementRepository, MySQLRequirementRepository)
    logger.info("✅ Using MySQL repositories (data persists in MySQL database)")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="LaunchPad API",
        description="API for matching candidates with jobs using AI-powered semantic matching",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For development; restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register repositories - Production setup with MySQL
    register_mysql_repositories(app)

    # Startup event to initialize database
    @app.on_event("startup")
    async def startup_event():
        """Initialize database on startup."""
        from infrastructure.db.database import init_db
        await init_db()
        logger.info("✅ Database tables initialized")

    # Include routers
    app.include_router(candidates.router, prefix=config.API_PREFIX)
    app.include_router(jobs.router, prefix=config.API_PREFIX)
    app.include_router(requirements.router, prefix=config.API_PREFIX)
    app.include_router(match.router, prefix=config.API_PREFIX)

    @app.get("/")
    async def root():
        return {"message": "Welcome to LaunchPad API - AI-Powered Job Matching"}

    @app.get("/healthz")
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()
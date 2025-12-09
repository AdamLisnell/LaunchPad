import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date
from core.domain.job import Job
from core.use_cases.job_management import JobManagement


@pytest.mark.asyncio
async def test_get_job():
    # Create mock repository
    mock_repo = AsyncMock()
    mock_repo.get.return_value = Job(id="123", title="Research Job")

    # Create use case with mock
    use_case = JobManagement(mock_repo)

    # Test get_job
    Job = await use_case.get_job("123")

    # Assert repository was called correctly
    mock_repo.get.assert_called_once_with("123")

    # Assert result is correct
    assert Job.id == "123"
    assert Job.title == "Research Job"


@pytest.mark.asyncio
async def test_get_available_jobs():
    # Create mock repository
    mock_repo = AsyncMock()
    today = date.today()
    mock_repo.find_available.return_value = [
        Job(id="123", title="Research Job", application_end_date=today)
    ]

    # Create use case with mock
    use_case = JobManagement(mock_repo)

    # Test get_available_jobs
    jobs = await use_case.get_available_jobs()

    # Assert repository was called correctly
    mock_repo.find_available.assert_called_once()

    # Assert result is correct
    assert len(jobs) == 1
    assert jobs[0].id == "123"
    assert jobs[0].title == "Research Job"

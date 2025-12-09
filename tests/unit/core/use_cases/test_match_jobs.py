import pytest
from unittest.mock import AsyncMock
from datetime import date
from core.domain.candidate import Candidate
from core.domain.job import Job
from core.use_cases.match_jobs import MatchJobs


@pytest.mark.asyncio
async def test_match_jobs_for_profile():
    # Create mock repository
    mock_repo = AsyncMock()
    mock_repo.find_available.return_value = [
        Job(
            id="123",
            title="Research Job",
            description="Job for science research",
            eligibility={"region": "North", "education": "PhD"},
        ),
        Job(
            id="456",
            title="Art Job",
            description="Job for art projects",
            eligibility={"region": "South"},
        ),
    ]

    # Create use case with mock
    use_case = MatchJobs(mock_repo)

    # Test matching with matching Candidate
    Candidate = Candidate(
        id="user1", education="PhD", region="North", interests=["Science"]
    )

    matches = await use_case.match_jobs_for_profile(Candidate)

    # Assert repository was called correctly
    mock_repo.find_available.assert_called_once()

    # Assert results are correct
    assert len(matches) > 0  # Should match at least one Job
    assert (
        matches[0]["Job"].id == "123"
    )  # Research Job should match with higher score
    assert matches[0]["score"] > 0
    assert len(matches[0]["match_reasons"]) > 0


@pytest.mark.asyncio
async def test_fallback_match():
    # Create mock repository
    mock_repo = AsyncMock()
    mock_repo.list.return_value = [
        Job(
            id="123", title="Science Research Job", description="Job for research"
        ),
        Job(id="456", title="Art Project Funding", description="Job for art"),
    ]

    # Create use case with mock
    use_case = MatchJobs(mock_repo)

    # Test fallback matching
    Candidate = Candidate(id="user1", interests=["Science", "Research"])

    matches = await use_case.fallback_match(Candidate)

    # Assert repository was called correctly
    mock_repo.list.assert_called_once()

    # Assert results are correct
    assert len(matches) > 0  # Should match at least one Job
    assert matches[0]["Job"].id == "123"  # Science Job should match
    assert len(matches[0]["match_reasons"]) > 0

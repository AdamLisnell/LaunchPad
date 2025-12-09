import pytest
from unittest.mock import AsyncMock, MagicMock
from core.domain.candidate import Candidate
from core.use_cases.candidate_management import CandidateManagement


@pytest.mark.asyncio
async def test_get_candidate():
    # Create mock repository
    mock_repo = AsyncMock()
    mock_repo.get.return_value = Candidate(id="123", education="Bachelor")

    # Create use case with mock
    use_case = CandidateManagement(mock_repo)

    # Test get_candidate
    Candidate = await use_case.get_candidate("123")

    # Assert repository was called correctly
    mock_repo.get.assert_called_once_with("123")

    # Assert result is correct
    assert Candidate.id == "123"
    assert Candidate.education == "Bachelor"


@pytest.mark.asyncio
async def test_create_candidate():
    # Create mock repository
    mock_repo = AsyncMock()
    Candidate = Candidate(education="Bachelor")
    mock_repo.create.return_value = Candidate(id="123", education="Bachelor")

    # Create use case with mock
    use_case = CandidateManagement(mock_repo)

    # Test create_candidate
    created = await use_case.create_candidate(Candidate)

    # Assert repository was called correctly
    mock_repo.create.assert_called_once_with(Candidate)

    # Assert result is correct
    assert created.id == "123"
    assert created.education == "Bachelor"

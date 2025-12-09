import pytest
from core.domain.candidate import Candidate


def test_profile_creation():
    # Test Candidate creatiocn with minimal parameters
    Candidate = Candidate()
    assert Candidate.id is None
    assert Candidate.education is None
    assert Candidate.region is None
    assert Candidate.interests == []
    assert Candidate.answers == {}

    # Test Candidate creation with parameters
    Candidate = Candidate(
        id="123",
        education="Bachelor",
        region="North",
        interests=["Science", "Art"],
        answers={"question1": "answer1"},
    )
    assert Candidate.id == "123"
    assert Candidate.education == "Bachelor"
    assert Candidate.region == "North"
    assert Candidate.interests == ["Science", "Art"]
    assert Candidate.answers == {"question1": "answer1"}

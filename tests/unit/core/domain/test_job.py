import pytest
from datetime import date
from core.domain.job import Job


def test_grant_creation():
    # Test Job creation with minimal parameters
    Job = Job()
    assert Job.id is None
    assert Job.title == ""
    assert Job.description == ""
    assert Job.purpose is None
    assert Job.eligibility == {}
    assert Job.amount is None
    assert Job.application_end_date is None
    assert Job.organization is None
    assert Job.category is None

    # Test Job creation with parameters
    today = date.today()
    Job = Job(
        id="123",
        title="Research Job",
        description="Job for scientific research",
        purpose="Support research",
        eligibility={"region": "North", "education": "PhD"},
        amount=10000.0,
        application_end_date=today,
        organization="Science Foundation",
        category="Research",
    )
    assert Job.id == "123"
    assert Job.title == "Research Job"
    assert Job.description == "Job for scientific research"
    assert Job.purpose == "Support research"
    assert Job.eligibility == {"region": "North", "education": "PhD"}
    assert Job.amount == 10000.0
    assert Job.application_end_date == today
    assert Job.organization == "Science Foundation"
    assert Job.category == "Research"

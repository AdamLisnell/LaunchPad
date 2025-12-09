from typing import Dict, List, Optional


class Candidate:
    """Candidate profile entity."""
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        email: str = "",
        education: Optional[str] = None,
        location: Optional[str] = None,
        skills: Optional[List[str]] = None,
        experience: Optional[str] = None,
        answers: Optional[Dict[str, str]] = None,
        embedding: Optional[List[float]] = None,  # ← NY RAD!
    ):
        self.id = id
        self.name = name
        self.email = email
        self.education = education
        self.location = location
        self.skills = skills or []
        self.experience = experience
        self.answers = answers or {}
        self.embedding = embedding  # ← NY RAD!
from datetime import date
from typing import Dict, Optional, List  # ← Lägg till List här!


class Job:
    """Job posting entity."""
    
    def __init__(
        self,
        id: Optional[str] = None,
        title: str = "",
        description: str = "",
        responsibilities: Optional[str] = None,
        requirements: Optional[Dict[str, str]] = None,
        salary: Optional[float] = None,
        application_end_date: Optional[date] = None,
        company: Optional[str] = None,
        category: Optional[str] = None,
        location: Optional[str] = None,
        embedding: Optional[List[float]] = None, 
    ):
        self.id = id
        self.title = title
        self.description = description
        self.responsibilities = responsibilities
        self.requirements = requirements or {}
        self.salary = salary
        self.application_end_date = application_end_date
        self.company = company
        self.category = category
        self.location = location
        self.embedding = embedding 
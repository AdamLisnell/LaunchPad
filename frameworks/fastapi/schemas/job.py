from typing import Dict, Optional
from datetime import date
from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    description: str
    responsibilities: Optional[str] = None
    requirements: Dict[str, str] = {}
    salary: Optional[float] = None
    application_end_date: Optional[date] = None
    company: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    requirements: Optional[Dict[str, str]] = None
    salary: Optional[float] = None
    application_end_date: Optional[date] = None
    company: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None


class JobRead(JobBase):
    id: str

    class Config:
        from_attributes = True
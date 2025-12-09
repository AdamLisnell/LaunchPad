from typing import List, Dict, Optional
from pydantic import BaseModel, EmailStr


class CandidateBase(BaseModel):
    name: str = ""
    email: str = ""
    education: Optional[str] = None
    location: Optional[str] = None
    skills: List[str] = []
    experience: Optional[str] = None
    answers: Dict[str, str] = {}


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[str] = None
    answers: Optional[Dict[str, str]] = None


class CandidateRead(CandidateBase):
    id: str

    class Config:
        from_attributes = True  # This replaces orm_mode=True in Pydantic v2
from typing import Dict, List, Optional
from pydantic import BaseModel


class ChoiceBase(BaseModel):
    """Base schema for choice data."""

    id: str
    text: str
    value: str


class RequirementBase(BaseModel):
    """Base schema for Requirement data."""

    text: str
    type: str = "text"  # text, single_choice, multiple_choice
    choices: List[ChoiceBase] = []
    depends_on: Optional[Dict[str, str]] = None  # Requirement ID -> answer that activates this Requirement
    order: int = 0


class RequirementCreate(RequirementBase):
    """Schema for creating a Requirement."""

    pass


class RequirementUpdate(BaseModel):
    """Schema for updating a Requirement."""

    text: Optional[str] = None
    type: Optional[str] = None
    choices: Optional[List[ChoiceBase]] = None
    depends_on: Optional[Dict[str, str]] = None
    order: Optional[int] = None


class RequirementRead(RequirementBase):
    """Schema for reading a Requirement."""

    id: str

    class Config:
        from_attributes = True
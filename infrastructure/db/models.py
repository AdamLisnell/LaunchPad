from datetime import date
from typing import Dict, List, Optional
import json

from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CandidateModel(Base):
    """SQLAlchemy model for Candidate."""

    __tablename__ = "candidates"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, default="")
    email = Column(String(255), nullable=False, default="")
    education = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    skills = Column(JSON, nullable=False, default=list)
    experience = Column(String(100), nullable=True)
    answers = Column(JSON, nullable=False, default=dict)
    embedding = Column(JSON, nullable=True)  # ← NY RAD!

    def to_domain(self):
        """Convert to domain model."""
        from core.domain.candidate import Candidate

        return Candidate(
            id=self.id,
            name=self.name,
            email=self.email,
            education=self.education,
            location=self.location,
            skills=self.skills,
            experience=self.experience,
            answers=self.answers,
            embedding=self.embedding,  # ← NY RAD!
        )

    @classmethod
    def from_domain(cls, candidate):
        """Create from domain model."""
        return cls(
            id=candidate.id,
            name=candidate.name,
            email=candidate.email,
            education=candidate.education,
            location=candidate.location,
            skills=candidate.skills,
            experience=candidate.experience,
            answers=candidate.answers,
            embedding=candidate.embedding,  # ← NY RAD!
        )


class JobModel(Base):
    """SQLAlchemy model for Job."""

    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    responsibilities = Column(Text, nullable=True)
    requirements = Column(JSON, nullable=False, default=dict)
    salary = Column(Float, nullable=True)
    application_end_date = Column(Date, nullable=True)
    company = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    embedding = Column(JSON, nullable=True)  # ← NY RAD!

    def to_domain(self):
        """Convert to domain model."""
        from core.domain.job import Job

        return Job(
            id=self.id,
            title=self.title,
            description=self.description,
            responsibilities=self.responsibilities,
            requirements=self.requirements,
            salary=self.salary,
            application_end_date=self.application_end_date,
            company=self.company,
            category=self.category,
            location=self.location,
            embedding=self.embedding,  # ← NY RAD!
        )

    @classmethod
    def from_domain(cls, job):
        """Create from domain model."""
        return cls(
            id=job.id,
            title=job.title,
            description=job.description,
            responsibilities=job.responsibilities,
            requirements=job.requirements,
            salary=job.salary,
            application_end_date=job.application_end_date,
            company=job.company,
            category=job.category,
            location=job.location,
            embedding=job.embedding,  # ← NY RAD!
        )


class ChoiceModel(Base):
    """SQLAlchemy model for choice."""

    __tablename__ = "choices"

    id = Column(String(36), primary_key=True)
    requirement_id = Column(String(36), ForeignKey("requirements.id"), nullable=False)
    text = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    requirement = relationship("RequirementModel", back_populates="choices")


class RequirementModel(Base):
    """SQLAlchemy model for Requirement."""

    __tablename__ = "requirements"

    id = Column(String(36), primary_key=True)
    text = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False, default="text")
    depends_on = Column(JSON, nullable=True)
    order = Column(Integer, nullable=False, default=0)

    choices = relationship(
        "ChoiceModel", back_populates="requirement", cascade="all, delete-orphan"
    )

    def to_domain(self):
        """Convert to domain model."""
        from core.domain.requirement import Requirement, Choice

        choices = [
            Choice(id=choice.id, text=choice.text, value=choice.value)
            for choice in self.choices
        ]

        return Requirement(
            id=self.id,
            text=self.text,
            type=self.type,
            choices=choices,
            depends_on=self.depends_on,
            order=self.order,
        )

    @classmethod
    def from_domain(cls, requirement):
        """Create from domain model."""
        from core.domain.requirement import Choice

        model = cls(
            id=requirement.id,
            text=requirement.text,
            type=requirement.type,
            depends_on=requirement.depends_on,
            order=requirement.order,
        )

        # Add choices
        model.choices = [
            ChoiceModel(id=choice.id, text=choice.text, value=choice.value)
            for choice in requirement.choices
        ]

        return model
# Project Dependency Map

This document outlines the key dependencies and relationships between components in the Global Job Project.

## Core Domain Dependencies
Candidate Entity
└── No dependencies
Job Entity
└── No dependencies
Requirement Entity
└── Choice Entity
ProfileRepository (Port)
└── Candidate Entity
GrantRepository (Port)
└── Job Entity
QuestionRepository (Port)
└── Requirement Entity
CandidateManagement (Use Case)
├── Candidate Entity
└── ProfileRepository
JobManagement (Use Case)
├── Job Entity
└── GrantRepository
RequirementManagement (Use Case)
├── Requirement Entity
└── QuestionRepository
MatchJobs (Use Case)
├── Candidate Entity
├── Job Entity
└── GrantRepository

## Adapter Dependencies
MemoryProfileRepository
├── ProfileRepository (implements)
└── Candidate Entity
MemoryGrantRepository
├── GrantRepository (implements)
└── Job Entity
MemoryQuestionRepository
├── QuestionRepository (implements)
└── Requirement Entity
MySQLProfileRepository
├── ProfileRepository (implements)
├── Candidate Entity
└── SQLAlchemy
MySQLGrantRepository
├── GrantRepository (implements)
├── Job Entity
└── SQLAlchemy
MySQLQuestionRepository
├── QuestionRepository (implements)
├── Requirement Entity
└── SQLAlchemy

## Framework Dependencies
FastAPI Application
├── CandidateManagement
├── JobManagement
├── RequirementManagement
└── MatchJobs
Repository Factory
└── All Repository Implementations
API Routes
├── Use Cases
└── Schemas
DB Models
├── SQLAlchemy
└── Domain Entities (conversion)

## External Dependencies
SQLAlchemy
└── Database (SQLite/MySQL)
FastAPI
├── Starlette
└── Pydantic
Alembic
└── SQLAlchemy
Pytest
└── AsyncIO

## Future Planned Dependencies
RAG Matching (Sprints 7-8)
├── MatchJobs (extends)
├── FAISS Index
└── Embedding Model
ML-Based Matching (Sprint 9)
├── MatchJobs (extends)
└── Feedback Data

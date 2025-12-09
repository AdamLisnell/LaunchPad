# LaunchPad – AI-Powered Job Matching Platform
Transforming how students discover internships, graduate roles, and early-career opportunities through intelligent semantic matching.

**Python Version:** 3.11  
**License:** MIT  
**Code Style:** black, flake8, isort, mypy

---

## Features

### AI-Enhanced Job Matching
- **Hybrid Matching System** – 70% semantic similarity + 30% rule-based filtering  
- **Contextual Understanding** – Deep embeddings (384-dim) powered by sentence-transformers  
- **Explainable Results** – Every match includes interpreted reasoning

### Modern Architecture
- **Hexagonal Architecture** – Clean separation of domain, adapters, and application layers  
- **Async/Await Stack** – High-performance FastAPI + async SQLAlchemy  
- **Production Ready** – Docker, Alembic migrations, CI/CD workflows  
- **Dynamic Questionnaires** – Conditional, requirement-driven forms for candidate profiling  

### Scalability & Reliability
- Handles **25,000+ job postings** efficiently  
- Safe fallback to rule-based matching if ML models are unreachable  
- Clear separation of concerns ensures testability and maintainability  

---

## Screenshots
*(coming soon)*

**REST API Interface**  
Screenshot coming soon

**Frontend React Application**  
Screenshot coming soon

---

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose  
- Node.js 16+  
- Git  

---

## Installation

### Clone the repository
```bash
git clone https://github.com/yourusername/LaunchPad.git
cd LaunchPad
Create a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
Install backend dependencies
bash
Copy code
pip install -r requirements.txt
Start MySQL
bash
Copy code
docker-compose up -d
Apply database migrations
bash
Copy code
alembic upgrade head
Run the backend
bash
Copy code
uvicorn frameworks.fastapi.main:app --reload
Run the frontend
bash
Copy code
cd frontend
npm install
npm start
Backend API: http://localhost:8000
Frontend UI: http://localhost:3000

Configuration
Create a .env file:

env
Copy code
ENVIRONMENT=development
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/launchpad
LOG_LEVEL=DEBUG
Production tips:

Use stronger credentials

Set ENVIRONMENT=production

API Documentation
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Usage
Import Job Data
bash
Copy code
python scripts/import_kaggle_jobs.py --file path/to/linkedin_jobs.csv
Generate Embeddings
bash
Copy code
python scripts/generate_embeddings.py
Seed the Database
bash
Copy code
python scripts/seed_db.py
Matching Algorithm
Semantic Matching (70%)
Embeddings generated using all-MiniLM-L6-v2

Cosine similarity comparison

Captures context, not just keywords

Rule-Based Matching (30%)
Location

Skills overlap

Education requirements

Experience alignment

Failover
If embedding service is unavailable, switches automatically to rule-based matching.

Technology Stack
Backend
Python 3.11

FastAPI

SQLAlchemy 2.0 (async)

MySQL 8.0

Alembic

Sentence-transformers

PyTorch

Frontend
React 19

Axios

Create React App

DevOps
Docker, Docker Compose

GitHub Actions

pytest

black, flake8, isort, mypy

Project Structure
graphql
Copy code
LaunchPad/
├── core/                     # Domain logic & business rules
│   ├── domain/               # Entities (Candidate, Job, Requirement)
│   ├── use_cases/            # Application services
│   ├── ports/                # Interface definitions
│   └── services/             # Embedding & ML logic
├── adapters/
│   ├── repositories/         # MySQL + in-memory implementations
│   └── services/             # External service adapters
├── frameworks/
│   └── fastapi/              # FastAPI REST API
├── infrastructure/
│   └── db/                   # Database configuration and ORM
├── frontend/                 # React application
└── scripts/                  # Data import & utilities
Development
Install development dependencies
bash
Copy code
pip install -e ".[dev]"
Run tests
bash
Copy code
pytest
Format code
bash
Copy code
black .
isort .
Type checking
bash
Copy code
mypy .
Linting
bash
Copy code
flake8 .
Running Tests With Coverage
bash
Copy code
pytest --cov=core --cov=adapters --cov=frameworks --cov-report=html
CI/CD Pipeline
GitHub Actions pipeline automatically:

Formats code

Lints

Sorts imports

Checks types

Runs the entire test suite

Performance Considerations
Fully async I/O

Connection pooling

Batch embedding generation

Pagination for large datasets

Rate limiting on import scripts

Future Enhancements
Redis caching layer

Vector database (Weaviate, Pinecone, FAISS)

A/B testing for match quality

Authentication & authorization

Real-time notifications

Admin dashboard

Contributing
Contributions welcome – standard workflow:

Fork repository

Create feature branch

Add tests

Ensure all checks pass

Open pull request

License
MIT License – see LICENSE file for details.

Author
Adam Lisnell

Acknowledgments
Kaggle LinkedIn Jobs Dataset

Sentence-transformers Team

FastAPI Framework

Open-source community
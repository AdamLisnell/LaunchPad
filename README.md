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

### 1. Clone the repository
```bash
git clone https://github.com/AdamLisnell/LaunchPad.git
cd LaunchPad
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
```

### 3. Install backend dependencies
```bash
pip install -r requirements.txt
```

### 4. Start MySQL
```bash
docker-compose up -d
```

### 5. Apply database migrations
```bash
alembic upgrade head
```

### 6. Run the backend
```bash
uvicorn frameworks.fastapi.main:app --reload
```

### 7. Run the frontend
```bash
cd frontend
npm install
npm start
```

**Backend API:** http://localhost:8000
**Frontend UI:** http://localhost:3000

---

## Configuration

Create a `.env` file:

```env
ENVIRONMENT=development
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/launchpad
LOG_LEVEL=DEBUG
```

**Production tips:**
- Use stronger credentials
- Set `ENVIRONMENT=production`

---

## API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Usage

### Import Job Data
```bash
python scripts/import_kaggle_jobs.py --file path/to/linkedin_jobs.csv
```

### Generate Embeddings
```bash
python scripts/generate_embeddings.py
```

### Seed the Database
```bash
python scripts/seed_db.py
```

---

## Matching Algorithm

### Semantic Matching (70%)
- Embeddings generated using `all-MiniLM-L6-v2`
- Cosine similarity comparison
- Captures context, not just keywords

### Rule-Based Matching (30%)
- Location
- Skills overlap
- Education requirements
- Experience alignment

### Failover
If embedding service is unavailable, LaunchPad falls back to rule-based matching.

---

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy 2.0 (async)
- MySQL 8.0
- Alembic
- Sentence-transformers
- PyTorch

### Frontend
- React 19
- Axios
- Create React App

### DevOps
- Docker, Docker Compose
- GitHub Actions
- pytest
- black, flake8, isort, mypy

---

## Project Structure

```
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
```

---

## Development

### Install development dependencies
```bash
pip install -e ".[dev]"
```

### Run tests
```bash
pytest
```

### Format code
```bash
black .
isort .
```

### Type checking
```bash
mypy .
```

### Linting
```bash
flake8 .
```

### Running Tests With Coverage
```bash
pytest --cov=core --cov=adapters --cov=frameworks --cov-report=html
```

---

## CI/CD Pipeline

GitHub Actions automatically:
- Formats code
- Lints
- Sorts imports
- Checks types
- Runs the entire test suite

---

## Performance Considerations

- Fully async I/O
- Connection pooling
- Batch embedding generation
- Pagination for large datasets
- Rate limiting on import scripts

---

## Future Enhancements

- Redis caching layer
- Vector database (Weaviate, Pinecone, FAISS)
- A/B testing for match quality
- Authentication & authorization
- Real-time notifications
- Admin dashboard

---

## Contributing

Contributions welcome – standard workflow:

1. Fork repository
2. Create feature branch
3. Add tests
4. Ensure all checks pass
5. Open pull request

---

## License

MIT License – see LICENSE file for details.

---

## Author

Adam Lisnell

---

## Acknowledgments

- Kaggle LinkedIn Jobs Dataset
- Sentence-transformers Team
- FastAPI Framework
- Open-source community

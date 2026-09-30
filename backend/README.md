# Backend - Semantic Plagiarism Detection API

FastAPI backend for semantic plagiarism detection system.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
```

5. Create directories:
```bash
mkdir uploads
mkdir generated_reports
```

6. Seed database:
```bash
python seed.py
```

## Running

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API documentation available at: http://localhost:8000/docs

## Project Structure

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── database.py          # Database connection and session
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── document.py
│   ├── comparison.py
│   └── report.py
├── schemas/             # Pydantic schemas
│   ├── user.py
│   ├── document.py
│   ├── comparison.py
│   └── report.py
├── routers/             # API endpoints
│   ├── auth.py
│   ├── documents.py
│   ├── comparisons.py
│   ├── reports.py
│   └── dashboard.py
├── services/            # Business logic
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── similarity.py
│   ├── plagiarism.py
│   ├── report_generator.py
│   └── explanation_agent.py
├── auth/                # Authentication
│   └── security.py
└── utils/               # Utilities
    └── file_handler.py
```

## API Endpoints

### Authentication
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me

### Documents
- POST /api/documents/upload
- GET /api/documents
- GET /api/documents/{id}
- DELETE /api/documents/{id}

### Comparisons
- POST /api/comparisons
- GET /api/comparisons
- GET /api/comparisons/{id}
- DELETE /api/comparisons/{id}

### Reports
- GET /api/reports/{comparison_id}
- POST /api/reports/{comparison_id}/generate
- GET /api/reports/{comparison_id}/download

### Dashboard
- GET /api/dashboard/student
- GET /api/dashboard/faculty
- GET /api/dashboard/admin

## Services

### DocumentProcessor
Extracts text from PDF, DOCX, and TXT files with paragraph splitting and chunking.

### EmbeddingService
Generates semantic embeddings using Sentence Transformers.

### SimilarityEngine
Calculates hybrid similarity scores (semantic, lexical, n-gram).

### PlagiarismDetector
Main detection engine that combines all services.

### ReportGenerator
Generates PDF reports using ReportLab.

### ExplanationAgent
Provides explanations for flagged sections.

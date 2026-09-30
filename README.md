# Semantic Plagiarism Detection Agent

A full-stack web application for detecting plagiarism based on semantic meaning, not just identical words. Built with React, FastAPI, and advanced NLP techniques.

## 🎯 Project Overview

This application uses semantic analysis to identify:
- **Exact copying** - Direct word-for-word matches
- **Paraphrasing** - Rewritten text with similar meaning
- **Semantic similarity** - Conceptually related content

Unlike traditional plagiarism detectors that only match identical words, this system understands meaning and can detect when content has been rephrased while preserving the original ideas.

## 🚀 Features

### Core Functionality
- **Semantic Analysis** - Uses Sentence Transformers for meaning-based comparison
- **Hybrid Similarity Engine** - Combines semantic, lexical, and n-gram similarity scores
- **Multi-format Support** - PDF, DOCX, and TXT file processing
- **Chunk-level Analysis** - Paragraph and sentence-level comparison
- **AI Explanations** - Automated explanations for flagged sections
- **PDF Reports** - Downloadable detailed plagiarism reports

### User Roles
- **Student** - Upload documents, compare, view results
- **Faculty** - View student submissions, analyze assignments
- **Admin** - Manage users, system statistics, document management

### Advanced Features
- Role-based authentication with JWT
- SQLite database (PostgreSQL-ready)
- Real-time similarity calculation
- Processing time tracking
- Comprehensive dashboard analytics
- Search and filter capabilities

## 🛠 Technology Stack

### Frontend
- **React 19** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Lucide React** - Icons

### Backend
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **JWT** - Authentication
- **SQLite** - Database

### NLP & ML
- **Sentence Transformers** - Semantic embeddings
- **PyTorch** - ML framework
- **scikit-learn** - ML algorithms
- **ReportLab** - PDF generation

## 📁 Project Structure

```
semantic-plagiarism-detector/
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── layouts/        # Layout components
│   │   ├── services/       # API services
│   │   ├── context/        # React context
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── auth/            # Authentication
│   │   └── utils/           # Utilities
│   ├── requirements.txt
│   └── .env.example
│
├── uploads/                 # Uploaded documents
├── generated_reports/       # PDF reports
└── README.md
```

## 📋 Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- pip
- npm

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment**
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
DATABASE_URL=sqlite:///./plagiarism.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
EMBEDDING_MODEL=all-MiniLM-L6-v2
SEMANTIC_WEIGHT=0.60
LEXICAL_WEIGHT=0.20
NGRAM_WEIGHT=0.20
MAX_FILE_SIZE_MB=10
UPLOAD_DIR=uploads
REPORT_DIR=generated_reports
FRONTEND_URL=http://localhost:5173
```

6. **Create directories**
```bash
mkdir uploads
mkdir generated_reports
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

## 🎮 Running the Application

### Start Backend

```bash
cd backend
# Activate virtual environment if not already active
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## 🔐 Authentication

### Default Accounts

After running the seed script, these accounts will be available:

**Student:**
- Email: `student@example.com`
- Password: `password123`

**Faculty:**
- Email: `faculty@example.com`
- Password: `password123`

**Admin:**
- Email: `admin@example.com`
- Password: `password123`

⚠️ **Important:** Change these passwords in production!

## 📊 Similarity Scoring

### Scoring Methodology

The system uses a hybrid approach combining three similarity metrics:

1. **Semantic Similarity (60%)** - Meaning-based comparison using embeddings
2. **Lexical Similarity (20%)** - Word overlap using TF-IDF
3. **N-gram Similarity (20%)** - Phrase overlap using n-grams

### Score Interpretation

- **0.80 - 1.00**: Very High Similarity - Likely direct copying
- **0.65 - 0.79**: High Similarity - Likely paraphrasing
- **0.45 - 0.64**: Moderate Similarity - Conceptually similar
- **Below 0.45**: Low Similarity - Weak or unrelated

### Match Classifications

- **Exact Copy** - Identical or nearly identical text
- **Near-Exact Copy** - Minor changes only
- **Likely Paraphrase** - Different wording, same meaning
- **Conceptually Similar** - Shared ideas, different expression
- **Weak Similarity** - Minimal overlap

## ⚠️ Limitations

1. **Semantic ≠ Plagiarism** - High similarity doesn't prove misconduct
2. **Common Phrases** - Academic terminology may create false positives
3. **Calibration Required** - Thresholds need domain-specific tuning
4. **OCR Needed** - Scanned PDFs require OCR preprocessing
5. **Context Matters** - Citations and quotes need separate handling
6. **Human Review Required** - Results should be reviewed by qualified personnel

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📝 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Document Endpoints

- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - Get user documents
- `GET /api/documents/{id}` - Get specific document
- `DELETE /api/documents/{id}` - Delete document

### Comparison Endpoints

- `POST /api/comparisons` - Create comparison
- `GET /api/comparisons` - Get user comparisons
- `GET /api/comparisons/{id}` - Get comparison details
- `DELETE /api/comparisons/{id}` - Delete comparison

### Report Endpoints

- `GET /api/reports/{comparison_id}` - Get report info
- `POST /api/reports/{comparison_id}/generate` - Generate PDF report
- `GET /api/reports/{comparison_id}/download` - Download PDF

### Dashboard Endpoints

- `GET /api/dashboard/student` - Student dashboard data
- `GET /api/dashboard/faculty` - Faculty dashboard data
- `GET /api/dashboard/admin` - Admin dashboard data

## 🚀 Deployment

### Backend Deployment

1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables
3. Use a production ASGI server (Gunicorn + Uvicorn)
4. Set up reverse proxy (Nginx)
5. Enable HTTPS

### Frontend Deployment

1. Build the frontend: `npm run build`
2. Serve static files using Nginx or similar
3. Configure CORS for production domain

## 🔧 Configuration

### Environment Variables

See `.env.example` for all configurable options:

- Database connection
- JWT secret and expiration
- Embedding model selection
- Similarity weights
- File size limits
- Upload directories

### Similarity Weights

Adjust the hybrid scoring in `.env`:

```env
SEMANTIC_WEIGHT=0.60
LEXICAL_WEIGHT=0.20
NGRAM_WEIGHT=0.20
```

## 📚 Future Improvements

- [ ] FAISS integration for large-scale similarity search
- [ ] Support for more file formats (RTF, ODT)
- [ ] OCR integration for scanned PDFs
- [ ] Batch comparison for multiple documents
- [ ] Citation detection and exclusion
- [ ] Plagiarism source detection
- [ ] Real-time collaboration features
- [ ] Advanced analytics and reporting
- [ ] Integration with LMS systems

## 🤝 Contributing

This is an academic project. Contributions should focus on:
- Improving accuracy of similarity detection
- Adding support for more file formats
- Enhancing user experience
- Fixing bugs and issues

## 📄 License

This project is for educational purposes. Please ensure compliance with your institution's academic integrity policies when using this software.

## 🙏 Acknowledgments

- Sentence Transformers team for the embedding model
- FastAPI community for the excellent framework
- React team for the frontend framework

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review the API docs at `/docs`
3. Check the troubleshooting section below

## 🔍 Troubleshooting

### Backend Issues

**Model not loading:**
- Ensure sufficient memory (2GB+ recommended)
- Check internet connection for first-time model download
- Try a smaller model if needed

**Database errors:**
- Delete `plagiarism.db` and restart
- Check database permissions
- Verify SQLAlchemy version compatibility

### Frontend Issues

**CORS errors:**
- Verify `FRONTEND_URL` in backend `.env`
- Check CORS middleware configuration

**Build errors:**
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility

### Performance Issues

**Slow comparisons:**
- Reduce chunk size in configuration
- Use GPU if available (configure in embeddings service)
- Limit document size

## 🎓 Academic Use

This project demonstrates:
- Modern full-stack development
- Natural language processing applications
- Semantic similarity detection
- Role-based access control
- Database design and management
- API development and documentation

Perfect for B.Tech/M.Tech projects and academic research.

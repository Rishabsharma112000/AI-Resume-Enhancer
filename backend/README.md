# ResumeBoost AI - Backend

## Setup Instructions

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your actual values, especially OpenAI API key
```

4. **Initialize database:**
```bash
python -c "from app.db.database import init_db; init_db()"
```

5. **Run development server:**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
pytest tests/ -v
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Configuration and security
│   ├── crew/             # CrewAI agents
│   ├── db/               # Database
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── utils/            # Utilities
├── tests/                # Unit tests
├── uploads/              # Resume uploads
├── main.py              # Application entry point
├── requirements.txt      # Dependencies
└── .env.example         # Environment variables template
```

## Main Features

### Authentication
- User registration and login
- JWT token-based authentication
- Profile management

### Resume Management
- Upload PDF/DOCX resumes
- Extract and store resume text
- Retrieve resume history

### Job Description Management
- Create job descriptions
- Upload job description files
- Store and retrieve job requirements

### Analysis Engine
- ATS (Applicant Tracking System) scoring
- Keyword matching and analysis
- Skills gap identification
- Resume strengths and weaknesses assessment

### Enhancement Features
- Professional summary rewriting
- Experience bullet point improvement
- ATS compatibility optimization
- Keyword integration

### CrewAI Workflow
Four specialized agents working sequentially:
1. **Resume Analyzer** - Extracts and structures resume information
2. **ATS Analyzer** - Calculates ATS scores and identifies gaps
3. **Resume Rewriter** - Enhances content and improves keywords
4. **Final Reviewer** - Quality checks and final recommendations

## Environment Variables

```
DATABASE_URL=sqlite:///./resume_enhance.db
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=pdf,docx,doc
DEBUG=False
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile

### Resumes
- `POST /api/v1/resumes/upload` - Upload resume
- `GET /api/v1/resumes/` - List user resumes
- `GET /api/v1/resumes/{id}` - Get resume details
- `DELETE /api/v1/resumes/{id}` - Delete resume

### Job Descriptions
- `POST /api/v1/job-descriptions/` - Create job description
- `POST /api/v1/job-descriptions/upload` - Upload job description
- `GET /api/v1/job-descriptions/` - List job descriptions
- `GET /api/v1/job-descriptions/{id}` - Get job description
- `DELETE /api/v1/job-descriptions/{id}` - Delete job description

### Analysis
- `POST /api/v1/analysis/analyze` - Analyze resume
- `GET /api/v1/analysis/{id}` - Get analysis results
- `POST /api/v1/analysis/enhance` - Enhance resume

## Docker Deployment

### Build Image
```bash
docker build -t resumeboost-api:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./resume_enhance.db \
  -e OPENAI_API_KEY=your-key \
  -v $(pwd)/uploads:/app/uploads \
  resumeboost-api:latest
```

## Database Schema

### Users
- id, email, full_name, hashed_password, is_active, created_at, updated_at

### Resumes
- id, user_id, filename, file_path, file_type, file_size, raw_text, created_at, updated_at

### JobDescriptions
- id, user_id, title, company, content, file_name, created_at, updated_at

### ResumeAnalyses
- id, user_id, resume_id, job_description_id, ats_score, keyword_match_score, missing_skills, missing_keywords, strengths, weaknesses, created_at, updated_at

### EnhancedResumes
- id, user_id, resume_id, analysis_id, enhanced_summary, enhanced_experience, enhanced_full_content, version, created_at, updated_at

## Performance Considerations

- Database queries are optimized with proper indexing
- File uploads use streaming to handle large files
- JSON responses use Pydantic for validation and serialization
- CORS middleware configured for frontend communication
- Text extraction cached in database to avoid re-processing

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- CORS protection
- Request validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM
- File upload validation (type and size checks)

## Troubleshooting

### Database Issues
```bash
# Reset database
rm resume_enhance.db
python -c "from app.db.database import init_db; init_db()"
```

### Module Import Errors
```bash
# Ensure you're in the backend directory
cd backend
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

### CORS Issues
Update `CORS_ORIGINS` in `.env`:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## License

MIT License

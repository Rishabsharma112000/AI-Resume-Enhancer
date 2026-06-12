# ResumeBoost AI - Quick Start Guide

## 🚀 What You Have

A complete, production-ready Resume Enhancer application with:

- **Backend**: FastAPI + CrewAI + SQLAlchemy
- **Frontend**: React + TypeScript + Tailwind CSS
- **AI Pipeline**: 4-agent sequential CrewAI workflow
- **Database**: SQLite (default) / PostgreSQL (production)
- **Authentication**: JWT-based security
- **Docker**: Full containerization for easy deployment

## ⚡ Quick Start (5 minutes)

### Option 1: Using Docker (Recommended)

**Prerequisites:**
- Docker & Docker Compose installed

**Steps:**

1. **Navigate to project:**
```bash
cd /Users/richasharma/Downloads/resume_enhance
```

2. **Set up environment:**
```bash
# Create .env with your OpenAI API key
cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=your-secret-key
EOF
```

3. **Start everything:**
```bash
docker-compose up -d
```

4. **Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Initialize database
python -c "from app.db.database import init_db; init_db()"

# Run server
uvicorn main:app --reload
```

Backend runs on: http://localhost:8000

#### Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cat > .env.local << EOF
VITE_API_URL=http://localhost:8000/api/v1
EOF

# Start dev server
npm run dev
```

Frontend runs on: http://localhost:3000

## 📋 Usage Workflow

### 1. Register/Login
- Go to http://localhost:3000
- Create an account or login
- JWT token is automatically saved

### 2. Upload Resume
- Go to Dashboard
- Click "Upload Resume" tab
- Drag and drop PDF/DOCX file
- Resume is processed and stored

### 3. (Optional) Add Job Description
- Paste job description text OR upload file
- Fill in job title and company
- Save for later matching

### 4. Analyze Resume
- Click "Analyze" tab
- Select resume to analyze
- Optionally select matching job description
- Click "Analyze Resume"
- View ATS score and recommendations

### 5. Enhance Resume
- After analysis, click "Enhance Resume"
- System rewrites and improves content
- Download enhanced version

## 🏗️ Project Structure

```
resume_enhance/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Config & security
│   │   ├── crew/           # CrewAI agents
│   │   ├── db/             # Database
│   │   ├── models/         # Data models
│   │   ├── schemas/        # Data validation
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── tests/              # Unit tests
│   └── main.py             # Entry point
│
├── frontend/                # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── store/          # State management
│   │   └── App.tsx         # Main component
│   └── index.html          # HTML template
│
└── docker-compose.yml      # Multi-container setup
```

## 🤖 CrewAI Workflow

The system uses 4 specialized AI agents:

```
Resume Text
    ↓
┌─────────────────────────┐
│ Resume Analyzer Agent   │ → Extracts structure & content
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  ATS Analyzer Agent     │ → Calculates scores & gaps
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Resume Rewriter Agent   │ → Enhances content
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Final Reviewer Agent   │ → Quality check
└─────────────────────────┘
    ↓
Enhanced Resume Output
```

## 📚 API Key Endpoints

### Authentication
```bash
# Register
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "password123"
}

# Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Resumes
```bash
# Upload resume
POST /api/v1/resumes/upload
(multipart/form-data with file)

# List resumes
GET /api/v1/resumes/

# Get resume details
GET /api/v1/resumes/{resume_id}

# Delete resume
DELETE /api/v1/resumes/{resume_id}
```

### Analysis
```bash
# Analyze resume
POST /api/v1/analysis/analyze
{
  "resume_id": 1,
  "job_description_id": null
}

# Get analysis results
GET /api/v1/analysis/{analysis_id}

# Enhance resume
POST /api/v1/analysis/enhance
{
  "analysis_id": 1
}

# Get enhanced resume
GET /api/v1/analysis/enhanced/{enhanced_id}
```

## 🔧 Common Commands

### Docker Commands
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild images
docker-compose build --no-cache

# Run command in container
docker-compose exec backend python -c "from app.db.database import init_db; init_db()"
```

### Backend Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Reset database
rm resume_enhance.db
python -c "from app.db.database import init_db; init_db()"

# Run migrations (if using Alembic)
alembic upgrade head
```

### Frontend Commands
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint

# Type check
npm run type-check
```

## 🔐 Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=sqlite:///./resume_enhance.db

# API
API_TITLE=ResumeBoost AI
API_VERSION=1.0.0
API_PREFIX=/api/v1

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_BASE_URL=https://api.openai.com/v1

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads

# Environment
DEBUG=False
ENVIRONMENT=development
```

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### OpenAI API Issues
- Verify API key is correct
- Check API rate limits
- Ensure account has credits
- Try using different model (gpt-3.5-turbo as fallback)

### Database Issues
```bash
cd backend
rm resume_enhance.db
python -c "from app.db.database import init_db; init_db()"
```

### CORS Errors
Update `CORS_ORIGINS` in backend `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Cannot Connect to Backend
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

## 📝 Example Usage Flow

```
1. User registers
   POST /auth/register

2. User uploads resume
   POST /resumes/upload

3. User adds job description (optional)
   POST /job-descriptions/

4. User analyzes resume
   POST /analysis/analyze

5. System processes through CrewAI:
   - Resume Analyzer: Extracts info
   - ATS Analyzer: Calculates scores
   - Resume Rewriter: Improves content
   - Final Reviewer: Quality check

6. User gets analysis results
   GET /analysis/{id}

7. User enhances resume
   POST /analysis/enhance

8. User downloads enhanced version
   GET /analysis/enhanced/{id}
```

## 📊 Database Schema

### Users Table
- id (PK)
- email (UNIQUE)
- full_name
- hashed_password
- is_active
- created_at, updated_at

### Resumes Table
- id (PK)
- user_id (FK)
- filename, original_filename
- file_path, file_type, file_size
- raw_text
- created_at, updated_at

### JobDescriptions Table
- id (PK)
- user_id (FK)
- title, company
- content, file_name
- created_at, updated_at

### ResumeAnalyses Table
- id (PK)
- user_id (FK), resume_id (FK), job_description_id (FK)
- ats_score, keyword_match_score
- missing_keywords (JSON), missing_skills (JSON)
- strengths (JSON), weaknesses (JSON)
- created_at, updated_at

### EnhancedResumes Table
- id (PK)
- user_id (FK), resume_id (FK), analysis_id (FK)
- enhanced_summary, enhanced_experience
- enhanced_full_content
- version
- created_at, updated_at

## 🎯 Next Steps

1. **Set OpenAI API Key**
   - Get key from https://platform.openai.com/api-keys
   - Add to .env file

2. **Test Upload**
   - Register an account
   - Upload a test resume
   - Check uploads folder

3. **Test Analysis**
   - Run analysis on uploaded resume
   - Check ATS score results

4. **Deploy (Optional)**
   - Update production .env
   - Use docker-compose for deployment
   - Set up reverse proxy (Nginx)
   - Use PostgreSQL for production

## 📞 Support

- Check README.md files in backend/ and frontend/
- Review API docs at http://localhost:8000/docs
- Check logs: `docker-compose logs`
- Review error messages in browser console

## 📄 License

MIT License

---

**Enjoy using ResumeBoost AI! 🚀**

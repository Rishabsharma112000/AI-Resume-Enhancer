# ResumeBoost AI - Complete Resume Enhancer

A production-ready, full-stack resume enhancement application built with CrewAI, FastAPI, React, and TypeScript.

## Project Overview

ResumeBoost AI is an intelligent resume enhancement platform that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) and improve their chances of getting hired. The application uses AI-powered analysis and automated enhancement to provide actionable feedback and improvements.

### Key Features

- **Resume Upload & Management** - Support for PDF and DOCX formats
- **AI-Powered Analysis** - ATS scoring, keyword matching, and gap analysis
- **Resume Enhancement** - Automatic rewriting and optimization
- **Job Description Matching** - Compare resume against target job descriptions
- **User Authentication** - Secure JWT-based authentication
- **Responsive UI** - Modern, mobile-friendly interface
- **CrewAI Workflow** - 4-agent sequential processing pipeline

## Architecture

### Technology Stack

**Backend:**
- Python 3.11
- FastAPI
- CrewAI (AI orchestration)
- SQLAlchemy (ORM)
- SQLite/PostgreSQL (Database)
- JWT Authentication

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Zustand (State management)
- Axios (HTTP client)
- Vite (Build tool)

**AI/ML:**
- OpenAI GPT-4 API
- CrewAI Agents
- LangChain

**DevOps:**
- Docker & Docker Compose
- Nginx (Frontend reverse proxy)

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TS)                    │
│                   Port 3000 | Tailwind CSS                  │
└────────────────────────────┬────────────────────────────────┘
                             │ API Calls
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                          │
│                   Port 8000                                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │     Auth     │  │   Services   │  │   API Routes     │  │
│  │  (JWT)       │  │ (Business    │  │  (/api/v1/*)     │  │
│  └──────────────┘  │  Logic)      │  └──────────────────┘  │
│                    └──────────────┘                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           CrewAI Workflow (Agents)                  │   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐            │   │
│  │  │Resume│  │ ATS  │  │Resume│  │Final │            │   │
│  │  │ Anly │→ │ Anly │→ │Rewr  │→ │Review│            │   │
│  │  └──────┘  └──────┘  └──────┘  └──────┘            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │   Database   │  │  File Store  │                        │
│  │  (SQLite)    │  │  (Uploads)   │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### CrewAI Agents Pipeline

The application uses 4 specialized agents working in sequence:

1. **Resume Analyzer**
   - Extracts structured information from resumes
   - Identifies key sections and achievements
   - Outputs: JSON with resume analysis

2. **ATS Analyzer**
   - Calculates ATS compatibility scores
   - Matches keywords against job description
   - Identifies missing skills and keywords
   - Outputs: JSON with ATS metrics

3. **Resume Rewriter**
   - Rewrites professional summary
   - Improves action verbs and bullets
   - Optimizes for ATS and keywords
   - Outputs: JSON with enhanced content

4. **Final Reviewer**
   - Quality assurance check
   - Verifies consistency and completeness
   - Provides final recommendations
   - Outputs: JSON with review assessment

## Project Structure

```
resume_enhance/
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── api/                     # API routes
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   ├── users.py             # User management
│   │   │   ├── resumes.py           # Resume endpoints
│   │   │   ├── job_descriptions.py  # Job description endpoints
│   │   │   └── analysis.py          # Analysis endpoints
│   │   ├── core/                    # Core configuration
│   │   │   ├── config.py            # Settings
│   │   │   └── security.py          # JWT & hashing
│   │   ├── crew/                    # CrewAI agents
│   │   │   └── agents.py            # Agent definitions
│   │   ├── db/                      # Database
│   │   │   └── database.py          # DB connection
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job_description.py
│   │   │   ├── resume_analysis.py
│   │   │   └── enhanced_resume.py
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job_description.py
│   │   │   ├── resume_analysis.py
│   │   │   └── enhanced_resume.py
│   │   ├── services/                # Business logic
│   │   │   ├── user_service.py
│   │   │   ├── resume_service.py
│   │   │   └── job_description_service.py
│   │   └── utils/                   # Utilities
│   │       ├── file_handler.py      # PDF/DOCX parsing
│   │       └── text_processor.py    # Text analysis
│   ├── tests/                       # Unit tests
│   ├── uploads/                     # Resume uploads
│   ├── main.py                      # App entry point
│   ├── requirements.txt             # Dependencies
│   ├── Dockerfile                   # Docker image
│   ├── .env.example                 # Env variables template
│   └── README.md                    # Backend docs
│
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── Layout.tsx
│   │   │   ├── Navbar.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── ResumeUpload.tsx
│   │   │   ├── ResumeList.tsx
│   │   │   ├── AnalysisResults.tsx
│   │   │   └── JobDescriptionForm.tsx
│   │   ├── pages/                   # Page components
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── ProfilePage.tsx
│   │   │   └── AnalysisPage.tsx
│   │   ├── services/                # API services
│   │   │   ├── api.ts               # Axios instance
│   │   │   └── authService.ts       # API calls
│   │   ├── store/                   # State management
│   │   │   └── authStore.ts         # Zustand store
│   │   ├── types/                   # TypeScript types
│   │   │   └── index.ts
│   │   ├── hooks/                   # Custom hooks
│   │   │   ├── useAuth.ts
│   │   │   └── useAsync.ts
│   │   ├── App.tsx                  # Main app component
│   │   ├── main.tsx                 # Entry point
│   │   └── index.css                # Global styles
│   ├── vite.config.ts              # Vite configuration
│   ├── tailwind.config.js           # Tailwind config
│   ├── tsconfig.json                # TypeScript config
│   ├── Dockerfile                   # Docker image
│   ├── nginx.conf                   # Nginx config
│   ├── index.html                   # HTML template
│   ├── package.json                 # Dependencies
│   └── README.md                    # Frontend docs
│
├── docker-compose.yml               # Docker Compose
└── README.md                        # This file
```

## Getting Started

### Prerequisites

- Docker & Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 16+
  - npm/yarn

### Quick Start with Docker

1. **Clone and setup:**
```bash
cd resume_enhance
```

2. **Create environment file:**
```bash
cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key-here
EOF
```

3. **Start services:**
```bash
docker-compose up -d
```

4. **Access application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

1. **Navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment:**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

5. **Initialize database:**
```bash
python -c "from app.db.database import init_db; init_db()"
```

6. **Run server:**
```bash
uvicorn main:app --reload
```

Backend runs on: http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create environment file:**
```bash
cat > .env.local << EOF
VITE_API_URL=http://localhost:8000/api/v1
EOF
```

4. **Start dev server:**
```bash
npm run dev
```

Frontend runs on: http://localhost:3000

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile
- `GET /api/v1/users/{id}` - Get user by ID

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
- `GET /api/v1/analysis/enhanced/{id}` - Get enhanced resume

## Database Schema

### Users
```sql
- id (PRIMARY KEY)
- email (UNIQUE)
- full_name
- hashed_password
- is_active
- created_at
- updated_at
```

### Resumes
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- filename
- original_filename
- file_path
- file_type
- file_size
- raw_text
- created_at
- updated_at
```

### JobDescriptions
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- title
- company
- content
- file_name
- created_at
- updated_at
```

### ResumeAnalyses
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- resume_id (FOREIGN KEY)
- job_description_id (FOREIGN KEY)
- ats_score
- keyword_match_score
- missing_keywords (JSON)
- missing_skills (JSON)
- strengths (JSON)
- weaknesses (JSON)
- created_at
- updated_at
```

### EnhancedResumes
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- resume_id (FOREIGN KEY)
- analysis_id (FOREIGN KEY)
- enhanced_summary
- enhanced_experience
- enhanced_full_content
- version
- created_at
- updated_at
```

## Usage Examples

### 1. User Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "secure_password_123"
  }'
```

### 2. Upload Resume

```bash
curl -X POST http://localhost:8000/api/v1/resumes/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@resume.pdf"
```

### 3. Analyze Resume

```bash
curl -X POST http://localhost:8000/api/v1/analysis/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description_id": 1
  }'
```

### 4. Enhance Resume

```bash
curl -X POST http://localhost:8000/api/v1/analysis/enhance \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_id": 1
  }'
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Production Deployment

### Using Docker

1. **Build images:**
```bash
docker-compose build
```

2. **Deploy:**
```bash
docker-compose up -d
```

3. **Scale services:**
```bash
docker-compose up -d --scale backend=3
```

### Environment Variables for Production

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:password@db:5432/resumeboost
OPENAI_API_KEY=sk-...
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com
```

**Frontend (.env.production):**
```env
VITE_API_URL=https://api.yourdomain.com/api/v1
```

## Performance Optimization

### Backend
- Database query optimization with indexes
- Connection pooling
- Response caching where applicable
- Efficient file upload handling

### Frontend
- Code splitting and lazy loading
- Image optimization
- CSS tree-shaking
- Build minification

## Security

### Features
- Password hashing with bcrypt
- JWT token authentication
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- File upload validation
- Input validation with Pydantic
- Rate limiting ready

## Monitoring & Logging

### Backend
- Application logs in stdout
- Request/response logging
- Error tracking ready (integrate Sentry)

### Frontend
- Browser console logging
- Error boundary handling

## Common Issues & Fixes

### Port Already in Use
```bash
# Kill process on port
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

### Database Lock
```bash
cd backend
rm resume_enhance.db
python -c "from app.db.database import init_db; init_db()"
```

### CORS Errors
- Check `CORS_ORIGINS` in backend `.env`
- Ensure frontend URL is in allowed origins

### OpenAI API Errors
- Verify API key is valid
- Check API rate limits
- Ensure account has credits

## Contributing

1. Create feature branch
2. Commit changes
3. Push to branch
4. Create Pull Request

## License

MIT License - see LICENSE file

## Support

For issues and questions:
- Check documentation in README files
- Review API documentation at `/api/v1/docs`
- Check backend logs: `docker logs resumeboost-api`
- Check frontend console in browser DevTools

## Future Enhancements

- [ ] Multiple resume versions
- [ ] Resume templates
- [ ] Cover letter generation
- [ ] Interview preparation
- [ ] Skill assessment
- [ ] Portfolio integration
- [ ] Real-time collaboration
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Integration with job boards

---

**ResumeBoost AI** - Enhance Your Resume, Ace Your Job Search 🚀

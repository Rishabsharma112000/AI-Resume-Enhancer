"""Database connection and session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.core.config import settings

# Create engine
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DATABASE_ECHO,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=True,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _migrate_enhanced_resumes():
    """Add columns to enhanced_resumes if missing (SQLite dev migration)."""
    from sqlalchemy import inspect, text

    inspector = inspect(engine)
    if "enhanced_resumes" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("enhanced_resumes")}
    with engine.begin() as conn:
        if "improvements_made" not in columns:
            conn.execute(text("ALTER TABLE enhanced_resumes ADD COLUMN improvements_made TEXT"))
        if "estimated_ats_score_gain" not in columns:
            conn.execute(text("ALTER TABLE enhanced_resumes ADD COLUMN estimated_ats_score_gain INTEGER"))


def init_db():
    """Initialize database tables"""
    from app.models.base import Base

    Base.metadata.create_all(bind=engine)
    _migrate_enhanced_resumes()

"""Authentication routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.services.user_service import UserService
from app.core.security import create_access_token
from app.core.config import settings
import logging

router = APIRouter(prefix="/auth", tags=["Authentication"])


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = UserService.create_user(db, user)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }


@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = UserService.authenticate_user(db, user_credentials.email, user_credentials.password)
    logger.info("Home endpoint called");
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

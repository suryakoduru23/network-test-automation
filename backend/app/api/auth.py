"""Authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserLogin, UserCreate, TokenResponse, UserResponse
from app.services.auth import AuthService
from app.core.exceptions import AuthenticationError, ValidationError

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    try:
        db_user = AuthService.register_user(db, user)
        return db_user
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    try:
        user, access_token = AuthService.login_user(db, credentials)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800
        }
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.post("/logout")
def logout():
    """Logout user"""
    return {"message": "Logged out successfully"}

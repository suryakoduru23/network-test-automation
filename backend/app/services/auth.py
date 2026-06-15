"""Authentication Service"""
from sqlalchemy.orm import Session
from typing import Optional
from app.models import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import AuthenticationError, ValidationError
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication Service"""
    
    @staticmethod
    def register_user(db: Session, user: UserCreate) -> User:
        """Register new user"""
        # Check if user exists
        existing = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email)
        ).first()
        if existing:
            raise ValidationError("Username or email already exists")
        
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=get_password_hash(user.password),
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User registered: {user.username}")
        return db_user
    
    @staticmethod
    def login_user(db: Session, credentials: UserLogin) -> tuple:
        """Authenticate user and return tokens"""
        user = db.query(User).filter(
            User.username == credentials.username
        ).first()
        
        if not user or not verify_password(credentials.password, user.hashed_password):
            logger.warning(f"Failed login attempt: {credentials.username}")
            raise AuthenticationError("Invalid credentials")
        
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
        
        # Create tokens
        access_token = create_access_token(
            data={"sub": user.username, "id": user.id, "role": user.role.value}
        )
        
        logger.info(f"User logged in: {user.username}")
        return user, access_token
    
    @staticmethod
    def get_current_user(db: Session, username: str) -> Optional[User]:
        """Get current user"""
        return db.query(User).filter(User.username == username).first()

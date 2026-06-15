"""Base Model"""
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class BaseModel(Base):
    """Base model with timestamps"""
    __abstract__ = True
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    referral_code = Column(String, unique=True, index=True)
    referred_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

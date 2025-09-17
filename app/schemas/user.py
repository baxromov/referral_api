from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    referral_code: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    referral_code: str
    referred_by: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    id: int
    name: str
    referral_count: int

    class Config:
        from_attributes = True

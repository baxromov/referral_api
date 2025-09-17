from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut, LeaderboardEntry
from app.services.user_service import (
    create_user,
    get_user,
    get_referrals,
    get_leaderboard,
)
from app.database import get_db

router = APIRouter(prefix="", tags=["users"])


@router.post("/users/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}/referrals", response_model=List[UserOut])
def read_referrals(user_id: int, db: Session = Depends(get_db)):
    return get_referrals(db, user_id)


@router.get("/leaderboard/", response_model=List[LeaderboardEntry])
def read_leaderboard(db: Session = Depends(get_db)):
    return get_leaderboard(db)

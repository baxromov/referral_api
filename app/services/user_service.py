import random
import string
from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func

from app.models.user import User
from app.schemas.user import UserCreate, UserOut, LeaderboardEntry


def generate_referral_code(db: Session) -> str:
    while True:
        length = random.randint(6, 8)
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not db.query(User).filter(User.referral_code == code).first():
            return code


def get_depth(db: Session, user: User) -> int:
    depth = 0
    current = user
    while current.referred_by:
        parent = (
            db.query(User).filter(User.referral_code == current.referred_by).first()
        )
        if not parent:
            raise HTTPException(status_code=400, detail="Invalid referral chain")
        current = parent
        depth += 1
    return depth


def create_user(db: Session, user_create: UserCreate) -> UserOut:
    if db.query(User).filter(User.email == user_create.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    referred_by = user_create.referral_code
    referrer = None
    if referred_by:
        referrer = db.query(User).filter(User.referral_code == referred_by).first()
        if not referrer:
            raise HTTPException(status_code=400, detail="Invalid referral code")
        depth = get_depth(db, referrer)
        if depth >= 2:
            raise HTTPException(
                status_code=400, detail="Maximum referral depth of 3 levels exceeded"
            )

    referral_code = generate_referral_code(db)
    new_user = User(
        name=user_create.name,
        email=user_create.email,
        referral_code=referral_code,
        referred_by=referred_by,
        created_at=datetime.utcnow(),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut.model_validate(new_user)


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_referrals(db: Session, user_id: int) -> List[UserOut]:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    referrals = db.query(User).filter(User.referred_by == user.referral_code).all()
    return [UserOut.model_validate(r) for r in referrals]


def get_leaderboard(db: Session) -> List[LeaderboardEntry]:
    invited = aliased(User)
    results = (
        db.query(User.id, User.name, func.count(invited.id).label("referral_count"))
        .outerjoin(invited, User.referral_code == invited.referred_by)
        .group_by(User.id, User.name)
        .order_by(func.count(invited.id).desc())
        .all()
    )
    return [LeaderboardEntry(id=r[0], name=r[1], referral_count=r[2]) for r in results]

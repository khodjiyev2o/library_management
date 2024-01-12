from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import UserMembership, User
from app.schemas import UserMembershipResponse
from app.api.dependency import get_current_user

from app.db import get_db

router = APIRouter()


@router.post("/create/", response_model=UserMembershipResponse, status_code=201)
async def create_user(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    async with db as session:
        # Check if the username already exists
        existing_user = await session.execute(
            select(UserMembership).where(UserMembership.user_id == current_user.id)
        )
        if existing_user.scalars().first():
            raise HTTPException(status_code=400, detail="Username already exists")

        new_membership = UserMembership(user_id=current_user.id, status=UserMembership.MembershipStatus.ACTIVE)
        session.add(new_membership)
        await session.commit()
        await session.refresh(new_membership)

        return new_membership

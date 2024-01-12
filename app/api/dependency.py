from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User, UserMembership
from app.db import get_db
from app.core.utils import Hash

oauth2_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not Validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = token.credentials

    token_data = Hash.verify_token_access(token, credentials_exception)

    async with db as session:
        # Check if the username already exists
        result = await session.execute(
            select(User).where(User.id == token_data.id)
        )
        user = result.scalars().first()
        if user:
            return user
        else:
            raise credentials_exception


async def admin_user(user: User = Depends(get_current_user)):
    if user.is_admin:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not an admin")


async def check_user_membership(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Check if the user has an active membership.py
    async with db as session:
        result = await session.execute(
            select(UserMembership).filter_by(user_id=user.id, status=UserMembership.MembershipStatus.ACTIVE)
        )
        membership = result.scalars().first()

        if not membership:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have an active membership")

    return user


__all__ = ['get_current_user', 'check_user_membership', 'admin_user']

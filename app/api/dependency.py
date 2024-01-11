from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
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

__all__ = ['get_current_user']

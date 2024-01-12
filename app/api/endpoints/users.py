from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User
from app.schemas import UserIn, UserOut, Token
from app.core.utils import Hash
from app.api.dependency import get_current_user

from app.db import get_db

router = APIRouter()


@router.post("/register/", response_model=UserOut, status_code=201)
async def create_user(user: UserIn, db: AsyncSession = Depends(get_db)):
    async with db as session:
        # Check if the username already exists
        existing_user = await session.execute(
            select(User).where(User.username == user.username)
        )
        if existing_user.scalars().first():
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = Hash.bcrypt(user.password)
        new_user = User(username=user.username, password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user


@router.post("/me/", response_model=UserOut, status_code=200)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/login/", response_model=Token)
async def login(user: UserIn, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(User).where(User.username == user.username))
        existing_user = result.scalars().first()
        if not existing_user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        valid_credentials = Hash.verify(hashed_password=existing_user.password, plain_password=user.password)

        if valid_credentials:
            access_token = Hash.create_access_token(data={"user_id": existing_user.id})
            return {"access_token": access_token, "token_type": "bearer"}

        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )




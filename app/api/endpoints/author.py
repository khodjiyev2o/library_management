from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Author, User
from app.schemas import AuthorBase
from app.api.dependency import admin_user

from app.db import get_db

router = APIRouter()


@router.post("/create/", response_model=AuthorBase, status_code=201)
async def create_author(
        new_author: AuthorBase,
        user: User = Depends(admin_user),
        db: AsyncSession = Depends(get_db),
):
    async with db as session:
        # Check if the book already exists
        existing_author = await session.execute(
            select(Author).where(Author.username == new_author.username)
        )
        if existing_author.scalars().first():
            raise HTTPException(status_code=400, detail="Author already exists")

        # Assuming you have the category and author IDs in new_book
        author = Author(
            username=new_author.username,
        )

        session.add(author)
        await session.commit()
        await session.refresh(author)

        return author

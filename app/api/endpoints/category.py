from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Category, User
from app.schemas import CategoryBase
from app.api.dependency import admin_user

from app.db import get_db

router = APIRouter()


@router.post("/create/", response_model=CategoryBase, status_code=201)
async def create_category(
    new_category: CategoryBase,
    user: User = Depends(admin_user),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        # Check if the book already exists
        existing_book = await session.execute(
            select(Category).where(Category.title == new_category.title)
        )
        if existing_book.scalars().first():
            raise HTTPException(status_code=400, detail="Category already exists")

        # Assuming you have the category and author IDs in new_book
        category = Category(
            title=new_category.title,
        )

        session.add(category)
        await session.commit()
        await session.refresh(category)

        return category

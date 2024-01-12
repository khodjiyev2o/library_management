import json
from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Book, User
from app.schemas import BookList, BookCreate, BookOut, BookCreateGoogle
from app.api.dependency import check_user_membership, admin_user
from app.db import get_db, redis_client
from app.config import CACHE_EXPIRE_DATE
from app.api.utils import fetch_and_create_books_by_category

router = APIRouter()


@router.get("/List", response_model=List[BookList])
async def books_list(current_user: User = Depends(check_user_membership),
                     db: AsyncSession = Depends(get_db),
                     search: Optional[str] = None,
                     category: Optional[int] = None,
                     ):
    cache_key = f"books_list:{search}"

    # Try to get cached data
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    async with db as session:
        query = select(Book)

        if search:
            if search:
                query = query.where(
                    or_(
                        Book.title.contains(search),
                        Book.isbn.contains(search)
                    )
                )

        if category:
            query = query.where(Book.category_id == category)

        result = await session.execute(query)
        books = result.scalars().all()

        if not books:
            raise HTTPException(status_code=404, detail="No books found")

        books_list = [BookList.from_orm(book) for book in books]

        # Cache the data
        redis_client.set(cache_key, json.dumps([book.dict() for book in books_list]), ex=CACHE_EXPIRE_DATE)
        return books_list


@router.post("/create/", response_model=BookOut, status_code=201)
async def create_book(
    new_book: BookCreate,
    user: User = Depends(admin_user),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        # Check if the book already exists
        existing_book = await session.execute(
            select(Book).where(Book.title == new_book.title)
        )
        if existing_book.scalars().first():
            raise HTTPException(status_code=400, detail="Book already exists")

        book = Book(
            title=new_book.title,
            isbn=new_book.isbn,
            category_id=new_book.category,
            author_id=new_book.author,
        )

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book


@router.post("/createGoogleBook/", status_code=201)
async def create_book_with_google(
    book_data: BookCreateGoogle,
    background_tasks: BackgroundTasks,
    user: User = Depends(admin_user),
    db: AsyncSession = Depends(get_db),
):
    # Add a background task
    background_tasks.add_task(fetch_and_create_books_by_category, db, book_data.category)

    return {"status": "ok"}

from fastapi import APIRouter

from app.api.endpoints import users, books, memberships, category, author


api_router = APIRouter()

api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(books.router, prefix='/books', tags=['Books'])
api_router.include_router(memberships.router, prefix='/memberships', tags=['Membership'])
api_router.include_router(category.router, prefix='/category', tags=['Category'])
api_router.include_router(author.router, prefix='/author', tags=['Author'])

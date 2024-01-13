from pydantic import BaseModel
from typing import Optional


class AuthorBase(BaseModel):
    id: int
    username: str


class CategoryBase(BaseModel):
    id: int
    title: str


class BookCreateGoogle(BaseModel):
    category: str


class BookList(BaseModel):
    id: int
    title: str
    isbn: str
    category_id: Optional[int]
    author_id: Optional[int]

    class ConfigDict:
        from_attributes = True


class BookCreate(BaseModel):
    id: int
    title: str
    isbn: str
    category: int
    author: int


class BookOut(BaseModel):
    id: int
    title: str
    isbn: str
    category_id: int
    author_id: int


class BookDetail(BaseModel):
    id: int
    title: str
    isbn: str
    category: CategoryBase
    author: AuthorBase


__all__ = ['BookDetail', 'BookList', 'BookCreate', 'BookOut', 'BookCreateGoogle']

from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int
    title: str


__all__ = ['CategoryBase']

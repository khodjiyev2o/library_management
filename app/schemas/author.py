from pydantic import BaseModel


class AuthorBase(BaseModel):
    id: int
    username: str


__all__ = ['AuthorBase']

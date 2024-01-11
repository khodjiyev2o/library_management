from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_admin: bool


__all__ = ['UserIn', 'UserOut']

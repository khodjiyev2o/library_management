from sqlalchemy import Column, DateTime, Integer, String, Boolean, func, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as PythonEnum

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Back-reference to memberships
    memberships = relationship("UserMembership", back_populates="user")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    # Back-reference to books
    books = relationship("Book", back_populates="author")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    # Back-reference to books
    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String)
    language = Column(String)
    publication_date = Column(DateTime(timezone=True))

    # Foreign key relationship with Category
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="books")

    # Foreign key relationship with Author
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", back_populates="books")


class UserMembership(Base):
    __tablename__ = "user_membership"

    class MembershipStatus(PythonEnum):
        ACTIVE = "active"
        BLOCKED = "blocked"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(MembershipStatus), default=MembershipStatus.ACTIVE)  # Added status column with Enum

    # Define relationships
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="memberships")

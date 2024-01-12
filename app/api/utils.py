import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Book, Author, Category


async def find_or_create_author(session, author_name):
    result = await session.execute(select(Author).where(Author.username == author_name))
    author = result.scalars().first()
    if not author:
        author = Author(username=author_name)
        session.add(author)
        await session.commit()
        await session.refresh(author)
    return author


async def find_or_create_category(session, category_name):
    result = await session.execute(select(Category).where(Category.title == category_name))
    category = result.scalars().first()
    if not category:
        category = Category(title=category_name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
    return category


async def fetch_and_create_books_by_category(session: AsyncSession, category: str):
    async def fetch_and_create_books_by_category(session: AsyncSession, category_name: str):
        google_books_url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{category_name}"
        async with httpx.AsyncClient() as client:
            response = await client.get(google_books_url)
            if response.status_code == 200:
                data = response.json()

                for item in data.get('items', []):
                    book_info = item.get('volumeInfo', {})
                    title = book_info.get('title', 'Unknown Title')
                    author = book_info.get('authors', ['Unknown Author'])[0]
                    category = book_info.get('categories', ['Unknown Category'])[0]
                    isbn_list = [identifier['identifier'] for identifier in book_info.get('industryIdentifiers', []) if
                                 identifier['type'] == 'ISBN_13']

                    # Check for existing ISBN and continue if found
                    if isbn_list:
                        isbn = isbn_list[0]
                        existing_book = await session.execute(select(Book).where(Book.isbn == isbn))
                        if existing_book.scalars().first():
                            continue

                    # Find or create the Author
                    result = await session.execute(select(Author).where(Author.username == author))
                    author = result.scalars().first()
                    if not author:
                        author = Author(username=author)
                        session.add(author)
                        await session.flush()  # Flush to assign an ID

                    # Find or create the Category
                    result = await session.execute(select(Category).where(Category.title == category))
                    category = result.scalars().first()
                    if not category:
                        category = Category(title=category_name)
                        session.add(category)
                        await session.flush()  # Flush to assign an ID

                    # Create new book
                    new_book = Book(title=title, isbn=isbn, author_id=author.id, category_id=category.id)
                    session.add(new_book)

                    await session.commit()



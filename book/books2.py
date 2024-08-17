from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: int | None = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "author",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2012,
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithruby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithruby', 'A great book', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithruby', 'A very nice book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book description', 3, 2028),
    Book(5, 'HP2', 'Author 2', 'Book description', 2, 2027),
    Book(6, 'HP3', 'Author 3', 'Book description', 1, 2026),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    # 굳이 for 문을 돌리네
    for book in BOOKS:
        if book.id == book_id:
            return book
    # 못 찾았을 때
    raise HTTPException(status_code=404, detail="Item not found")


# 뭘로 가야하지
@app.get("/books/publish/")
async def read_book_by_published_date(book_published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == book_published_date:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/")
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else len(BOOKS) + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    # 업데이트 북을 한다.
    book_chage = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_chage = True
            break
    if not book_chage:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_chage = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_chage = True
            break
    if not book_chage:
        raise HTTPException(status_code=404, detail="Item not found")

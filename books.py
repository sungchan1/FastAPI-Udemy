from typing import List

from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Six', 'category': 'math'},
]

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    print(new_book)
    BOOKS.append(new_book)
    return BOOKS




@app.get("/books")
async def read_all_books():
    return BOOKS









@app.get("/books/mybook")
async def read_my_book():
    return {'title': 'My Book', 'author': 'Me', 'category': 'science'}



@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book['title'] == book_title:
            return book


@app.get("/books/{book_title}")
async def read_category_by_query(book_author: str, category: str):
    books = []
    for book in BOOKS:
        if book.get('author') == book_author and book.get('category') == category:
            books.append(book)



@app.get("/books/")
async def read_books_by_category(category: str):
    books = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books.append(book)
    return books


@app.get("/books/{book_author}/")
async def read_books_by_author(category: str, book_author: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books.append(book)
    return books



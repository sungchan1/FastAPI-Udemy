from typing import List

from fastapi import FastAPI
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









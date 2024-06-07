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


# Pydantic 모델 정의
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

items = [
    {"name": "Item1", "description": "This is item 1", "price": 10.5, "tax": 0.5},
    {"name": "Item2", "description": "This is item 2", "price": 20.0, "tax": 1.0},
]

# 경로 연산자 및 요청 처리 함수 정의
@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

# 특정 아이템을 ID로 조회하는 엔드포인트 정의

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    return items[item_id]

# 새로운 아이템을 추가하는 엔드포인트 정의
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item.dict())
    return item





@app.get("/books")
async def read_all_books():
    return BOOKS




@app.get("/books/mybook")
async def read_my_book():
    return {'title': 'My Book', 'author': 'Me', 'category': 'science'}



@app.get("/books/{book_name}")
async def read_book(book_name: str):
    return BOOKS[int(book_name)]








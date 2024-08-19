from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user



router = APIRouter(
    prefix="/admin",
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")
    return db.query(Todos).all()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")
    todo_model = db.query(Todos).filter(todo_id == Todos.id).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Todo not found")
    db.query(Todos).filter(todo_id == Todos.id).delete()
    db.commit()




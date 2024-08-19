from fastapi import status

from .utils import *
from ..routers.admin import get_db, get_current_user
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'completed': False, 'title': "Learn to code!",
                                'description': "Need to learn every day!",
                                'id': 1,
                                'priority': 1,
                                "owner_id": 1,
                                }]
def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    db.query(Todos).filter(1 == Todos.id).first()

    assert Todos in None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}

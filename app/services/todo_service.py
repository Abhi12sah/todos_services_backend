from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from app.exceptions.custom import (
    UserNotFoundException,
    TodoNotFoundException,
)

from app.models.user import User


def get_todo_or_404(
    db: Session,
    todo_id: int
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .first()
    )

    if not todo:
        raise TodoNotFoundException()

    return todo


def get_todos(
    db: Session,
    user_id: int | None = None
):
    query = db.query(Todo)

    if user_id is not None:
        query = query.filter(
            Todo.user_id == user_id
        )

    return query.all()


def get_user_todos(
    db: Session,
    user_id: int
):
  
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise UserNotFoundException()

    return (
        db.query(Todo)
        .filter(Todo.user_id == user_id)
        .all()
    )


def create_todo(
    db: Session,
    todo_data: TodoCreate
):
    
    user = (
        db.query(User)
        .filter(User.id == todo_data.user_id)
        .first()
    )

    if not user:
        raise UserNotFoundException()

    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        status=todo_data.status,
        priority=todo_data.priority,
        due_date=todo_data.due_date,
        user_id=todo_data.user_id
    )

    db.add(new_todo)

    try:
        db.commit()
        db.refresh(new_todo)
    except Exception:
        db.rollback()
        raise

    return new_todo


def update_todo(
    db: Session,
    todo_id: int,
    todo_data: TodoUpdate
):
    todo = get_todo_or_404(
        db=db,
        todo_id=todo_id
    )

    update_data = todo_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(todo, field, value)

    try:
        db.commit()
        db.refresh(todo)
    except Exception:
        db.rollback()
        raise

    return todo


def delete_todo(
    db: Session,
    todo_id: int
):
    todo = get_todo_or_404(
        db=db,
        todo_id=todo_id
    )

    db.delete(todo)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return None
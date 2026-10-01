from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut


router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@router.post(
    "",
    response_model=TodoOut,
    status_code=status.HTTP_201_CREATED
)
def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db)
):
   
    user = (
        db.query(User)
        .filter(User.id == todo_data.user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        status=todo_data.status.value,
        priority=todo_data.priority.value,
        due_date=todo_data.due_date,
        user_id=todo_data.user_id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get(
    "",
    response_model=list[TodoOut]
)
def get_todos(
    user_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Todo)


    if user_id is not None:
        query = query.filter(Todo.user_id == user_id)

    todos = query.all()

    return todos


@router.get(
    "/{todo_id}",
    response_model=TodoOut
)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .first()
    )

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@router.patch(
    "/{todo_id}",
    response_model=TodoOut
)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db)
):
    # Find Todo
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .first()
    )

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    update_data = todo_data.model_dump(exclude_unset=True)


    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = update_data["status"].value

    if "priority" in update_data and update_data["priority"] is not None:
        update_data["priority"] = update_data["priority"].value

   
    for field, value in update_data.items():
        setattr(todo, field, value)


    db.commit()
    db.refresh(todo)

    return todo



@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
  
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .first()
    )

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()

    return None
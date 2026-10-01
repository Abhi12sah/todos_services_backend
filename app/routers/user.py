from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.models.todo import Todo
from app.schemas.todo import TodoOut


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
   
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

  
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )


    new_user = User(
        email=user_data.email,
        name=user_data.name
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


@router.get(
    "",
    response_model=list[UserOut]
)
def get_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return users


@router.get(
    "/{user_id}",
    response_model=UserOut
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

   
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.patch(
    "/{user_id}",
    response_model=UserOut
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_data.email is not None:
        existing_user = (
            db.query(User)
            .filter(
                User.email == user_data.email,
                User.id != user_id
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

    update_data = user_data.model_dump(exclude_unset=True)

   
    for field, value in update_data.items():
        setattr(user, field, value)

    
    db.commit()
    db.refresh(user)

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    db.delete(user)

    db.commit()

    return None

@router.get(
    "/{user_id}/todos",
    response_model=list[TodoOut]
)
def get_user_todos(
    user_id: int,
    db: Session = Depends(get_db)
):
    
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    todos = (
        db.query(Todo)
        .filter(Todo.user_id == user_id)
        .all()
    )

    return todos
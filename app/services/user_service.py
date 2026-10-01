from fastapi import status
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserUpdate
from app.exceptions.custom import (
    UserNotFoundException,
    EmailAlreadyExistsException,
)


def get_user_or_404(
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

    return user


def get_users(
    db: Session
):
    return db.query(User).all()


def create_user(
    db: Session,
    user_data: UserCreate
):
    
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise EmailAlreadyExistsException()

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise

    return new_user


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate
):
    user = get_user_or_404(
        db=db,
        user_id=user_id
    )

    if user_data.name is not None:
        user.name = user_data.name

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
            raise EmailAlreadyExistsException()

        user.email = user_data.email

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    return user


def delete_user(
    db: Session,
    user_id: int
):
    user = get_user_or_404(
        db=db,
        user_id=user_id
    )

    db.delete(user)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return None
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field



class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128
    )



class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128
    )


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
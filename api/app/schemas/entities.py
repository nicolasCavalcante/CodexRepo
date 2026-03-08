from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=255)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = Field(default=None, min_length=2, max_length=255)


class UserRead(UserCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    sku: str = Field(min_length=2, max_length=100)
    name: str = Field(min_length=2, max_length=255)
    price: float = Field(gt=0)


class ProductRead(ProductCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(gt=0, default=1)


class OrderRead(OrderCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

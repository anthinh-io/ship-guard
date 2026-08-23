import uuid
from datetime import UTC, datetime
from typing import Literal

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# Database model, database table inferred from class name
class Order(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_code: str = Field(unique=True, index=True, max_length=64)
    customer_id: str | None = Field(default=None, index=True, max_length=64)
    estimated_delivery_date: datetime = Field(sa_type=DateTime(timezone=True))  # type: ignore
    actual_delivery_date: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    processing_status: str = Field(default="Chưa xử lý", max_length=50)


# Database model, database table inferred from class name
class Product(SQLModel, table=True):
    product_id: str = Field(primary_key=True, max_length=64)
    category_name: str | None = Field(default=None, max_length=100)
    category_name_english: str | None = Field(default=None, max_length=100)


# Database model, database table inferred from class name
class Seller(SQLModel, table=True):
    seller_id: str = Field(primary_key=True, max_length=64)
    seller_city: str | None = Field(default=None, max_length=100)
    seller_state: str | None = Field(default=None, max_length=2)


# Database model, database table inferred from class name
class Customer(SQLModel, table=True):
    customer_id: str = Field(primary_key=True, max_length=64)
    customer_city: str | None = Field(default=None, max_length=100)
    customer_state: str | None = Field(default=None, max_length=2)
    customer_zip_code_prefix: str | None = Field(default=None, max_length=10)


# Database model, database table inferred from class name
class OrderItem(SQLModel, table=True):
    order_id: str = Field(primary_key=True, max_length=64)
    order_item_id: int = Field(primary_key=True)
    product_id: str = Field(index=True, max_length=64)
    seller_id: str = Field(index=True, max_length=64)


class DashboardKpi(SQLModel):
    on_time_count: int
    late_count: int
    on_time_rate: float | None  # fraction 0.0-1.0, None khi chưa đủ dữ liệu
    late_rate: float | None


class OrderLookupItem(SQLModel):
    product_category: str | None
    seller_city: str | None
    seller_state: str | None


class OrderLookupResult(SQLModel):
    order_code: str
    estimated_delivery_date: datetime
    actual_delivery_date: datetime | None
    status: Literal["on_time", "late", "undetermined"]
    items: list[OrderLookupItem]
    customer_city: str | None
    customer_state: str | None
    customer_zip_code_prefix: str | None


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)

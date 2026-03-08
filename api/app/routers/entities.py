from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Order, Product, User
from app.schemas.entities import (
    OrderCreate,
    OrderRead,
    ProductCreate,
    ProductRead,
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.services.crud import CRUDService

router = APIRouter(prefix="/v1")

user_service = CRUDService(User)
product_service = CRUDService(Product)
order_service = CRUDService(Order)


@router.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return user_service.list(db)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.create(db, payload.model_dump())


@router.patch("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = user_service.update(db, user_id, payload.model_dump(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ok = user_service.delete(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return product_service.list(db)


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create(db, payload.model_dump())


@router.get("/orders", response_model=list[OrderRead])
def list_orders(db: Session = Depends(get_db)):
    return order_service.list(db)


@router.post("/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create(db, payload.model_dump())

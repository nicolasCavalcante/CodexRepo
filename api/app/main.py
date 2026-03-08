from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import engine, ensure_database_exists, get_db
from app.models import Base, Todo
from app.schemas import TodoCreate, TodoRead, TodoUpdate

app = FastAPI(title="TODO API")


@app.on_event("startup")
def on_startup() -> None:
    ensure_database_exists()
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/todos", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)) -> TodoRead:
    todo = Todo(**todo_in.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.get("/v1/todos", response_model=list[TodoRead])
def list_todos(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[TodoRead]:
    return db.query(Todo).offset(skip).limit(limit).all()


@app.get("/v1/todos/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> TodoRead:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@app.put("/v1/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, todo_in: TodoUpdate, db: Session = Depends(get_db)) -> TodoRead:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    for field, value in todo_in.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/v1/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> None:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    db.delete(todo)
    db.commit()

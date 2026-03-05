from fastapi import FastAPI

from app.db.session import Base, engine
from app.routers.entities import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD + Analytics Platform")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}

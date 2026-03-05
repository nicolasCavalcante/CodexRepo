from typing import Any

from sqlalchemy.orm import Session


class CRUDService:
    def __init__(self, model: Any):
        self.model = model

    def list(self, db: Session):
        return db.query(self.model).all()

    def get(self, db: Session, item_id: int):
        return db.get(self.model, item_id)

    def create(self, db: Session, payload: dict):
        instance = self.model(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def update(self, db: Session, item_id: int, payload: dict):
        instance = self.get(db, item_id)
        if not instance:
            return None
        for key, value in payload.items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
        return instance

    def delete(self, db: Session, item_id: int):
        instance = self.get(db, item_id)
        if not instance:
            return False
        db.delete(instance)
        db.commit()
        return True

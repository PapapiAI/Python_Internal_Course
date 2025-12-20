from typing import Any, Generic, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # -------- READ --------
    def get_by_id(self, db: Session, entity_id: Any) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == entity_id)  # type: ignore[attr-defined]
        return db.execute(stmt).scalars().first()

    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> list[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        return list(db.execute(stmt).scalars().all())

    # -------- WRITE --------
    def create(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: ModelType, data: dict[str, Any]) -> ModelType:
        for field, value in data.items():
            setattr(obj, field, value)

        db.flush()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: ModelType) -> None:
        db.delete(obj)
        db.flush()

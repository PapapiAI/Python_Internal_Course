from __future__ import annotations

from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.base import Base  # DeclarativeBase của bạn


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    BaseRepository chuẩn enterprise (SQLAlchemy 2.x, sync).

    Lưu ý quan trọng:
    - Repository KHÔNG commit/rollback/close session.
    - Middleware quản lý transaction theo request.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # -------- READ --------
    def get_by_id(self, db: Session, entity_id: Any) -> ModelType | None:
        """
        Lấy bản ghi theo ID. Không tìm thấy -> None
        """
        stmt = select(self.model).where(self.model.id == entity_id)  # type: ignore[attr-defined]
        return db.execute(stmt).scalars().first()

    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> list[ModelType]:
        """
        Lấy danh sách bản ghi (cơ bản).
        """
        stmt = select(self.model).offset(offset).limit(limit)
        return list(db.execute(stmt).scalars().all())

    # -------- WRITE --------
    def create(self, db: Session, obj: ModelType) -> ModelType:
        """
        Tạo mới bản ghi.
        - db.add để đưa object vào session
        - db.flush để DB cấp ID (nếu auto increment)
        - db.refresh để lấy dữ liệu mới nhất từ DB
        """
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: ModelType) -> None:
        """
        Xóa bản ghi (hard delete).
        """
        db.delete(obj)
        db.flush()

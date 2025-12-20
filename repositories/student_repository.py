from sqlalchemy import select
from sqlalchemy.orm import Session

from models.student import Student
from repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository[Student]):

    def __init__(self):
        super().__init__(Student)

    def get_by_email(self, db: Session, email: str) -> Student | None:
        stmt = select(Student).where(Student.email == email)
        return db.execute(stmt).scalars().first()

    def search(
            self,
            db: Session,
            *,
            keyword: str | None = None,
            min_age: int | None = None,
            max_age: int | None = None,
            offset: int = 0,
            limit: int = 100,
    ) -> list[Student]:
        stmt = select(Student)

        if keyword:
            stmt = stmt.where(Student.full_name.ilike(f"%{keyword}%"))

        if min_age is not None:
            stmt = stmt.where(Student.age >= min_age)

        if max_age is not None:
            stmt = stmt.where(Student.age <= max_age)

        stmt = stmt.offset(offset).limit(limit)
        return list(db.execute(stmt).scalars().all())

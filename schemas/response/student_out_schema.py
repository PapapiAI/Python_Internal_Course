from datetime import datetime
from pydantic import BaseModel, EmailStr


class StudentOut(BaseModel):
    id: int
    full_name: str
    age: int
    email: EmailStr
    phone_number: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        # Cho phép map trực tiếp từ SQLAlchemy ORM object
        from_attributes = True

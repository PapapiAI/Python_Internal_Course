from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    # Base hiện tại chưa cần thêm logic
    # nhưng bắt buộc phải tồn tại như một lớp con
    # để SQLAlchemy sử dụng
    pass
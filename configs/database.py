from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs.env import settings_config

settings = settings_config()

engine = create_engine(
    settings.database_url,
    echo=False, # tắt echo để tránh duplicate log DB
    pool_pre_ping=True,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

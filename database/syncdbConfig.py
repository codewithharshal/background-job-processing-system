import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:admin123@localhost:3307/jobProcess",
)

engine = create_engine(
    database_url,
    echo=True,
    pool_size=5,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(engine, expire_on_commit=False)

import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

database_url = os.getenv(
    "ASYNC_DATABASE_URL",
    "mysql+aiomysql://root:admin123@localhost:3307/jobProcess",
)

engine = create_async_engine(
    database_url,
    echo=True,
    pool_size=5,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

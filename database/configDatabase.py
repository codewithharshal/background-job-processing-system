from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    "mysql+aiomysql://root:admin123@localhost:3306/jobProcess",
    echo=True,
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
from sqlalchemy.orm import DeclarativeBase
from database.asyncdbConfig import AsyncSessionLocal
from database.syncdbConfig import SessionLocal

class Base(DeclarativeBase):
    pass


# Asysnc Session DB Engine
async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# Sync Session DB Engine
def get_sync_db():
    with SessionLocal() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
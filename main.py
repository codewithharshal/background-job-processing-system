from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from database.configDatabase import engine
from apis.jobs import router

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Open the database connection pool at startup and dispose it at shutdown."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)

from .config import settings
from .models import Base

async_engine: AsyncEngine = create_async_engine(url=settings.DATABASE_URL, echo=False)


async_session: AsyncSession = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_async_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

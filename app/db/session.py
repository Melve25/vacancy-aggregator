from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

async_engine = create_async_engine(settings.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
	async with AsyncSessionLocal() as session:
		yield session
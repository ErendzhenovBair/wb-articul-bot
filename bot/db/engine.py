from typing import Union

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from data import config
from db.base_class import Base
from db import models

BASE_URL = URL.create(
    "postgresql+asyncpg",
    username=config.POSTGRES_USER,
    host=config.POSTGRES_HOST,
    password=config.POSTGRES_PASSWORD,
    port=config.POSTGRES_PORT
    )

engine = create_async_engine(url=BASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
from typing import TypeVar, Generic, Type, Optional, List
import logging

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from db.base_class import Base
from db.engine import SessionLocal

ModelType = TypeVar('ModelType', bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @staticmethod
    def get_session():
        return SessionLocal()
        
    async def get_last_n_requests(self, n: int):
        async with self.get_session() as session:
            query = select(self.model).order_by(self.model.request_time.desc()).limit(n)
            result = await session.execute(query)
            last_requests = result.scalars().all()
            logging.debug(f"Last requests retrieved: {last_requests}")
            return last_requests

    async def create(self, **obj_in_data) -> ModelType:
        async with self.get_session() as session:
            db_obj = self.model(**obj_in_data)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def remove(self, id: int):
        async with self.get_session() as session:
            await session.execute(delete(self.model).where(self.model.id == id))
            await session.commit()

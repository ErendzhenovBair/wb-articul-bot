from typing import Generic, List, Type, TypeVar

from sqlalchemy import delete, select

from db.base_class import Base
from db.engine import SessionLocal

ModelType = TypeVar('ModelType', bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @staticmethod
    def get_session():
        return SessionLocal()
        
    async def get_last_n_requests(self, n: int) -> List[ModelType]:
        async with self.get_session() as session:
            query = select(
                self.model
                ).order_by(self.model.request_time.desc()).limit(n)
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_requests_by_user_article(
            self, 
            user_id: int,
            article_number: int
    ) -> List[ModelType]:
        async with self.get_session() as session:
            query = (
                select(self.model)
                .filter(
                    self.model.user_id == user_id,
                    self.model.product_article == article_number)
            )
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_requests_by_user_id(
            self, 
            user_id: int,
    ) -> List[ModelType]:
        async with self.get_session() as session:
            query = (
                select(self.model)
                .filter(
                    self.model.user_id == user_id,
                    self.model.subscribed
                )
            )
            result = await session.execute(query)
            return result.scalars().all()
        
    async def get_subscribed_article_numbers(
            self) -> List[ModelType]:
            async with self.get_session() as session:
                query = (
                    select(
                        self.model.user_id,
                        self.model.product_article)
                        .filter(self.model.subscribed)
                        .distinct()
                )
                result = await session.execute(query)
                return result.fetchall()

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
    
    async def update(self, db_obj: ModelType, **obj_in_data) -> ModelType:
        async with self.get_session() as session:
            for field, value in obj_in_data.items():
                setattr(db_obj, field, obj_in_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

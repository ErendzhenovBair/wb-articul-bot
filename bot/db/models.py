from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func

from db.base_class import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    request_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    product_article = Column(String, nullable=False)

    def __str__(self):
        return (
            f"Пользователь:{self.user_id}, "
            f"Время запроса:{self.request_time}, "
            f"Артикул товара:{self.product_article}"
        )

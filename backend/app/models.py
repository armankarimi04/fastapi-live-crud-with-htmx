import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase



class Base(AsyncAttrs, DeclarativeBase):

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),  
    }



class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64))
    author: Mapped[str] = mapped_column(nullable=True)
import datetime
from typing import List
from decimal import Decimal

from sqlalchemy import DateTime, String, ForeignKey, Numeric
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase



class Base(AsyncAttrs, DeclarativeBase):

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),  
    }



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")
    in_stock: Mapped[int] = mapped_column(nullable=True)
    available: Mapped[bool] = mapped_column(nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=3), default=0) # precision: num of digits in number, scale: num of digits to the right side of the decimal point


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    products: Mapped[List["Product"]] = relationship(back_populates="category")


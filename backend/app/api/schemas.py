from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from decimal import Decimal

from app.models import Product


class ProductIn(BaseModel):
    name: str
    category_id: int
    in_stock: int | None = None
    available: bool | None = False
    price: Decimal = Decimal(value="0")

    @model_validator(mode="before")
    @classmethod
    def clean_empty_values_for_numeric(cls, values):
        values = values.copy()

        if values.get("in_stock") == "":
            values["in_stock"] = 0

        if values.get("price") == "":
            values["price"] = Decimal("0")

        return values


class ProductUpdate(BaseModel):
    name: str
    category_id: int
    in_stock: int | None = None
    available: bool | None = False
    price: Decimal | None = None
    row_index: int | None = None



class ProductPartialUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    in_stock: int | None = None
    available: bool | None = False
    price: Decimal | None = None
    row_index: int | None = None



class ProductOut(BaseModel):
    id: int
    name: str
    category_id: int
    in_stock: int | None = None
    available: bool | None = None
    price: float | None = None
    
    model_config = ConfigDict(from_attributes=True)


class MultipleProducts(BaseModel):
    products: list[ProductOut]
    total: int


class CategoryIn(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str


# Kept as a sample to demonstrate another approach
class _ProductIn(BaseModel):
    name: str
    category_id: int
    in_stock: int | None = None
    available: bool | None = False
    price: Decimal = Decimal(value="0")

    # now this handles "" (empty string) submitted from html forms
    @field_validator("in_stock", mode="before")
    @classmethod
    def convert_empty_stock_to_zero(cls, value):
        if value == "":
            return 0
        return value

    @field_validator("price", mode="before")
    @classmethod
    def convert_empty_price_to_zero(cls, value):
        if value == "":
            return Decimal("0")
        return value
from pydantic import BaseModel



class ProductIn(BaseModel):
    name: str
    category_id: int
    in_stock: int | None = None
    available: bool | None = False


class ProductUpdate(BaseModel):
    name: str
    category_id: int
    in_stock: int | None = None
    available: bool | None = False
    row_index: int | None = None


class ProductOut(BaseModel):
    id: int
    name: str
    category_id: int
    in_stock: int | None = None
    available: bool | None = None


class MultipleProducts(BaseModel):
    items: list[ProductOut]


class CategoryIn(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str
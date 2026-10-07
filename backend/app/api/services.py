from decimal import Decimal
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi_filters.ext.sqlalchemy import apply_sorting

from app.dependencies import AsyncSessionDep
from app.models import Product, Category
from .schemas import ProductIn, ProductOut, ProductPartialUpdate


async def get_all_products_sorted(db: AsyncSessionDep, sorting):
    stmt = apply_sorting(select(Product), sorting=sorting)
    query = await db.scalars(stmt)
    result = query.all()
    return result


async def get_product(item_id: int, db: AsyncSessionDep) -> Product:
    stmt = select(Product).options(selectinload(Product.category)).where(Product.id == item_id)
    item = await db.scalar(stmt)
    if item:
        return item
    return None



async def create_product(db: AsyncSessionDep, data: ProductIn) -> Product:
    new_item = Product(
        name=data.name, category_id=data.category_id, in_stock=data.in_stock, available=data.available, price=data.price
    )
    db.add(new_item)
    await db.flush() # insert but do not close transaction
    result = await db.execute(select(Product).where(Product.id == new_item.id).options(selectinload(Product.category)))
    item = result.scalar_one()
    await db.commit()
    return item


async def update_product(item_id: int, data: ProductIn, db: AsyncSessionDep):
    item_db = await get_product(item_id, db)
    if item_db:
        data = data.model_dump()
        for field, value in data.items():
            setattr(item_db, field, value)
        await db.commit()
        await db.refresh(item_db)
        return item_db
    return None


async def update_product_partially(item_id: int, data: ProductPartialUpdate, db: AsyncSessionDep) -> Product:
    item = await get_product(item_id, db)
    if not item:
        return None
    update_values = data.model_dump(exclude_unset=True)
    for field, value in update_values.items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item



async def remove_product(item_id: int, db: AsyncSessionDep) -> None:
    await db.execute(delete(Product).where(Product.id == item_id))
    await db.commit()


async def remove_multiple_products() -> int:
    pass


async def all_products(db: AsyncSessionDep) -> tuple[list, int]:
    query = await db.scalars(
        statement=select(Product)
            .options(selectinload(Product.category))
    )
    results = query.all()
    return results, len(results)


async def all_products_by_category(category_id: int, db: AsyncSessionDep) -> tuple[list, int]:
    stmt = select(Product).where(Product.category_id == category_id)
    query = await db.scalars(stmt)
    results = query.all()
    return results, len(results)


async def create_category(db: AsyncSessionDep, name: str) -> Category | None:
    try:
        new_item = Category(name=name)
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
        return new_item
    except IntegrityError:
        await db.rollback()
        return None


async def get_all_categories(db: AsyncSessionDep):
    query = await db.scalars(statement=select(Category))
    items = query.all()
    return items

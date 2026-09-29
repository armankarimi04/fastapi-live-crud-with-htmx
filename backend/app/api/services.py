from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.dependencies import AsyncSessionDep
from app.models import Product, Category
from .schemas import ProductIn


async def get_product(item_id: int, db: AsyncSessionDep):
    stmt = select(Product).options(selectinload(Product.category)).where(Product.id == item_id)
    query = await db.scalar(stmt)
    return query


async def create_product(
    db: AsyncSessionDep,
    name: str,
    category_id: int,
    in_stock: int = 0,
    available: bool = False,
) -> Product:
    new_item = Product(
        name=name, 
        category_id=category_id, 
        in_stock=in_stock, 
        available=available
    )
    db.add(new_item)
    await db.flush() # insert but do not close transaction
    # await db.commit()
    # await db.refresh(new_item)
    # return new_item
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


async def remove_product():
    pass


async def all_products(db: AsyncSessionDep) -> tuple[list, int]:
    query = await db.scalars(
        statement=select(Product)
            .options(
                selectinload(Product.category)
            )
    )
    results = query.all()
    return results, len(results)


async def get_all_products_by_category():
    pass


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

import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models import Category, Product
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)
async_session = async_sessionmaker(engine)


async def seed_categories():
    with open("app/seed/categories.json") as f:
        data = json.load(f)

    async with async_session() as session:
        for item in data:
            category = Category(name=item["name"])
            session.add(category)
        try: 
            await session.commit()
        except IntegrityError:
            pass


async def seed_products():
    with open("app/seed/products.json") as f:
        data = json.load(f)

    async with async_session() as session:
        for item in data:
            category = Product(
                name=item["name"],
                category_id=item["category_id"],
                in_stock=item["in_stock"],
                available=item["available"],
                price=item["price"]
            )
            session.add(category)
        try:
            await session.commit()
        except IntegrityError:
            pass


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_categories())
    asyncio.run(seed_products())


# to validate before seeding
# with open("app/seed/products.json") as f:
#     raw_data = json.load(f)

# products = [ProductSeed.model_validate(item) for item in raw_data]

# with Session(engine) as session:
#     for data in products:
#         session.add(Product(**data.model_dump()))

#     session.commit()
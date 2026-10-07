# This file contains json responses
from typing import Annotated
from fastapi import APIRouter, Request, Response, HTTPException, status, Form, Depends
from fastapi.responses import JSONResponse
from datatables_server import DataTable, Column
from fastapi_filters import SortingValues, create_sorting

from app.utilities import templates
from app.dependencies import AsyncSessionDep
from app.database import async_engine
from . import schemas
from .schemas import ProductOut
from . import services


router = APIRouter()


@router.get("/products/sorted")
async def get_sorted_products(
        db: AsyncSessionDep, 
        sorting: SortingValues = Depends(create_sorting("name"))
    ) -> schemas.MultipleProducts:
    products = await services.get_all_products_sorted(db, sorting)
    if products:
        return schemas.MultipleProducts(products=products, total=len(products))



@router.post("/categories/")
async def categories_create(request: Request, data: schemas.CategoryIn, db: AsyncSessionDep) -> schemas.CategoryOut:
    new_category = await services.create_category(db, name=data.name)
    if new_category:
        return schemas.CategoryOut.model_validate(new_category)
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="This Category already exists")



@router.post("/products")
async def products_create(request: Request, data: schemas.ProductIn, db: AsyncSessionDep):
    new_product = await services.create_product(db, data)
    if new_product:
        return new_product
    raise HTTPException(500)



@router.get("/product/{item_id}")
async def get_item(request: Request, item_id: int, db: AsyncSessionDep) -> ProductOut:
    item = await services.get_product(item_id, db)
    if item:
        return ProductOut.model_validate(item)
    raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Product not found 404")



@router.get("/product/by-category/{category_id}")
async def get_products_by_category(request: Request, category_id: int, db: AsyncSessionDep):
    products = await services.all_products_by_category(category_id, db)
    if products:
        return {"products": products[0], "count": products[1]}
    raise None



@router.get("/products")
async def get_products(request: Request, db: AsyncSessionDep) -> schemas.MultipleProducts:
    products = await services.all_products(db)
    if products:
        return schemas.MultipleProducts(products=products[0], total=products[1])
    return None



# Datatables.js
@router.get("/provide-data")
async def provide_data(request: Request, db: AsyncSessionDep):
    params = request.query_params
    draw = int(params.get("draw", 1))
    start = int(params.get("start", 0))
    length = int(params.get("length", 10))
    search = params.get("search[value]", "")
    items, count = await services.all_products(db)
    items_list = [ProductOut.model_validate(product) for product in items]
    items_dict = [product.model_dump() for product in items_list]
    return JSONResponse({
        "draw": draw,
        "recordsTotal": count,
        "recordsFiltered": count,
        "data": items_dict
    })
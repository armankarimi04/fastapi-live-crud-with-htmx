# This file contains json responses
from typing import Annotated
from fastapi import APIRouter, Request, Response, HTTPException, status, Form
from fastapi.responses import JSONResponse
from datatables_server import DataTable, Column

from app.utilities import templates
from app.dependencies import AsyncSessionDep
from app.database import async_engine
from . import schemas
from .schemas import ProductOut
from . import services


router = APIRouter()



@router.get("/get-message")
async def get_message(request: Request):
    if request.headers.get("HX-Request"):
        return "Hello from fastapi"
    return "Request was not htmx"



@router.post("/categories/")
async def categories_create(request: Request, data: schemas.CategoryIn, db: AsyncSessionDep) -> schemas.CategoryOut:
    new_category = await services.create_category(db, name=data.name)
    if new_category:
        return new_category
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="This Category already exists")




@router.get("/item/{item_id}")
async def get_item(request: Request, item_id: int, db: AsyncSessionDep) -> ProductOut:
    item = await services.get_product(item_id, db)
    if item:
        return ProductOut.model_validate(item)



# this is just for my learning purposes, please ignore it
@router.get("/some")
async def html_or_swagger(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return {"response": "HTML request"}
    return {"response": "API/Swagger request"}



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
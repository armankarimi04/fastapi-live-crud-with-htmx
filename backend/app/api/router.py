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


@router.get("/list2")
async def test_table(request: Request, db: AsyncSessionDep):
    items, count = await services.all_products(db)
    categories = await services.get_all_categories(db)
    return templates.TemplateResponse(request, "main/list2.html", {'items': items, 'count': count, 'categories': categories})


# wroks with errors, renaming to 2
@router.get("/provide-data2", response_model=list[schemas.ProductOut])
async def provide_data2(request: Request, db: AsyncSessionDep):
    items, count = await services.all_products(db)
    return items


@router.get("/provide-data")
async def provide_data(request: Request, db: AsyncSessionDep):
    params = request.query_params
    draw = int(params.get("draw", 1))
    start = int(params.get("start", 0))
    length = int(params.get("length", 10))
    search = params.get("search[value]", "")
    items, count = await services.all_products(db)
    # print("\nITEMS ->", items, "\n")
    items_list = [
        ProductOut.model_validate(product)
        for product in items
    ]

    # print("\nITEMS_LIST ->", items_list, "\n")

    items_dict = [
        product.model_dump() for product in items_list
    ]

    # print("\nITEMS_DICT ->", items_dict, "\n")

    return JSONResponse({
        "draw": draw,
        "recordsTotal": len(items),
        "recordsFiltered": len(items),
        "data": [product.model_dump() for product in items_list]
    })


@router.get("/")
async def index(request: Request) -> Response:
    return templates.TemplateResponse(request, "main/index.html", {})


@router.get("/list")
async def items_list(request: Request, db: AsyncSessionDep) -> Response:
    items, count = await services.all_products(db)
    categories = await services.get_all_categories(db)
    return templates.TemplateResponse(request, "main/list.html", {'items': items, 'count': count, 'categories': categories})


@router.get("/all")
async def items_all(request: Request, db: AsyncSessionDep):
    items, _ = await services.all_products(db)
    return templates.TemplateResponse(request, "main/fragments/data/table-body.html", {'items': items})


@router.post("/")
async def items_create(request: Request, data: Annotated[schemas.ProductIn, Form()], db: AsyncSessionDep):
    new_product = await services.create_product(db, data)
    if new_product:
        if request.headers.get("HX-Request"):
            response = templates.TemplateResponse(request, "main/fragments/data/row.html", {'item': new_product})
            response.headers["HX-Trigger"] = "success"
            return response
        return new_product
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Something went wrong")


@router.post("/categories/")
async def categories_create(request: Request, data: schemas.CategoryIn, db: AsyncSessionDep) -> schemas.CategoryOut:
    new_category = await services.create_category(db, name=data.name)
    if new_category:
        return new_category
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="This Category already exists")


@router.get("/load-categories")
async def load_categories(request: Request, db: AsyncSessionDep):
    all_categories = await services.get_all_categories(db)
    if all_categories:
        return templates.TemplateResponse(request, "main/fragments/forms/categories-selectbox.html", {'categories': all_categories})


@router.get("/item/{item_id}")
async def get_row(request: Request, item_id: int, db: AsyncSessionDep):
    item = await services.get_product(item_id, db)
    if item:
        return templates.TemplateResponse(request, "main/fragments/data/row.html", {'product': item})



@router.put("/items/{item_id}")
async def update_product(
    request: Request, 
    item_id: int, 
    data: Annotated[schemas.ProductUpdate, Form()], 
    db: AsyncSessionDep
):
    # if don't need to return the object or update joined tables, ORM's update statement is more efficient
    updated_item = await services.update_product(item_id, data, db)
    if updated_item:
        response = templates.TemplateResponse(request, "main/fragments/data/row.html", {'item': updated_item, 'row_index': data.row_index})
        response.headers["HX-Trigger"] = f"editSuccess_{updated_item.id}"
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item was not found")



# this is just for my learning purposes, please ignore it
@router.get("/some")
async def html_or_swagger(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return {"response": "HTML request"}
    return {"response": "API/Swagger request"}
# This file contains template responses
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi import (
    APIRouter, 
    Request, 
    Response, 
    HTTPException, 
    status, 
    Form
)

from app.utilities import templates
from app.dependencies import AsyncSessionDep
from . import schemas
from . import services


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "main/index.html", {})



@router.get("/list", response_class=HTMLResponse)
async def items_list(request: Request, db: AsyncSessionDep):
    items, count = await services.all_products(db)
    categories = await services.get_all_categories(db)
    return templates.TemplateResponse(request, "main/list.html", {'items': items, 'count': count, 'categories': categories})



@router.get("/all", response_class=HTMLResponse)
async def items_all(request: Request, db: AsyncSessionDep):
    import time
    time.sleep(1)
    items, _ = await services.all_products(db)
    return templates.TemplateResponse(request, "main/fragments/data/table-body.html", {'items': items})



@router.post("/", response_class=HTMLResponse)
async def items_create(request: Request, data: Annotated[schemas.ProductIn, Form()], db: AsyncSessionDep):
    new_product = await services.create_product(db, data)
    if new_product:
        if request.headers.get("HX-Request"):
            response = templates.TemplateResponse(request, "main/fragments/data/row.html", {'item': new_product})
            response.headers["HX-Trigger"] = "success"
            return response
        return new_product
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Something went wrong")



@router.get("/load-categories", response_class=HTMLResponse)
async def load_categories(request: Request, db: AsyncSessionDep):
    all_categories = await services.get_all_categories(db)
    if all_categories:
        return templates.TemplateResponse(request, "main/fragments/forms/categories-selectbox.html", {'categories': all_categories})



@router.get("/item/{item_id}", response_class=HTMLResponse)
async def get_row(request: Request, item_id: int, db: AsyncSessionDep):
    item = await services.get_product(item_id, db)
    if item:
        return templates.TemplateResponse(request, "main/fragments/data/row.html", {'product': item})



@router.put("/items/{item_id}", )
async def update_product(
    request: Request, 
    item_id: int, 
    data: Annotated[schemas.ProductUpdate, Form()], 
    db: AsyncSessionDep
):
    # if don't need to return the object or update joined tables, ORM's update statement is more efficient
    updated_item = await services.update_product(item_id, data, db)
    if updated_item:
        context = {}
        context['item'] = updated_item
        context['row_index'] = data.row_index
        response = templates.TemplateResponse(request, "main/fragments/data/row.html", context)
        response.headers["HX-Trigger"] = f"editSuccess_{updated_item.id}"
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item was not found")



@router.patch("/items/{item_id}")
async def update_product_partially(request: Request, item_id: int, form_data: Annotated[schemas.ProductPartialUpdate, Form()], db: AsyncSessionDep):
    updated_item = await services.update_product_partially(item_id, data=form_data, db=db)
    if updated_item:
        pass


# Datatables.js
@router.get("/list2")
async def test_table(request: Request, db: AsyncSessionDep):
    items, count = await services.all_products(db)
    categories = await services.get_all_categories(db)
    return templates.TemplateResponse(request, "main/list2.html", {
            'items': items, 
            'count': count, 
            'categories': categories
        })
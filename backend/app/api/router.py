# This file contains json responses
from typing import Annotated
from fastapi import APIRouter, Request, Response, HTTPException, status, Form
from fastapi.responses import JSONResponse

from app.utilities import templates
from app.dependencies import AsyncSessionDep
from . import schemas
from . import services

router = APIRouter()


# this is not reliable
@router.get("/some")
async def something(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return {"response": "HTML request"}
    return {"response": "API/Swagger request"}


@router.get("/")
async def index(request: Request) -> Response:
    return templates.TemplateResponse(request, "main/index.html", {})


@router.get("/list")
async def items_list(request: Request, db: AsyncSessionDep) -> Response:
    items, count = await services.all_products(db)
    categories = await services.get_all_categories(db)
    return templates.TemplateResponse(request, "main/list.html", {'items': items, 'count': count, 'categories': categories})


@router.get("/items/all")
async def items_all(request: Request, db: AsyncSessionDep):
    import time
    time.sleep(2)
    items, _ = await services.all_products(db)
    return templates.TemplateResponse(request, "main/fragments/data/table-body.html", {'items': items})


@router.get("/edit-row/{item_id}")
async def edit_row(request: Request, item_id: int, db: AsyncSessionDep):
    item = await services.get_product(item_id, db)
    if item:
        return templates.TemplateResponse(request, "main/fragments/forms/row-edit-form.html", {'product': item})


@router.post("/items/")
async def items_create(request: Request, data: Annotated[schemas.ProductIn, Form()], db: AsyncSessionDep):
    new_product = await services.create_product(db, **data.model_dump())
    if new_product:
        if request.headers["HX-Request"]:
            response = templates.TemplateResponse(request, "main/fragments/data/row.html", {'item': new_product})
            response.headers["HX-Trigger"] = "success"
            return response
        return new_product
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Something went wrong")


@router.post("/new-product")
async def new_product(request: Request, data: Annotated[schemas.ProductIn, Form()], db: AsyncSessionDep):
    new_product = await services.create_product(db, name=data.name, category_id=data.category_id, in_stock=data.in_stock, available=data.available)
    if new_product:
        if request.headers["HX-Request"]:
            return templates.TemplateResponse(request, "main/fragments/messages/result.html")
    raise HTTPException(500)


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


@router.get("/row/{item_id}")
async def get_row(request: Request, item_id: int, db: AsyncSessionDep):
    item = await services.get_product(item_id, db)
    if item:
        return templates.TemplateResponse(request, "main/fragments/data/row.html", {'product': item})


@router.get("/get-message")
async def get_message_for_htmx(request: Request):
    return templates.TemplateResponse(request, "main/fragments/message.html", {'message': "hi"})


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


# Perhaps partial update (patch) was easier


@router.get("/load/new-product-form")
async def new_product_form(request: Request, db: AsyncSessionDep):
    categories = await services.get_all_categories(db)
    if request.headers["HX-Request"]:
        return templates.TemplateResponse(request, "main/fragments/forms/new-product-form.html", {'categories': categories})
    return Response("htmx failed")



# @app.post("/items")
# async def create_item(request: Request):
#     item = await create_item_in_db(...)

#     return templates.TemplateResponse(
#         "partials/item_row.html",
#         {
#             "request": request,
#             "item": item,
#         },
#     )
# Then:

# <!-- partials/item_row.html -->

# <tr>
#     <td>{{ item.name }}</td>
#     <td>{{ item.created_at }}</td>
# </tr>

# Because you have:

# hx-target="#items-table-body"
# hx-swap="beforeend"

# the new row gets appended to the table.



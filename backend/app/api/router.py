from fastapi import APIRouter, Request, Response

from app.utilities import templates

router = APIRouter()


@router.get("/")
async def index(request: Request) -> Response:
    return templates.TemplateResponse(request, "index.html", {})


@router.get("/get-message")
async def get_message_for_htmx(request: Request):
    return templates.TemplateResponse(request, "fragments/message.html", {'message': "hi"})
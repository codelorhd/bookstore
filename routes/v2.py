from fastapi.routing import APIRouter
from models.author import Author
from fastapi.params import Body
from models.user import User
from fastapi import FastAPI, Body, Header, File
from models.book import Book
from starlette import status
from starlette.responses import Response

app_v2 = APIRouter()


@app_v2.post("/user", status_code=status.HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request body": "it is version 2"}

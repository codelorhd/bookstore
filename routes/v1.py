from os import stat

import jwt
from models.author import Author
from fastapi.params import Body
from models.user import User
from fastapi import FastAPI, Body, Header, File, Depends, HTTPException, APIRouter
from models.book import Book
from starlette import status
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from utils.security import authenticate_user, check_jwt_token, create_jwt_token
from models.jwt_user import JWTUser

app_v1 = APIRouter()


# authentication is needed
@app_v1.post("/user", status_code=status.HTTP_201_CREATED, tags=["User"])
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request body": user, "custom header": x_custom}


@app_v1.get("/user", tags=["User"])
async def get_user_validation(password: str):
    return {"query paramater": password}


@app_v1.get(
    "/book/{isbn}",
    response_model=Book,
    response_model_include=["name", "year"],
    tags=["Book"],
)
async def get_book_with_isbn(isbn):
    author_dict = {"name": "author1", "book": ["book1", "book2"]}
    author1 = Author(**author_dict)
    book_dict = {"isbn": "isbn1", "name": "book1", "year": 2019, "author": author1}
    book1 = Book(**book_dict)
    return book1


@app_v1.get("/author/{id}/book", tags=["Author"])
async def get_author_books(id: int, category: str, order: str = "asc"):
    return {"query ": order + category + str(id)}


@app_v1.patch("/author/name", tags=["Author"])
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}


@app_v1.post("/user/author", tags=["Author"])
async def post_user_and_author(
    user: User, author: Author, bookstore_name: str = Body(..., embed=True)
):
    return {["User"]: user, "author": author, "bookstore_name": bookstore_name}


@app_v1.post("/user/photo", tags=["User"])
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")

    return {"file size": len(profile_photo)}

import pickle
from os import stat

import jwt
from fastapi import APIRouter, Body, Depends, FastAPI, File, Header, HTTPException
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import Response

import utils.redis_object as re
from models.author import Author
from models.book import Book
from models.user import User
from utils.db_functions import (
    db_check_personel,
    db_get_author,
    db_get_author_from_id,
    db_get_book_with_isbn,
    db_insert_personnel,
    db_patch_author_name,
)
from utils.helper_functions import upload_image_to_img_server

app_v1 = APIRouter()


# authentication is needed
@app_v1.post("/user", status_code=status.HTTP_201_CREATED, tags=["User"])
async def post_user(user: User):
    await db_insert_personnel(user)
    return {"result": "Personel is created"}

    # return {"request body": user, "custom header": x_custom}


@app_v1.post("/login", tags=["User"])
async def get_user_validation(username: str = Body(...), password: str = Body(...)):
    # talk to redis first
    redis_key = f"{username}-{password}"
    result = await re.redis.get(redis_key, encoding="utf-8")

    # Redis has the data
    if result:
        if result == "true":
            return {"is_valid {redis}": True}
        else:
            return {"is_valid {redis}": False}

    # Redis does not have the data
    else:
        result = await db_check_personel(username, password)
        await re.redis.set(redis_key, str(result), expire=60)

        return {"is_valiid {db}": result}


@app_v1.get(
    "/book/{isbn}",
    response_model=Book,
    response_model_include=["name", "year"],
    tags=["Book"],
)
async def get_book_with_isbn(isbn):

    result = await re.redis.get(isbn)
    if result:
        result_book = pickle.loads(result)
        return result_book
    else:
        book_dict = await db_get_book_with_isbn(isbn)

        if book_dict:
            author_dict = await db_get_author(book_dict["author"])
            if author_dict:
                author_obj = Author(**author_dict)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Author not found."
                )

            book_dict["author"] = author_obj
            book_obj = Book(**book_dict)

            await re.redis.set(isbn, pickle.dumps(book_obj))

            return book_obj

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app_v1.get("/author/{id}/book", tags=["Author"])
async def get_author_books(id: int, order: str = "asc"):
    author = await db_get_author_from_id(id)
    if author is not None:
        books = author["books"]
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)

        return {"books": books}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No author with such id",
        )

    # return {"query ": order + category + str(id)}


@app_v1.patch("/author/{id}/name", tags=["Author"])
async def patch_author_name(id: int, name: str = Body(..., embed=True)):
    await db_patch_author_name(id, name)
    return {"result": "Name has been updated"}


# not implemented
@app_v1.post("/user/author", tags=["Author"])
async def post_user_and_author(
    user: User, author: Author, bookstore_name: str = Body(..., embed=True)
):
    return {["User"]: user, "author": author, "bookstore_name": bookstore_name}


# FILE UPLOAD
@app_v1.post("/user/photo", tags=["User"])
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    # response.headers["x-file-size"] = str(len(profile_photo))
    # response.set_cookie(key="cookie-api", value="test")
    url = await upload_image_to_img_server(profile_photo)

    return {"file size": len(profile_photo), "url": url}

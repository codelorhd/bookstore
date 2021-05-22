# from tests.tests import get_hashed_password
from fastapi.param_functions import Query
from sqlalchemy.sql.expression import false
from models.user import User
from run import JWTUser
from utils.db import execute, fetch


async def db_check_jwt_username(username):
    query = """ SELECT * FROM users WHERE username = :username """
    values = {"username": username}

    result = await fetch(query, True, values)

    if result is None:
        return False
    else:
        return True


async def db_insert_user(user: User):
    query = """ INSERT INTO users (username, password, mail, role) 
                VALUES (:name, :password, :mail, :role ) """
    values = dict(user)
    print(values)
    await execute(query=query, is_many=False, values=values)

async def db_insert_personnel(user: User):
    query = """ INSERT INTO personnel (username, password, mail, role) 
                VALUES (:name, :password, :mail, :role ) """
    values = dict(user)
    print(values)
    await execute(query=query, is_many=False, values=values)


async def db_check_token_user(user: JWTUser):
    query = """ SELECT * FROM users WHERE username = :username """
    values = {"username": user.username}

    result = await fetch(query, False, values)

    return result


async def db_check_personel(username: str, password: str):
    query = """ SELECT * FROM personel WHERE username = :username AND password = :password """
    values = {"username": username, "password": password}

    result = await fetch(query, True, values)
    return result is not None


async def db_get_book_with_isbn(isbn: str):
    query = """ SELECT * FROM books WHERE isbn = :isbn """
    values = {"isbn": isbn}
    book = await fetch(query=query, is_one=True, values=values)
    return book


async def db_get_author(author_name):
    query = """ SELECT * FROM authors WHERE name = :name"""
    values = {"name": author_name}
    author = await fetch(query=query, is_one=True, values=values)
    return author


async def db_get_author_from_id(id):
    query = """ SELECT * FROM authors WHERE id = :id"""
    values = {"id": id}
    author = await fetch(query=query, is_one=True, values=values)
    return author


async def db_patch_author_name(id, name):
    query = """ UPDATE authors SET name = :name WHERE id = :id """
    values = {"name": name, "id": id}
    await execute(query, False, values)
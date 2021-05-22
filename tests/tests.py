import asyncio
import os

# local imports
import sys

from starlette.testclient import TestClient

# if __name__ == "__main__":
# if you will be running this directly append this
sys.path.append(r"/home/adeleke/Documents/Station/LEARN/FastAPI/bookstore/")
sys.path.append(
    r"/home/adeleke/Documents/Station/LEARN/FastAPI/bookstore/env/lib/python3.8/site-packages"
)

from passlib.context import CryptContext
from utils.db import execute, fetch

from run import app

client = TestClient(app)
loop = asyncio.get_event_loop()
pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password):
    return pwd_context.hash(password)


def insert_user(username, password, mail=None, role=None):
    query = """ INSERT INTO users (username, password) VALUES (:username, :password) """
    hashed_password = get_hashed_password(password)

    values = {"username": username, "password": hashed_password}

    # run async functions in a non-async function
    loop.run_until_complete(
        execute(
            query,
            is_many=False,
            values=values,
        )
    )


def check_user(username, mail):
    query = """ SELECT * FROM USERS WHERE username=:username AND mail=:mail"""
    values = {"username": username, "mail": mail}

    # run async functions in a non-async function
    result = loop.run_until_complete(
        fetch(
            query,
            True,
            values,
        )
    )

    if result is None:
        return False

    return True


def clear_db():
    query = """ delete from users; """
    loop.run_until_complete(execute(query, False))
    query = """ delete from authors; """
    loop.run_until_complete(execute(query, False))
    query = """  delete from books;  """
    loop.run_until_complete(execute(query, False))
    query = """  delete from personel; """
    loop.run_until_complete(execute(query, False))


def get_auth_header():
    insert_user("testuser", "test")
    response = client.post("/token", dict(username="testuser", password="test"))
    jwt_token = response.json()["access_token"]

    header = {"Authorization": f"Bearer {jwt_token}"}
    return header


def test_token_successful():
    # create a new user fir this test
    insert_user("user1", "pass1")
    # get token
    response = client.post("/token", dict(username="user1", password="pass1"))

    assert response.status_code == 200
    assert "access_token" in response.json()

    clear_db()


def test_token_unauthorized():
    # create a new user fir this test
    insert_user("user1", "pass1")
    # get token
    response = client.post("/token", dict(username="user2", password="pass1"))

    assert response.status_code == 401

    clear_db()


def test_post_user():
    auth_header = get_auth_header()

    user_dict = {
        "name": "user2",
        "password": "secret",
        "mail": "a@b.com",
        "role": "ADMIN",
    }

    response = client.post("/v1/user", json=user_dict, headers=auth_header)

    # print(response.json())
    assert response.status_code == 201
    assert check_user(username="user2", mail="a@b.com")
    clear_db()

from databases import Database

from utils.const import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, TESTING
from utils.db_object import db


async def execute(query, is_many, values=None) -> None:

    if TESTING:
        await db.connect()  # connect to the test database

    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)

    if TESTING:
        await db.disconnect()


async def fetch(query, is_one, values=None) -> None:
    if TESTING:
        await db.connect()

    if is_one:
        result = await db.fetch_one(query=query, values=values)
        if result is None:
            out = None
        else:
            out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        if result is None:
            out = None
        else:
            out = []
            for row in result:
                out.append(dict(row))

    if TESTING:
        await db.disconnect()

    return out


# query = "INSERT INTO books values (:isbn, :name, :author, :year)"
# values = [
#     {"isbn": "isbn2", "name": "book2", "author": "author2", "year": 2018},
#     {"isbn": "isbn3", "name": "book3", "author": "author3", "year": 2017},
# ]

# query = "SELECT * FROM books"

# loop = asyncio.get_event_loop()
# loop.run_until_complete(fetch(query=query, is_one=False))

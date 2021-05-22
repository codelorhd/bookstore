from databases.core import Database


from utils.const import (
    DB_URL,
    DB_URL_PRODUCTION,
    IS_LOAD_TEST,
    IS_PRODUCTION,
    TESTING,
    TEST_DB_URL,
)
from databases import Database

if TESTING or IS_LOAD_TEST:
    db = Database(TEST_DB_URL)

elif IS_PRODUCTION:
    db = Database(DB_URL_PRODUCTION)
else:
    db = Database(DB_URL)
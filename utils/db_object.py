from databases.core import Database


from utils.const import DB_URL, IS_LOAD_TEST, TESTING, TEST_DB_URL
from databases import Database

if TESTING or IS_LOAD_TEST:
    db = Database(TEST_DB_URL)
else:
    db = Database(DB_URL)
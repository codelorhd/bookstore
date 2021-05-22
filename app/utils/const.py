import os

# openssl rand -hex 32
JWT_SECREY_KEY = "8b669d926fcba72c7cc324977aa659725aba29a711390e149fc7b1ee66fbeb37"

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 69 * 24 * 5  # 5 days

TOKEN_DESCRIPTION = (
    "It checks username and password if they are true, it returns a JWT token"
)
TOKEN_SUMMARY = "It returns JWT token"

ISBN_DESCRIPTION = "It is a unique identifier for a post"

DB_HOST = "104.236.56.177"  # should be localhost sha
DB_HOST_PRODUCTION = "10.108.0.2"  # private network IP of the database
DB_USER = "admin"
DB_PASSWORD = "ADMIN"
DB_NAME = "bookstore"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DB_URL_PRODUCTION = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_PRODUCTION}/{DB_NAME}"
)

UPLOAD_PHOTO_API_KEY = "80e299be072507da25cc01f72061c39d"
UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?key={UPLOAD_PHOTO_API_KEY}"

REDIS_URL = "redis://104.236.56.177"
REDIS_URL_PRODUCTION = "redis://10.108.0.2"

TESTING = False
IS_LOAD_TEST = False
IS_PRODUCTION = True if os.environ["PRODUCTION"] == "true" else False

TEST_DB_HOST = "localhost:5433"
TEST_DB_USER = "test"
TEST_DB_PASSWORD = "test"
TEST_DB_NAME = "test"
TEST_DB_URL = (
    f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/{TEST_DB_NAME}"
)


TEST_REDIS_URL = "redis://localhost:6378/1"
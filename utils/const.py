# openssl rand -hex 32
JWT_SECREY_KEY = "8b669d926fcba72c7cc324977aa659725aba29a711390e149fc7b1ee66fbeb37"

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 69 * 24 * 5  # 5 days

TOKEN_DESCRIPTION = (
    "It checks username and password if they are true, it returns a JWT token"
)
TOKEN_SUMMARY = "It returns JWT token"

ISBN_DESCRIPTION = "It is a unique identifier for a post"

DB_HOST = "104.236.56.177"
DB_USER = "admin"
DB_PASSWORD = "ADMIN"
DB_NAME = "bookstore"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

UPLOAD_PHOTO_API_KEY = "80e299be072507da25cc01f72061c39d"
UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?key={UPLOAD_PHOTO_API_KEY}"

REDIS_URL = "redis://104.236.56.177"

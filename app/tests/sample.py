# local imports
import sys

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password):
    return pwd_context.hash(password)


sys.path.append(r"/home/adeleke/Documents/Station/LEARN/FastAPI/bookstore/")
sys.path.append(
    r"/home/adeleke/Documents/Station/LEARN/FastAPI/bookstore/env/lib/python3.8/site-packages"
)
print(get_hashed_password("secret"))

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password):
    return pwd_context.hash(password)


print(get_hashed_password("secret"))

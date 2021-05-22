import enum

from pydantic import BaseModel
from pydantic.networks import EmailStr


class Role(str, enum.Enum):
    ADMIN: str = "ADMIN"
    PERSONEL: str = "PERSONEL"


class User(BaseModel):
    name: str
    password: str
    mail: EmailStr
    role: Role
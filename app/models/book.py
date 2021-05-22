from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.schema import schema

from models.author import Author
from utils.const import ISBN_DESCRIPTION


class Book(BaseModel):
    isbn: str = schema([], description=ISBN_DESCRIPTION)
    name: str
    author: Author
    year: int
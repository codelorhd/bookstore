from models.author import Author
from pydantic import BaseModel
from pydantic.networks import EmailStr


class Book(BaseModel):
    isbn: str
    name: str
    author: Author
    year: int
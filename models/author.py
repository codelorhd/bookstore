from typing import List
from pydantic import BaseModel
from pydantic.networks import EmailStr


class Author(BaseModel):
    name: str
    book: List[str]
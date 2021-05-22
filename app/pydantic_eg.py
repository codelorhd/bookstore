from pydantic import BaseModel
from typing import Dict, List, Set, Tuple


class Book(BaseModel):
    name: str
    price: float = 10.0
    year: int


book1 = {"name": "book1", "price": 11.0, "year": 2021}
book_object = Book(**book1)


def print_book(book: Book):
    print(book)


print_book(book_object)

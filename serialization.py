from dataclasses import dataclass
from typing import Any
from marshmallow import Schema, fields, EXCLUDE, # INCLUDE

class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    # description = fields.Str()
    
@dataclass
class Book:
    title: str
    author: str
    # description: str
    
incoming_book_data = {
    "title": "Clean Code",
    "author": "Bob Martin",
    "description": "A book about writing cleaner code.",
}
    
# book = Book("Clean Code", "Bob Martin", "A book about writing cleaner code.")

book_schema = BookSchema(unknown=EXCLUDE)
book:Any = book_schema.load(incoming_book_data)
book_obj = Book(**book)

print(book_obj)
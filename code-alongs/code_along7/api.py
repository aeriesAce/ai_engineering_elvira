from fastapi import FastAPI
from .data_processing import library_data, Book

app = FastAPI()

library = library_data("library.json")
books = library.books

# GET endpoint, fetch data
@app.get("/books")
async def read_books():
    return books

# path parameter, fetch exact title, case-insensitive
@app.get("/books/title/{title}")
async def read_book_by_title(title: str):
    return [book for book in books if book.title.casefold() == title.casefold()]

# POST endpoint, create new data
@app.post("/books/create_book")
async def create_book(book_request: Book):
    new_book = Book.model_validate(book_request)
    books.append(new_book)

    return new_book
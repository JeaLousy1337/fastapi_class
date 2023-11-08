from datetime import datetime
from fastapi import FastAPI, Request, status, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from storage import database as db
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory='templates')


app.mount('/static', StaticFiles(directory='static'), name='static')


class NewBook(BaseModel):
    title: str
    author: str
    description: str = None
    cover: str


class Book(NewBook):
    pk: int
    created_at: datetime


def _serialize_books(books: list[tuple]) -> list[Book]:
    books_serialized = [
        Book(
            pk=book[0],
            title=book[1],
            author=book[2],
            description=book[3],
            cover=book[4],
            created_at=book[5],
        )
        for book in books
    ]
    return books_serialized
# WEB


@app.get('/', tags=['web'], include_in_schema=False)
def main(request: Request):
    books = db.last_five_stories()
    books_serialized = _serialize_books(books)
    context = {
        'title': 'Welcome to the my Hystory website',
        'request': request,
        'unicode': '\U0001F30D',
        'books': books_serialized,
    }
    return templates.TemplateResponse('index.html', context=context)


@app.get('/all-books', tags=['web'])
@app.post('/search', tags=['web'])
def all_books(request: Request, search_text: str = Form(None)):
    if search_text:
        books = db.get_book_by_title_or_other_str(query_str=search_text)
    else:
        books = db.get_books(limit=15)
    books_serialized = _serialize_books(books)
    context = {
        'title': f'Search result for text {search_text}' if search_text else 'Our stories',
        'request': request,
        'books': books_serialized,
        'unicodes': '\U00002B07'
    }

    return templates.TemplateResponse('all_books.html', context=context)


@app.get('/add-book', tags=['web'])
def add_books(request: Request):
    context = {
        'title': 'Add your story',
        'request': request,
    }

    return templates.TemplateResponse('add_book.html', context=context)


@app.post('/add-book', tags=['web'])
def add_book_final(request: Request,
                   title: str = Form(),
                   author: str = Form(),
                   description: str = Form(None),
                   cover: str = Form(),
):
    db.add_book(
        title=title,
        author=author,
        description=description,
        cover=cover,
    )

    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)

# API


@app.post('/api/add_book', status_code=status.HTTP_201_CREATED, tags=['API'])
def add_book(book: NewBook):
    db.add_book(
        title=book.title,
        author=book.author,
        description=book.description,
        cover=book.cover,
    )
    return book


@app.post('/api/get_books', tags=['API'])
@app.get('/api/get_books', tags=['API'])
def get_books(limit: int = 10) -> list[Book]:
    books = db.get_books(limit=limit)
    return _serialize_books(books)


@app.get('/api/get_books_search', tags=['API'])
def get_books_search(query_str: str) -> list[Book]:
    books = db.get_book_by_title_or_other_str(query_str=query_str)
    return _serialize_books(books)

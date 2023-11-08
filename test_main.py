from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_book_api():
    params = {
        'title': 'test',
        'author': 'test222',
        'description': 'test',
        'price': 100.0,
        'cover': 'test',
    }
    response = client.post('/api/add_book', json=params)
    assert response.status_code == 201
    assert "title" in response.json()


def test_get_books():
    response = client.get('/api/get_books')
    assert response.status_code == 200
    assert response.json()[0]['author'] == 'test222'


def test_get_books_post_method():
    response = client.post('/api/get_books')
    assert response.status_code == 200


def test_get_books_by_title():
    params = {
        'query_str': 'jhgasd'
    }
    response = client.get('/api/get_books_search', params=params)
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_books_by_title_success():
    params = {
        'query_str': 'test222'
    }
    response = client.get('/api/get_books_search', params=params)
    assert response.status_code == 200
    assert response.json()

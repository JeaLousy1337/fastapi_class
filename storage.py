import sqlite3
from abc import ABC, abstractmethod


class StorageBase(ABC):
    @abstractmethod
    def get_books(self, limit: int = 10):
        pass

    @abstractmethod
    def get_book_by_title_or_other_str(self, query_str: str):
        pass

    @abstractmethod
    def add_book(self, *, title: str, author: str, description: str, cover: str):
        pass


class StorageSQLite3(StorageBase):
    def __init__(self, database_name: str):
        self.database_name = database_name
        with sqlite3.connect(database_name) as connection:
            cursor = connection.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                description TEXT,
                cover TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(query)
            connection.commit()

    def get_books(self, limit: int = 10):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = """
                SELECT * 
                FROM books
                ORDER BY id DESC
                LIMIT :Limit_last
            """
            result = cursor.execute(query, {'Limit_last': limit})
            return result

    def get_book_by_title_or_other_str(self, query_str: str):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT * 
                FROM books
                WHERE 
                    title LIKE '%{query_str}%'
                OR 
                    author LIKE '%{query_str}%'
                OR
                    description LIKE '%{query_str}%'
                
                ORDER BY id DESC
            """
            result = cursor.execute(query)
            return result.fetchall()

    def add_book(self, *, title: str, author: str, description: str, cover: str):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO books (title, author, description, cover)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (title, author, description, cover))
            connection.commit()

    def last_five_stories(self, limit: int = 5):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = """
                SELECT * 
                FROM books
                ORDER BY id DESC
                LIMIT :Limit_last
            """
            result = cursor.execute(query, {'Limit_last': limit})
            return result


database = StorageSQLite3('database12345.sqlite3')


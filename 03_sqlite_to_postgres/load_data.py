import os
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch

load_dotenv()

#  postgres
dsn = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
    'dbname': os.environ.get('DB_NAME')
}

#  sqlite
db_path = 'db.sqlite'


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()


# DATACLASSES
@dataclass()
class Filmwork:
    title: str
    description: str
    creation_date: str
    type: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    rating: float = field(default=0.0)
    created: datetime = datetime.now()
    modified: datetime = datetime.now()


@dataclass()
class Person:
    full_name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = datetime.now()
    modified: datetime = datetime.now()


@dataclass()
class Genre:
    name: str
    description: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = datetime.now()
    modified: datetime = datetime.now()


@dataclass()
class GenreFilmwork:
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = datetime.now()


@dataclass()
class PersonFilmwork:
    role: str
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = datetime.now()


class SQLiteLoader:

    def __init__(self, conn):
        self.conn = conn
        self.curs = self.conn.cursor()

    def load_film_work(self):
        table = 'film_work'
        query = f"SELECT title, description, creation_date, type, id, rating FROM {table};"
        self.curs.execute(query)
        return {table: [Filmwork(*row) for row in self.curs.fetchall()]}

    def load_person(self):
        table = 'person'
        query = f"SELECT full_name, id FROM {table};"
        self.curs.execute(query)
        return {table: [Person(*row) for row in self.curs.fetchall()]}

    def load_genre(self):
        table = 'genre'
        query = f"SELECT name, description, id FROM {table};"
        self.curs.execute(query)
        return {table: [Genre(*row) for row in self.curs.fetchall()]}

    def load_genre_film_work(self):
        table = 'genre_film_work'
        query = f"SELECT film_work_id, genre_id, id FROM {table};"
        self.curs.execute(query)
        return {table: [GenreFilmwork(*row) for row in self.curs.fetchall()]}

    def load_person_film_work(self):
        table = 'person_film_work'
        query = f"SELECT role, film_work_id, person_id, id FROM {table};"
        self.curs.execute(query)
        return {table: [PersonFilmwork(*row) for row in self.curs.fetchall()]}

    def load_movies(self):
        data = {}
        data.update(self.load_film_work())
        data.update(self.load_person())
        data.update(self.load_genre())
        data.update(self.load_genre_film_work())
        data.update(self.load_person_film_work())
        return data


class PostgresSaver:

    PAGE_SIZE = 5000

    def __init__(self, conn):
        self.conn = conn
        self.curs = self.conn.cursor()

    def save_film_work(self, data: list[Filmwork]):
        #  convert list of dataclass objects to list with nested tuples (row)
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO film_work (title, description, creation_date, type, id, rating, created, modified)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_person(self, data: list[Person]):
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO person (full_name, id, created, modified)
                   VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_genre(self, data: list[Genre]):
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO genre (name, description, id, created, modified)
                   VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_genre_film_work(self, data: list[GenreFilmwork]):
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO genre_film_work (film_work_id, genre_id, id, created)
                   VALUES (%s, %s, %s, %s) ON CONFLICT (film_work_id, genre_id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_person_film_work(self, data: list[PersonFilmwork]):
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO person_film_work (role, film_work_id, person_id, id, created)
                   VALUES (%s, %s, %s, %s, %s) ON CONFLICT (film_work_id, person_id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_all_data(self, data: dict[str, list]):
        self.save_film_work(data.get('film_work'))
        self.save_person(data.get('person'))
        self.save_genre(data.get('genre'))
        self.save_genre_film_work(data.get('genre_film_work'))
        self.save_person_film_work(data.get('person_film_work'))


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with conn_context(db_path) as sqlite_conn, psycopg2.connect(**dsn) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

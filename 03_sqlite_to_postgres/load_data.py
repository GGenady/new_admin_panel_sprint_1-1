import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from db_tools import PostgresSaver, SQLiteLoader
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch
from config import dsn, db_path

load_dotenv()

@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    # Cначала загружаются данные из основных таблиц (film_work, person, genre), затем от зависивых
    for load_method in sqlite_loader.get_load_methods():

        # Загружаю данные пачками с каждой таблице по отдельности, до полного переноса
        while True:
            data = load_method()
            if not any(data.values()):
                break
            postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with conn_context(db_path) as sqlite_conn, psycopg2.connect(**dsn) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

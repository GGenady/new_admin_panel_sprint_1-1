import os
import sys

import psycopg2

sys.path.append(os.path.join(sys.path[0], '../../03_sqlite_to_postgres'))
from load_data import conn_context  # for sqlite
from load_data import dsn  # for postgres

#  sqlite
db_path = '../../03_sqlite_to_postgres/db.sqlite'

tables = [
    'film_work',
    'person',
    'genre',
    'person_film_work',
    'genre_film_work'
]


def sqlite_query(query):
    with conn_context(db_path) as conn:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()


def postgres_query(query):
    with psycopg2.connect(**dsn) as conn:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()


def test_count_rows():

    counts = {}

    for table in tables:
        query = "SELECT COUNT(*) FROM {table};".format(table=table)

        counts.update({table: {
            'postgres': postgres_query(query)[0][0],
            'sqlite': sqlite_query(query)[0][0]}
        })

    assert counts['film_work']['postgres'] == counts['film_work']['sqlite']
    assert counts['person']['postgres'] == counts['person']['sqlite']
    assert counts['genre']['postgres'] == counts['genre']['sqlite']
    assert counts['genre_film_work']['postgres'] == counts['genre_film_work']['sqlite']
    # diff 457
    assert counts['person_film_work']['postgres'] == counts['person_film_work']['sqlite']


def test_content_rows():

    content = {}

    for table in tables:

        if table == 'film_work':
            query = "SELECT title, description, creation_date, type, rating FROM film_work;"

        if table == 'person':
            query = "SELECT full_name FROM person;"

        if table == 'genre':
            query = "SELECT name, description FROM genre;"

        if table == 'genre_film_work':
            query = "SELECT film_work_id, genre_id FROM genre_film_work;"

        if table == 'person_film_work':
            query = "SELECT role, film_work_id, person_id FROM person_film_work;"

        content.update({table: {
            'postgres': postgres_query(query),
            'sqlite': sqlite_query(query)}
        })

    assert len(set(content['film_work']['sqlite']) - set(content['film_work']['postgres'])) == 0
    assert len(set(content['genre']['sqlite']) - set(content['genre']['postgres'])) == 0
    assert len(set(content['person']['sqlite']) - set(content['person']['postgres'])) == 0
    assert len(set(content['genre_film_work']['sqlite']) -
               set(content['genre_film_work']['postgres'])) == 0
    assert len(set(content['person_film_work']['sqlite']) -
               set(content['person_film_work']['postgres'])) == 0


if __name__ == "__main__":
    test_count_rows()
    test_content_rows()

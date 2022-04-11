from dc_models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork
from psycopg2.extras import execute_batch


class SQLiteLoader:

    SIZE = 500  # for fetchmany(size)

    FILM_WORK_LOADING = False
    PERSON_LOADING = False
    GENRE_LOADING = False
    GENRE_FILM_WORK_LOADING = False
    PERSON_FILM_WORK_LOADING = False

    def __init__(self, conn):
        self.conn = conn
        self.curs = self.conn.cursor()

    def load_film_work(self):
        table = 'film_work'
        query = f"SELECT title, description, creation_date, type, id, rating FROM {table};"

        # чтобы курсор переходил к другой пачке при повторном вызове метода
        if not SQLiteLoader.FILM_WORK_LOADING:
            self.curs.execute(query)
            SQLiteLoader.FILM_WORK_LOADING = True

        return {table: [Filmwork(*row) for row in self.curs.fetchmany(SQLiteLoader.SIZE)]}

    def load_person(self):
        table = 'person'
        query = f"SELECT full_name, id FROM {table};"

        if not SQLiteLoader.PERSON_LOADING:
            self.curs.execute(query)
            SQLiteLoader.PERSON_LOADING = True

        return {table: [Person(*row) for row in self.curs.fetchmany(SQLiteLoader.SIZE)]}

    def load_genre(self):
        table = 'genre'
        query = f"SELECT name, description, id FROM {table};"

        if not SQLiteLoader.GENRE_LOADING:
            self.curs.execute(query)
            SQLiteLoader.GENRE_LOADING = True

        return {table: [Genre(*row) for row in self.curs.fetchmany(SQLiteLoader.SIZE)]}

    def load_genre_film_work(self):
        table = 'genre_film_work'
        query = f"SELECT film_work_id, genre_id, id FROM {table};"

        if not SQLiteLoader.GENRE_FILM_WORK_LOADING:
            self.curs.execute(query)
            SQLiteLoader.GENRE_FILM_WORK_LOADING = True

        return {table: [GenreFilmwork(*row) for row in self.curs.fetchmany(SQLiteLoader.SIZE)]}

    def load_person_film_work(self):
        table = 'person_film_work'
        query = f"SELECT role, film_work_id, person_id, id FROM {table};"

        if not SQLiteLoader.PERSON_FILM_WORK_LOADING:
            self.curs.execute(query)
            SQLiteLoader.PERSON_FILM_WORK_LOADING = True

        return {table: [PersonFilmwork(*row) for row in self.curs.fetchmany(SQLiteLoader.SIZE)]}

    def get_load_methods(self):
        return [
            self.load_film_work,
            self.load_person,
            self.load_genre,
            self.load_genre_film_work,
            self.load_person_film_work
        ]


class PostgresSaver:

    PAGE_SIZE = 5000

    def __init__(self, conn):
        self.conn = conn
        self.curs = self.conn.cursor()

    def save_film_work(self, data: list[Filmwork]):
        #  convert list of dataclass objects to list with nested tuples (row)
        if not data:
            return
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO film_work (title, description, creation_date, type, id, rating, created, modified)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_person(self, data: list[Person]):
        if not data:
            return
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO person (full_name, id, created, modified)
                   VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_genre(self, data: list[Genre]):
        if not data:
            return
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO genre (name, description, id, created, modified)
                   VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_genre_film_work(self, data: list[GenreFilmwork]):
        if not data:
            return
        data = [tuple(dc_obj.__dict__.values()) for dc_obj in data]
        query = """INSERT INTO genre_film_work (film_work_id, genre_id, id, created)
                   VALUES (%s, %s, %s, %s) ON CONFLICT (film_work_id, genre_id) DO NOTHING;"""
        execute_batch(self.curs, query, data, page_size=PostgresSaver.PAGE_SIZE)
        self.conn.commit()

    def save_person_film_work(self, data: list[PersonFilmwork]):
        if not data:
            return
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

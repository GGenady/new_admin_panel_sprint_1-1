
-- DATABASE movies_database

BEGIN;

CREATE SCHEMA IF NOT EXISTS content;


CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone,
    CONSTRAINT fk_film_work_id FOREIGN KEY(film_work_id) REFERENCES content.film_work(id) ON DELETE CASCADE,
    CONSTRAINT fk_person_id FOREIGN KEY(person_id) REFERENCES content.person(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created timestamp with time zone,
    CONSTRAINT fk_film_work_id FOREIGN KEY(film_work_id) REFERENCES content.film_work(id) ON DELETE CASCADE,
    CONSTRAINT fk_genre_id FOREIGN KEY(genre_id) REFERENCES content.genre(id) ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS film_work_title_idx ON content.film_work(title);

CREATE INDEX IF NOT EXISTS person_full_name_idx ON content.person(full_name);

CREATE INDEX IF NOT EXISTS creation_date_rating_type_idx ON content.film_work (creation_date, rating, type);

CREATE INDEX IF NOT EXISTS rating_type_idx ON content.film_work (rating, type);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);

-- ALTER ROLE app SET search_path TO content,public;

COMMIT;
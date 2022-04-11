import uuid
from dataclasses import dataclass, field
from datetime import datetime


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

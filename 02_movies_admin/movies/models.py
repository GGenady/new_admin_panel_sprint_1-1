import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.TextField('name', max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Person(UUIDMixin, TimeStampedMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.TextField('name', max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Type(models.TextChoices):
        MOVIE = 'movie', 'Movie'
        TV_SHOW = 'tv_show', 'TV show'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField('title', max_length=255)
    description = models.TextField('description', blank=True, null=True)
    creation_date = models.DateField('creation date', blank=True, null=True)
    rating = models.FloatField('rating', blank=True, null=True, validators=[MinValueValidator(0),
                                                                            MaxValueValidator(100)])
    type = models.TextField('Type', choices=Type.choices, max_length=255)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', db_column='film_work_id', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', db_column='genre_id', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        unique_together = (('film_work', 'genre'),)


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', db_column='film_work_id', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', db_column='person_id', on_delete=models.CASCADE)
    role = models.TextField('role', max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = (('film_work', 'person'),)

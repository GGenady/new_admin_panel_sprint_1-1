import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(_('created'), auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(_('modified'), auto_now=True)

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
    name = models.TextField(_('name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.TextField(_('full_name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV show')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)

    rating = models.FloatField(_('rating'),
                               blank=True,
                               null=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])

    type = models.TextField(_('type'), choices=Type.choices, max_length=255)
    genres = models.ManyToManyField(Genre, verbose_name=_('genres'), through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film_work')
        verbose_name_plural = _('film_works')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork',
                                  verbose_name=_('film_work'),
                                  db_column='film_work_id',
                                  on_delete=models.CASCADE)

    genre = models.ForeignKey('Genre',
                              verbose_name=_('genre'),
                              db_column='genre_id',
                              on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        unique_together = (('film_work', 'genre'),)
        verbose_name = _('genre_film_work')
        verbose_name_plural = _('genre_film_works')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork',
                                  verbose_name=_('film_work'),
                                  db_column='film_work_id',
                                  on_delete=models.CASCADE)

    person = models.ForeignKey('Person',
                               verbose_name=_('person'),
                               db_column='person_id',
                               on_delete=models.CASCADE)

    role = models.TextField(_('role'), max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = (('film_work', 'person'),)
        verbose_name = _('person_film_work')
        verbose_name_plural = _('person_film_works')

from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ['person']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description', 'id',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    ordering = ['full_name']
    search_fields = ['full_name']

    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name', 'id',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')

    # Фильтрация в списке
    list_filter = ('type', 'genres', 'creation_date', 'rating')

    # Поиск по полям
    search_fields = ('title', 'description', 'id',)

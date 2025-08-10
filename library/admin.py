from django.contrib import admin

from library.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Класс для отображения модели в админке"""
    list_display = ('id', 'first_name', 'last_name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Класс для отображения модели в админке"""
    list_display = ('id', 'title', 'author')

from rest_framework import serializers

from library.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора"""
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книги"""
    class Meta:
        model = Book
        fields = "__all__"
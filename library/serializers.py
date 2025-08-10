from rest_framework import serializers

from library.models import Author, Book
from library.validators import validate_profanity


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора"""

    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книги"""
    title = serializers.CharField(validators=[validate_profanity])
    description = serializers.CharField(validators=[validate_profanity])

    class Meta:
        model = Book
        fields = "__all__"

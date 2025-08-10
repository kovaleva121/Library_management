from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView)
from library.models import Author, Book
from library.pagination import MyPagination
from library.permissions import IsOwner, IsModer
from library.serializers import AuthorSerializer, BookSerializer


class AuthorCreateAPIView(CreateAPIView):
    """Контроллер создания автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def perform_create(self, serializer):
        """Привязка пользователя при создании"""
        serializer.save(owner=self.request.user)


class AuthorListAPIView(ListAPIView):
    """Контроллер просмотра списка авторов"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = MyPagination


class AuthorUpdateAPIView(UpdateAPIView):
    """Контроллер обновления автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsOwner]


class AuthorRetrieveAPIView(RetrieveAPIView):
    """Контроллер редактирования автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsOwner]


class AuthorDestroyAPIView(DestroyAPIView):
    """Контроллер удаления автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsOwner, IsModer]


class BookCreateAPIView(CreateAPIView):
    """Контроллер создания книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        """Привязка пользователя при создании"""
        serializer.save(owner=self.request.user)


class BookListAPIView(ListAPIView):
    """Контроллер просмотра списка книг"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'genres', 'published_date', 'pages', 'status']


class BookUpdateAPIView(UpdateAPIView):
    """Контроллер обновления книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwner]


class BookRetrieveAPIView(RetrieveAPIView):
    """Контроллер редактирования книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwner]


class BookDestroyAPIView(DestroyAPIView):
    """Контроллер удаления книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwner, IsModer]

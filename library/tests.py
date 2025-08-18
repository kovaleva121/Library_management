from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Book, Author, Loan, Genre
from users.models import User


class LibraryCRUDTestCase(APITestCase):
    """Тесты по CRUD операциям авторов, книг и выдачи книг"""

    def setUp(self):
        # Создаем группу модераторов
        from django.contrib.auth.models import Group
        moder_group, _ = Group.objects.get_or_create(name="moders")
        self.moderator = User.objects.create(email="moder@test.com", password="moderpass", is_staff=True)
        self.moderator.groups.add(moder_group)  # Добавляем в группу модераторов

        # создаем пользователя, жанр, книгу, автора и выдачу книги
        self.user = User.objects.create(email='test@example.com', password='123qwe')
        self.other_user = User.objects.create(email='test2@example.com', password='123qwer')
        self.author = Author.objects.create(first_name='test', last_name='test', patronymic='test', owner=self.user)
        self.genre = Genre.objects.create(name='new genre')
        self.book = Book.objects.create(title='test2', author=self.author,
                                        published_date='2025-08-14', owner=self.user,
                                        status='AVAILABLE')
        self.book.genres.add(self.genre)
        self.loan = Loan.objects.create(book=self.book, borrower=self.user)

        # URL для тестирования автора
        self.author_create_url = reverse("library:author_create")
        self.author_update_url = reverse("library:author_update", kwargs={"pk": self.author.pk})
        self.author_retrieve_url = reverse("library:author_retrieve", kwargs={"pk": self.author.pk})
        self.author_list_url = reverse("library:author_list")
        self.author_destroy_url = reverse("library:author_delete", kwargs={"pk": self.author.pk})

        # URL для тестирования книги
        self.book_create_url = reverse("library:book_create")
        self.book_update_url = reverse("library:book_update", kwargs={"pk": self.book.pk})
        self.book_retrieve_url = reverse("library:book_retrieve", kwargs={"pk": self.book.pk})
        self.book_list_url = reverse("library:book_list")
        self.book_destroy_url = reverse("library:book_delete", kwargs={"pk": self.book.pk})

        # URL для тестирования выдачи книги
        self.loan_create_url = reverse("library:loan_create")
        self.loan_update_url = reverse("library:loan_update", kwargs={"pk": self.loan.pk})

        # URL для тестирования жанра
        self.genre_create_url = reverse("library:genre_create")
        self.genre_update_url = reverse("library:genre_update", kwargs={"pk": self.genre.pk})
        self.genre_retrieve_url = reverse("library:genre_retrieve", kwargs={"pk": self.genre.pk})
        self.genre_list_url = reverse("library:genre_list")
        self.genre_destroy_url = reverse("library:genre_delete", kwargs={"pk": self.genre.pk})

    def test_create_author_user(self):
        """Тест создания автора"""
        self.client.force_authenticate(user=self.user)
        data = {"first_name": "new_test", "last_name": "new_test", "patronymic": "new_test", "owner": self.user.pk}
        response = self.client.post(self.author_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["owner"], self.user.pk)

    def test_update_author_user(self):
        """Тест обновления автора для создателя"""
        self.client.force_authenticate(user=self.user)
        data = {"first_name": "new_name"}
        response = self.client.patch(self.author_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_author_other_user(self):
        """Тест ограничения прав доступа обновления автора для не создателя"""
        self.client.force_authenticate(user=self.other_user)
        data = {"first_name": "new_name"}
        response = self.client.patch(self.author_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_author_user(self):
        """Тест получения информации об авторе для создателя"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.author_retrieve_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.author.first_name)

    def test_retrieve_author_other_user(self):
        """Тест ограничения доступа получения информации об авторе для не создателя """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.author_retrieve_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_list_user(self):
        """Тест получения списка авторов"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.author_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_list_unauthenticated(self):
        """Тест ограничения получения списка авторов для не авторизованных пользователей"""
        response = self.client.get(self.author_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_author_user(self):
        """Тест удаления автора создателем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.author_destroy_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_destroy_author_moderator(self):
        """Тест удаления автора модератором"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.author_destroy_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_book_create_user(self):
        """Тест создания книги пользователем"""
        self.client.force_authenticate(user=self.user)
        data = {"title": "Clean Book Title", "author": self.author.pk, "published_date": "2025-08-14",
                "owner": self.user.pk,
                "status": "AVAILABLE", "description": "Test description", "genres": [self.genre.pk]}
        response = self.client.post(self.book_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], self.author.pk)
        self.assertEqual(response.data["owner"], self.user.pk)

    def test_book_update_user(self):
        """Тест обновления книги создателем"""
        self.client.force_authenticate(user=self.user)
        data = {"title": "Update Title"}
        response = self.client.patch(self.book_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_update_other_user(self):
        """Тест обновления книги не создателем"""
        self.client.force_authenticate(user=self.other_user)
        data = {"title": "Update Title"}
        response = self.client.patch(self.book_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_retrieve_user(self):
        """Тест получения информации о книге создателем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.book_retrieve_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_book_retrieve_other_user(self):
        """Тест получения информации о книге не создателем"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.book_retrieve_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_list_user(self):
        """Тест списка книг пользователем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.book_list_url, fornat="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_list_unauthenticated(self):
        """Тест списка книг не авторизованным пользователем"""
        response = self.client.get(self.book_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_destroy_user(self):
        """Тест удаления книги пользователем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_destroy_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_book_destroy_moderator(self):
        """Тест удаления книги модератором"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.book_destroy_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_loan_create_user(self):
        """Тест создания выдачи книги"""
        self.client.force_authenticate(user=self.user)
        data = {"book": self.book.pk, "borrower": self.user.pk}
        response = self.client.post(self.loan_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book"], self.book.pk)
        self.assertEqual(response.data["borrower"], self.user.pk)

    def test_loan_update_user(self):
        """Тест обновления выдачи книги"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.loan_update_url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_create(self):
        """Тест создания жанра пользователем"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "test genre"}
        response = self.client.post(self.genre_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_genre_update(self):
        """Тест обновления жанра"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Update genre"}
        response = self.client.patch(self.genre_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_retrieve(self):
        """Тест получения информации о жанре"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.genre_retrieve_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.genre.name)

    def test_genre_list(self):
        """Тест списка жанров"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.genre_list_url, fornat="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_list_unauthenticated(self):
        """Тест списка жанров неавторизованным пользователем"""
        response = self.client.get(self.genre_list_url, fornat="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_genre_destroy(self):
        """Тест удаления жанра"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.genre_destroy_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)

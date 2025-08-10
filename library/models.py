from django.db import models

from users.models import User


class Author(models.Model):
    """Класс - автор"""
    POPULARITY_CHOICES = {
        1: "Неизвестная",
        2: "Малоизвестная",
        3: "Популярная"
    }
    first_name = models.CharField(max_length=100, verbose_name='Имя', help_text='Напишите имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия', help_text='Напишите фамилию')
    patronymic = models.CharField(max_length=250, verbose_name='Отчество', help_text='Напишите отчество')
    bio = models.TextField(blank=True, null=True, verbose_name='Биография', help_text='Напишите биографию')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения',
                                     help_text='Укажите дату рождения')
    date_of_death = models.DateField(blank=True, null=True, verbose_name='Дата смерти', help_text='Укажите дату смерти')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    popularity = models.PositiveIntegerField(blank=True, null=True, choices=POPULARITY_CHOICES, default=1,
                                             verbose_name='Популярность',
                                             help_text='Укажите популярность')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",
                              help_text="Укажите пользователя")

    class Meta:
        """Метаданные"""
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        """Строковый вывод"""
        return f'{self.first_name} {self.last_name} {self.patronymic}'


class Book(models.Model):
    """Класс - книга"""
    STATUS_CHOICES = [
        ('AVAILABLE', 'Доступна'),
        ('RESERVED', 'Зарезервирована'),
        ('LOANED', 'Выдана'),
    ]
    title = models.CharField(max_length=200, verbose_name='Название', help_text='Напишите название книги')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор', help_text='Укажите автора')
    description = models.TextField(blank=True, null=True, verbose_name='Описание', help_text='Напишите описание')
    genres = models.CharField(max_length=100, blank=True, null=True, verbose_name='Жанр', help_text='Напишите жанр')
    published_date = models.DateField(verbose_name='Дата публикации', help_text='Укажите дату публикации')
    pages = models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество страниц',
                                        help_text='Укажите кол-во страниц')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",
                              help_text="Укажите пользователя")

    class Meta:
        """Метаданные"""
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        """Строковый вывод"""
        return f'Название:{self.title}, автор: {self.author}'

# class BookLoan(models.Model):
#     """Класс - выдача книг"""
#     LOAN_STATUS_CHOICES = [
#         ('ACTIVE', 'Активна'),
#         ('RETURNED', 'Возвращена'),
#         ('OVERDUE', 'Просрочена'),
#     ]
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга', help_text='Выберите книгу')
#     borrower = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Читатель', help_text='Выберите читателя')
#     loan_date = models.DateField(auto_now_add=True, verbose_name='Дата выдачи')
#     due_date = models.DateField(verbose_name='Дата возврата', help_text='Укажите дату возврата книги')
#     return_date = models.DateField(null=True, blank=True, verbose_name='Фактическая дата возврата')
#     status = models.CharField(max_length=10, choices=LOAN_STATUS_CHOICES, default='ACTIVE',
#                               verbose_name='Статус выдачи')
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_loans',
#                                    verbose_name='Кем выдана')
#
#     class Meta:
#         """Метаданные"""
#         verbose_name = 'Выдача книги'
#         verbose_name_plural = 'Выдачи книг'
#
#     def __str__(self):
#         """Строковый вывод"""
#         return f'Читатель:{self.borrower}, книга:{self.book} - статус выдачи:{self.status}'

from django.conf import settings
from django.db import models


class Author(models.Model):
    """Модель автора книги.

    Attributes:
        name (str): Имя автора, максимальная длина 100 символов
        birth_date (Date): Дата рождения автора, может быть пустой
    """

    name = models.CharField("Имя автора", max_length=100)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра книги.

    Attributes:
        name (str): Название жанра, уникальное, максимальная длина 50 символов
    """

    name = models.CharField("Жанр", max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def books_count(self):
        """Возвращает количество книг в данном жанре.

        Returns:
            int: Количество книг, принадлежащих этому жанру
        """
        return self.books.count()


class Book(models.Model):
    """Модель книги в библиотеке.

    Attributes:
        title (str): Название книги, максимальная длина 200 символов
        author (ForeignKey): Ссылка на автора книги
        genres (ManyToMany): Жанры, к которым принадлежит книга
        published_date (Date): Дата публикации книги
        isbn (str): ISBN книги, уникальный, 13 символов
    """

    title = models.CharField("Название", max_length=200)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор"
    )
    genres = models.ManyToManyField(Genre, related_name="books", verbose_name="Жанры")
    published_date = models.DateField("Дата публикации")
    isbn = models.CharField("ISBN", max_length=13, unique=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.author.name})"


class IssueBook(models.Model):
    """Модель выдачи книги пользователю.

    Attributes:
        user (ForeignKey): Пользователь, которому выдана книга
        book (ForeignKey): Выданная книга
        issued_at (Date): Дата выдачи (автоматически устанавливается при создании)
        return_due (Date): Срок возврата книги
        returned_at (Date): Дата фактического возврата книги (может быть пустой)
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issued_books"
    )
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    issued_at = models.DateField(auto_now_add=True)
    return_due = models.DateField()
    returned_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} → {self.book.title}"

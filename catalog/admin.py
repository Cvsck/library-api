from django.contrib import admin

from .models import Author, Book, Genre, IssueBook


class GenreAdmin(admin.ModelAdmin):
    """Админка для модели Genre.

    Настройки отображения:
    - list_display: Показывает название жанра и количество книг
    - search_fields: Поиск по названию жанра
    """

    list_display = ["name", "books_count"]
    search_fields = ["name"]

    def books_count(self, obj):
        """Возвращает количество книг в жанре.

        Args:
            obj: Объект жанра

        Returns:
            int: Количество книг в данном жанре
        """
        return obj.books.count()

    books_count.short_description = "Количество книг"


class BookAdmin(admin.ModelAdmin):
    """Админка для модели Book.

    Настройки отображения:
    - list_display: Показывает название, автора, жанры, дату публикации и ISBN
    - list_filter: Фильтрация по жанрам, авторам и дате публикации
    - search_fields: Поиск по названию книги и имени автора
    - filter_horizontal: Удобный виджет выбора жанров
    """

    list_display = ["title", "author", "display_genres", "published_date", "isbn"]
    list_filter = ["genres", "author", "published_date"]
    search_fields = ["title", "author__name"]
    filter_horizontal = ["genres"]  # Удобный выбор жанров

    def display_genres(self, obj):
        """Отображает жанры книги через запятую.

        Args:
            obj: Объект книги

        Returns:
            str: Строка с названиями жанров, разделенными запятыми
        """
        return ", ".join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = "Жанры"


class IssueBookAdmin(admin.ModelAdmin):
    """Админка для модели IssueBook.

    Настройки отображения:
    - list_display: Показывает книгу, пользователя, даты и статус
    - list_filter: Фильтрация по датам выдачи, возврата и фактического возврата
    - search_fields: Поиск по названию книги и email пользователя
    """

    list_display = ["book", "user", "issued_at", "return_due", "returned_at", "status"]
    list_filter = ["issued_at", "return_due", "returned_at"]
    search_fields = ["book__title", "user__email"]

    def status(self, obj):
        """Определяет и отображает статус возврата книги.

        Варианты статусов:
        - Возвращена с опозданием/вовремя/досрочно
        - Просрочена на X дней
        - Вернуть сегодня/завтра
        - Осталось X дней

        Args:
            obj: Объект выдачи книги

        Returns:
            str: Текстовый статус с эмодзи
        """
        from datetime import date

        if obj.returned_at:
            # Книга возвращена - проверяем вовремя ли
            days_late = (obj.returned_at - obj.return_due).days
            if days_late > 0:
                return f"⚠️ Возвращена с опозданием на {days_late} д."
            elif days_late == 0:
                return "✅ Возвращена вовремя"
            else:
                return "✅ Возвращена досрочно"
        else:
            # Книга еще не возвращена
            days_remaining = (obj.return_due - date.today()).days
            if days_remaining < 0:
                return f"❌ Просрочена на {-days_remaining} д."
            elif days_remaining == 0:
                return "⏳ Вернуть сегодня"
            elif days_remaining == 1:
                return "⏳ Вернуть завтра"
            else:
                return f"⏳ Осталось {days_remaining} д."

    status.short_description = "Статус"


class AuthorAdmin(admin.ModelAdmin):
    """Админка для модели Author.

    Настройки отображения:
    - list_display: Показывает имя, дату рождения и количество книг
    - search_fields: Поиск по имени автора
    """

    list_display = ["name", "birth_date", "books_count"]
    search_fields = ["name"]

    def books_count(self, obj):
        """Возвращает количество книг автора.

        Args:
            obj: Объект автора

        Returns:
            int: Количество книг данного автора
        """
        return obj.books.count()

    books_count.short_description = "Количество книг"


# Регистрация моделей с кастомными админками
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(IssueBook, IssueBookAdmin)

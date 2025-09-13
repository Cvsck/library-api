from django.contrib import admin

from .models import Author, Book, Genre, IssueBook


# Кастомная админка для жанров
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "books_count"]
    search_fields = ["name"]

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = "Количество книг"


# Кастомная админка для книг
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "display_genres", "published_date", "isbn"]
    list_filter = ["genres", "author", "published_date"]
    search_fields = ["title", "author__name"]
    filter_horizontal = ["genres"]  # Удобный выбор жанров

    def display_genres(self, obj):
        """Отображает жанры через запятую"""
        return ", ".join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = "Жанры"


# Кастомная админка для выдачи книг
class IssueBookAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "issued_at", "return_due", "returned_at", "status"]
    list_filter = ["issued_at", "return_due", "returned_at"]
    search_fields = ["book__title", "user__email"]

    def status(self, obj):
        """Показывает статус возврата книги"""
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


# Кастомная админка для авторов
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date", "books_count"]
    search_fields = ["name"]

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = "Количество книг"


# Регистрация моделей с кастомными админками
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(IssueBook, IssueBookAdmin)

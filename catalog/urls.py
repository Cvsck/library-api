from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.views import (AuthorViewSet, BookViewSet, GenreViewSet,
                           IssueBookViewSet, MyIssuedBooksViewSet,
                           RegisterView, book_statistics, issues_by_date_range)

# Маршрутизатор DRF для автоматической генерации URL для ViewSets
router = DefaultRouter()

# Регистрация ViewSets с соответствующими префиксами URL
router.register(r"authors", AuthorViewSet)  # /api/catalog/authors/
router.register(r"genres", GenreViewSet)  # /api/catalog/genres/
router.register(r"books", BookViewSet)  # /api/catalog/books/
router.register(r"issue-books", IssueBookViewSet)  # /api/catalog/issue-books/

# Регистрация кастомного ViewSet с указанием basename
router.register(
    r"my-issued-books",
    MyIssuedBooksViewSet,
    basename="my-issued-books",  # /api/catalog/my-issued-books/
)

# Основные URL patterns приложения catalog
urlpatterns = [
    # Включение всех URL, сгенерированных роутером
    path("", include(router.urls)),
    # Регистрация нового пользователя
    path("register/", RegisterView.as_view(), name="register"),
    # Статистика библиотеки (популярные книги, авторы, выдачи)
    path("statistics/", book_statistics, name="book-statistics"),
    # Фильтрация выдач книг по диапазону дат
    path("issues-by-date/", issues_by_date_range, name="issues-by-date"),
]

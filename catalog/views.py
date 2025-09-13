from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from catalog.models import Author, Book, Genre, IssueBook
from catalog.serializers import (AuthorSerializer, BookReadSerializer,
                                 BookWriteSerializer, GenreSerializer,
                                 IssueBookSerializer, MyIssueBookSerializer,
                                 RegisterSerializer)


# -------------------------------
# AuthorViewSet — управление авторами
# -------------------------------
@extend_schema_view(
    list=extend_schema(
        summary="Список авторов",
        description="Возвращает список всех авторов. Поддерживает поиск и сортировку по имени.",
        responses={200: AuthorSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Получить автора по ID",
        description="Возвращает одного автора по его идентификатору.",
        responses={200: AuthorSerializer},
    ),
    create=extend_schema(
        summary="Создать нового автора",
        description="Создаёт нового автора. Требуется имя и дата рождения.",
        request=AuthorSerializer,
        responses={201: AuthorSerializer},
    ),
    update=extend_schema(
        summary="Обновить автора",
        description="Полное обновление данных автора.",
        request=AuthorSerializer,
        responses={200: AuthorSerializer},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление автора",
        description="Обновление отдельных полей автора.",
        request=AuthorSerializer,
        responses={200: AuthorSerializer},
    ),
    destroy=extend_schema(
        summary="Удалить автора",
        description="Удаляет автора по ID.",
        responses={204: None},
    ),
)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    @method_decorator(cache_page(60 * 15))  # Кеш на 15 минут
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# -------------------------------
# GenreViewSet — управление жанрами
# -------------------------------
@extend_schema_view(
    list=extend_schema(
        summary="Список жанров",
        description="Возвращает список всех жанров. Поддерживает поиск и сортировку по названию.",
        responses={200: GenreSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Получить жанр по ID",
        description="Возвращает один жанр по его идентификатору.",
        responses={200: GenreSerializer},
    ),
    create=extend_schema(
        summary="Создать новый жанр",
        description="Создаёт новый жанр. Требуется название.",
        request=GenreSerializer,
        responses={201: GenreSerializer},
    ),
    update=extend_schema(
        summary="Обновить жанр",
        description="Полное обновление названия жанра.",
        request=GenreSerializer,
        responses={200: GenreSerializer},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление жанра",
        description="Обновление отдельных полей жанра.",
        request=GenreSerializer,
        responses={200: GenreSerializer},
    ),
    destroy=extend_schema(
        summary="Удалить жанр",
        description="Удаляет жанр по ID.",
        responses={204: None},
    ),
)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    @method_decorator(cache_page(60 * 15))  # Кеш на 15 минут
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# -------------------------------
# BookViewSet — управление книгами
# -------------------------------
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["author", "genres"]
    search_fields = ["title"]
    ordering_fields = ["title", "published_date"]
    ordering = ["title"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BookReadSerializer
        return BookWriteSerializer

    @method_decorator(cache_page(60 * 5))  # Кеш на 5 минут
    @extend_schema(
        summary="Список книг",
        description="Получить все книги с авторами и жанрами. Поддерживает фильтрацию и поиск.",
        responses={200: BookReadSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создать книгу",
        description="Создание новой книги с указанием автора, жанров, даты публикации и ISBN.",
        request=BookWriteSerializer,
        responses={201: BookReadSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получить книгу",
        description="Получить одну книгу по её ID.",
        responses={200: BookReadSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновить книгу",
        description="Полное обновление книги по ID.",
        request=BookWriteSerializer,
        responses={200: BookReadSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частично обновить книгу",
        description="Обновление отдельных полей книги.",
        request=BookWriteSerializer,
        responses={200: BookReadSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удалить книгу",
        description="Удаление книги по ID.",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Расширенный поиск книг",
        description="Полнотекстовый поиск по названию, автору и жанрам",
        tags=["Книги"],
    )
    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")

        books = Book.objects.filter(
            Q(title__icontains=query)
            | Q(author__name__icontains=query)
            | Q(genres__name__icontains=query)
        ).distinct()

        page = self.paginate_queryset(books)
        serializer = BookReadSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# -------------------------------
# RegisterView — регистрация пользователя
# -------------------------------
@extend_schema(
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя по email и паролю.",
    request=RegisterSerializer,
    responses={201: RegisterSerializer},
    tags=["Пользователь"],
)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# -------------------------------
# IssueBookViewSet — управление выдачами
# -------------------------------
@extend_schema_view(
    list=extend_schema(
        summary="Список всех выдач",
        description="Возвращает все записи о выдаче книг. Доступно авторизованным пользователям.",
        responses={200: IssueBookSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Получить выдачу по ID",
        description="Возвращает одну запись о выдаче книги по её идентификатору.",
        responses={200: IssueBookSerializer},
    ),
    create=extend_schema(
        summary="Создать выдачу книги",
        description="Создаёт новую запись о выдаче книги. Доступно только администраторам.",
        request=IssueBookSerializer,
        responses={201: IssueBookSerializer},
    ),
    update=extend_schema(
        summary="Обновить выдачу",
        description="Полное обновление записи о выдаче. Только для администраторов.",
        request=IssueBookSerializer,
        responses={200: IssueBookSerializer},
    ),
    partial_update=extend_schema(
        summary="Частично обновить выдачу",
        description="Обновление отдельных полей записи о выдаче. Только для администраторов.",
        request=IssueBookSerializer,
        responses={200: IssueBookSerializer},
    ),
    destroy=extend_schema(
        summary="Удалить выдачу",
        description="Удаляет запись о выдаче книги. Только для администраторов.",
        responses={204: None},
    ),
)
class IssueBookViewSet(viewsets.ModelViewSet):
    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    # Убираем автоматическую привязку к текущему пользователю
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# -------------------------------
# MyIssuedBooksViewSet — мои выдачи
# -------------------------------
@extend_schema_view(
    list=extend_schema(
        summary="Мои выданные книги",
        description="Список книг, выданных текущему пользователю.",
        responses={200: MyIssueBookSerializer(many=True)},
        tags=["Выдачи пользователя"],
    )
)
class MyIssuedBooksViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MyIssueBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return IssueBook.objects.none()
        return (
            IssueBook.objects.filter(user=self.request.user)
            .select_related("book", "book__author")
            .prefetch_related("book__genres")
        )


# -------------------------------
# Аналитика и статистика
# -------------------------------
@extend_schema(
    summary="Статистика популярности книг",
    description="Возвращает статистику по самым популярным книгам и авторам",
    tags=["Аналитика"],
)
@api_view(["GET"])
def book_statistics(request):
    # Самые популярные книги
    popular_books = Book.objects.annotate(issue_count=Count("issuebook")).order_by(
        "-issue_count"
    )[:10]

    # Самые популярные авторы
    popular_authors = Author.objects.annotate(
        book_count=Count("books"), total_issues=Count("books__issuebook")
    ).order_by("-total_issues")[:10]

    # Книги, которые сейчас выданы
    currently_issued = IssueBook.objects.filter(returned_at__isnull=True).count()

    # Просроченные книги
    overdue_books = IssueBook.objects.filter(
        returned_at__isnull=True, return_due__lt=timezone.now().date()
    ).count()

    return Response(
        {
            "popular_books": [
                {"title": book.title, "issue_count": book.issue_count}
                for book in popular_books
            ],
            "popular_authors": [
                {"name": author.name, "total_issues": author.total_issues}
                for author in popular_authors
            ],
            "currently_issued": currently_issued,
            "overdue_books": overdue_books,
        }
    )


@extend_schema(
    summary="Выдачи по диапазону дат",
    description="Фильтрация выдач по периоду",
    tags=["Аналитика"],
)
@api_view(["GET"])
def issues_by_date_range(request):
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    issues = IssueBook.objects.all()

    if start_date:
        issues = issues.filter(issued_at__gte=start_date)
    if end_date:
        issues = issues.filter(issued_at__lte=end_date)

    serializer = IssueBookSerializer(issues, many=True)
    return Response(serializer.data)

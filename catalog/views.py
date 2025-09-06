from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Author, Book, Genre, IssueBook
from catalog.serializers import (AuthorSerializer, BookReadSerializer,
                                 BookWriteSerializer, GenreSerializer,
                                 IssueBookSerializer, RegisterSerializer)


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
        summary="Удалить жанр", description="Удаляет жанр по ID.", responses={204: None}
    ),
)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


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


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class IssueBookViewSet(viewsets.ModelViewSet):
    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

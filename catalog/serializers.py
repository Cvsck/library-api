from datetime import date, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers

from catalog.models import Author, Book, Genre, IssueBook

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Author.

    Предоставляет данные об авторе: ID, имя и дату рождения.
    Используется для чтения и записи данных авторов.
    """

    class Meta:
        model = Author
        fields = ["id", "name", "birth_date"]


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre.

    Предоставляет данные о жанре: ID и название.
    Используется для управления жанрами книг.
    """

    class Meta:
        model = Genre
        fields = ["id", "name"]


class BookReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения данных книги.

    Включает полные данные об авторе и жанрах.
    Используется для операций чтения (list, retrieve).
    """

    author = AuthorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи данных книги.

    Используется для создания и обновления книг.
    Содержит валидацию данных книги.
    """

    class Meta:
        model = Book
        fields = "__all__"

    def validate_published_date(self, value):
        """Проверяет, что дата публикации не в будущем."""
        if value > date.today():
            raise serializers.ValidationError(
                "Дата публикации не может быть в будущем."
            )
        return value

    def validate(self, data):
        """Проверяет, что название книги не совпадает с именем автора."""
        if data["author"].name.lower() == data["title"].lower():
            raise serializers.ValidationError(
                "Название книги не должно совпадать с именем автора."
            )
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей.

    Обрабатывает email и пароль при создании пользователя.
    Проверяет уникальность email.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate_email(self, value):
        """Проверяет, что email не занят другим пользователем."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return value

    def create(self, validated_data):
        """Создает нового пользователя с хешированием пароля."""
        return User.objects.create_user(**validated_data)


class IssueBookSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи книг.

    Используется администраторами для создания и управления выдачами.
    Содержит валидацию сроков выдачи и расчет оставшихся дней.
    """

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, label="Пользователь"
    )
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = IssueBook
        fields = "__all__"
        read_only_fields = ["issued_at"]

    def get_days_remaining(self, obj):
        """Рассчитывает количество дней до возврата книги.

        Возвращает 0 если книга уже возвращена, иначе - количество дней до срока.
        """
        if obj.returned_at:
            return 0
        return (obj.return_due - date.today()).days

    def validate_return_due(self, value):
        """Валидация срока возврата книги.

        Проверяет:
        - Дата возврата не может быть в прошлом
        - Выдача не может быть более чем на 1 год
        """
        if value < date.today():
            raise serializers.ValidationError("Дата возврата не может быть в прошлом")
        if value > date.today() + timedelta(days=365):
            raise serializers.ValidationError("Выдача не может быть более чем на 1 год")
        return value


class BookShortSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор книги.

    Используется для вложенного отображения в других сериализаторах.
    Содержит только основные поля: ID, название и ISBN.
    """

    class Meta:
        model = Book
        fields = ["id", "title", "isbn"]


class MyIssueBookSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра своих выдач.

    Используется пользователями для просмотра своих выданных книг.
    Включает упрощенные данные книги и расчет оставшихся дней.
    """

    book = BookShortSerializer()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = IssueBook
        fields = [
            "id",
            "book",
            "issued_at",
            "return_due",
            "returned_at",
            "days_remaining",
        ]

    def get_days_remaining(self, obj):
        """Рассчитывает количество дней до возврата книги для текущего пользователя."""
        if obj.returned_at:
            return 0
        return (obj.return_due - date.today()).days

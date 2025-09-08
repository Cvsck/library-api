from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import serializers

from catalog.models import Author, Book, Genre, IssueBook

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "birth_date"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class BookReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate_published_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Дата публикации не может быть в будущем."
            )
        return value

    def validate(self, data):
        if data["author"].name.lower() == data["title"].lower():
            raise serializers.ValidationError(
                "Название книги не должно совпадать с именем автора."
            )
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class IssueBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueBook
        fields = "__all__"
        read_only_fields = ["user", "issued_at"]


class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "isbn"]


class MyIssueBookSerializer(serializers.ModelSerializer):
    book = BookShortSerializer()

    class Meta:
        model = IssueBook
        fields = ["id", "book", "issued_at", "returned_at"]

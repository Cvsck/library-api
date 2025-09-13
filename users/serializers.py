from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Сериализатор для аутентификации пользователя.

    Обрабатывает вход по email и паролю, возвращает JWT токены.

    Fields:
        email (EmailField): Email пользователя
        password (CharField): Пароль пользователя (write-only)
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Валидирует учетные данные и генерирует JWT токены.

        Args:
            attrs: Атрибуты с email и паролем

        Returns:
            dict: Содержит access и refresh токены

        Raises:
            ValidationError: Если аутентификация не удалась
        """
        email = attrs.get("email")
        password = attrs.get("password")

        # Аутентификация по email
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Неверный email или пароль.")

        # Генерация JWT-токенов
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя.

    Предоставляет информацию о текущем пользователе.

    Fields:
        id (int): ID пользователя
        email (str): Email пользователя
        is_active (bool): Активен ли аккаунт
        is_staff (bool): Имеет ли доступ к админке
        is_superuser (bool): Является ли суперпользователем
    """

    class Meta:
        model = User
        fields = ("id", "email", "is_active", "is_staff", "is_superuser")

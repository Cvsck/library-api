from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя с email в качестве идентификатора.

    Наследуется от AbstractBaseUser и PermissionsMixin для полной
    функциональности аутентификации и прав доступа Django.

    Attributes:
        email (EmailField): Уникальный email пользователя (используется как username)
        is_staff (BooleanField): Определяет доступ к админке
        is_active (BooleanField): Активен ли аккаунт
        date_joined (DateTimeField): Дата и время регистрации
    """

    email = models.EmailField("Email", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Поле, используемое для аутентификации (вместо username)
    USERNAME_FIELD = "email"

    # Поля, required при создании суперпользователя (кроме USERNAME_FIELD и password)
    REQUIRED_FIELDS = []

    # Кастомный менеджер пользователей
    objects = CustomUserManager()

    def __str__(self):
        """Строковое представление пользователя.

        Returns:
            str: Email пользователя
        """
        return self.email

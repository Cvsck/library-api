from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import LoginSerializer, ProfileSerializer

User = get_user_model()


@extend_schema(
    summary="Авторизация по email и паролю",
    request=LoginSerializer,
    responses={200: LoginSerializer},
    tags=["Пользователь"],
)
class LoginView(APIView):
    """View для аутентификации пользователя.

    Принимает email и пароль, возвращает JWT токены при успешной аутентификации.
    """

    @staticmethod
    def post(request):
        """Обрабатывает POST запрос для аутентификации.

        Args:
            request: HTTP запрос с данными аутентификации

        Returns:
            Response: 200 с JWT токенами при успехе, 400 с ошибками при неудаче
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)


@extend_schema(
    summary="Профиль текущего пользователя",
    description="Возвращает email, статус и права текущего пользователя. Требуется авторизация.",
    responses={200: ProfileSerializer},
    tags=["Пользователь"],
)
class ProfileView(RetrieveAPIView):
    """View для получения профиля текущего аутентифицированного пользователя.

    Предоставляет информацию о пользователе: email, статус аккаунта и права доступа.
    Требует аутентификации через JWT токен.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Возвращает объект текущего пользователя.

        Returns:
            User: Объект аутентифицированного пользователя
        """
        return self.request.user

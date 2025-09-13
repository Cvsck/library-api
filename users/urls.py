from django.urls import path

from users.views import LoginView, ProfileView

# URL patterns для приложения users
#
# Предоставляет endpoints для:
# - Аутентификации пользователей
# - Получения профиля текущего пользователя
urlpatterns = [
    # Аутентификация пользователя по email и паролю
    # POST /api/users/login/
    path("login/", LoginView.as_view(), name="login"),
    # Получение профиля текущего аутентифицированного пользователя
    # GET /api/users/profile/
    path("profile/", ProfileView.as_view(), name="profile"),
]

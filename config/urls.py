# 📦 Импорты
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

# 🔐 JWT-аутентификация
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 🌐 Основные маршруты
urlpatterns = [
    path("admin/", admin.site.urls),
    # 📚 Эндпоинты каталога
    path("api/catalog/", include("catalog.urls")),
    # 👥 Эндпоинты пользователей
    path("api/users/", include("users.urls")),
    # 🔐 JWT-аутентификация
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# 🧪 Swagger и Redoc — только в режиме DEBUG
if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView,
    )

    urlpatterns += [
        # 📄 Сырая OpenAPI-схема
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        # 🧭 Swagger UI
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        # 📘 Redoc UI
        path(
            "api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
        ),
    ]

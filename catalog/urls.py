from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.auth import CustomTokenObtainPairView
from catalog.views import (AuthorViewSet, BookViewSet, GenreViewSet,
                           IssueBookViewSet, RegisterView)

router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"books", BookViewSet)
router.register(r"issue-books", IssueBookViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
]

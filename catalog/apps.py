from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Конфигурация приложения Catalog.

    Приложение отвечает за управление основной бизнес-логикой библиотеки:
    - Авторы книг
    - Жанры литературы
    - Книги и их характеристики
    - Выдача книг пользователям
    - Учет возвратов и сроков

    Attributes:
        default_auto_field (str): Тип поля для автоматических первичных ключей
        name (str): Имя приложения в проекте Django
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"

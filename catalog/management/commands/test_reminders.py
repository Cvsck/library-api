from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test email reminders functionality"

    def handle(self, *args, **options):
        # Тест 1: Напоминание о скором возврате
        self.stdout.write("📧 Тест напоминаний о скором возврате...")
        send_mail(
            "Тест: Напоминание о возврате книги",
            'Уважаемый читатель!\n\nКнига "Война и мир" должна быть возвращена до 25.09.2025.\nОсталось 3 дня!\n\nС уважением,\nБиблиотечная система',
            "PeMaksim1983@yandex.ru",  # Отправитель (Yandex)
            ["moikrym@mail.ru"],  # Получатель (Mail.ru)
            fail_silently=False,
        )

        # Тест 2: Просроченная книга
        self.stdout.write("📧 Тест напоминаний о просрочке...")
        send_mail(
            "СРОЧНО: Книга просрочена!",
            'Уважаемый читатель!\n\nКнига "Преступление и наказание" просрочена на 5 дней!\nПожалуйста, верните книгу как можно скорее.\n\nС уважением,\nБиблиотечная система',
            "PeMaksim1983@yandex.ru",  # Отправитель (Yandex)
            ["moikrym@mail.ru"],  # Получатель (Mail.ru)
            fail_silently=False,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "✅ Тестовые emails отправлены с PeMaksim1983@yandex.ru на moikrym@mail.ru"
            )
        )

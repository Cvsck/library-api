from datetime import timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import IssueBook


class Command(BaseCommand):
    help = "Send email reminders for books due soon or overdue"

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Книги, которые нужно вернуть через 3 дня
        due_soon = IssueBook.objects.filter(
            returned_at__isnull=True, return_due=today + timedelta(days=3)
        )

        # Просроченные книги
        overdue = IssueBook.objects.filter(
            returned_at__isnull=True, return_due__lt=today
        )

        # Отправка уведомлений
        for issue in due_soon:
            self.send_reminder(issue, "soon")

        for issue in overdue:
            self.send_reminder(issue, "overdue")

        self.stdout.write(
            self.style.SUCCESS(
                f"Sent {due_soon.count()} soon-due and {overdue.count()} overdue reminders"
            )
        )

    def send_reminder(self, issue, reminder_type):
        if reminder_type == "soon":
            subject = (
                f'Напоминание: верните книгу "{issue.book.title}" до {issue.return_due}'
            )
            message = f"""
            Уважаемый {issue.user.email},

            Напоминаем, что книга "{issue.book.title}" должна быть возвращена до {issue.return_due}.
            Осталось 3 дня!

            С уважением,
            Библиотека
            """
        else:
            days_overdue = (timezone.now().date() - issue.return_due).days
            subject = (
                f'СРОЧНО: книга "{issue.book.title}" просрочена на {days_overdue} дней!'
            )
            message = f"""
            Уважаемый {issue.user.email},

            Книга "{issue.book.title}" просрочена на {days_overdue} дней!
            Пожалуйста, верните книгу как можно скорее.

            С уважением, 
            Библиотека
            """

        send_mail(
            subject,
            message,
            "noreply@library.com",
            [issue.user.email],
            fail_silently=False,
        )

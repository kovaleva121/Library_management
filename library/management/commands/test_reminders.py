from django.core.management.base import BaseCommand
from library.tasks import send_due_date_reminders


class Command(BaseCommand):
    help = 'Тестирование отправки напоминаний'

    def handle(self, *args, **options):
        send_due_date_reminders.delay()
        self.stdout.write(self.style.SUCCESS('Задача отправки напоминаний запущена'))

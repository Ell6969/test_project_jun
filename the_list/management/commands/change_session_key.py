from django.contrib.sessions.models import Session
from django.core.management import BaseCommand

from the_list.models import Products



class Command(BaseCommand):
    help = 'If session_key change, reassign the key value'

    def handle(self, *args, **options):
        self._change_session_key()

    def _change_session_key(self):
        try:
            session_key = Session.objects.first().session_key
        except Session.DoesNotExist:
            raise ValueError("Сессия не найдена. Не удалось получить session_key.")

        for product in Products.objects.all():
            product.session_key = session_key

        self.stdout.write(self.style.SUCCESS('Change products successfully'))

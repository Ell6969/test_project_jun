import uuid

from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from the_list.models import Products


class Command(BaseCommand):
    help = 'add 999 products if session.exists()'

    def handle(self, *args, **options):
        self._add_client()

    def _add_client(self) -> None:

        try:
            session_key = Session.objects.first().session_key
        except Session.DoesNotExist:
            raise ValueError("Сессия не найдена. Не удалось получить session_key.")

        products = []
        description = 'bla bla bla blablablapbla bla bla blablablapbla bla bla blablablapbla bla bla blablablap'
        for i in range(1, 1000):
            name = f'Product_{i}'
            base_slug = slugify(name)
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            product = Products(
                name=name,
                slug=unique_slug,
                price=i,
                description=description,
                session_key=session_key,)
            products.append(product)
        Products.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS('Added products successfully'))

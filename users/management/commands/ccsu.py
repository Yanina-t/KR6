from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='vyanint@gmail.com',
            first_name='Admin',
            last_name='Yanina',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('123qwe456rty')
        user.save()

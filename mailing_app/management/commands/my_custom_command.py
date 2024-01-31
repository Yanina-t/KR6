from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "My custom command"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('My custom command ran successfully'))

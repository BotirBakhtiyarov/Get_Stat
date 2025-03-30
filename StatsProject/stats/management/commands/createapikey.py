from django.core.management.base import BaseCommand
from rest_framework_api_key.models import APIKey

class Command(BaseCommand):
    help = "Yangi API Key yaratish"

    def handle(self, *args, **options):
        api_key, key = APIKey.objects.create_key(name="stats-app-key")
        self.stdout.write(f"API Key: {key}")
        self.stdout.write(self.style.SUCCESS('API Key muvaffaqiyatli yaratildi!'))
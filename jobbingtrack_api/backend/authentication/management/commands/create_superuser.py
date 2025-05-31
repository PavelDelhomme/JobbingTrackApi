from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Créer automatiquement le superutilisateur si non existant"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@delhomme.ovh")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name="Admin",
                last_name="Auto",
                job="Admin",
                phone_number="0000000000",
                address="Adresse admin",
                city="AdminCity",
                postal_code="00000",
                country="AdminLand",
                subject="Auto-created admin"
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Superutilisateur créé ({email})"))
        else:
            self.stdout.write(f"ℹ️ Superutilisateur déjà existant ({email})")

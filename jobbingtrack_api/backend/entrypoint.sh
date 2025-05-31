#!/bin/sh

echo "⏳ Attente de PostgreSQL..."
./scripts/wait-for-postgres.sh db

echo "✅ Base PostgreSQL prête. Migration..."
python manage.py migrate

python -m pip install --upgrade pip --break-system-packages

echo "🛠️ Création du superutilisateur si inexistant..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os
User = get_user_model()
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
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
    print("✅ Superutilisateur créé :", email)
else:
    print("ℹ️ Superutilisateur déjà existant :", email)
EOF

echo "🚀 Lancement du serveur Django"
exec python manage.py runserver 0.0.0.0:8000

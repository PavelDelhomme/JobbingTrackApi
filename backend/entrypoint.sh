#!/bin/sh
set -e

echo "🚀 Démarrage du backend JobbingTrack..."

# Attendre Postgres
echo "⏳ Attente de la DB..."
python manage.py wait_for_db

# Migrations automatiques
echo "🗄  Application des migrations..."
python manage.py migrate --noinput

# Collecte des fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Création du superuser si variables présentes
if [ "$DJANGO_SUPERUSER_EMAIL" ]; then
  echo "👑 Vérification/création du superuser..."
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
email = "$DJANGO_SUPERUSER_EMAIL"
pwd = "$DJANGO_SUPERUSER_PASSWORD"
if not User.objects.filter(email=email).exists():
    print(f"Création superuser: {email}")
    User.objects.create_superuser(email=email, password=pwd)
    print("✅ Superuser créé")
else:
    print("ℹ️  Superuser existe déjà")
END
fi

echo "🎯 Lancement du serveur..."
exec "$@"

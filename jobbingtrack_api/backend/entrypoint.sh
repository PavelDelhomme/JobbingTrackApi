#!/bin/sh

echo "⏳ Attente de PostgreSQL..."
./scripts/wait-for-postgres.sh db

echo "✅ Base PostgreSQL prête. Migration..."
python manage.py migrate

python -m pip install --upgrade pip --broke-system-packages
echo "🛠️ Création du superutilisateur si inexistant..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='${DJANGO_SUPERUSER_EMAIL}').exists():
    User.objects.create_superuser('${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')
    print("✅ Superutilisateur créé")
else:
    print("ℹ️ Superutilisateur déjà existant")
EOF

echo "🚀 Lancement du serveur Django"
exec python manage.py runserver 0.0.0.0:8000

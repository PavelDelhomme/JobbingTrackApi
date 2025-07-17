#!/bin/bash
echo "🔄 Exécution des migrations..."
python manage.py makemigrations
python manage.py migrate --noinput
echo "✅ Migrations terminées"

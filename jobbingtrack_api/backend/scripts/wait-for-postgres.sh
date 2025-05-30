#!/bin/sh

# Attente tant que la base n’est pas prête
until nc -z $1 5432; do
  echo "⏳ Attente de PostgreSQL ($1)..."
  sleep 1
done

echo "✅ PostgreSQL est prêt !"
exec "$@"

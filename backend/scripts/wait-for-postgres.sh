#!/bin/bash
echo "⏳ Attente de PostgreSQL..."

until PGPASSWORD=$POSTGRES_PASSWORD pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "PostgreSQL indisponible - nouvelle tentative dans 1s..."
  sleep 1
done

echo "✅ PostgreSQL opérationnel"

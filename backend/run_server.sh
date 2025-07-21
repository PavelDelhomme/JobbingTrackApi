#!/bin/bash
docker compose -f docker-compose.yml up
# docker compose down -v && docker compose build --no-cache && docker compose up
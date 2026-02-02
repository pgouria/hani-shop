#!/bin/bash
set -e



# Change these names to match your docker-compose setup

BACKUP_DIR="./backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

mkdir -p $BACKUP_DIR

echo "🧠 Backing up database before starting..."
# copy the sql lite database to a backup folder
cp ./backend/db.sqlite3 $BACKUP_DIR/db-$DATE.sqlite3



echo ">>> Building and starting Docker Compose..."


docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --build

echo ">>> Pruning old images..."
docker image prune -f


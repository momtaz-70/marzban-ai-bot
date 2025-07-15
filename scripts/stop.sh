#!/bin/bash

# Marzban AI Bot Stop Script

set -e

echo "🛑 Stopping Marzban AI Bot..."

# Stop and remove containers
docker-compose down

echo "🧹 Cleaning up..."

# Optional: Remove unused images (uncomment if needed)
# docker image prune -f

echo "✅ Marzban AI Bot stopped successfully!"
echo "🔄 To start again: ./scripts/start.sh"
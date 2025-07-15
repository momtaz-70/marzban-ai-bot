#!/bin/bash

# Marzban AI Bot Update Script

set -e

echo "🔄 Updating Marzban AI Bot..."

# Backup current .env file
if [ -f .env ]; then
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "💾 Backed up .env file"
fi

# Pull latest code
echo "📥 Pulling latest code..."
git pull

# Stop current services
echo "🛑 Stopping current services..."
docker-compose down

# Rebuild and start
echo "🏗️  Rebuilding and starting services..."
docker-compose up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 15

# Check health
echo "🔍 Checking service health..."
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Update completed successfully!"
    echo "📊 View logs: docker-compose logs -f"
else
    echo "❌ Update failed. Check logs:"
    docker-compose logs --tail=20
    exit 1
fi

echo "🎉 Marzban AI Bot updated successfully!"
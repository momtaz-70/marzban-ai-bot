#!/bin/bash

# Marzban AI Bot Startup Script
# This script helps with easy deployment and management

set -e

echo "🚀 Starting Marzban AI Bot..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration and run this script again."
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Pull latest images and start services
echo "📦 Pulling latest images..."
docker-compose pull

echo "🏗️  Building and starting services..."
docker-compose up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check health
echo "🔍 Checking service health..."
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Bot is healthy and running!"
    echo "📊 View logs: docker-compose logs -f"
    echo "🛑 Stop bot: docker-compose down"
else
    echo "❌ Bot health check failed. Check logs:"
    docker-compose logs --tail=20
fi

echo "🎉 Marzban AI Bot started successfully!"
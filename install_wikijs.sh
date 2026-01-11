#!/bin/bash
# Wiki.js Installation & Update Script
# Installs Docker (if needed) and starts Wiki.js 2.5.309

set -e

echo "=========================================="
echo "Wiki.js 2.5.309 Installation Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing Docker Desktop..."
    echo ""
    echo "Please choose installation method:"
    echo "  1. Install via Homebrew (recommended)"
    echo "  2. Manual download from docker.com"
    echo ""
    read -p "Enter choice (1 or 2): " choice

    if [ "$choice" = "1" ]; then
        echo "Installing Docker Desktop via Homebrew..."
        brew install --cask docker
        echo ""
        echo "✓ Docker Desktop installed!"
        echo ""
        echo "⚠️  IMPORTANT: Open Docker Desktop from Applications now"
        echo "    Wait for the whale icon to appear in your menu bar"
        echo "    Then press Enter to continue..."
        read -p ""
    else
        echo "Please download Docker Desktop from:"
        echo "https://www.docker.com/products/docker-desktop/"
        echo ""
        echo "After installing and starting Docker Desktop, run this script again."
        exit 0
    fi
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "⚠️  Docker is installed but not running"
    echo "    Please start Docker Desktop and wait for it to be ready"
    echo "    Then press Enter to continue..."
    read -p ""
fi

# Verify Docker is now working
if ! docker info &> /dev/null; then
    echo "❌ Docker is still not running. Please start Docker Desktop first."
    exit 1
fi

echo "✓ Docker is running!"
echo ""

# Navigate to directory
cd "$(dirname "$0")"

# Check if containers are already running
if docker compose ps | grep -q "wiki-app"; then
    echo "Wiki.js is already running. Stopping for update..."
    docker compose down
    echo ""
fi

# Pull the new image
echo "Pulling Wiki.js 2.5.309 image..."
docker compose pull

# Start services
echo ""
echo "Starting Wiki.js 2.5.309..."
docker compose up -d

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 5

# Check status
echo ""
echo "=========================================="
echo "Status Check"
echo "=========================================="
docker compose ps

echo ""
echo "=========================================="
echo "✓ Wiki.js 2.5.309 Installation Complete!"
echo "=========================================="
echo ""
echo "Access Wiki.js at: http://localhost:8080"
echo ""
echo "To view logs: docker compose logs -f wiki"
echo "To stop: docker compose down"
echo "To restart: docker compose up -d"
echo ""

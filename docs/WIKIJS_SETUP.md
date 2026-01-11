# Wiki.js Setup & Update Guide

## Current Status
- Docker is not installed
- Wiki.js docker-compose.yml exists but not running
- Need to update to Wiki.js 2.5.309

## Option 1: Docker Setup (Recommended)

### 1. Install Docker Desktop for Mac
```bash
# Download from: https://www.docker.com/products/docker-desktop/
# Or install via Homebrew:
brew install --cask docker
```

### 2. Start Docker Desktop
- Open Docker Desktop from Applications
- Wait for Docker to start (whale icon in menu bar)

### 3. Update docker-compose.yml to specify version
```yaml
services:
  wiki:
    image: requarks/wiki:2.5.309  # Pin to specific version
    # ... rest of config
```

### 4. Start Wiki.js
```bash
cd /Users/zachbeaudoin/disability-wiki
docker compose up -d
```

### 5. Access Wiki.js
- Open browser to: http://localhost:8080
- Complete initial setup if first time

### 6. Future Updates
```bash
# Edit docker-compose.yml to new version
# Then run:
docker compose pull
docker compose up -d
```

## Option 2: Native Installation (Alternative)

If you don't want to use Docker, you can install Wiki.js natively:

### 1. Install Node.js
```bash
brew install node
```

### 2. Install Wiki.js
```bash
cd /Users/zachbeaudoin/disability-wiki
npm install wiki.js@2.5.309
```

### 3. Configure Database
- Install PostgreSQL: `brew install postgresql`
- Create database: `createdb wiki`

### 4. Run Wiki.js
```bash
node server
```

## Recommended: Option 1 (Docker)
Docker is easier to manage, update, and isolate from system changes.

## Current docker-compose.yml Location
`/Users/zachbeaudoin/disability-wiki/docker-compose.yml`

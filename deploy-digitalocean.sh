#!/bin/bash

# DigitalOcean App Platform Deployment Script
# This script deploys your Docker containers to DigitalOcean App Platform

set -e

echo "🚀 Starting DigitalOcean App Platform Deployment..."

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ DigitalOcean CLI (doctl) not found."
    echo "📥 Install it from: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build the image
echo "📦 Building Docker image..."
docker build -f Dockerfile.prod -t smetool:latest .

# Create app spec
echo "📝 Creating app specification..."
cat > app.yaml << EOF
name: smetool
services:
- name: web
  source_dir: /
  github:
    repo: your-username/smetool
    branch: main
  run_command: gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 120 app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8080
  health_check:
    http_path: /health
  envs:
  - key: FLASK_ENV
    value: production
  - key: SECRET_KEY
    value: your-production-secret-key
  - key: PORT
    value: "8080"

- name: nginx
  source_dir: /
  github:
    repo: your-username/smetool
    branch: main
  run_command: nginx -g "daemon off;"
  environment_slug: docker
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 80
  routes:
  - path: /
  envs:
  - key: NGINX_PORT
    value: "80"
EOF

echo "✅ App specification created!"
echo "📋 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Run: doctl apps create --spec app.yaml"
echo "3. Your app will be deployed to DigitalOcean App Platform"

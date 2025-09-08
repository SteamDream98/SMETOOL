#!/bin/bash

# Render.com Deployment Script
# This script deploys your Docker containers to Render.com

set -e

echo "🚀 Starting Render.com Deployment..."

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build the image
echo "📦 Building Docker image..."
docker build -f Dockerfile.prod -t smetool:latest .

echo "✅ Docker image built successfully!"
echo ""
echo "📋 Next steps for Render.com deployment:"
echo ""
echo "1. 🌐 Go to https://render.com and sign up/login"
echo "2. 📁 Connect your GitHub repository"
echo "3. 🐳 Choose 'Web Service' and select 'Docker'"
echo "4. ⚙️ Configure your service:"
echo "   - Name: smetool"
echo "   - Environment: Docker"
echo "   - Build Command: docker build -f Dockerfile.prod -t smetool ."
echo "   - Start Command: gunicorn --bind 0.0.0.0:10000 --workers 4 --timeout 120 app:app"
echo "5. 🔧 Set environment variables:"
echo "   - FLASK_ENV=production"
echo "   - SECRET_KEY=your-production-secret-key"
echo "   - PORT=10000"
echo "6. 🚀 Deploy!"
echo ""
echo "💡 Render.com will automatically deploy from your GitHub repository."
echo "🔄 Any push to your main branch will trigger a new deployment."

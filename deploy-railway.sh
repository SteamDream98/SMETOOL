#!/bin/bash

# Railway Deployment Script
# This script deploys your Docker containers to Railway

set -e

echo "🚀 Starting Railway Deployment..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found."
    echo "📥 Install it with: npm install -g @railway/cli"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Create new project
echo "📁 Creating Railway project..."
railway init

# Set environment variables
echo "⚙️ Setting environment variables..."
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-production-secret-key
railway variables set PORT=5000

# Deploy
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment completed successfully!"
echo "🌐 Your application is now live on Railway!"
echo "📊 Monitor your deployment at: https://railway.app/dashboard"

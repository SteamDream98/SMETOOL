#!/bin/bash

# AWS ECS Deployment Script for SME Debt Management Tool
# This script deploys your Docker containers to AWS ECS

set -e

# Configuration
AWS_REGION="us-east-1"
CLUSTER_NAME="smetool-cluster"
SERVICE_NAME="smetool-service"
TASK_DEFINITION="smetool-task"
REPOSITORY_NAME="smetool"

echo "🚀 Starting AWS ECS Deployment..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and tag the image
echo "📦 Building Docker image..."
docker build -f Dockerfile.prod -t $REPOSITORY_NAME:latest .

# Tag for ECR
ECR_URI="$(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com/$REPOSITORY_NAME"
docker tag $REPOSITORY_NAME:latest $ECR_URI:latest

# Login to ECR
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

# Create ECR repository if it doesn't exist
echo "📁 Creating ECR repository..."
aws ecr describe-repositories --repository-names $REPOSITORY_NAME --region $AWS_REGION || \
aws ecr create-repository --repository-name $REPOSITORY_NAME --region $AWS_REGION

# Push image to ECR
echo "⬆️ Pushing image to ECR..."
docker push $ECR_URI:latest

echo "✅ Deployment completed successfully!"
echo "🌐 Your application will be available at your ECS service endpoint."
echo "📊 Monitor your deployment in the AWS ECS console."

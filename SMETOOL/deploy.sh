#!/bin/bash

# SME Debt Management Tool - Deployment Script
# This script deploys the application to a production server

set -e

echo "🚀 Starting deployment of SME Debt Management Tool..."

# Configuration
APP_NAME="sme-debt-tool"
APP_DIR="/opt/$APP_NAME"
SERVICE_USER="sme-debt"
NGINX_SITES_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed"
        exit 1
    fi
    
    if ! command -v nginx &> /dev/null; then
        print_warning "Nginx is not installed. You may need to install it separately."
    fi
    
    print_status "Dependencies check completed"
}

# Create application directory
setup_directories() {
    print_status "Setting up directories..."
    
    sudo mkdir -p $APP_DIR
    sudo mkdir -p $APP_DIR/logs
    sudo mkdir -p $APP_DIR/static
    
    print_status "Directories created"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    pip3 install --user -r requirements.txt
    
    print_status "Dependencies installed"
}

# Copy application files
deploy_application() {
    print_status "Deploying application files..."
    
    # Copy application files
    sudo cp -r . $APP_DIR/
    sudo chown -R $USER:$USER $APP_DIR
    
    print_status "Application files deployed"
}

# Create systemd service
create_service() {
    print_status "Creating systemd service..."
    
    sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null <<EOF
[Unit]
Description=SME Debt Management Tool
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$PATH
Environment=FLASK_ENV=production
Environment=SECRET_KEY=$(openssl rand -hex 32)
ExecStart=/usr/bin/python3 $APP_DIR/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable $APP_NAME
    
    print_status "Systemd service created"
}

# Configure Nginx
configure_nginx() {
    print_status "Configuring Nginx..."
    
    sudo tee $NGINX_SITES_DIR/$APP_NAME > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static/ {
        alias $APP_DIR/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    sudo ln -sf $NGINX_SITES_DIR/$APP_NAME $NGINX_ENABLED_DIR/
    sudo nginx -t
    
    print_status "Nginx configured"
}

# Start services
start_services() {
    print_status "Starting services..."
    
    sudo systemctl start $APP_NAME
    sudo systemctl restart nginx
    
    print_status "Services started"
}

# Check deployment
check_deployment() {
    print_status "Checking deployment..."
    
    sleep 5
    
    if systemctl is-active --quiet $APP_NAME; then
        print_status "✅ Application service is running"
    else
        print_error "❌ Application service is not running"
        sudo systemctl status $APP_NAME
        exit 1
    fi
    
    if systemctl is-active --quiet nginx; then
        print_status "✅ Nginx service is running"
    else
        print_error "❌ Nginx service is not running"
        sudo systemctl status nginx
        exit 1
    fi
    
    print_status "Deployment check completed"
}

# Main deployment function
main() {
    print_status "Starting deployment process..."
    
    check_dependencies
    setup_directories
    install_dependencies
    deploy_application
    create_service
    configure_nginx
    start_services
    check_deployment
    
    print_status "🎉 Deployment completed successfully!"
    print_status "Your application is now running at http://your-domain.com"
    print_warning "Remember to:"
    print_warning "1. Update the domain name in Nginx configuration"
    print_warning "2. Set up SSL certificates"
    print_warning "3. Configure firewall rules"
    print_warning "4. Set up monitoring and backups"
}

# Run main function
main "$@"

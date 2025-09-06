# SME Debt Management Tool - Deployment Guide

This guide covers various deployment options for the SME Debt Management Tool.

## 🚀 Quick Start (Development)

For local development or testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:5000
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Clone and prepare:**
   ```bash
   git clone <repository-url>
   cd sme-debt-tool-germany
   ```

2. **Configure environment:**
   ```bash
   cp config.env.example .env
   # Edit .env with your production settings
   ```

3. **Deploy:**
   ```bash
   docker-compose up -d
   ```

4. **Access:** http://your-domain.com

### Manual Docker

```bash
# Build image
docker build -t sme-debt-tool .

# Run container
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  sme-debt-tool
```

## 🐧 Linux Server Deployment

### Ubuntu/Debian

1. **Prepare server:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx git
   ```

2. **Deploy application:**
   ```bash
   git clone <repository-url>
   cd sme-debt-tool-germany
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Configure domain:**
   - Update `/etc/nginx/sites-available/sme-debt-tool`
   - Replace `your-domain.com` with your actual domain
   - Restart nginx: `sudo systemctl restart nginx`

### CentOS/RHEL

1. **Prepare server:**
   ```bash
   sudo yum update
   sudo yum install python3 python3-pip nginx git
   ```

2. **Deploy manually:**
   ```bash
   git clone <repository-url>
   cd sme-debt-tool-germany
   pip3 install -r requirements.txt
   sudo cp -r . /opt/sme-debt-tool/
   ```

3. **Create systemd service:**
   ```bash
   sudo tee /etc/systemd/system/sme-debt-tool.service > /dev/null <<EOF
   [Unit]
   Description=SME Debt Management Tool
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/sme-debt-tool
   ExecStart=/usr/bin/python3 /opt/sme-debt-tool/app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

4. **Start service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable sme-debt-tool
   sudo systemctl start sme-debt-tool
   ```

## 🪟 Windows Server Deployment

1. **Prepare server:**
   - Install Python 3.11
   - Install IIS (optional)
   - Download NSSM (Non-Sucking Service Manager)

2. **Deploy:**
   ```cmd
   # Run as Administrator
   deploy.bat
   ```

3. **Manual deployment:**
   ```cmd
   # Copy files to C:\inetpub\wwwroot\sme-debt-tool
   pip install -r requirements.txt
   python app.py
   ```

## ☁️ Cloud Deployment

### AWS EC2

1. **Launch EC2 instance:**
   - Ubuntu 20.04 LTS
   - t3.micro (free tier eligible)
   - Security group: HTTP (80), HTTPS (443), SSH (22)

2. **Connect and deploy:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   git clone <repository-url>
   cd sme-debt-tool-germany
   ./deploy.sh
   ```

3. **Configure Elastic IP:**
   - Allocate Elastic IP
   - Associate with instance
   - Update DNS records

### Google Cloud Platform

1. **Create VM instance:**
   ```bash
   gcloud compute instances create sme-debt-tool \
     --image-family=ubuntu-2004-lts \
     --image-project=ubuntu-os-cloud \
     --machine-type=e2-micro \
     --tags=http-server,https-server
   ```

2. **Deploy application:**
   ```bash
   gcloud compute ssh sme-debt-tool
   # Follow Linux deployment steps
   ```

### Azure

1. **Create VM:**
   ```bash
   az vm create \
     --resource-group myResourceGroup \
     --name sme-debt-tool \
     --image UbuntuLTS \
     --size Standard_B1s \
     --public-ip-sku Standard
   ```

2. **Deploy application:**
   ```bash
   az vm run-command invoke \
     --resource-group myResourceGroup \
     --name sme-debt-tool \
     --command-id RunShellScript \
     --scripts "git clone <repository-url> && cd sme-debt-tool-germany && ./deploy.sh"
   ```

## 🔒 SSL/HTTPS Configuration

### Let's Encrypt (Free SSL)

1. **Install Certbot:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Get certificate:**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. **Auto-renewal:**
   ```bash
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

### Commercial SSL

1. **Purchase SSL certificate**
2. **Install certificate files**
3. **Update Nginx configuration:**
   ```nginx
   ssl_certificate /path/to/certificate.crt;
   ssl_certificate_key /path/to/private.key;
   ```

## 📊 Monitoring & Maintenance

### Health Checks

- **Application health:** `curl http://your-domain.com/health`
- **Service status:** `sudo systemctl status sme-debt-tool`
- **Nginx status:** `sudo systemctl status nginx`

### Logs

- **Application logs:** `/opt/sme-debt-tool/logs/`
- **Nginx logs:** `/var/log/nginx/`
- **System logs:** `journalctl -u sme-debt-tool`

### Backup

```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/backups/sme-debt-tool"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /opt/sme-debt-tool
tar -czf $BACKUP_DIR/nginx_$DATE.tar.gz /etc/nginx

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## 🔧 Troubleshooting

### Common Issues

1. **Port 5000 already in use:**
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

2. **Permission denied:**
   ```bash
   sudo chown -R www-data:www-data /opt/sme-debt-tool
   ```

3. **Service won't start:**
   ```bash
   sudo journalctl -u sme-debt-tool -f
   ```

4. **Nginx configuration error:**
   ```bash
   sudo nginx -t
   ```

### Performance Optimization

1. **Enable gzip compression**
2. **Set up caching headers**
3. **Use CDN for static files**
4. **Implement rate limiting**
5. **Add database connection pooling**

## 📈 Scaling

### Horizontal Scaling

1. **Load balancer setup**
2. **Multiple application instances**
3. **Session management**
4. **Database clustering**

### Vertical Scaling

1. **Increase server resources**
2. **Optimize application code**
3. **Database optimization**
4. **Caching implementation**

## 🔐 Security Considerations

1. **Firewall configuration**
2. **Regular security updates**
3. **SSL/TLS encryption**
4. **Input validation**
5. **Rate limiting**
6. **Security headers**
7. **Regular backups**

## 📞 Support

For deployment issues:
1. Check logs first
2. Verify configuration
3. Test connectivity
4. Review security settings

---

**Note:** This tool is for educational purposes only. Consult financial professionals for advice.

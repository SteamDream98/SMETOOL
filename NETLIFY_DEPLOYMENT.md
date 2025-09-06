# Netlify Deployment Guide for SME Debt Management Tool

## Overview
This guide will help you deploy the SME Debt Management Tool to Netlify as a static site with serverless functions for API endpoints.

## Prerequisites
- Netlify account (free tier available)
- Git repository (GitHub, GitLab, or Bitbucket)
- Python 3.8+ installed locally

## Deployment Methods

### Method 1: Automatic Deployment from Git (Recommended)

#### Step 1: Prepare Your Repository
1. **Push your code to Git repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: SME Debt Management Tool"
   git branch -M main
   git remote add origin https://github.com/yourusername/sme-debt-tool.git
   git push -u origin main
   ```

#### Step 2: Connect to Netlify
1. **Go to [Netlify](https://netlify.com) and sign in**
2. **Click "New site from Git"**
3. **Choose your Git provider (GitHub/GitLab/Bitbucket)**
4. **Select your repository**

#### Step 3: Configure Build Settings
- **Build command:** `python build_static.py`
- **Publish directory:** `dist`
- **Python version:** `3.11` (or latest available)

#### Step 4: Deploy
1. **Click "Deploy site"**
2. **Wait for build to complete**
3. **Your site will be available at `https://your-site-name.netlify.app`**

### Method 2: Manual Deployment

#### Step 1: Build Static Site Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Build static site
python build_static.py
```

#### Step 2: Deploy to Netlify
1. **Go to Netlify dashboard**
2. **Drag and drop the `dist` folder** to the deploy area
3. **Your site will be deployed instantly**

## Configuration Files

### netlify.toml
The `netlify.toml` file configures:
- Build command and publish directory
- Redirects for API endpoints
- Environment variables
- Branch-specific settings

### _redirects
Handles client-side routing and API redirects:
```
/api/* /.netlify/functions/:splat 200
/* /index.html 200
```

### _headers
Sets security headers:
```
/*
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  X-Content-Type-Options: nosniff
```

## API Functions

The deployment includes serverless functions for:
- `/api/debt-brake` - Debt brake calculations
- `/api/cost-analysis` - Cost analysis calculations
- `/api/debt-equity` - Debt-equity swap simulations
- `/api/debt-snowball` - Debt snowball calculations
- `/api/funding-guidance` - Funding opportunity search
- `/api/covenant-tracking` - Covenant management

## Environment Variables

Set these in Netlify dashboard under Site Settings > Environment Variables:

```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax
```

## Custom Domain Setup

1. **Go to Site Settings > Domain Management**
2. **Add your custom domain**
3. **Configure DNS records as instructed by Netlify**
4. **Enable HTTPS (automatic with Netlify)**

## Features Included

### ✅ Static Site Generation
- **English and German pages** generated automatically
- **Responsive design** with Bootstrap 5
- **SEO optimized** with meta tags
- **PWA ready** with manifest.json

### ✅ Serverless Functions
- **API endpoints** for all calculations
- **CORS enabled** for cross-origin requests
- **Error handling** with proper HTTP status codes
- **Mock calculations** (replace with real logic)

### ✅ Security Features
- **Security headers** configured
- **HTTPS enforced** by Netlify
- **CSP headers** for XSS protection
- **Frame options** to prevent clickjacking

## Post-Deployment Steps

### 1. Test Your Site
- **Visit your Netlify URL**
- **Test all pages** (English and German)
- **Test API endpoints** with POST requests
- **Verify language switching** works

### 2. Update API Functions
Replace mock calculations in `.netlify/functions/` with real business logic:

```javascript
// Example: debt-brake function
case 'debt-brake':
    result = {
        debt_limit: data.revenue * 0.0035,
        available_capacity: Math.max(0, (data.revenue * 0.0035) - data.currentDebt),
        debt_usage: data.currentDebt > 0 ? (data.currentDebt / (data.revenue * 0.0035)) * 100 : 0,
        status: debtUsage > 100 ? 'Over Limit' : debtUsage > 80 ? 'Near Limit' : 'Within Limits',
        status_class: debtUsage > 100 ? 'bg-danger' : debtUsage > 80 ? 'bg-warning' : 'bg-success'
    };
    break;
```

### 3. Configure Analytics
- **Add Google Analytics** or other tracking
- **Set up Netlify Analytics** (Pro plan)
- **Monitor performance** and user behavior

### 4. Set Up Continuous Deployment
- **Push changes** to your Git repository
- **Netlify will automatically rebuild** and deploy
- **Preview deployments** for pull requests

## Troubleshooting

### Build Failures
- **Check Python version** in netlify.toml
- **Verify all dependencies** are in requirements.txt
- **Check build logs** in Netlify dashboard

### API Function Issues
- **Test functions locally** using Netlify CLI
- **Check function logs** in Netlify dashboard
- **Verify CORS settings** for frontend requests

### Translation Issues
- **Verify translations.txt** file exists
- **Check template syntax** for `{{ _('text') }}`
- **Test language switching** functionality

## Performance Optimization

### 1. Enable Netlify Features
- **Asset optimization** (automatic)
- **Image optimization** (Pro plan)
- **Edge functions** for better performance
- **CDN distribution** (automatic)

### 2. Monitor Performance
- **Use Netlify Analytics** to track metrics
- **Monitor Core Web Vitals**
- **Optimize images** and assets
- **Minimize JavaScript** bundles

## Cost Considerations

### Free Tier Limits
- **100GB bandwidth** per month
- **300 build minutes** per month
- **100GB storage**
- **Basic analytics**

### Pro Plan Benefits
- **1TB bandwidth** per month
- **500 build minutes** per month
- **Advanced analytics**
- **Priority support**

## Support and Resources

- **Netlify Documentation:** https://docs.netlify.com/
- **Netlify Community:** https://community.netlify.com/
- **Function Examples:** https://functions.netlify.com/examples/
- **Deployment Guides:** https://docs.netlify.com/site-deploys/overview/

## Success Checklist

- [ ] Repository pushed to Git
- [ ] Netlify site connected to repository
- [ ] Build settings configured
- [ ] Site deployed successfully
- [ ] All pages load correctly
- [ ] German translations working
- [ ] API endpoints responding
- [ ] Custom domain configured (optional)
- [ ] Analytics configured (optional)
- [ ] Performance optimized

Your SME Debt Management Tool is now live on Netlify! 🎉

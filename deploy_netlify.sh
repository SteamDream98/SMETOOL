#!/bin/bash
# Quick deployment script for Netlify

echo "🚀 SME Debt Management Tool - Netlify Deployment"
echo "================================================"

# Check if dist directory exists
if [ -d "dist" ]; then
    echo "📁 Removing existing dist directory..."
    rm -rf dist
fi

# Build static site
echo "🔨 Building static site..."
python build_static.py

# Check if build was successful
if [ -d "dist" ]; then
    echo "✅ Build successful!"
    echo "📊 Build summary:"
    echo "   - HTML pages: $(find dist -name "*.html" | wc -l)"
    echo "   - Static files: $(find dist -name "*.css" -o -name "*.js" -o -name "*.json" | wc -l)"
    echo "   - API functions: $(find dist/.netlify/functions -type d | wc -l)"
    
    echo ""
    echo "🌐 Ready for deployment!"
    echo "📋 Next steps:"
    echo "   1. Push your code to Git repository"
    echo "   2. Connect repository to Netlify"
    echo "   3. Set build command: python build_static.py"
    echo "   4. Set publish directory: dist"
    echo "   5. Deploy!"
    echo ""
    echo "📖 See NETLIFY_DEPLOYMENT.md for detailed instructions"
else
    echo "❌ Build failed! Check the error messages above."
    exit 1
fi

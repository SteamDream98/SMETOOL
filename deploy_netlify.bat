@echo off
REM Quick deployment script for Netlify (Windows)

echo 🚀 SME Debt Management Tool - Netlify Deployment
echo ================================================

REM Check if dist directory exists
if exist "dist" (
    echo 📁 Removing existing dist directory...
    rmdir /s /q dist
)

REM Build static site
echo 🔨 Building static site...
python build_static.py

REM Check if build was successful
if exist "dist" (
    echo ✅ Build successful!
    echo 📊 Build summary:
    echo    - HTML pages: Generated
    echo    - Static files: Copied
    echo    - API functions: Created
    
    echo.
    echo 🌐 Ready for deployment!
    echo 📋 Next steps:
    echo    1. Push your code to Git repository
    echo    2. Connect repository to Netlify
    echo    3. Set build command: python build_static.py
    echo    4. Set publish directory: dist
    echo    5. Deploy!
    echo.
    echo 📖 See NETLIFY_DEPLOYMENT.md for detailed instructions
) else (
    echo ❌ Build failed! Check the error messages above.
    exit /b 1
)

pause

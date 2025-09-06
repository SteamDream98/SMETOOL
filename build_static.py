#!/usr/bin/env python3
"""
Static Site Generator for SME Debt Management Tool
Converts Flask app to static HTML files for Netlify deployment
"""

import os
import shutil
import json
from flask import Flask, render_template_string
from app import create_app

def create_static_site():
    """Generate static HTML files from Flask templates"""
    
    # Create output directory
    output_dir = "dist"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Create Flask app
    app = create_app()
    
    # Define all routes and their templates
    routes = [
        ("/", "index.html", "index"),
        ("/debt-brake", "debt-brake.html", "debt_brake"),
        ("/cost-analysis", "cost-analysis.html", "cost_analysis"),
        ("/debt-equity", "debt-equity.html", "debt_equity"),
        ("/debt-snowball", "debt-snowball.html", "debt_snowball"),
        ("/funding-guidance", "funding-guidance.html", "funding_guidance"),
        ("/covenant-tracking", "covenant-tracking.html", "covenant_tracking"),
        ("/about", "about.html", "about"),
        ("/404", "404.html", "not_found"),
        ("/500", "500.html", "internal_error")
    ]
    
    print("🚀 Generating static site...")
    
    with app.app_context():
        # Generate English pages
        print("📄 Generating English pages...")
        for route, filename, template_name in routes:
            try:
                with app.test_request_context():
                    if template_name == "index":
                        html_content = app.jinja_env.get_template('index.html').render()
                    elif template_name == "not_found":
                        html_content = app.jinja_env.get_template('404.html').render()
                    elif template_name == "internal_error":
                        html_content = app.jinja_env.get_template('500.html').render()
                    else:
                        html_content = app.jinja_env.get_template(f'{template_name}.html').render()
                    
                    # Write HTML file
                    file_path = os.path.join(output_dir, filename)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"✅ Generated: {filename}")
                
            except Exception as e:
                print(f"❌ Error generating {filename}: {e}")
        
        # Generate German pages
        print("📄 Generating German pages...")
        for route, filename, template_name in routes:
            try:
                # Set German language in session for translation
                with app.test_request_context():
                    from flask import session
                    session['language'] = 'de'
                    
                    if template_name == "index":
                        html_content = app.jinja_env.get_template('index.html').render()
                    elif template_name == "not_found":
                        html_content = app.jinja_env.get_template('404.html').render()
                    elif template_name == "internal_error":
                        html_content = app.jinja_env.get_template('500.html').render()
                    else:
                        html_content = app.jinja_env.get_template(f'{template_name}.html').render()
                    
                    # Create German directory structure
                    de_filename = filename.replace('.html', '-de.html')
                    file_path = os.path.join(output_dir, de_filename)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"✅ Generated: {de_filename}")
                    
            except Exception as e:
                print(f"❌ Error generating German {filename}: {e}")
    
    # Copy static files
    print("📁 Copying static files...")
    static_files = ['css', 'js', 'images', 'favicon.ico', 'manifest.json', 'robots.txt']
    
    for item in static_files:
        src_path = os.path.join('static', item)
        dst_path = os.path.join(output_dir, item)
        
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
            print(f"✅ Copied: {item}")
    
    # Create API functions for Netlify
    print("🔧 Creating Netlify functions...")
    functions_dir = os.path.join(output_dir, '.netlify', 'functions')
    os.makedirs(functions_dir, exist_ok=True)
    
    # Create API function files
    api_functions = [
        'debt-brake',
        'cost-analysis', 
        'debt-equity',
        'debt-snowball',
        'funding-guidance',
        'covenant-tracking'
    ]
    
    for func_name in api_functions:
        func_dir = os.path.join(functions_dir, func_name)
        os.makedirs(func_dir, exist_ok=True)
        
        # Create index.js for each function
        func_code = f'''const {{ Handler }} = require('@netlify/functions');

exports.handler = Handler(async (event, context) => {{
    // Handle CORS
    const headers = {{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    }};

    if (event.httpMethod === 'OPTIONS') {{
        return {{
            statusCode: 200,
            headers,
            body: ''
        }};
    }}

    if (event.httpMethod !== 'POST') {{
        return {{
            statusCode: 405,
            headers,
            body: JSON.stringify({{ error: 'Method not allowed' }})
        }};
    }}

    try {{
        const data = JSON.parse(event.body);
        
        // Mock calculation logic (replace with actual calculations)
        let result = {{}};
        
        switch ('{func_name}') {{
            case 'debt-brake':
                result = {{
                    debt_limit: data.revenue * 0.0035,
                    available_capacity: Math.max(0, (data.revenue * 0.0035) - data.currentDebt),
                    debt_usage: data.currentDebt > 0 ? (data.currentDebt / (data.revenue * 0.0035)) * 100 : 0,
                    status: 'Within Limits',
                    status_class: 'bg-success'
                }};
                break;
            case 'cost-analysis':
                const monthlyRate = data.interestRate / 100 / 12;
                const numPayments = data.term * 12;
                const monthlyPayment = data.principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / (Math.pow(1 + monthlyRate, numPayments) - 1);
                result = {{
                    monthly_payment: monthlyPayment,
                    total_payment: monthlyPayment * numPayments,
                    total_interest: (monthlyPayment * numPayments) - data.principal,
                    after_tax_interest: ((monthlyPayment * numPayments) - data.principal) * (1 - data.taxRate / 100),
                    effective_rate: data.interestRate * (1 - data.taxRate / 100)
                }};
                break;
            default:
                result = {{ message: 'Function not implemented yet' }};
        }}

        return {{
            statusCode: 200,
            headers,
            body: JSON.stringify(result)
        }};
        
    }} catch (error) {{
        return {{
            statusCode: 500,
            headers,
            body: JSON.stringify({{ error: 'Internal server error' }})
        }};
    }}
}});
'''
        
        with open(os.path.join(func_dir, 'index.js'), 'w') as f:
            f.write(func_code)
        
        print(f"✅ Created function: {func_name}")
    
    # Create package.json for functions
    package_json = {
        "name": "sme-debt-tool-functions",
        "version": "1.0.0",
        "description": "Netlify functions for SME Debt Management Tool",
        "main": "index.js",
        "dependencies": {
            "@netlify/functions": "^2.0.0"
        }
    }
    
    with open(os.path.join(functions_dir, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)
    
    print("✅ Created package.json for functions")
    
    # Create _redirects file for SPA routing
    redirects_content = '''# API redirects
/api/* /.netlify/functions/:splat 200

# SPA fallback
/* /index.html 200
'''
    
    with open(os.path.join(output_dir, '_redirects'), 'w') as f:
        f.write(redirects_content)
    
    print("✅ Created _redirects file")
    
    # Create _headers file for security
    headers_content = '''/*
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
'''
    
    with open(os.path.join(output_dir, '_headers'), 'w') as f:
        f.write(headers_content)
    
    print("✅ Created _headers file")
    
    print(f"\n🎉 Static site generated successfully in '{output_dir}' directory!")
    print("📁 Files generated:")
    print(f"   - HTML pages: {len(routes) * 2} (English + German)")
    print(f"   - Static assets: {len(static_files)} directories/files")
    print(f"   - API functions: {len(api_functions)}")
    print(f"   - Configuration files: _redirects, _headers")
    
    return output_dir

if __name__ == "__main__":
    create_static_site()

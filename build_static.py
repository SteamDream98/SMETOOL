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
        ("/donation", "donation.html", "donation"),
        ("/debt-brake", "debt_brake.html", "debt_brake"),
        ("/cost-analysis", "cost_analysis.html", "cost_analysis"),
        ("/debt-equity", "debt_equity.html", "debt_equity"),
        ("/debt-snowball", "debt_snowball.html", "debt_snowball"),
        ("/funding", "funding_guidance.html", "funding_guidance"),
        ("/covenants", "covenant_tracking.html", "covenant_tracking"),
        ("/about", "about.html", "about"),
    ]
    
    print("🚀 Generating static site...")
    
    with app.app_context():
        # Generate English pages
        print("📄 Generating English pages...")
        for route, filename, template_name in routes:
            try:
                with app.test_request_context():
                    if template_name == "index":
                        html_content = app.jinja_env.get_template('index.html').render(lang='en')
                    elif template_name == "donation":
                        html_content = app.jinja_env.get_template('donation.html').render(lang='en')
                    elif template_name == "debt_brake":
                        html_content = app.jinja_env.get_template('debt_brake.html').render(lang='en')
                    elif template_name == "cost_analysis":
                        html_content = app.jinja_env.get_template('cost_analysis.html').render(lang='en')
                    elif template_name == "debt_equity":
                        html_content = app.jinja_env.get_template('debt_equity.html').render(lang='en')
                    elif template_name == "debt_snowball":
                        html_content = app.jinja_env.get_template('debt_snowball.html').render(lang='en')
                    elif template_name == "funding_guidance":
                        html_content = app.jinja_env.get_template('funding_guidance.html').render(lang='en')
                    elif template_name == "covenant_tracking":
                        html_content = app.jinja_env.get_template('covenant_tracking.html').render(lang='en')
                    elif template_name == "about":
                        html_content = app.jinja_env.get_template('about.html').render(lang='en')
                    
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
                        html_content = app.jinja_env.get_template('index.html').render(lang='de')
                    elif template_name == "donation":
                        html_content = app.jinja_env.get_template('donation.html').render(lang='de')
                    elif template_name == "debt_brake":
                        html_content = app.jinja_env.get_template('debt_brake.html').render(lang='de')
                    elif template_name == "cost_analysis":
                        html_content = app.jinja_env.get_template('cost_analysis.html').render(lang='de')
                    elif template_name == "debt_equity":
                        html_content = app.jinja_env.get_template('debt_equity.html').render(lang='de')
                    elif template_name == "debt_snowball":
                        html_content = app.jinja_env.get_template('debt_snowball.html').render(lang='de')
                    elif template_name == "funding_guidance":
                        html_content = app.jinja_env.get_template('funding_guidance.html').render(lang='de')
                    elif template_name == "covenant_tracking":
                        html_content = app.jinja_env.get_template('covenant_tracking.html').render(lang='de')
                    elif template_name == "about":
                        html_content = app.jinja_env.get_template('about.html').render(lang='de')
                    
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
            case '{func_name}':
                if ('{func_name}' === 'debt-brake') {{
                    result = {{
                        debt_limit: data.revenue * 0.0035,
                        available_capacity: Math.max(0, (data.revenue * 0.0035) - data.currentDebt),
                        debt_usage: data.currentDebt > 0 ? (data.currentDebt / (data.revenue * 0.0035)) * 100 : 0,
                        status: 'Within Limits',
                        status_class: 'bg-success'
                    }};
                }} else if ('{func_name}' === 'cost-analysis') {{
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
                }} else if ('{func_name}' === 'debt-equity') {{
                    const newShares = Math.round(data.debtAmount / data.sharePrice);
                    const totalShares = data.existingShares + newShares;
                    const ownershipDilution = (newShares / totalShares) * 100;
                    result = {{
                        new_shares_issued: newShares,
                        total_shares_after: totalShares,
                        new_share_price: data.sharePrice,
                        ownership_dilution: ownershipDilution,
                        debt_reduction: data.debtAmount,
                        impact: ownershipDilution > 20 ? 'High dilution - consider alternative' : 'Acceptable dilution'
                    }};
                }} else if ('{func_name}' === 'debt-snowball') {{
                    // Sort debts by interest rate (highest first)
                    const sortedDebts = data.debts.sort((a, b) => b.interestRate - a.interestRate);
                    let totalInterest = 0;
                    let totalPaid = 0;
                    let months = 0;
                    
                    for (const debt of sortedDebts) {{
                        const monthlyRate = debt.interestRate / 100 / 12;
                        const numPayments = Math.log(1 + (debt.balance * monthlyRate) / data.monthlyPayment) / Math.log(1 + monthlyRate);
                        const interest = (data.monthlyPayment * numPayments) - debt.balance;
                        totalInterest += interest;
                        totalPaid += debt.balance + interest;
                        months += numPayments;
                    }}
                    
                    result = {{
                        total_interest: totalInterest,
                        total_paid: totalPaid,
                        total_months: months,
                        monthly_payment: data.monthlyPayment,
                        strategy: 'Pay highest interest first'
                    }};
                }} else if ('{func_name}' === 'funding-guidance') {{
                    result = {{
                        recommended_programs: ['Innovation Funding', 'Green Transition Support', 'Digital Transformation Grant'],
                        estimated_amount: data.revenue * 0.05,
                        application_time: '2-6 months',
                        success_rate: '65%'
                    }};
                }} else if ('{func_name}' === 'covenant-tracking') {{
                    const debtToEbitda = data.totalDebt / data.ebitda;
                    const interestCoverage = data.ebitda / data.interestExpense;
                    const debtToAssets = data.totalDebt / data.totalAssets;
                    const cashFlowCoverage = data.operatingCashFlow / data.debtService;
                    
                    result = {{
                        debt_to_ebitda: debtToEbitda,
                        interest_coverage: interestCoverage,
                        debt_to_assets: debtToAssets,
                        cash_flow_coverage: cashFlowCoverage,
                        overall_status: (debtToEbitda < 3 && interestCoverage > 3) ? 'Compliant' : 'At Risk'
                    }};
                }}
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

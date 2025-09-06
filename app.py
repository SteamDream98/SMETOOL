from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))  # 16MB
    
    # Security headers
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    app.config['SESSION_COOKIE_HTTPONLY'] = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
    app.config['SESSION_COOKIE_SAMESITE'] = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    
    # Simple translation function
    def _(text):
        """Simple translation function"""
        lang = session.get('language', 'en')
        if lang == 'de':
            # Load German translations
            translations_file = 'translations/de/LC_MESSAGES/translations.txt'
            if os.path.exists(translations_file):
                try:
                    with open(translations_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            if '|' in line:
                                en_text, de_text = line.strip().split('|', 1)
                                if en_text == text:
                                    return de_text
                except:
                    pass
        return text
    
    # Make translation function available in templates
    app.jinja_env.globals.update(_=_)
    
    # Production setup
    if os.environ.get('FLASK_ENV') == 'production':
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Language switching route
    @app.route('/set_language/<lang>')
    def set_language(lang):
        if lang in ['en', 'de']:
            session['language'] = lang
        return redirect(request.referrer or url_for('index'))
    
    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/debt-brake')
    def debt_brake():
        return render_template('debt_brake.html')
    
    @app.route('/cost-analysis')
    def cost_analysis():
        return render_template('cost_analysis.html')
    
    @app.route('/debt-equity')
    def debt_equity():
        return render_template('debt_equity.html')
    
    @app.route('/debt-snowball')
    def debt_snowball():
        return render_template('debt_snowball.html')
    
    @app.route('/funding-guidance')
    def funding_guidance():
        return render_template('funding_guidance.html')
    
    @app.route('/covenant-tracking')
    def covenant_tracking():
        return render_template('covenant_tracking.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/donation')
    def donation():
        return render_template('donation.html')
    
    # API Routes for calculations
    @app.route('/api/debt-brake', methods=['POST'])
    def calculate_debt_brake():
        data = request.get_json()
        revenue = float(data.get('revenue', 0))
        
        # Germany's debt brake: 0.35% of GDP equivalent
        # For SMEs, we'll use 0.35% of annual revenue as a conservative estimate
        debt_limit = revenue * 0.0035
        
        return jsonify({
            'debt_limit': debt_limit,
            'revenue': revenue,
            'percentage': 0.35
        })
    
    @app.route('/api/cost-analysis', methods=['POST'])
    def calculate_cost_analysis():
        data = request.get_json()
        principal = float(data.get('principal', 0))
        interest_rate = float(data.get('interest_rate', 0))
        term_years = float(data.get('term_years', 0))
        tax_rate = float(data.get('tax_rate', 0))
        
        # Calculate monthly payment
        monthly_rate = interest_rate / 12 / 100
        num_payments = term_years * 12
        
        if monthly_rate > 0:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = principal / num_payments
        
        total_payment = monthly_payment * num_payments
        total_interest = total_payment - principal
        
        # After-tax cost
        after_tax_interest = total_interest * (1 - tax_rate / 100)
        after_tax_cost = principal + after_tax_interest
        
        return jsonify({
            'monthly_payment': monthly_payment,
            'total_payment': total_payment,
            'total_interest': total_interest,
            'after_tax_interest': after_tax_interest,
            'after_tax_cost': after_tax_cost,
            'effective_rate': (after_tax_interest / principal) * 100
        })
    
    @app.route('/api/debt-snowball', methods=['POST'])
    def calculate_debt_snowball():
        data = request.get_json()
        debts = data.get('debts', [])
        
        # Sort debts by interest rate (highest first)
        sorted_debts = sorted(debts, key=lambda x: float(x.get('interest_rate', 0)), reverse=True)
        
        results = []
        total_interest_saved = 0
        
        for i, debt in enumerate(sorted_debts):
            principal = float(debt.get('principal', 0))
            interest_rate = float(debt.get('interest_rate', 0))
            minimum_payment = float(debt.get('minimum_payment', 0))
            
            # Calculate payoff time with minimum payment
            monthly_rate = interest_rate / 12 / 100
            if monthly_rate > 0:
                payoff_months = -1 * (1 / monthly_rate) * (1 - (1 + monthly_rate)**(-principal / minimum_payment))
            else:
                payoff_months = principal / minimum_payment
            
            results.append({
                'debt_id': i + 1,
                'principal': principal,
                'interest_rate': interest_rate,
                'minimum_payment': minimum_payment,
                'payoff_months': payoff_months,
                'priority': i + 1
            })
        
        return jsonify({
            'prioritized_debts': results,
            'total_interest_saved': total_interest_saved
        })
    
    @app.route('/api/funding-guidance', methods=['POST'])
    def get_funding_guidance():
        data = request.get_json()
        company_size = data.get('company_size', '')
        industry = data.get('industry', '')
        purpose = data.get('purpose', '')
        
        # Sample funding programs for German SMEs
        funding_programs = [
            {
                'name': 'KfW SME Loan',
                'description': 'Low-interest loans for small and medium enterprises',
                'max_amount': 1000000,
                'interest_rate': 2.5,
                'eligibility': 'SMEs with less than 250 employees'
            },
            {
                'name': 'EU Horizon Europe',
                'description': 'Innovation and research funding',
                'max_amount': 5000000,
                'interest_rate': 0,
                'eligibility': 'Innovation-focused companies'
            },
            {
                'name': 'Digital Innovation Fund',
                'description': 'Funding for digital transformation',
                'max_amount': 500000,
                'interest_rate': 1.5,
                'eligibility': 'Companies implementing digital solutions'
            }
        ]
        
        # Filter programs based on criteria
        recommended_programs = []
        for program in funding_programs:
            if company_size == 'small' and program['max_amount'] <= 500000:
                recommended_programs.append(program)
            elif company_size == 'medium' and program['max_amount'] <= 2000000:
                recommended_programs.append(program)
            elif company_size == 'large':
                recommended_programs.append(program)
        
        return jsonify({
            'recommended_programs': recommended_programs,
            'total_programs': len(recommended_programs)
        })
    
    @app.route('/api/covenant-tracking', methods=['POST'])
    def calculate_covenants():
        data = request.get_json()
        
        # Extract financial data
        total_debt = float(data.get('total_debt', 0))
        ebitda = float(data.get('ebitda', 0))
        current_assets = float(data.get('current_assets', 0))
        current_liabilities = float(data.get('current_liabilities', 0))
        net_worth = float(data.get('net_worth', 0))
        
        # Calculate key ratios
        debt_to_ebitda = total_debt / ebitda if ebitda > 0 else 0
        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
        debt_to_equity = total_debt / net_worth if net_worth > 0 else 0
        
        # Covenant thresholds (typical for German SMEs)
        covenants = {
            'debt_to_ebitda': {
                'value': debt_to_ebitda,
                'threshold': 3.0,
                'compliant': debt_to_ebitda <= 3.0,
                'description': 'Debt-to-EBITDA Ratio'
            },
            'current_ratio': {
                'value': current_ratio,
                'threshold': 1.2,
                'compliant': current_ratio >= 1.2,
                'description': 'Current Ratio'
            },
            'debt_to_equity': {
                'value': debt_to_equity,
                'threshold': 2.0,
                'compliant': debt_to_equity <= 2.0,
                'description': 'Debt-to-Equity Ratio'
            }
        }
        
        return jsonify({
            'covenants': covenants,
            'overall_compliant': all(c['compliant'] for c in covenants.values())
        })
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
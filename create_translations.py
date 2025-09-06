# German translations compiled file
# This is a simplified approach for immediate deployment

import os
import struct

def create_mo_file():
    """Create a simple .mo file for German translations"""
    
    # Simple translation mapping
    translations = {
        'SME Debt Tool': 'SME-Schulden-Tool',
        'Debt Brake': 'Schuldenbremse',
        'Cost Analysis': 'Kostenanalyse',
        'Debt-Equity Swap': 'Schulden-Eigenkapital-Tausch',
        'Debt Snowball': 'Schulden-Schneeball',
        'Funding': 'Finanzierung',
        'Covenants': 'Covenants',
        'Language': 'Sprache',
        'About': 'Über',
        'SME Debt Management Tool': 'SME-Schuldenmanagement-Tool',
        'Comprehensive debt management solutions for German SMEs': 'Umfassende Schuldenmanagement-Lösungen für deutsche KMU',
        'Calculate': 'Berechnen',
        'Analyze': 'Analysieren',
        'Simulate': 'Simulieren',
        'Prioritize': 'Priorisieren',
        'Explore': 'Erkunden',
        'Track': 'Verfolgen',
        'Debt Brake Calculator': 'Schuldenbremse-Rechner',
        'Calculate borrowing limits based on Germany\'s debt brake mechanism': 'Berechnen Sie Kreditlimits basierend auf Deutschlands Schuldenbremse-Mechanismus',
        'Annual Revenue (€)': 'Jahresumsatz (€)',
        'Enter annual revenue': 'Jahresumsatz eingeben',
        'Your company\'s total annual revenue': 'Der Gesamtjahresumsatz Ihres Unternehmens',
        'Current Debt (€)': 'Aktuelle Schulden (€)',
        'Enter current debt': 'Aktuelle Schulden eingeben',
        'Your current outstanding debt': 'Ihre aktuellen ausstehenden Schulden',
        'Calculate Debt Limit': 'Schuldenlimit berechnen',
        'Debt Brake Limit': 'Schuldenbremse-Limit',
        '0.35% of annual revenue': '0,35% des Jahresumsatzes',
        'Available Capacity': 'Verfügbare Kapazität',
        'Remaining borrowing capacity': 'Verbleibende Kreditkapazität',
        'Current Debt Usage': 'Aktuelle Schuldennutzung',
        'Within Limits': 'Innerhalb der Grenzen',
        'Near Limit': 'Nahe dem Limit',
        'Over Limit': 'Über dem Limit',
        'Cost of Debt Analysis': 'Schuldenkosten-Analyse',
        'Analyze pre-tax and after-tax cost of debt with detailed breakdowns': 'Analysieren Sie Vor- und Nachsteuer-Schuldenkosten mit detaillierten Aufschlüsselungen',
        'Loan Principal (€)': 'Darlehenssumme (€)',
        'Enter loan amount': 'Darlehenssumme eingeben',
        'Total amount borrowed': 'Gesamtbetrag des Darlehens',
        'Interest Rate (%)': 'Zinssatz (%)',
        'Enter interest rate': 'Zinssatz eingeben',
        'Annual interest rate': 'Jährlicher Zinssatz',
        'Loan Term (Years)': 'Darlehenslaufzeit (Jahre)',
        'Enter loan term': 'Darlehenslaufzeit eingeben',
        'Length of loan in years': 'Länge des Darlehens in Jahren',
        'Tax Rate (%)': 'Steuersatz (%)',
        'Enter tax rate': 'Steuersatz eingeben',
        'Corporate tax rate (default: 30%)': 'Körperschaftsteuersatz (Standard: 30%)',
        'Calculate Cost Analysis': 'Kostenanalyse berechnen',
        'Monthly Payment': 'Monatliche Zahlung',
        'Fixed monthly payment': 'Feste monatliche Zahlung',
        'Total Payment': 'Gesamtzahlung',
        'Total amount to be paid': 'Gesamtbetrag zu zahlen',
        'Total Interest (Pre-tax)': 'Gesamtzinsen (Vor Steuern)',
        'Interest before tax benefits': 'Zinsen vor Steuervorteilen',
        'After-tax Interest': 'Nachsteuer-Zinsen',
        'Interest after tax benefits': 'Zinsen nach Steuervorteilen',
        'Effective Interest Rate': 'Effektiver Zinssatz',
        'After-tax effective interest rate': 'Nachsteuer-effektiver Zinssatz',
        'This tool is for educational purposes only. Consult financial professionals for advice.': 'Dieses Tool dient nur zu Bildungszwecken. Konsultieren Sie Finanzexperten für Beratung.',
        'Built with Flask & Bootstrap': 'Erstellt mit Flask & Bootstrap',
        'Privacy Policy': 'Datenschutzrichtlinie',
        'Terms of Service': 'Nutzungsbedingungen',
        'An error occurred. Please try again.': 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.',
        'Please fill in all required fields.': 'Bitte füllen Sie alle erforderlichen Felder aus.',
        'Invalid input. Please check your values.': 'Ungültige Eingabe. Bitte überprüfen Sie Ihre Werte.'
    }
    
    # Create directory if it doesn't exist
    os.makedirs('translations/de/LC_MESSAGES', exist_ok=True)
    
    # Write a simple text-based translation file for now
    with open('translations/de/LC_MESSAGES/translations.txt', 'w', encoding='utf-8') as f:
        for en, de in translations.items():
            f.write(f"{en}|{de}\n")
    
    print("✅ German translations file created successfully!")
    print("📁 Location: translations/de/LC_MESSAGES/translations.txt")

if __name__ == "__main__":
    create_mo_file()

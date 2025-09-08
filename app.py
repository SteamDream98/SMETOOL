import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@smedebttool.com')
    
    # Initialize Flask-Mail
    mail = Mail(app)
    
    # Make mail available to routes
    app.mail = mail
    
    # Use ProxyFix for production deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Custom translation function
    def _(text):
        """Simple translation function"""
        if session.get('language', 'de') == 'de':
            translations = {
                # Navigation
                'SME Debt Management Tool - Germany': 'SME-Schuldenmanagement-Tool - Deutschland',
                'SME Debt Tool': 'SME-Schulden-Tool',
                'SME Debt Management Tool': 'SME-Schuldenmanagement-Tool',
                'Debt Brake': 'Schuldenbremse',
                'Cost Analysis': 'Kostenanalyse',
                'Debt-Equity Swap': 'Schulden-Eigenkapital-Tausch',
                'Simulation Results': 'Simulationsergebnisse',
                'A debt-for-equity swap converts outstanding debt into company shares.': 'Ein Schulden-Eigenkapital-Tausch konvertiert ausstehende Schulden in Unternehmensaktien.',
                'Process:': 'Prozess:',
                'Determine company valuation': 'Unternehmensbewertung bestimmen',
                'Calculate share price': 'Aktienpreis berechnen',
                'Apply conversion ratio': 'Konvertierungsverhältnis anwenden',
                'Issue new shares to creditors': 'Neue Aktien an Gläubiger ausgeben',
                'Debt Snowball': 'Schulden-Schneeball',
                'Repayment Plan': 'Rückzahlungsplan',
                'Strategies': 'Strategien',
                'Snowball Method': 'Schneeball-Methode',
                'Pay off debts from smallest to largest balance. Provides psychological motivation.': 'Zahlen Sie Schulden vom kleinsten zum größten Saldo ab. Bietet psychologische Motivation.',
                'Avalanche Method': 'Lawinen-Methode',
                'Pay off debts with highest interest rates first. Saves money in the long term.': 'Zahlen Sie Schulden mit den höchsten Zinssätzen zuerst ab. Spart Geld auf lange Sicht.',
                'Funding': 'Finanzierung',
                'Covenants': 'Covenants',
                'About': 'Über',
                'Support': 'Unterstützung',
                'Language': 'Sprache',
                'Switch to German': 'Zu Deutsch wechseln',
                
                # Additional common terms
                'Guidance': 'Beratung',
                'Tracking': 'Verfolgung',
                'Funding Guidance': 'Finanzierungsberatung',
                'Covenant Tracking': 'Covenant-Verfolgung',
                
                # Common terms
                'Calculate': 'Berechnen',
                'Reset': 'Zurücksetzen',
                'Results': 'Ergebnisse',
                'Information': 'Information',
                'Warning': 'Warnung',
                'Success': 'Erfolg',
                'Error': 'Fehler',
                'Amount': 'Betrag',
                'Interest Rate': 'Zinssatz',
                'Term': 'Laufzeit',
                'Monthly Payment': 'Monatliche Zahlung',
                'Total Interest': 'Gesamtzinsen',
                'Total Amount': 'Gesamtbetrag',
                'Total Fees': 'Gesamtgebühren',
                'Total Cost': 'Gesamtkosten',
                'Cost Breakdown': 'Kostenaufstellung',
                'Interest': 'Zinsen',
                'Fees': 'Gebühren',
                'Opportunity': 'Opportunität',
                
                # Homepage
                'Comprehensive debt management solutions for German SMEs': 'Umfassende Schuldenmanagement-Lösungen für deutsche KMU',
                'Pushing innovation through the people of Germany with appreciation for the beauty of Volkach': 'Innovation durch die Menschen Deutschlands vorantreiben mit Wertschätzung für die Schönheit von Volkach',
                'Calculate debt limits, analyze costs, prioritize repayments, and find funding opportunities': 'Berechnen Sie Schuldengrenzen, analysieren Sie Kosten, priorisieren Sie Rückzahlungen und finden Sie Finanzierungsmöglichkeiten',
                'Get Started': 'Loslegen',
                'Learn More': 'Mehr erfahren',
                
                # Features
                'Debt Brake Calculator': 'Schuldenbremse-Rechner',
                'Calculate maximum sustainable debt levels': 'Berechnen Sie maximale nachhaltige Schuldenniveaus',
                'Cost of Debt Analysis': 'Schuldenkosten-Analyse',
                'Analyze total cost of borrowing': 'Analysieren Sie die Gesamtkosten der Kreditaufnahme',
                'Debt-for-Equity Swap Simulation': 'Schulden-Eigenkapital-Tausch-Simulation',
                'Simulate debt restructuring scenarios': 'Simulieren Sie Schuldenrestrukturierungsszenarien',
                'Debt Snowball Prioritization': 'Schulden-Schneeball-Priorisierung',
                'Optimize debt repayment strategy': 'Optimieren Sie die Schuldenrückzahlungsstrategie',
                'EU/Federal Funding Guidance': 'EU/Bundesfinanzierungsberatung',
                'Find available funding programs': 'Finden Sie verfügbare Finanzierungsprogramme',
                'View Programs': 'Programme anzeigen',
                'Innovation & R&D': 'Innovation & Forschung',
                'Funding for research, development, and innovation projects': 'Finanzierung für Forschungs-, Entwicklungs- und Innovationsprojekte',
                'Green Transition': 'Grüner Übergang',
                'Support for sustainable and environmental initiatives': 'Unterstützung für nachhaltige und umweltfreundliche Initiativen',
                'Digitalization': 'Digitalisierung',
                'Funding for digital transformation and technology adoption': 'Finanzierung für digitale Transformation und Technologieeinführung',
                'Export & International': 'Export & Internationales',
                'Support for international expansion and export activities': 'Unterstützung für internationale Expansion und Exportaktivitäten',
                'Training & Skills': 'Schulung & Fähigkeiten',
                'Funding for employee training and skill development': 'Finanzierung für Mitarbeiterschulung und Kompetenzentwicklung',
                'Infrastructure': 'Infrastruktur',
                'Support for infrastructure development and modernization': 'Unterstützung für Infrastrukturentwicklung und Modernisierung',
                'Funding Programs': 'Förderprogramme',
                'Debt Covenant Tracking': 'Schulden-Covenant-Verfolgung',
                'Monitor debt agreement compliance': 'Überwachen Sie die Einhaltung von Schuldenvereinbarungen',
                'Check Compliance': 'Compliance prüfen',
                'Compliance Report': 'Compliance-Bericht',
                'Common Covenants': 'Häufige Covenants',
                'Debt-to-EBITDA Ratio': 'Schulden-zu-EBITDA-Verhältnis',
                'Measures debt relative to earnings before interest, taxes, depreciation, and amortization': 'Misst Schulden im Verhältnis zu Erträgen vor Zinsen, Steuern, Abschreibungen und Amortisation',
                'Interest Coverage Ratio': 'Zinsdeckungsgrad',
                'Measures ability to pay interest expenses': 'Misst die Fähigkeit, Zinsaufwendungen zu zahlen',
                'Debt-to-Assets Ratio': 'Schulden-zu-Vermögen-Verhältnis',
                'Measures debt relative to total company assets': 'Misst Schulden im Verhältnis zum Gesamtvermögen des Unternehmens',
                'Cash Flow Coverage': 'Cashflow-Deckung',
                'Measures cash flow relative to debt obligations': 'Misst Cashflow im Verhältnis zu Schuldenverpflichtungen',
                'Compliance Status': 'Compliance-Status',
                'Current Ratio': 'Aktuelles Verhältnis',
                'Required Ratio': 'Erforderliches Verhältnis',
                'Status': 'Status',
                'Compliant': 'Konform',
                'Non-Compliant': 'Nicht konform',
                'At Risk': 'Gefährdet',
                
                # Footer
                'This tool is for educational purposes only. Consult financial professionals for advice.': 'Dieses Tool dient nur zu Bildungszwecken. Konsultieren Sie Finanzexperten für Beratung.',
                'Built with Flask & Bootstrap': 'Erstellt mit Flask & Bootstrap',
                'Privacy Policy': 'Datenschutzrichtlinie',
                'Terms of Service': 'Nutzungsbedingungen',
                
                # Donation page - Updated for Startup & Volkach theme
                'Support Development': 'Entwicklung unterstützen',
                'Support Our Startup Journey': 'Unterstützen Sie unsere Startup-Reise',
                'Pushing innovation through the people of Germany with appreciation for the beauty of Volkach': 'Innovation durch die Menschen Deutschlands vorantreiben mit Wertschätzung für die Schönheit von Volkach',
                'A startup founded with love for German culture, innovation, and the picturesque beauty of Volkach, Bavaria': 'Ein Startup gegründet mit Liebe zur deutschen Kultur, Innovation und der malerischen Schönheit von Volkach, Bayern',
                
                # Personal Message - Neighborly Support
                'A Message from Your Friendly Neighbor': 'Eine Nachricht von Ihrem freundlichen Nachbarn',
                'Dear friends and neighbors,': 'Liebe Freunde und Nachbarn,',
                'As someone who has fallen in love with the beauty of Volkach and the incredible spirit of German innovation, I wanted to reach out personally. This startup isn\'t just about building tools—it\'s about celebrating what makes Germany special: the warmth of its people, the precision of its craftsmanship, and the forward-thinking spirit that drives progress.': 'Als jemand, der sich in die Schönheit von Volkach und den unglaublichen Geist der deutschen Innovation verliebt hat, wollte ich mich persönlich bei Ihnen melden. Dieses Startup geht nicht nur darum, Tools zu bauen – es geht darum, zu feiern, was Deutschland besonders macht: die Wärme seiner Menschen, die Präzision seines Handwerks und der zukunftsorientierte Geist, der den Fortschritt vorantreibt.',
                'Every German SME deserves the best tools to succeed, and I\'m honored to be part of this journey. Your support, whether through kind words, sharing our story, or a small contribution, means the world to us. Together, we\'re not just building software—we\'re strengthening the bonds between neighbors and fostering innovation that benefits everyone.': 'Jedes deutsche KMU verdient die besten Tools, um erfolgreich zu sein, und ich bin geehrt, Teil dieser Reise zu sein. Ihre Unterstützung, sei es durch freundliche Worte, das Teilen unserer Geschichte oder einen kleinen Beitrag, bedeutet uns die Welt. Gemeinsam bauen wir nicht nur Software auf – wir stärken die Bindungen zwischen Nachbarn und fördern Innovation, von der alle profitieren.',
                'Thank you for being part of this beautiful German story. With appreciation and warm regards,': 'Vielen Dank, dass Sie Teil dieser schönen deutschen Geschichte sind. Mit Wertschätzung und herzlichen Grüßen,',
                'Your friendly neighbor and startup founder': 'Ihr freundlicher Nachbar und Startup-Gründer',
                
                # Index page - Additional translations
                'About This Tool': 'Über dieses Tool',
                'This comprehensive debt management tool is designed specifically for German SMEs to help them make informed financial decisions.': 'Dieses umfassende Schuldenmanagement-Tool wurde speziell für deutsche KMU entwickelt, um ihnen bei fundierten Finanzentscheidungen zu helfen.',
                'Our tools help you:': 'Unsere Tools helfen Ihnen:',
                'Calculate sustainable debt levels based on your income': 'Berechnen Sie nachhaltige Schuldenniveaus basierend auf Ihrem Einkommen',
                'Analyze the true cost of borrowing': 'Analysieren Sie die wahren Kosten der Kreditaufnahme',
                'Optimize your debt repayment strategy': 'Optimieren Sie Ihre Schuldenrückzahlungsstrategie',
                'Find available funding opportunities': 'Finden Sie verfügbare Finanzierungsmöglichkeiten',
                'Monitor debt covenant compliance': 'Überwachen Sie die Einhaltung von Schuldenvereinbarungen',
                'Important Notice': 'Wichtiger Hinweis',
                'Support': 'Unterstützung',
                'Analyze': 'Analysieren',
                'Simulate': 'Simulieren',
                'Optimize': 'Optimieren',
                'Find Funding': 'Finanzierung finden',
                'Track': 'Verfolgen',
                
                # Navigation and footer
                'SME Debt Management Tool Home': 'SME-Schuldenmanagement-Tool Startseite',
                'Language': 'Sprache',
                
                # Cost Analysis - Additional
                'Analysis Results': 'Analyseergebnisse',
                
                # JavaScript Messages
                'Please fill in all fields.': 'Bitte füllen Sie alle Felder aus.',
                'Please enter your monthly payment amount.': 'Bitte geben Sie Ihren monatlichen Zahlungsbetrag ein.',
                'Please add at least one debt account.': 'Bitte fügen Sie mindestens ein Schuldenkonto hinzu.',
                'Please fill in all required financial metrics.': 'Bitte füllen Sie alle erforderlichen Finanzkennzahlen aus.',
                'Thank you for your feedback! We appreciate your input.': 'Vielen Dank für Ihr Feedback! Wir schätzen Ihre Eingabe.',
                'An error occurred while sending your feedback. Please try again later.': 'Beim Senden Ihres Feedbacks ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.',
                
                # Additional missing strings
                'Net Income': 'Nettogewinn',
                'Max Monthly Debt Service': 'Maximaler monatlicher Schuldendienst',
                'Max New Debt Capacity': 'Maximale neue Schuldenkapazität',
                'Current Debt-to-Income Ratio': 'Aktuelles Schulden-zu-Einkommen-Verhältnis',
                'Sustainable': 'Nachhaltig',
                'Warning': 'Warnung',
                'Your current debt level is within sustainable limits.': 'Ihr aktueller Schuldenstand liegt innerhalb nachhaltiger Grenzen.',
                'Your current debt level exceeds recommended limits. Consider reducing debt or increasing income.': 'Ihr aktueller Schuldenstand überschreitet die empfohlenen Grenzen. Erwägen Sie, Schulden zu reduzieren oder Einkommen zu erhöhen.',
                'Monthly Payment': 'Monatliche Zahlung',
                'Total Payment': 'Gesamtzahlung',
                'Total Interest': 'Gesamtzinsen',
                'Effective Rate': 'Effektiver Zinssatz',
                'Why Support Our Mission?': 'Warum unsere Mission unterstützen?',
                'Why Support Our Startup Journey?': 'Warum unsere Startup-Reise unterstützen?',
                'Help us continue building tools for Germany': 'Helfen Sie uns, weiterhin Tools für Deutschland zu bauen',
                'Startup Innovation': 'Startup-Innovation',
                'Supporting a startup that pushes technological boundaries for German SMEs': 'Unterstützung eines Startups, das technologische Grenzen für deutsche KMU verschiebt',
                'Love for Volkach': 'Liebe zu Volkach',
                'Inspired by the beauty of Volkach, Bavaria - a symbol of German heritage and innovation': 'Inspiriert von der Schönheit von Volkach, Bayern - ein Symbol deutschen Erbes und Innovation',
                'People-Powered Innovation': 'Von Menschen angetriebene Innovation',
                'Driving innovation through the people of Germany, by the people, for the people': 'Innovation durch die Menschen Deutschlands vorantreiben, von den Menschen, für die Menschen',
                'Sustainable Growth': 'Nachhaltiges Wachstum',
                'Help us build a sustainable startup that creates lasting value for German businesses': 'Helfen Sie uns, ein nachhaltiges Startup aufzubauen, das bleibenden Wert für deutsche Unternehmen schafft',
                'Donate via PayPal': 'Spenden Sie über PayPal',
                'Buy Me a Coffee': 'Kaufen Sie mir einen Kaffee',
                'Every contribution helps us maintain and improve these tools for the German SME community.': 'Jeder Beitrag hilft uns, diese Tools für die deutsche KMU-Gemeinschaft zu erhalten und zu verbessern.',
                'Thank you for your support!': 'Vielen Dank für Ihre Unterstützung!',
                
                # Error pages
                'Page Not Found': 'Seite nicht gefunden',
                'The page you are looking for does not exist.': 'Die gesuchte Seite existiert nicht.',
                'Go Home': 'Zur Startseite',
                'Go Back': 'Zurück gehen',
                'Popular Pages': 'Beliebte Seiten',
                'Internal Server Error': 'Interner Serverfehler',
                'Something went wrong on our end.': 'Etwas ist auf unserer Seite schief gelaufen.',
                'We apologize for the inconvenience. Our team has been notified and is working to fix the issue.': 'Wir entschuldigen uns für die Unannehmlichkeiten. Unser Team wurde benachrichtigt und arbeitet daran, das Problem zu beheben.',
                'Try Again': 'Erneut versuchen',
                'What You Can Do': 'Was Sie tun können',
                'Try refreshing the page': 'Versuchen Sie, die Seite zu aktualisieren',
                'Check your internet connection': 'Überprüfen Sie Ihre Internetverbindung',
                'Try again in a few minutes': 'Versuchen Sie es in ein paar Minuten erneut',
                'Contact us if the problem persists': 'Kontaktieren Sie uns, wenn das Problem weiterhin besteht',
                
                # Debt Brake Calculator
                'Annual Revenue': 'Jahresumsatz',
                'Annual Expenses': 'Jahresausgaben',
                'Existing Debt': 'Bestehende Schulden',
                'Max Debt Service Ratio': 'Maximales Schuldendienstverhältnis',
                'Your total annual revenue': 'Ihr gesamter Jahresumsatz',
                'Your total annual expenses': 'Ihre gesamten Jahresausgaben',
                'Current outstanding debt': 'Aktuelle ausstehende Schulden',
                'Maximum percentage of net income for debt service': 'Maximaler Prozentsatz des Nettoeinkommens für Schuldendienst',
                'Calculate the maximum sustainable debt level for your SME based on income and expenses.': 'Berechnen Sie das maximale nachhaltige Schuldenniveau für Ihr KMU basierend auf Einkommen und Ausgaben.',
                'How It Works': 'Wie es funktioniert',
                'The Debt Brake Calculator helps you determine the maximum sustainable debt level for your business.': 'Der Schuldenbremse-Rechner hilft Ihnen, das maximale nachhaltige Schuldenniveau für Ihr Unternehmen zu bestimmen.',
                'Calculation Method:': 'Berechnungsmethode:',
                'Calculate net income (Revenue - Expenses)': 'Nettoeinkommen berechnen (Umsatz - Ausgaben)',
                'Determine maximum debt service (Net Income × Ratio)': 'Maximalen Schuldendienst bestimmen (Nettoeinkommen × Verhältnis)',
                'Calculate maximum new debt capacity': 'Maximale neue Schuldenkapazität berechnen',
                'Assess current debt-to-income ratio': 'Aktuelles Schulden-zu-Einkommen-Verhältnis bewerten',
                'Tip:': 'Tipp:',
                'A debt service ratio of 30% is generally considered safe for most businesses.': 'Ein Schuldendienstverhältnis von 30% wird für die meisten Unternehmen als sicher angesehen.',
                'Important Notes': 'Wichtige Hinweise',
                'This is a simplified calculation': 'Dies ist eine vereinfachte Berechnung',
                'Consider seasonal variations in income': 'Berücksichtigen Sie saisonale Einkommensschwankungen',
                'Account for emergency reserves': 'Berücksichtigen Sie Notfallreserven',
                'Consult with financial advisors': 'Konsultieren Sie Finanzberater',
                
                # Cost Analysis
                'Loan Amount': 'Darlehensbetrag',
                'Annual Interest Rate': 'Jährlicher Zinssatz',
                'Loan Term': 'Darlehenslaufzeit',
                'Upfront Fees': 'Vorabgebühren',
                'Monthly Fees': 'Monatliche Gebühren',
                'Opportunity Cost Rate': 'Opportunitätskostensatz',
                'Total amount borrowed': 'Gesamtbetrag des Darlehens',
                'Annual percentage rate': 'Jährlicher Prozentsatz',
                'Repayment period': 'Rückzahlungszeitraum',
                'Processing fees, origination fees, etc.': 'Bearbeitungsgebühren, Darlehensgebühren usw.',
                'Account maintenance fees': 'Kontoführungsgebühren',
                'Alternative investment return rate': 'Alternative Anlagerendite',
                'Analyze the total cost of borrowing including interest, fees, and opportunity costs.': 'Analysieren Sie die Gesamtkosten der Kreditaufnahme einschließlich Zinsen, Gebühren und Opportunitätskosten.',
                'Cost Components': 'Kostenelemente',
                'The total cost of debt includes several components:': 'Die Gesamtkosten der Schulden umfassen mehrere Komponenten:',
                'Interest Costs': 'Zinskosten',
                'The primary cost of borrowing money': 'Die Hauptkosten der Kreditaufnahme',
                'Fees': 'Gebühren',
                'Upfront and ongoing fees charged by the lender': 'Vorab- und laufende Gebühren des Kreditgebers',
                'Opportunity Cost': 'Opportunitätskosten',
                'Potential returns from alternative investments': 'Potenzielle Renditen aus alternativen Investitionen',
                'Compare different loan options to find the most cost-effective solution.': 'Vergleichen Sie verschiedene Darlehensoptionen, um die kosteneffektivste Lösung zu finden.',
                'Rates may vary based on creditworthiness': 'Zinssätze können je nach Bonität variieren',
                'Consider tax implications of interest': 'Berücksichtigen Sie steuerliche Auswirkungen von Zinsen',
                'Factor in inflation effects': 'Berücksichtigen Sie Inflationsauswirkungen',
                'Review all loan terms carefully': 'Überprüfen Sie alle Darlehensbedingungen sorgfältig',
                
                # Debt-Equity Swap Tool
                'Simulate debt restructuring scenarios by converting debt to equity.': 'Simulieren Sie Schuldenrestrukturierungsszenarien durch Konvertierung von Schulden in Eigenkapital.',
                'Debt Amount': 'Schuldenbetrag',
                'Amount of debt to convert': 'Zu konvertierender Schuldenbetrag',
                'Company Valuation': 'Unternehmensbewertung',
                'Current company value': 'Aktueller Unternehmenswert',
                'Existing Shares': 'Bestehende Aktien',
                'Current number of shares': 'Aktuelle Anzahl der Aktien',
                'Conversion Ratio': 'Konvertierungsverhältnis',
                'Debt to equity conversion ratio': 'Schulden-zu-Eigenkapital-Konvertierungsverhältnis',
                'Considerations': 'Überlegungen',
                'Reduces debt burden': 'Reduziert Schuldenlast',
                'Improves cash flow': 'Verbessert Cashflow',
                'Dilutes ownership': 'Verdünnt Eigentum',
                'May affect control': 'Kann Kontrolle beeinflussen',
                'Current Share Price': 'Aktueller Aktienpreis',
                'New Shares Issued': 'Neue ausgegebene Aktien',
                'Total Shares After': 'Gesamtaktien danach',
                'New Share Price': 'Neuer Aktienpreis',
                'Ownership Dilution': 'Eigentumsverdünnung',
                'Debt Reduction': 'Schuldenreduktion',
                'Impact:': 'Auswirkung:',
                'This swap reduces debt by': 'Dieser Tausch reduziert Schulden um',
                'but dilutes ownership by': 'aber verdünnt Eigentum um',
                'This can improve cash flow by reducing debt service obligations.': 'Dies kann den Cashflow verbessern, indem es Schuldenverpflichtungen reduziert.',
                
                # JavaScript Messages for Debt-Equity Tool
                'Please fill in all required fields.': 'Bitte füllen Sie alle erforderlichen Felder aus.',
                
                # Additional Debt-Equity Translations
                'How It Works': 'Wie es funktioniert',
                'Tip:': 'Tipp:',
                '1:1 (Par Value)': '1:1 (Nennwert)',
                '1:1.2 (Premium)': '1:1.2 (Prämie)',
                '1:1.5 (High Premium)': '1:1.5 (Hohe Prämie)',
                '1:0.8 (Discount)': '1:0.8 (Rabatt)',
                
                # Debt-Snowball Tool
                'Optimize your debt repayment strategy using the snowball method.': 'Optimieren Sie Ihre Schuldenrückzahlungsstrategie mit der Schneeball-Methode.',
                'Total Monthly Payment': 'Monatliche Gesamtzahlung',
                'Total amount available for debt payments': 'Gesamtbetrag verfügbar für Schuldenzahlungen',
                'Repayment Strategy': 'Rückzahlungsstrategie',
                'Snowball (Smallest Balance First)': 'Schneeball (Kleinster Saldo zuerst)',
                'Avalanche (Highest Interest First)': 'Lawine (Höchster Zinssatz zuerst)',
                'Choose your repayment strategy': 'Wählen Sie Ihre Rückzahlungsstrategie',
                'Debt Accounts': 'Schuldenkonten',
                'Debt Name': 'Schuldenname',
                'Balance': 'Saldo',
                'Add Debt': 'Schulden hinzufügen',
                'Remove Debt': 'Schulden entfernen',
                'Calculate': 'Berechnen',
                'Pay off debts from highest to lowest interest rate. Saves more money in interest.': 'Zahlen Sie Schulden vom höchsten zum niedrigsten Zinssatz ab. Spart mehr Geld an Zinsen.',
                'Choose the method that motivates you to stick with the plan.': 'Wählen Sie die Methode, die Sie motiviert, beim Plan zu bleiben.',
                'Benefits': 'Vorteile',
                'Reduces total interest paid': 'Reduziert die Gesamtzinsen',
                'Provides clear payoff timeline': 'Bietet klare Tilgungszeitplan',
                'Builds momentum': 'Baut Momentum auf',
                'Improves credit score': 'Verbessert Bonität',
                
                # JavaScript Messages for Debt-Snowball Tool
                'Summary': 'Zusammenfassung',
                'Total Debt': 'Gesamtschulden',
                'Months to Payoff': 'Monate bis zur Tilgung',
                'Total Paid': 'Gesamtbetrag bezahlt',
                'Original Balance': 'Ursprünglicher Saldo',
                'Interest': 'Zinsen',
                'Months': 'Monate',
                
                # Funding-Guidance Tool
                'Find available funding programs and grants for German SMEs.': 'Finden Sie verfügbare Förderprogramme und Zuschüsse für deutsche KMU.',
                'Key Resources': 'Wichtige Ressourcen',
                'Main source for federal funding programs': 'Hauptquelle für Bundesförderprogramme',
                'Low-interest loans and guarantees': 'Zinsgünstige Kredite und Garantien',
                'Grants and subsidies for various sectors': 'Zuschüsse und Subventionen für verschiedene Sektoren',
                'Research and innovation funding': 'Forschungs- und Innovationsförderung',
                'Application Tips': 'Bewerbungstipps',
                'Start early - applications can take months': 'Frühzeitig beginnen - Bewerbungen können Monate dauern',
                'Read guidelines carefully': 'Richtlinien sorgfältig lesen',
                'Prepare detailed project descriptions': 'Detaillierte Projektbeschreibungen vorbereiten',
                'Include realistic budgets and timelines': 'Realistische Budgets und Zeitpläne einbeziehen',
                'Seek professional advice if needed': 'Bei Bedarf professionelle Beratung suchen',
                'Keep detailed records of all correspondence': 'Detaillierte Aufzeichnungen aller Korrespondenz aufbewahren',
                'Funding availability and criteria may change. Always check official sources for current information.': 'Verfügbarkeit und Kriterien der Förderung können sich ändern. Überprüfen Sie immer offizielle Quellen für aktuelle Informationen.',
                'Amount:': 'Betrag:',
                'Deadline:': 'Frist:',
                'Learn More': 'Mehr erfahren',
                'Continuous': 'Laufend',
                'Varies by region': 'Variiert je nach Region',
                'Note:': 'Hinweis:',
                'Support for R&D projects in SMEs': 'Unterstützung für FuE-Projekte in KMU',
                'Innovation funding for SMEs': 'Innovationsförderung für KMU',
                'Support for energy-efficient buildings': 'Unterstützung für energieeffiziente Gebäude',
                'Low-interest loans for energy efficiency': 'Zinsgünstige Kredite für Energieeffizienz',
                'Digital transformation support': 'Unterstützung für digitale Transformation',
                'Digitalization consulting and implementation': 'Digitalisierungsberatung und -umsetzung',
                'Export financing and guarantees': 'Exportfinanzierung und Garantien',
                'Support for international market entry': 'Unterstützung für den internationalen Markteintritt',
                'Training for older employees': 'Weiterbildung für ältere Mitarbeiter',
                'Vocational training support': 'Berufliche Weiterbildungsunterstützung',
                'Regional development funding': 'Förderung der regionalen Entwicklung',
                'Infrastructure development loans': 'Infrastrukturentwicklungskredite',
                'Up to €350,000': 'Bis zu €350.000',
                'Up to €2M': 'Bis zu €2 Mio.',
                'Up to €75,000': 'Bis zu €75.000',
                'Up to €25M': 'Bis zu €25 Mio.',
                'Up to €17,000': 'Bis zu €17.000',
                'Up to €16,500': 'Bis zu €16.500',
                'Up to €5M': 'Bis zu €5 Mio.',
                'Up to €50,000': 'Bis zu €50.000',
                'Up to €2,000': 'Bis zu €2.000',
                'Up to €3,000': 'Bis zu €3.000',
                'Up to €1M': 'Bis zu €1 Mio.',
                'Up to €10M': 'Bis zu €10 Mio.',
                'Monitor compliance with debt agreement covenants and requirements.': 'Überwachen Sie die Einhaltung von Schuldenvertragsklauseln und -anforderungen.',
                'Company Name': 'Firmenname',
                'Your Company GmbH': 'Ihre Firma GmbH',
                'Reporting Date': 'Berichtsdatum',
                'Financial Metrics': 'Finanzkennzahlen',
                'Total Assets (€)': 'Gesamtvermögen (€)',
                'Operating Cash Flow (€)': 'Operativer Cashflow (€)',
                'Covenant Requirements': 'Covenant-Anforderungen',
                'Max Debt-to-EBITDA Ratio': 'Max. Schulden-zu-EBITDA-Verhältnis',
                'Min Interest Coverage Ratio': 'Min. Zinsdeckungsgrad',
                'Max Debt-to-Assets Ratio': 'Max. Schulden-zu-Vermögen-Verhältnis',
                'Min Cash Flow Coverage': 'Min. Cashflow-Deckung',
                'Common Covenants': 'Häufige Covenants',
                'Measures ability to pay interest expenses from operating income': 'Misst die Fähigkeit, Zinsaufwendungen aus dem Betriebsertrag zu zahlen',
                'Measures percentage of assets financed by debt': 'Misst den Prozentsatz der durch Schulden finanzierten Vermögenswerte',
                'Measures ability to service debt from operating cash flow': 'Misst die Fähigkeit, Schulden aus dem operativen Cashflow zu bedienen',
                'Compliance Tips': 'Compliance-Tipps',
                'Monitor ratios regularly': 'Verhältnisse regelmäßig überwachen',
                'Maintain adequate cash reserves': 'Ausreichende Liquiditätsreserven aufrechterhalten',
                'Plan for seasonal variations': 'Für saisonale Schwankungen planen',
                'Communicate with lenders early': 'Frühzeitig mit Kreditgebern kommunizieren',
                'Consider covenant amendments if needed': 'Bei Bedarf Covenant-Änderungen in Betracht ziehen',
                'Please fill in all required financial metrics.': 'Bitte füllen Sie alle erforderlichen Finanzkennzahlen aus.',
                'All Covenants Compliant': 'Alle Covenants eingehalten',
                'Covenant Violations Detected': 'Covenant-Verstöße erkannt',
                'Your company is in compliance with all debt covenants.': 'Ihr Unternehmen hält alle Schulden-Covenants ein.',
                'Some covenants are not being met. Review the details below.': 'Einige Covenants werden nicht eingehalten. Überprüfen Sie die Details unten.',
                'Debt-to-EBITDA Ratio': 'Schulden-zu-EBITDA-Verhältnis',
                'Interest Coverage Ratio': 'Zinsdeckungsgrad',
                'Debt-to-Assets Ratio': 'Schulden-zu-Vermögen-Verhältnis',
                'Cash Flow Coverage': 'Cashflow-Deckung',
                'Compliant': 'Eingehalten',
                'Violation': 'Verstoß',
                'Current:': 'Aktuell:',
                'Limit:': 'Grenzwert:',
                'Action Required:': 'Maßnahme erforderlich:',
                'Consider reducing debt or increasing EBITDA through operational improvements.': 'Erwägen Sie Schuldenreduzierung oder EBITDA-Steigerung durch operative Verbesserungen.',
                'Focus on increasing operating income or reducing interest expenses.': 'Konzentrieren Sie sich auf die Steigerung des Betriebsertrags oder die Senkung der Zinsaufwendungen.',
                'Consider reducing debt or increasing asset base through investments.': 'Erwägen Sie Schuldenreduzierung oder Vermögensaufstockung durch Investitionen.',
                'Improve operating cash flow or consider debt restructuring.': 'Verbessern Sie den operativen Cashflow oder erwägen Sie eine Umschuldung.',
                'Review financial performance and consider corrective actions.': 'Überprüfen Sie die finanzielle Leistung und erwägen Sie Korrekturmaßnahmen.',
                'About SME Debt Management Tool': 'Über SME-Schuldenmanagement-Tool',
                'A startup initiative pushing innovation through the people of Germany with appreciation for the beauty of Volkach, Bavaria. We create digital solutions that empower German SMEs to thrive in the modern economy.': 'Eine Startup-Initiative, die Innovation durch die Menschen Deutschlands vorantreibt, mit Wertschätzung für die Schönheit von Volkach in Bayern. Wir schaffen digitale Lösungen, die deutschen KMU helfen, in der modernen Wirtschaft zu gedeihen.',
                'Our Startup Journey': 'Unsere Startup-Reise',
                'Founded with deep appreciation for German culture and innovation, our startup is inspired by the picturesque beauty of Volkach. We believe in driving technological progress through the people of Germany, by the people, for the people. Our mission is to create sustainable digital solutions that strengthen German SMEs and contribute to the nation\'s innovative spirit.': 'Gegründet mit tiefer Wertschätzung für deutsche Kultur und Innovation, ist unser Startup inspiriert von der malerischen Schönheit von Volkach. Wir glauben daran, technologischen Fortschritt durch die Menschen Deutschlands, von den Menschen, für die Menschen voranzutreiben. Unsere Mission ist es, nachhaltige digitale Lösungen zu schaffen, die deutsche KMU stärken und zum innovativen Geist der Nation beitragen.',
                'What We Offer': 'Was wir anbieten',
                'Calculate maximum sustainable debt levels based on your income and expenses.': 'Berechnen Sie maximale nachhaltige Schuldenlevels basierend auf Ihren Einnahmen und Ausgaben.',
                'Optimize your debt repayment strategy using proven methods.': 'Optimieren Sie Ihre Schuldenrückzahlungsstrategie mit bewährten Methoden.',
                'Why We Built This': 'Warum wir das gebaut haben',
                'German SMEs face unique challenges in managing debt and accessing funding. We recognized the need for specialized tools that understand the German business environment, regulatory framework, and funding landscape.': 'Deutsche KMU stehen vor einzigartigen Herausforderungen bei der Verwaltung von Schulden und dem Zugang zu Finanzierungen. Wir erkannten die Notwendigkeit spezialisierter Tools, die die deutsche Geschäftsumgebung, den regulatorischen Rahmen und die Finanzierungslandschaft verstehen.',
                'Our tools are designed to be:': 'Unsere Tools sind so konzipiert, dass sie:',
                'Accessible:': 'Zugänglich:',
                'Accurate:': 'Genau:',
                'Practical:': 'Praktisch:',
                'Multilingual:': 'Mehrsprachig:',
                'Mobile-Friendly:': 'Mobilfreundlich:',
                'Free to use with no registration required': 'Kostenlos zu verwenden, ohne Registrierung erforderlich',
                'Based on established financial principles and German regulations': 'Basierend auf etablierten Finanzprinzipien und deutschen Vorschriften',
                'Designed for real-world business scenarios': 'Entwickelt für reale Geschäftsszenarien',
                'Available in English and German': 'Verfügbar in Englisch und Deutsch',
                'Optimized for use on all devices': 'Optimiert für die Verwendung auf allen Geräten',
                'Our Commitment': 'Unser Engagement',
                'We are committed to providing accurate, up-to-date tools that help German SMEs make better financial decisions. However, we want to emphasize that:': 'Wir verpflichten uns, genaue und aktuelle Tools bereitzustellen, die deutschen KMU helfen, bessere finanzielle Entscheidungen zu treffen. Wir möchten jedoch betonen, dass:',
                'Important Disclaimer:': 'Wichtiger Haftungsausschluss:',
                'This tool is for educational purposes only. It should not be considered as professional financial advice. Always consult with qualified financial professionals before making important financial decisions.': 'Dieses Tool dient nur zu Bildungszwecken. Es sollte nicht als professionelle Finanzberatung betrachtet werden. Konsultieren Sie immer qualifizierte Finanzexperten, bevor Sie wichtige finanzielle Entscheidungen treffen.',
                'Support Our Mission': 'Unterstützen Sie unsere Mission',
                'Your friendly American citizen building bipartisan tools for Germany': 'Ihr freundlicher amerikanischer Bürger, der überparteiliche Tools für Deutschland baut',
                'Technical Details': 'Technische Details',
                'This application is built using modern web technologies:': 'Diese Anwendung wurde mit modernen Webtechnologien erstellt:',
                'Backend:': 'Backend:',
                'Frontend:': 'Frontend:',
                'JavaScript:': 'JavaScript:',
                'Design:': 'Design:',
                'Languages:': 'Sprachen:',
                'Python Flask': 'Python Flask',
                'Bootstrap 5, HTML5, CSS3': 'Bootstrap 5, HTML5, CSS3',
                'Vanilla JS with mobile optimization': 'Vanilla JS mit mobiler Optimierung',
                'Mobile-first responsive design': 'Mobile-first responsives Design',
                'English and German support': 'Englisch- und Deutschunterstützung',
                'Contact & Feedback': 'Kontakt & Feedback',
                'We welcome your feedback and suggestions for improvement.': 'Wir freuen uns über Ihr Feedback und Verbesserungsvorschläge.',
                'Send Feedback': 'Feedback senden',
                'Support Us': 'Unterstützen Sie uns',
                'Your Name': 'Ihr Name',
                'Email Address': 'E-Mail-Adresse',
                'Message': 'Nachricht',
                'Cancel': 'Abbrechen',
                'Please fill in all fields.': 'Bitte füllen Sie alle Felder aus.',
                'Thank you for your feedback! We appreciate your input.': 'Vielen Dank für Ihr Feedback! Wir schätzen Ihre Eingabe.',
                'What Your Support Enables': 'Was Ihre Unterstützung ermöglicht',
                'Server Costs': 'Serverkosten',
                'Keeping our tools online and accessible 24/7': 'Unsere Tools online und rund um die Uhr zugänglich halten',
                'Bug Fixes': 'Fehlerbehebungen',
                'Maintaining code quality and fixing issues': 'Codequalität erhalten und Probleme beheben',
                'New Features': 'Neue Funktionen',
                'Adding new tools and improving existing ones': 'Neue Tools hinzufügen und bestehende verbessern'
            }
            return translations.get(text, text)
        return text
    
    # Make translation function available in templates
    app.jinja_env.globals.update(_=_)
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'timestamp': str(datetime.now())})
    
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
    
    # Language switching route
    @app.route('/set-language/<lang>')
    def set_language(lang):
        if lang in ['en', 'de']:
            session['language'] = lang
        return redirect(request.referrer or url_for('index'))
    
    # Feedback submission route
    @app.route('/submit-feedback', methods=['POST'])
    def submit_feedback():
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()
            
            # Validate required fields
            if not all([name, email, message]):
                return jsonify({'success': False, 'message': _('Please fill in all fields.')}), 400
            
            # Basic email validation
            import re
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_regex, email):
                return jsonify({'success': False, 'message': _('Please enter a valid email address.')}), 400
            
            # Send email
            msg = Message(
                subject=f"SME Debt Tool Feedback from {name}",
                recipients=['theradicalblack@gmail.com'],
                body=f"""
New feedback received from SME Debt Management Tool:

Name: {name}
Email: {email}
Message:
{message}

---
This feedback was submitted via the About page feedback form.
Timestamp: {request.headers.get('Date', 'Unknown')}
User Agent: {request.headers.get('User-Agent', 'Unknown')}
IP Address: {request.remote_addr}
                """,
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            
            app.mail.send(msg)
            
            return jsonify({'success': True, 'message': _('Thank you for your feedback! We appreciate your input.')})
            
        except Exception as e:
            print(f"Error sending feedback email: {e}")
            return jsonify({'success': False, 'message': _('An error occurred while sending your feedback. Please try again later.')}), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
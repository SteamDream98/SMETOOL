#!/usr/bin/env python3
"""
Translation compilation script for SME Debt Management Tool
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main function to compile translations"""
    print("🌍 SME Debt Management Tool - Translation Compilation")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('babel.cfg'):
        print("❌ Error: babel.cfg not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Extract messages
    if not run_command('pybabel extract -F babel.cfg -k _l -o messages.pot .', "Extracting messages"):
        sys.exit(1)
    
    # Update German translation
    if not run_command('pybabel update -i messages.pot -d translations -l de', "Updating German translation"):
        sys.exit(1)
    
    # Compile German translation
    if not run_command('pybabel compile -d translations -l de', "Compiling German translation"):
        sys.exit(1)
    
    print("\n🎉 Translation compilation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Review translations in translations/de/LC_MESSAGES/messages.po")
    print("2. Update any translations as needed")
    print("3. Re-run this script to compile changes")
    print("4. Restart your Flask application")
    print("\n🌐 Test translations:")
    print("- English: http://localhost:5000/?lang=en")
    print("- German:  http://localhost:5000/?lang=de")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for SME Debt Management Tool API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_debt_brake():
    """Test debt brake calculator endpoint"""
    print("Testing Debt Brake Calculator...")
    data = {
        "revenue": 1000000,
        "currentDebt": 50000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/debt-brake", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Debt limit: €{result['debt_limit']:,.2f}")
            print(f"✓ Revenue: €{result['revenue']:,.2f}")
            print(f"✓ Percentage: {result['percentage']}%")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def test_cost_analysis():
    """Test cost analysis endpoint"""
    print("\nTesting Cost Analysis...")
    data = {
        "principal": 100000,
        "interest_rate": 5.0,
        "term_years": 5,
        "tax_rate": 30
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/cost-analysis", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Monthly payment: €{result['monthly_payment']:,.2f}")
            print(f"✓ Total interest: €{result['total_interest']:,.2f}")
            print(f"✓ After-tax interest: €{result['after_tax_interest']:,.2f}")
            print(f"✓ Effective rate: {result['effective_rate']:.2f}%")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def test_debt_snowball():
    """Test debt snowball endpoint"""
    print("\nTesting Debt Snowball...")
    data = {
        "debts": [
            {
                "principal": 50000,
                "interest_rate": 8.0,
                "minimum_payment": 1000
            },
            {
                "principal": 30000,
                "interest_rate": 6.0,
                "minimum_payment": 800
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/debt-snowball", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Prioritized {len(result['prioritized_debts'])} debts")
            for debt in result['prioritized_debts']:
                print(f"  - Priority {debt['priority']}: €{debt['principal']:,.2f} at {debt['interest_rate']}%")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def test_funding_guidance():
    """Test funding guidance endpoint"""
    print("\nTesting Funding Guidance...")
    data = {
        "company_size": "small",
        "industry": "technology",
        "purpose": "innovation",
        "amount": 100000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/funding-guidance", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Found {result['total_programs']} funding programs")
            for program in result['recommended_programs']:
                print(f"  - {program['name']}: €{program['max_amount']:,.2f}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def test_covenant_tracking():
    """Test covenant tracking endpoint"""
    print("\nTesting Covenant Tracking...")
    data = {
        "total_debt": 200000,
        "ebitda": 100000,
        "current_assets": 150000,
        "current_liabilities": 100000,
        "net_worth": 200000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/covenant-tracking", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Overall compliant: {result['overall_compliant']}")
            for name, covenant in result['covenants'].items():
                print(f"  - {covenant['description']}: {covenant['value']:.2f} ({'✓' if covenant['compliant'] else '✗'})")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def main():
    """Run all tests"""
    print("SME Debt Management Tool - API Tests")
    print("=" * 50)
    
    test_debt_brake()
    test_cost_analysis()
    test_debt_snowball()
    test_funding_guidance()
    test_covenant_tracking()
    
    print("\n" + "=" * 50)
    print("API tests completed!")

if __name__ == "__main__":
    main()

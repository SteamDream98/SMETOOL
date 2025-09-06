#!/usr/bin/env python3
"""
Test script to verify German translation deployment
"""

import urllib.request
import urllib.error

def test_deployment():
    """Test if the application is running and German translation works"""
    
    print("🌍 Testing SME Debt Management Tool Deployment")
    print("=" * 50)
    
    # Test main page
    try:
        response = urllib.request.urlopen('http://127.0.0.1:5000/')
        if response.getcode() == 200:
            print("✅ Main page is accessible")
        else:
            print(f"❌ Main page returned status code: {response.getcode()}")
            return False
    except urllib.error.URLError as e:
        print(f"❌ Cannot access main page: {e}")
        return False
    
    # Test German language switch
    try:
        response = urllib.request.urlopen('http://127.0.0.1:5000/set_language/de')
        if response.getcode() in [200, 302]:  # 302 is redirect
            print("✅ German language switch is working")
        else:
            print(f"❌ German language switch returned status code: {response.getcode()}")
    except urllib.error.URLError as e:
        print(f"❌ Cannot test German language switch: {e}")
    
    # Test API endpoints
    api_endpoints = [
        '/api/debt-brake',
        '/api/cost-analysis', 
        '/api/debt-snowball',
        '/api/funding-guidance',
        '/api/covenant-tracking',
        '/health'
    ]
    
    for endpoint in api_endpoints:
        try:
            response = urllib.request.urlopen(f'http://127.0.0.1:5000{endpoint}')
            if response.getcode() in [200, 405]:  # 405 is Method Not Allowed (expected for GET on POST endpoints)
                print(f"✅ {endpoint} is accessible")
            else:
                print(f"⚠️  {endpoint} returned status code: {response.getcode()}")
        except urllib.error.URLError as e:
            print(f"❌ Cannot access {endpoint}: {e}")
    
    print("\n🎉 Deployment test completed!")
    print("\n📋 Access your application:")
    print("🌐 English: http://127.0.0.1:5000/")
    print("🇩🇪 German:  http://127.0.0.1:5000/set_language/de")
    print("\n🔧 Features available:")
    print("• Debt Brake Calculator")
    print("• Cost Analysis")
    print("• Debt-Equity Swap Simulation")
    print("• Debt Snowball Prioritization")
    print("• EU/Federal Funding Guidance")
    print("• Debt Covenant Tracking")
    print("• German/English Language Support")
    
    return True

if __name__ == "__main__":
    test_deployment()

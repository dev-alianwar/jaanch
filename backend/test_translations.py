#!/usr/bin/env python3
"""
Test script to verify translation seeding and API endpoints
"""
import requests
import json
import sys

def test_translation_endpoints():
    """Test translation API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing translation endpoints...")
    
    # Test English translations
    try:
        response = requests.get(f"{base_url}/translations/locale/en")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ English translations loaded: {len(data.get('translations', {}))} keys")
        else:
            print(f"❌ Failed to load English translations: {response.status_code}")
    except Exception as e:
        print(f"❌ Error loading English translations: {e}")
    
    # Test Urdu translations
    try:
        response = requests.get(f"{base_url}/translations/locale/ur")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Urdu translations loaded: {len(data.get('translations', {}))} keys")
        else:
            print(f"❌ Failed to load Urdu translations: {response.status_code}")
    except Exception as e:
        print(f"❌ Error loading Urdu translations: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend health: {data.get('status')}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking backend health: {e}")

if __name__ == "__main__":
    test_translation_endpoints()
#!/usr/bin/env python3
"""
Test runner for modular structure
"""
import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Health: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


def test_registration():
    """Test user registration"""
    user_data = {
        "email": "modular_test@example.com",
        "password": "testpass123",
        "first_name": "Modular",
        "last_name": "Test",
        "role": "customer"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
        print(f"Registration: {response.status_code} - {response.text}")
        
        if response.status_code == 201:
            return response.json()
        return None
    except Exception as e:
        print(f"Registration failed: {e}")
        return None


def test_login():
    """Test user login"""
    login_data = {
        "email": "modular_test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Login: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Login failed: {e}")
        return None


def test_protected_endpoint(access_token):
    """Test protected endpoint"""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
        print(f"Protected endpoint: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Protected endpoint failed: {e}")
        return False


def main():
    """Run modular structure tests"""
    print("🧪 Testing Modular Backend Structure")
    print(f"Testing against: {BASE_URL}")
    
    # Check server
    if not test_health():
        print("❌ Server not available")
        print("Start the server with: python3 main_new.py")
        sys.exit(1)
    
    print("✅ Server is healthy")
    
    # Test registration
    registration_data = test_registration()
    if not registration_data:
        print("❌ Registration failed")
        sys.exit(1)
    
    print("✅ Registration successful")
    access_token = registration_data["access_token"]
    
    # Test login
    login_data = test_login()
    if not login_data:
        print("❌ Login failed")
        sys.exit(1)
    
    print("✅ Login successful")
    
    # Test protected endpoint
    if not test_protected_endpoint(access_token):
        print("❌ Protected endpoint failed")
        sys.exit(1)
    
    print("✅ Protected endpoint successful")
    print("🎉 All modular tests passed!")


if __name__ == "__main__":
    main()
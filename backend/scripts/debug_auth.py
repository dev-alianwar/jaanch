#!/usr/bin/env python3
"""
Debug authentication issues
"""
import requests
import json

def test_health():
    """Test if server is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Root endpoint: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_simple_registration():
    """Test simple registration"""
    user_data = {
        "email": "debug@example.com",
        "password": "debugpass123",
        "first_name": "Debug",
        "last_name": "User",
        "role": "customer"
    }
    
    try:
        response = requests.post("http://localhost:8000/auth/register", json=user_data)
        print(f"Registration: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 201:
            # Try to get more details
            print("Headers:", dict(response.headers))
        
        return response.status_code == 201
    except Exception as e:
        print(f"Registration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Debugging Authentication Issues")
    
    if not test_health():
        print("❌ Server health check failed")
        exit(1)
    
    if not test_root():
        print("❌ Root endpoint failed")
        exit(1)
    
    if not test_simple_registration():
        print("❌ Registration failed")
        exit(1)
    
    print("✅ All debug tests passed")
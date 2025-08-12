#!/usr/bin/env python3
"""
Simple authentication tests using requests
"""
import requests
import json
import time
import sys

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test_user_e2e@example.com"
TEST_PASSWORD = "testpassword123"

def test_user_registration():
    """Test user registration"""
    print("🧪 Testing User Registration...")
    
    # Test data
    user_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "role": "customer"
    }
    
    # Make registration request
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == TEST_EMAIL
        print("✅ Registration test PASSED")
        return data
    else:
        print("❌ Registration test FAILED")
        return None

def test_user_login():
    """Test user login"""
    print("\n🧪 Testing User Login...")
    
    # Login data
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    # Make login request
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == TEST_EMAIL
        print("✅ Login test PASSED")
        return data
    else:
        print("❌ Login test FAILED")
        return None

def test_login_wrong_password():
    """Test login with wrong password"""
    print("\n🧪 Testing Login with Wrong Password...")
    
    # Login data with wrong password
    login_data = {
        "email": TEST_EMAIL,
        "password": "wrongpassword"
    }
    
    # Make login request
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 401:
        print("✅ Wrong password test PASSED")
        return True
    else:
        print("❌ Wrong password test FAILED")
        return False

def test_login_nonexistent_user():
    """Test login with non-existent user"""
    print("\n🧪 Testing Login with Non-existent User...")
    
    # Login data for non-existent user
    login_data = {
        "email": "nonexistent@example.com",
        "password": "somepassword"
    }
    
    # Make login request
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 401:
        print("✅ Non-existent user test PASSED")
        return True
    else:
        print("❌ Non-existent user test FAILED")
        return False

def test_protected_endpoint(access_token):
    """Test accessing protected endpoint"""
    print("\n🧪 Testing Protected Endpoint Access...")
    
    # Headers with authorization
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Make request to protected endpoint
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        assert data["email"] == TEST_EMAIL
        print("✅ Protected endpoint test PASSED")
        return True
    else:
        print("❌ Protected endpoint test FAILED")
        return False

def test_token_refresh(refresh_token):
    """Test token refresh"""
    print("\n🧪 Testing Token Refresh...")
    
    # Refresh data
    refresh_data = {
        "refresh_token": refresh_token
    }
    
    # Make refresh request
    response = requests.post(f"{BASE_URL}/auth/refresh", json=refresh_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        print("✅ Token refresh test PASSED")
        return data
    else:
        print("❌ Token refresh test FAILED")
        return None

def test_duplicate_registration():
    """Test duplicate email registration"""
    print("\n🧪 Testing Duplicate Email Registration...")
    
    # Same user data as before
    user_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "role": "customer"
    }
    
    # Make registration request
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 400:
        print("✅ Duplicate registration test PASSED")
        return True
    else:
        print("❌ Duplicate registration test FAILED")
        return False

def cleanup_test_user():
    """Clean up test user (if possible)"""
    print("\n🧹 Cleaning up test user...")
    # This would require admin access or a cleanup endpoint
    # For now, we'll just note that cleanup should be done
    print("Note: Test user should be cleaned up manually if needed")

def main():
    """Run all authentication tests"""
    print("🚀 Starting Authentication E2E Tests")
    print(f"Testing against: {BASE_URL}")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not healthy")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Server is not running or not accessible")
        print("Please start the backend server first:")
        print("cd backend && python3 main.py")
        sys.exit(1)
    
    print("✅ Server is running")
    
    # Run tests
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Registration
    total_tests += 1
    registration_data = test_user_registration()
    if registration_data:
        tests_passed += 1
        access_token = registration_data["access_token"]
        refresh_token = registration_data["refresh_token"]
    else:
        print("❌ Cannot continue without successful registration")
        sys.exit(1)
    
    # Test 2: Login
    total_tests += 1
    login_data = test_user_login()
    if login_data:
        tests_passed += 1
        # Update tokens from login
        access_token = login_data["access_token"]
        refresh_token = login_data["refresh_token"]
    
    # Test 3: Wrong password
    total_tests += 1
    if test_login_wrong_password():
        tests_passed += 1
    
    # Test 4: Non-existent user
    total_tests += 1
    if test_login_nonexistent_user():
        tests_passed += 1
    
    # Test 5: Protected endpoint
    total_tests += 1
    if test_protected_endpoint(access_token):
        tests_passed += 1
    
    # Test 6: Token refresh
    total_tests += 1
    refresh_data = test_token_refresh(refresh_token)
    if refresh_data:
        tests_passed += 1
    
    # Test 7: Duplicate registration
    total_tests += 1
    if test_duplicate_registration():
        tests_passed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests PASSED!")
        cleanup_test_user()
        sys.exit(0)
    else:
        print(f"❌ {total_tests - tests_passed} tests FAILED!")
        cleanup_test_user()
        sys.exit(1)

if __name__ == "__main__":
    main()
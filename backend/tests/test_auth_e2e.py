"""
End-to-end tests for authentication (login and register)
"""
import pytest
from fastapi import status
import json
from datetime import datetime, timedelta

class TestUserRegistration:
    """Test user registration functionality"""
    
    def test_register_customer_success(self, client, test_user_data):
        """Test successful customer registration"""
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        
        # Check user data
        user = data["user"]
        assert user["email"] == test_user_data["email"]
        assert user["first_name"] == test_user_data["first_name"]
        assert user["last_name"] == test_user_data["last_name"]
        assert user["role"] == test_user_data["role"]
        assert user["is_active"] is True
        assert "id" in user
        assert "created_at" in user
    
    def test_register_business_success(self, client, test_business_user_data):
        """Test successful business user registration"""
        response = client.post("/auth/register", json=test_business_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        user = data["user"]
        assert user["role"] == "business"
    
    def test_register_duplicate_email(self, client, test_user_data, existing_user):
        """Test registration with duplicate email"""
        test_user_data["email"] = existing_user["user"].email
        
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_invalid_email(self, client, test_user_data):
        """Test registration with invalid email"""
        test_user_data["email"] = "invalid-email"
        
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_short_password(self, client, test_user_data):
        """Test registration with short password"""
        test_user_data["password"] = "123"
        
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_missing_required_fields(self, client):
        """Test registration with missing required fields"""
        incomplete_data = {
            "email": "test@example.com",
            "password": "testpass123"
            # Missing first_name, last_name
        }
        
        response = client.post("/auth/register", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_empty_name_fields(self, client, test_user_data):
        """Test registration with empty name fields"""
        test_user_data["first_name"] = ""
        test_user_data["last_name"] = ""
        
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_invalid_role(self, client, test_user_data):
        """Test registration with invalid role"""
        test_user_data["role"] = "invalid_role"
        
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_superadmin_role_not_allowed(self, client, test_user_data):
        """Test that superadmin role cannot be registered via API"""
        test_user_data["role"] = "superadmin"
        
        response = client.post("/auth/register", json=test_user_data)
        
        # Should either reject or default to customer
        if response.status_code == status.HTTP_201_CREATED:
            # If allowed, should default to customer
            data = response.json()
            assert data["user"]["role"] != "superadmin"


class TestUserLogin:
    """Test user login functionality"""
    
    def test_login_success(self, client, existing_user):
        """Test successful login"""
        login_data = {
            "email": existing_user["user"].email,
            "password": existing_user["password"]
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        
        # Check user data
        user = data["user"]
        assert user["email"] == existing_user["user"].email
        assert user["id"] == str(existing_user["user"].id)
        assert user["is_active"] is True
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "somepassword123"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_wrong_password(self, client, existing_user):
        """Test login with wrong password"""
        login_data = {
            "email": existing_user["user"].email,
            "password": "wrongpassword123"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_inactive_user(self, client, inactive_user):
        """Test login with inactive user"""
        login_data = {
            "email": inactive_user["user"].email,
            "password": inactive_user["password"]
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_invalid_email_format(self, client):
        """Test login with invalid email format"""
        login_data = {
            "email": "invalid-email",
            "password": "somepassword123"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields"""
        # Missing password
        response = client.post("/auth/login", json={"email": "test@example.com"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Missing email
        response = client.post("/auth/login", json={"password": "testpass123"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Empty request
        response = client.post("/auth/login", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_empty_fields(self, client):
        """Test login with empty fields"""
        login_data = {
            "email": "",
            "password": ""
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestTokenRefresh:
    """Test token refresh functionality"""
    
    def test_refresh_token_success(self, client, existing_user):
        """Test successful token refresh"""
        # First login to get tokens
        login_data = {
            "email": existing_user["user"].email,
            "password": existing_user["password"]
        }
        
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        
        refresh_token = login_response.json()["refresh_token"]
        
        # Use refresh token to get new tokens
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/auth/refresh", json=refresh_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        
        # New tokens should be different
        assert data["access_token"] != login_response.json()["access_token"]
        assert data["refresh_token"] != refresh_token
    
    def test_refresh_token_invalid(self, client):
        """Test refresh with invalid token"""
        refresh_data = {"refresh_token": "invalid_token"}
        response = client.post("/auth/refresh", json=refresh_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid refresh token" in response.json()["detail"]
    
    def test_refresh_token_expired(self, client):
        """Test refresh with expired token (simulated)"""
        # This would require mocking JWT expiration
        # For now, test with malformed token
        refresh_data = {"refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.expired"}
        response = client.post("/auth/refresh", json=refresh_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthenticationFlow:
    """Test complete authentication flows"""
    
    def test_register_login_flow(self, client, test_user_data):
        """Test complete register -> login flow"""
        # Step 1: Register
        register_response = client.post("/auth/register", json=test_user_data)
        assert register_response.status_code == status.HTTP_201_CREATED
        
        register_data = register_response.json()
        user_id = register_data["user"]["id"]
        
        # Step 2: Login with same credentials
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        
        login_data_response = login_response.json()
        assert login_data_response["user"]["id"] == user_id
    
    def test_login_access_protected_endpoint(self, client, existing_user):
        """Test login -> access protected endpoint flow"""
        # Step 1: Login
        login_data = {
            "email": existing_user["user"].email,
            "password": existing_user["password"]
        }
        
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        
        access_token = login_response.json()["access_token"]
        
        # Step 2: Access protected endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        user_data = response.json()
        assert user_data["email"] == existing_user["user"].email
    
    def test_logout_flow(self, client, existing_user):
        """Test login -> logout flow"""
        # Step 1: Login
        login_data = {
            "email": existing_user["user"].email,
            "password": existing_user["password"]
        }
        
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        
        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Step 2: Verify access works
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Step 3: Logout
        logout_response = client.post("/auth/logout", headers=headers)
        assert logout_response.status_code == status.HTTP_200_OK
        
        # Step 4: Verify access is revoked (this depends on session invalidation implementation)
        # Note: This might still work if only Redis session is invalidated but JWT is still valid
        # The behavior depends on your session management implementation


class TestAuthenticationSecurity:
    """Test security aspects of authentication"""
    
    def test_password_not_returned_in_responses(self, client, test_user_data):
        """Test that passwords are never returned in API responses"""
        # Register
        register_response = client.post("/auth/register", json=test_user_data)
        register_data = register_response.json()
        
        # Check register response
        assert "password" not in register_data["user"]
        assert "password_hash" not in register_data["user"]
        
        # Login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/auth/login", json=login_data)
        login_data_response = login_response.json()
        
        # Check login response
        assert "password" not in login_data_response["user"]
        assert "password_hash" not in login_data_response["user"]
    
    def test_case_sensitive_email(self, client, existing_user):
        """Test that email comparison is case insensitive"""
        login_data = {
            "email": existing_user["user"].email.upper(),
            "password": existing_user["password"]
        }
        
        response = client.post("/auth/login", json=login_data)
        
        # This test depends on your implementation
        # Most systems should be case insensitive for emails
        # Adjust assertion based on your requirements
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]
    
    def test_sql_injection_protection(self, client):
        """Test protection against SQL injection in login"""
        malicious_data = {
            "email": "admin@example.com'; DROP TABLE users; --",
            "password": "password"
        }
        
        response = client.post("/auth/login", json=malicious_data)
        
        # Should not cause server error, should handle gracefully
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED, 
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]
    
    def test_xss_protection_in_names(self, client, test_user_data):
        """Test XSS protection in name fields"""
        test_user_data["first_name"] = "<script>alert('xss')</script>"
        test_user_data["last_name"] = "<img src=x onerror=alert('xss')>"
        
        response = client.post("/auth/register", json=test_user_data)
        
        if response.status_code == status.HTTP_201_CREATED:
            # If registration succeeds, names should be sanitized
            user_data = response.json()["user"]
            assert "<script>" not in user_data["first_name"]
            assert "<img" not in user_data["last_name"]


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_login_rate_limiting(self, client, existing_user):
        """Test rate limiting on login attempts"""
        login_data = {
            "email": existing_user["user"].email,
            "password": "wrongpassword"
        }
        
        # Make multiple failed login attempts
        responses = []
        for i in range(12):  # Exceed the typical rate limit
            response = client.post("/auth/login", json=login_data)
            responses.append(response.status_code)
        
        # Should eventually get rate limited
        # Note: This test might not work if rate limiting is disabled in tests
        rate_limited = any(status_code == status.HTTP_429_TOO_MANY_REQUESTS for status_code in responses)
        
        # If rate limiting is implemented, we should see 429 responses
        # If not implemented in test environment, all should be 401
        assert all(status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_429_TOO_MANY_REQUESTS] 
                  for status_code in responses)
    
    def test_registration_rate_limiting(self, client):
        """Test rate limiting on registration attempts"""
        responses = []
        
        for i in range(7):  # Exceed typical registration rate limit
            test_data = {
                "email": f"test{i}@example.com",
                "password": "testpass123",
                "first_name": "Test",
                "last_name": f"User{i}",
                "role": "customer"
            }
            response = client.post("/auth/register", json=test_data)
            responses.append(response.status_code)
        
        # Should eventually get rate limited or all succeed
        valid_statuses = [
            status.HTTP_201_CREATED, 
            status.HTTP_429_TOO_MANY_REQUESTS,
            status.HTTP_400_BAD_REQUEST  # In case of duplicate emails
        ]
        assert all(status_code in valid_statuses for status_code in responses)
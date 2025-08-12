"""
Authentication tests for modular structure
"""
import pytest
from fastapi import status


@pytest.mark.integration
class TestAuthenticationModular:
    """Test authentication with new modular structure"""
    
    def test_register_success(self, client, test_user_data):
        """Test successful user registration"""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        
        # Check user data
        user = data["user"]
        assert user["email"] == test_user_data["email"]
        assert user["first_name"] == test_user_data["first_name"]
        assert user["role"] == test_user_data["role"]
    
    def test_login_success(self, client, existing_user):
        """Test successful login"""
        login_data = {
            "email": existing_user["user"].email,
            "password": existing_user["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert data["user"]["email"] == existing_user["user"].email
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_protected_endpoint(self, client, existing_user):
        """Test accessing protected endpoint"""
        # First login
        login_data = {
            "email": existing_user["user"].email,
            "password": existing_user["password"]
        }
        
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        
        access_token = login_response.json()["access_token"]
        
        # Access protected endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert user_data["email"] == existing_user["user"].email
    
    def test_duplicate_registration(self, client, test_user_data, existing_user):
        """Test registration with duplicate email"""
        test_user_data["email"] = existing_user["user"].email
        
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_health_endpoint(self, client):
        """Test health endpoint"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
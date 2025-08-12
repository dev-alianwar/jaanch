"""
End-to-end tests for authentication flow
"""
import pytest
import requests
from fastapi import status


@pytest.mark.e2e
class TestAuthenticationFlow:
    """Test complete authentication workflows"""
    
    def test_complete_registration_login_flow(self, server_url, e2e_session, e2e_user_data):
        """Test complete registration -> login -> protected access flow"""
        
        # Step 1: Register user
        register_response = e2e_session.post(
            f"{server_url}/api/v1/auth/register",
            json=e2e_user_data
        )
        
        # Fallback to old API structure if new one fails
        if register_response.status_code == 404:
            register_response = e2e_session.post(
                f"{server_url}/auth/register",
                json=e2e_user_data
            )
        
        assert register_response.status_code == status.HTTP_201_CREATED
        
        register_data = register_response.json()
        assert "user" in register_data
        assert "access_token" in register_data
        assert register_data["user"]["email"] == e2e_user_data["email"]
        
        # Step 2: Login with same credentials
        login_data = {
            "email": e2e_user_data["email"],
            "password": e2e_user_data["password"]
        }
        
        login_response = e2e_session.post(
            f"{server_url}/api/v1/auth/login",
            json=login_data
        )
        
        # Fallback to old API structure if new one fails
        if login_response.status_code == 404:
            login_response = e2e_session.post(
                f"{server_url}/auth/login",
                json=login_data
            )
        
        assert login_response.status_code == status.HTTP_200_OK
        
        login_response_data = login_response.json()
        assert login_response_data["user"]["email"] == e2e_user_data["email"]
        
        # Step 3: Access protected endpoint
        access_token = login_response_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        me_response = e2e_session.get(
            f"{server_url}/api/v1/auth/me",
            headers=headers
        )
        
        # Fallback to old API structure if new one fails
        if me_response.status_code == 404:
            me_response = e2e_session.get(
                f"{server_url}/auth/me",
                headers=headers
            )
        
        assert me_response.status_code == status.HTTP_200_OK
        
        me_data = me_response.json()
        assert me_data["email"] == e2e_user_data["email"]
    
    def test_token_refresh_flow(self, server_url, e2e_session, e2e_user_data):
        """Test token refresh workflow"""
        
        # Step 1: Register user
        register_response = e2e_session.post(
            f"{server_url}/api/v1/auth/register",
            json=e2e_user_data
        )
        
        if register_response.status_code == 404:
            register_response = e2e_session.post(
                f"{server_url}/auth/register",
                json=e2e_user_data
            )
        
        assert register_response.status_code == status.HTTP_201_CREATED
        
        register_data = register_response.json()
        original_refresh_token = register_data["refresh_token"]
        
        # Step 2: Use refresh token to get new tokens
        refresh_data = {"refresh_token": original_refresh_token}
        
        refresh_response = e2e_session.post(
            f"{server_url}/api/v1/auth/refresh",
            json=refresh_data
        )
        
        if refresh_response.status_code == 404:
            refresh_response = e2e_session.post(
                f"{server_url}/auth/refresh",
                json=refresh_data
            )
        
        assert refresh_response.status_code == status.HTTP_200_OK
        
        refresh_response_data = refresh_response.json()
        assert "access_token" in refresh_response_data
        assert "refresh_token" in refresh_response_data
        
        # New tokens should be different
        assert refresh_response_data["access_token"] != register_data["access_token"]
        assert refresh_response_data["refresh_token"] != original_refresh_token
        
        # Step 3: Use new access token
        new_access_token = refresh_response_data["access_token"]
        headers = {"Authorization": f"Bearer {new_access_token}"}
        
        me_response = e2e_session.get(
            f"{server_url}/api/v1/auth/me",
            headers=headers
        )
        
        if me_response.status_code == 404:
            me_response = e2e_session.get(
                f"{server_url}/auth/me",
                headers=headers
            )
        
        assert me_response.status_code == status.HTTP_200_OK
    
    def test_logout_flow(self, server_url, e2e_session, e2e_user_data):
        """Test logout workflow"""
        
        # Step 1: Register and login
        register_response = e2e_session.post(
            f"{server_url}/api/v1/auth/register",
            json=e2e_user_data
        )
        
        if register_response.status_code == 404:
            register_response = e2e_session.post(
                f"{server_url}/auth/register",
                json=e2e_user_data
            )
        
        assert register_response.status_code == status.HTTP_201_CREATED
        
        register_data = register_response.json()
        access_token = register_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Step 2: Verify access works
        me_response = e2e_session.get(
            f"{server_url}/api/v1/auth/me",
            headers=headers
        )
        
        if me_response.status_code == 404:
            me_response = e2e_session.get(
                f"{server_url}/auth/me",
                headers=headers
            )
        
        assert me_response.status_code == status.HTTP_200_OK
        
        # Step 3: Logout
        logout_response = e2e_session.post(
            f"{server_url}/api/v1/auth/logout",
            headers=headers
        )
        
        if logout_response.status_code == 404:
            logout_response = e2e_session.post(
                f"{server_url}/auth/logout",
                headers=headers
            )
        
        assert logout_response.status_code == status.HTTP_200_OK
    
    def test_invalid_credentials_flow(self, server_url, e2e_session):
        """Test various invalid credential scenarios"""
        
        # Test 1: Login with non-existent user
        login_data = {
            "email": "nonexistent@example.com",
            "password": "somepassword123"
        }
        
        login_response = e2e_session.post(
            f"{server_url}/api/v1/auth/login",
            json=login_data
        )
        
        if login_response.status_code == 404:
            login_response = e2e_session.post(
                f"{server_url}/auth/login",
                json=login_data
            )
        
        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Test 2: Access protected endpoint without token
        me_response = e2e_session.get(f"{server_url}/api/v1/auth/me")
        
        if me_response.status_code == 404:
            me_response = e2e_session.get(f"{server_url}/auth/me")
        
        assert me_response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Test 3: Access protected endpoint with invalid token
        headers = {"Authorization": "Bearer invalid.token.here"}
        
        me_response_invalid = e2e_session.get(
            f"{server_url}/api/v1/auth/me",
            headers=headers
        )
        
        if me_response_invalid.status_code == 404:
            me_response_invalid = e2e_session.get(
                f"{server_url}/auth/me",
                headers=headers
            )
        
        assert me_response_invalid.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_duplicate_registration(self, server_url, e2e_session, e2e_user_data):
        """Test duplicate email registration"""
        
        # Step 1: Register user first time
        register_response1 = e2e_session.post(
            f"{server_url}/api/v1/auth/register",
            json=e2e_user_data
        )
        
        if register_response1.status_code == 404:
            register_response1 = e2e_session.post(
                f"{server_url}/auth/register",
                json=e2e_user_data
            )
        
        assert register_response1.status_code == status.HTTP_201_CREATED
        
        # Step 2: Try to register same email again
        register_response2 = e2e_session.post(
            f"{server_url}/api/v1/auth/register",
            json=e2e_user_data
        )
        
        if register_response2.status_code == 404:
            register_response2 = e2e_session.post(
                f"{server_url}/auth/register",
                json=e2e_user_data
            )
        
        assert register_response2.status_code == status.HTTP_400_BAD_REQUEST
        
        error_data = register_response2.json()
        assert "already registered" in error_data.get("detail", "").lower() or \
               "already registered" in str(error_data).lower()


@pytest.mark.e2e
class TestAPIHealthAndStatus:
    """Test API health and status endpoints"""
    
    def test_health_endpoint(self, server_url, e2e_session):
        """Test health check endpoint"""
        response = e2e_session.get(f"{server_url}/health")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self, server_url, e2e_session):
        """Test root endpoint"""
        response = e2e_session.get(f"{server_url}/")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_api_documentation(self, server_url, e2e_session):
        """Test API documentation endpoints"""
        # Test OpenAPI schema
        docs_response = e2e_session.get(f"{server_url}/openapi.json")
        assert docs_response.status_code == status.HTTP_200_OK
        
        # Test Swagger UI (should return HTML)
        swagger_response = e2e_session.get(f"{server_url}/docs")
        assert swagger_response.status_code == status.HTTP_200_OK
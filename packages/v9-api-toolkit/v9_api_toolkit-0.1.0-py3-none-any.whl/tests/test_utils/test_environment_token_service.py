import pytest
from unittest.mock import MagicMock, patch
import requests
from datetime import datetime, timedelta
from v9_api_toolkit.utils.environment_token_service import (
    get_access_token,
    refresh_access_token,
    is_token_valid
)

class TestEnvironmentTokenService:
    """Tests for the environment_token_service module."""
    
    def test_get_access_token(self):
        """Test get_access_token function."""
        # Mock the requests.post method
        with patch('requests.post') as mock_post:
            # Set up the mock response
            mock_response = MagicMock()
            mock_response.ok = True
            mock_response.json.return_value = {
                "access_token": "test-token",
                "refresh_token": "test-refresh-token",
                "expires_in": 3600
            }
            mock_post.return_value = mock_response
            
            # Call the function
            result = get_access_token(
                client_id="test-client-id",
                api_url="https://api.example.com",
                username="test-user",
                password="test-password"
            )
            
            # Verify the result
            assert result["access_token"] == "test-token"
            assert result["refresh_token"] == "test-refresh-token"
            assert "expires_at" in result
            assert result["client_identifier"] == "test-client-id"
            
            # Verify the mock was called correctly
            mock_post.assert_called_once_with(
                "https://api.example.com/api/v9/identity/clients/test-client-id/auth/token",
                json={
                    "username": "test-user",
                    "password": "test-password",
                    "grant_type": "password"
                }
            )
            
    def test_get_access_token_error(self):
        """Test get_access_token function with error."""
        # Mock the requests.post method
        with patch('requests.post') as mock_post:
            # Set up the mock response
            mock_response = MagicMock()
            mock_response.ok = False
            mock_response.status_code = 401
            mock_response.text = "Unauthorized"
            mock_response.json.side_effect = ValueError("No JSON")
            mock_post.return_value = mock_response
            
            # Call the function and expect an exception
            with pytest.raises(Exception) as excinfo:
                get_access_token(
                    client_id="test-client-id",
                    api_url="https://api.example.com",
                    username="test-user",
                    password="test-password"
                )
            
            # Verify the exception message
            assert "Failed to get token: 401" in str(excinfo.value)
            
    def test_refresh_access_token(self):
        """Test refresh_access_token function."""
        # Mock the requests.post method
        with patch('requests.post') as mock_post:
            # Set up the mock response
            mock_response = MagicMock()
            mock_response.ok = True
            mock_response.json.return_value = {
                "access_token": "new-test-token",
                "refresh_token": "new-test-refresh-token",
                "expires_in": 3600
            }
            mock_post.return_value = mock_response
            
            # Call the function
            result = refresh_access_token(
                client_id="test-client-id",
                api_url="https://api.example.com",
                refresh_token="test-refresh-token"
            )
            
            # Verify the result
            assert result["access_token"] == "new-test-token"
            assert result["refresh_token"] == "new-test-refresh-token"
            assert "expires_at" in result
            assert result["client_identifier"] == "test-client-id"
            
            # Verify the mock was called correctly
            mock_post.assert_called_once_with(
                "https://api.example.com/api/v9/identity/clients/test-client-id/auth/token",
                json={
                    "refresh_token": "test-refresh-token",
                    "grant_type": "refresh_token"
                }
            )
            
    def test_refresh_access_token_error(self):
        """Test refresh_access_token function with error."""
        # Mock the requests.post method
        with patch('requests.post') as mock_post:
            # Set up the mock response
            mock_response = MagicMock()
            mock_response.ok = False
            mock_response.status_code = 401
            mock_response.text = "Invalid refresh token"
            mock_response.json.side_effect = ValueError("No JSON")
            mock_post.return_value = mock_response
            
            # Call the function and expect an exception
            with pytest.raises(Exception) as excinfo:
                refresh_access_token(
                    client_id="test-client-id",
                    api_url="https://api.example.com",
                    refresh_token="test-refresh-token"
                )
            
            # Verify the exception message
            assert "Failed to refresh token: 401" in str(excinfo.value)
            
    def test_is_token_valid(self):
        """Test is_token_valid function."""
        # Create token data with future expiration
        future_expires_at = (datetime.utcnow() + timedelta(hours=1)).isoformat()
        token_data = {
            "access_token": "test-token",
            "refresh_token": "test-refresh-token",
            "expires_at": future_expires_at,
            "client_identifier": "test-client-id"
        }
        
        # Call the function
        result = is_token_valid(token_data)
        
        # Verify the result
        assert result is True
        
        # Create token data with past expiration
        past_expires_at = (datetime.utcnow() - timedelta(hours=1)).isoformat()
        token_data = {
            "access_token": "test-token",
            "refresh_token": "test-refresh-token",
            "expires_at": past_expires_at,
            "client_identifier": "test-client-id"
        }
        
        # Call the function
        result = is_token_valid(token_data)
        
        # Verify the result
        assert result is False
        
        # Create token data with invalid expiration
        token_data = {
            "access_token": "test-token",
            "refresh_token": "test-refresh-token",
            "expires_at": "invalid-date",
            "client_identifier": "test-client-id"
        }
        
        # Call the function
        result = is_token_valid(token_data)
        
        # Verify the result
        assert result is False

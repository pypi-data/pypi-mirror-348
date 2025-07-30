from datetime import datetime, timedelta
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def get_access_token(client_id: str, api_url: str, username: str, password: str) -> Dict[str, Any]:
    """
    Get an access token from the V9 API.
    
    Args:
        client_id: The client identifier
        api_url: The API URL
        username: The username for authentication
        password: The password for authentication
        
    Returns:
        A dictionary containing the access token, refresh token, and expiration time
    """
    endpoint = f"{api_url}/api/v9/identity/clients/{client_id}/auth/token"
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        if not response.ok:
            error_msg = f"Failed to get token: {response.status_code}"
            try:
                error_details = response.json()
                error_msg += f", details: {error_details}"
            except:
                error_msg += f", response: {response.text[:200]}"
                
            logger.error(error_msg)
            raise Exception(error_msg)
            
        data = response.json()
        expires_at = (datetime.utcnow() + timedelta(seconds=data.get("expires_in", 10800))).isoformat()
        
        return {
            "access_token": data["access_token"],
            "refresh_token": data.get("refresh_token"),
            "expires_at": expires_at,
            "client_identifier": client_id
        }
    except requests.RequestException as e:
        logger.error(f"Request error during token acquisition: {str(e)}")
        raise Exception(f"Request error during token acquisition: {str(e)}")

def refresh_access_token(client_id: str, api_url: str, refresh_token: str) -> Dict[str, Any]:
    """
    Refresh an access token using a refresh token.
    
    Args:
        client_id: The client identifier
        api_url: The API URL
        refresh_token: The refresh token
        
    Returns:
        A dictionary containing the new access token, refresh token, and expiration time
    """
    endpoint = f"{api_url}/api/v9/identity/clients/{client_id}/auth/token"
    payload = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        if not response.ok:
            error_msg = f"Failed to refresh token: {response.status_code}"
            try:
                error_details = response.json()
                error_msg += f", details: {error_details}"
            except:
                error_msg += f", response: {response.text[:200]}"
                
            logger.error(error_msg)
            raise Exception(error_msg)
            
        data = response.json()
        expires_at = (datetime.utcnow() + timedelta(seconds=data.get("expires_in", 10800))).isoformat()
        
        return {
            "access_token": data["access_token"],
            "refresh_token": data.get("refresh_token", refresh_token),
            "expires_at": expires_at,
            "client_identifier": client_id
        }
    except requests.RequestException as e:
        logger.error(f"Request error during token refresh: {str(e)}")
        raise Exception(f"Request error during token refresh: {str(e)}")

def is_token_valid(token_data: Dict[str, Any]) -> bool:
    """
    Check if a token is still valid.
    
    Args:
        token_data: The token data containing the expiration time
        
    Returns:
        True if the token is still valid, False otherwise
    """
    try:
        expires_at = datetime.fromisoformat(token_data["expires_at"])
        now = datetime.utcnow()
        
        # Add a buffer of 5 minutes to avoid edge cases
        return expires_at > now + timedelta(minutes=5)
    except Exception as e:
        logger.error(f"Error checking token validity: {str(e)}")
        return False

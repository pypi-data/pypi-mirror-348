import pytest
from unittest.mock import MagicMock, patch
from v9_api_toolkit.api.v9_api_service import V9ApiService

@pytest.fixture
def mock_config():
    """Fixture for mock configuration."""
    return {
        "api_url": "https://api.example.com",
        "client_identifier": "test-client-id",
        "username": "test-user",
        "password": "test-password"
    }

@pytest.fixture
def mock_token():
    """Fixture for mock token."""
    return "mock-token-12345"

@pytest.fixture
def mock_api_service(mock_config, mock_token):
    """Fixture for mock API service."""
    with patch('v9_api_toolkit.api.v9_api_service.V9ApiService._get_token', return_value=mock_token):
        api_service = V9ApiService(mock_config, user_email="test@example.com")
        
        # Replace the _make_request method with a mock
        api_service._make_request = MagicMock()
        
        return api_service

@pytest.fixture
def mock_site_data():
    """Fixture for mock site data."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "fid": "site-123",
                    "name": "Test Site",
                    "typeCode": "site-outline",
                    "extra": {
                        "description": "Test site description"
                    }
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [0, 0],
                            [0, 1],
                            [1, 1],
                            [1, 0],
                            [0, 0]
                        ]
                    ]
                }
            }
        ]
    }

@pytest.fixture
def mock_building_data():
    """Fixture for mock building data."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "fid": "building-123",
                    "name": "Test Building",
                    "typeCode": "building-outline",
                    "sid": "site-123",
                    "buildingType": "office",
                    "extra": {
                        "floors": 5,
                        "area": 10000
                    }
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [0.1, 0.1],
                            [0.1, 0.9],
                            [0.9, 0.9],
                            [0.9, 0.1],
                            [0.1, 0.1]
                        ]
                    ]
                }
            }
        ]
    }

@pytest.fixture
def mock_level_data():
    """Fixture for mock level data."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "fid": "level-123",
                    "name": "Floor 1",
                    "typeCode": "level",
                    "floorNumber": 1,
                    "extra": {
                        "height": 3.5
                    }
                },
                "geometry": None
            }
        ]
    }

@pytest.fixture
def mock_client_data():
    """Fixture for mock client data."""
    return {
        "identifier": "test-client-id",
        "name": "Test Client",
        "extra": {
            "industry": "Technology",
            "region": "North America"
        }
    }

@pytest.fixture
def mock_sdk_config_data():
    """Fixture for mock SDK configuration data."""
    return [
        {
            "key": "config1",
            "value": "value1"
        },
        {
            "key": "config2",
            "value": True
        },
        {
            "key": "config3",
            "value": {
                "nestedKey": "nestedValue"
            }
        }
    ]

@pytest.fixture
def mock_create_response():
    """Fixture for mock create response."""
    return {
        "fid": "new-entity-123"
    }

import pytest
from v9_api_toolkit.dto.client_metadata_dto import ClientMetadataDTO
from v9_api_toolkit.dto.validation import ValidationError

class TestClientMetadataDTO:
    """Tests for the ClientMetadataDTO class."""
    
    def test_init(self):
        """Test initialization of ClientMetadataDTO."""
        client = ClientMetadataDTO(
            identifier="client-123",
            name="Test Client",
            extraData={"industry": "Technology"}
        )
        
        assert client.identifier == "client-123"
        assert client.name == "Test Client"
        assert client.extraData == {"industry": "Technology"}
        
    def test_from_api_json(self):
        """Test from_api_json method."""
        data = {
            "identifier": "client-123",
            "name": "Test Client",
            "extra": {
                "industry": "Technology",
                "region": "North America"
            }
        }
        
        client = ClientMetadataDTO.from_api_json(data)
        
        assert client.identifier == "client-123"
        assert client.name == "Test Client"
        assert client.extraData == {"industry": "Technology", "region": "North America"}
        
    def test_from_api_json_missing_required_field(self):
        """Test from_api_json method with missing required field."""
        data = {
            "identifier": "client-123",
            # Missing name
        }
        
        with pytest.raises(ValidationError) as excinfo:
            ClientMetadataDTO.from_api_json(data)
        
        assert "Missing required field: name" in str(excinfo.value)
        
    def test_to_api_json(self):
        """Test to_api_json method."""
        client = ClientMetadataDTO(
            identifier="client-123",
            name="Test Client",
            extraData={"industry": "Technology"}
        )
        
        result = client.to_api_json()
        
        assert result["identifier"] == "client-123"
        assert result["name"] == "Test Client"
        assert result["extra"] == {"industry": "Technology"}

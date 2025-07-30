import pytest
from v9_api_toolkit.dto.create_response_dto import CreateResponseDTO
from v9_api_toolkit.dto.validation import ValidationError

class TestCreateResponseDTO:
    """Tests for the CreateResponseDTO class."""
    
    def test_init(self):
        """Test initialization of CreateResponseDTO."""
        response = CreateResponseDTO(fid="entity-123")
        
        assert response.fid == "entity-123"
        
    def test_from_api_json_direct_fid(self):
        """Test from_api_json method with direct FID."""
        data = {
            "fid": "entity-123"
        }
        
        response = CreateResponseDTO.from_api_json(data)
        
        assert response.fid == "entity-123"
        
    def test_from_api_json_feature_collection(self):
        """Test from_api_json method with feature collection."""
        data = {
            "features": [
                {
                    "properties": {
                        "fid": "entity-123"
                    }
                }
            ]
        }
        
        response = CreateResponseDTO.from_api_json(data)
        
        assert response.fid == "entity-123"
        
    def test_from_api_json_no_fid(self):
        """Test from_api_json method with no FID."""
        data = {
            "features": [
                {
                    "properties": {
                        # No FID
                    }
                }
            ]
        }
        
        with pytest.raises(ValidationError) as excinfo:
            CreateResponseDTO.from_api_json(data)
        
        assert "No FID found in create response" in str(excinfo.value)

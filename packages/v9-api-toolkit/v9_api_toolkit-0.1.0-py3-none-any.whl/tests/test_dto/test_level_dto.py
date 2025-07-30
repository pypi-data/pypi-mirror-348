import pytest
from v9_api_toolkit.dto.level_dto import LevelDTO
from v9_api_toolkit.dto.validation import ValidationError

class TestLevelDTO:
    """Tests for the LevelDTO class."""
    
    def test_init(self):
        """Test initialization of LevelDTO."""
        level = LevelDTO(
            fid="level-123",
            name="Floor 1",
            typeCode="level",
            extraData={"height": 3.5}
        )
        
        assert level.fid == "level-123"
        assert level.name == "Floor 1"
        assert level.typeCode == "level"
        assert level.extraData == {"height": 3.5}
        assert level.floorNumber is None
        
    def test_from_api_json(self):
        """Test from_api_json method."""
        data = {
            "fid": "level-123",
            "name": "Floor 1",
            "typeCode": "level",
            "floorNumber": 1,
            "extra": {
                "height": 3.5
            }
        }
        
        level = LevelDTO.from_api_json(data)
        
        assert level.fid == "level-123"
        assert level.name == "Floor 1"
        assert level.typeCode == "level"
        assert level.floorNumber == 1
        assert level.extraData == {"height": 3.5}
        
    def test_from_api_json_missing_required_field(self):
        """Test from_api_json method with missing required field."""
        data = {
            "fid": "level-123",
            # Missing name
            "typeCode": "level"
        }
        
        with pytest.raises(ValidationError) as excinfo:
            LevelDTO.from_api_json(data)
        
        assert "Missing required field: name" in str(excinfo.value)
        
    def test_list_from_api_json_list(self):
        """Test list_from_api_json method with list."""
        data = [
            {
                "fid": "level-123",
                "name": "Floor 1",
                "typeCode": "level",
                "floorNumber": 1
            },
            {
                "fid": "level-456",
                "name": "Floor 2",
                "typeCode": "level",
                "floorNumber": 2
            }
        ]
        
        levels = LevelDTO.list_from_api_json(data)
        
        assert len(levels) == 2
        assert levels[0].fid == "level-123"
        assert levels[0].name == "Floor 1"
        assert levels[0].floorNumber == 1
        assert levels[1].fid == "level-456"
        assert levels[1].name == "Floor 2"
        assert levels[1].floorNumber == 2
        
    def test_list_from_api_json_feature_collection(self):
        """Test list_from_api_json method with feature collection."""
        data = {
            "features": [
                {
                    "properties": {
                        "fid": "level-123",
                        "name": "Floor 1",
                        "typeCode": "level",
                        "floorNumber": 1
                    }
                },
                {
                    "properties": {
                        "fid": "level-456",
                        "name": "Floor 2",
                        "typeCode": "level",
                        "floorNumber": 2
                    }
                }
            ]
        }
        
        levels = LevelDTO.list_from_api_json(data)
        
        assert len(levels) == 2
        assert levels[0].fid == "level-123"
        assert levels[0].name == "Floor 1"
        assert levels[0].floorNumber == 1
        assert levels[1].fid == "level-456"
        assert levels[1].name == "Floor 2"
        assert levels[1].floorNumber == 2
        
    def test_to_api_json(self):
        """Test to_api_json method."""
        level = LevelDTO(
            fid="level-123",
            name="Floor 1",
            typeCode="level",
            extraData={"height": 3.5}
        )
        level.floorNumber = 1
        
        result = level.to_api_json()
        
        assert result["fid"] == "level-123"
        assert result["name"] == "Floor 1"
        assert result["typeCode"] == "level"
        assert result["floorNumber"] == 1
        assert result["extra"] == {"height": 3.5}

import pytest
from v9_api_toolkit.dto.building_dto import BuildingDTO
from v9_api_toolkit.dto.validation import ValidationError

class TestBuildingDTO:
    """Tests for the BuildingDTO class."""
    
    def test_init(self):
        """Test initialization of BuildingDTO."""
        building = BuildingDTO(
            fid="building-123",
            name="Test Building",
            typeCode="building-outline",
            sid="site-123",
            extraData={"floors": 5}
        )
        
        assert building.fid == "building-123"
        assert building.name == "Test Building"
        assert building.typeCode == "building-outline"
        assert building.sid == "site-123"
        assert building.extraData == {"floors": 5}
        assert building.bid is None
        
    def test_from_api_json_feature_collection(self):
        """Test from_api_json method with feature collection."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "building-123",
                        "name": "Test Building",
                        "typeCode": "building-outline",
                        "sid": "site-123",
                        "bid": "bid-123",
                        "extra": {
                            "floors": 5
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
        
        building = BuildingDTO.from_api_json(data)
        
        assert building.fid == "building-123"
        assert building.name == "Test Building"
        assert building.typeCode == "building-outline"
        assert building.sid == "site-123"
        assert building.bid == "bid-123"
        assert building.extraData == {"floors": 5}
        
    def test_from_api_json_direct_properties(self):
        """Test from_api_json method with direct properties."""
        data = {
            "fid": "building-123",
            "name": "Test Building",
            "typeCode": "building-outline",
            "sid": "site-123",
            "bid": "bid-123",
            "extra": {
                "floors": 5
            }
        }
        
        building = BuildingDTO.from_api_json(data)
        
        assert building.fid == "building-123"
        assert building.name == "Test Building"
        assert building.typeCode == "building-outline"
        assert building.sid == "site-123"
        assert building.bid == "bid-123"
        assert building.extraData == {"floors": 5}
        
    def test_from_api_json_missing_required_field(self):
        """Test from_api_json method with missing required field."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "building-123",
                        # Missing name
                        "typeCode": "building-outline",
                        "sid": "site-123"
                    }
                }
            ]
        }
        
        with pytest.raises(ValidationError) as excinfo:
            BuildingDTO.from_api_json(data)
        
        assert "Missing required field: name" in str(excinfo.value)
        
    def test_list_from_api_json_feature_collection(self):
        """Test list_from_api_json method with feature collection."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "building-123",
                        "name": "Test Building 1",
                        "typeCode": "building-outline",
                        "sid": "site-123"
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "building-456",
                        "name": "Test Building 2",
                        "typeCode": "building-outline",
                        "sid": "site-123"
                    }
                }
            ]
        }
        
        buildings = BuildingDTO.list_from_api_json(data)
        
        assert len(buildings) == 2
        assert buildings[0].fid == "building-123"
        assert buildings[0].name == "Test Building 1"
        assert buildings[1].fid == "building-456"
        assert buildings[1].name == "Test Building 2"
        
    def test_to_api_json(self):
        """Test to_api_json method."""
        building = BuildingDTO(
            fid="building-123",
            name="Test Building",
            typeCode="building-outline",
            sid="site-123",
            extraData={"floors": 5}
        )
        building.bid = "bid-123"
        
        result = building.to_api_json()
        
        assert result["type"] == "Feature"
        assert result["properties"]["fid"] == "building-123"
        assert result["properties"]["name"] == "Test Building"
        assert result["properties"]["typeCode"] == "building-outline"
        assert result["properties"]["sid"] == "site-123"
        assert result["properties"]["bid"] == "bid-123"
        assert result["properties"]["extra"] == {"floors": 5}
        assert result["geometry"] is None

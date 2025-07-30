import pytest
from v9_api_toolkit.dto.gps_geofence_dto import GpsGeofenceDTO
from v9_api_toolkit.dto.validation import ValidationError

class TestGpsGeofenceDTO:
    """Tests for the GpsGeofenceDTO class."""
    
    def test_init(self):
        """Test initialization of GpsGeofenceDTO."""
        geofence = GpsGeofenceDTO(
            fid="geofence-123",
            name="Test Geofence",
            typeCode="gps-geofence",
            extraData={"radius": 100}
        )
        
        assert geofence.fid == "geofence-123"
        assert geofence.name == "Test Geofence"
        assert geofence.typeCode == "gps-geofence"
        assert geofence.extraData == {"radius": 100}
        
    def test_from_api_json_feature(self):
        """Test from_api_json method with feature."""
        data = {
            "type": "Feature",
            "properties": {
                "fid": "geofence-123",
                "name": "Test Geofence",
                "typeCode": "gps-geofence",
                "extra": {
                    "radius": 100
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
        
        geofence = GpsGeofenceDTO.from_api_json(data)
        
        assert geofence.fid == "geofence-123"
        assert geofence.name == "Test Geofence"
        assert geofence.typeCode == "gps-geofence"
        assert geofence.extraData == {"radius": 100}
        
    def test_from_api_json_direct_properties(self):
        """Test from_api_json method with direct properties."""
        data = {
            "fid": "geofence-123",
            "name": "Test Geofence",
            "typeCode": "gps-geofence",
            "extra": {
                "radius": 100
            }
        }
        
        geofence = GpsGeofenceDTO.from_api_json(data)
        
        assert geofence.fid == "geofence-123"
        assert geofence.name == "Test Geofence"
        assert geofence.typeCode == "gps-geofence"
        assert geofence.extraData == {"radius": 100}
        
    def test_from_api_json_missing_required_field(self):
        """Test from_api_json method with missing required field."""
        data = {
            "fid": "geofence-123",
            # Missing name
            "typeCode": "gps-geofence"
        }
        
        with pytest.raises(ValidationError) as excinfo:
            GpsGeofenceDTO.from_api_json(data)
        
        assert "Missing required field: name" in str(excinfo.value)
        
    def test_list_from_api_json(self):
        """Test list_from_api_json method."""
        data = [
            {
                "fid": "geofence-123",
                "name": "Test Geofence 1",
                "typeCode": "gps-geofence"
            },
            {
                "fid": "geofence-456",
                "name": "Test Geofence 2",
                "typeCode": "gps-geofence"
            }
        ]
        
        geofences = GpsGeofenceDTO.list_from_api_json(data)
        
        assert len(geofences) == 2
        assert geofences[0].fid == "geofence-123"
        assert geofences[0].name == "Test Geofence 1"
        assert geofences[1].fid == "geofence-456"
        assert geofences[1].name == "Test Geofence 2"
        
    def test_to_api_json(self):
        """Test to_api_json method."""
        geofence = GpsGeofenceDTO(
            fid="geofence-123",
            name="Test Geofence",
            typeCode="gps-geofence",
            extraData={"radius": 100}
        )
        
        result = geofence.to_api_json()
        
        assert result["type"] == "Feature"
        assert result["properties"]["fid"] == "geofence-123"
        assert result["properties"]["name"] == "Test Geofence"
        assert result["properties"]["typeCode"] == "gps-geofence"
        assert result["properties"]["extra"] == {"radius": 100}
        assert result["geometry"] is None

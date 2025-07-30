import pytest
from v9_api_toolkit.dto.site_dto import SiteDTO
from v9_api_toolkit.dto.validation import ValidationError

class TestSiteDTO:
    """Tests for the SiteDTO class."""
    
    def test_init(self):
        """Test initialization of SiteDTO."""
        site = SiteDTO(
            fid="site-123",
            name="Test Site",
            typeCode="site-outline",
            extraData={"description": "Test site description"}
        )
        
        assert site.fid == "site-123"
        assert site.name == "Test Site"
        assert site.typeCode == "site-outline"
        assert site.extraData == {"description": "Test site description"}
        assert site.eid is None
        assert site.sid is None
        
    def test_from_api_json_feature_collection(self):
        """Test from_api_json method with feature collection."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "site-123",
                        "name": "Test Site",
                        "typeCode": "site-outline",
                        "eid": "eid-123",
                        "sid": "sid-123",
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
        
        site = SiteDTO.from_api_json(data)
        
        assert site.fid == "site-123"
        assert site.name == "Test Site"
        assert site.typeCode == "site-outline"
        assert site.eid == "eid-123"
        assert site.sid == "sid-123"
        assert site.extraData == {"description": "Test site description"}
        
    def test_from_api_json_direct_properties(self):
        """Test from_api_json method with direct properties."""
        data = {
            "fid": "site-123",
            "name": "Test Site",
            "typeCode": "site-outline",
            "eid": "eid-123",
            "sid": "sid-123",
            "extra": {
                "description": "Test site description"
            }
        }
        
        site = SiteDTO.from_api_json(data)
        
        assert site.fid == "site-123"
        assert site.name == "Test Site"
        assert site.typeCode == "site-outline"
        assert site.eid == "eid-123"
        assert site.sid == "sid-123"
        assert site.extraData == {"description": "Test site description"}
        
    def test_from_api_json_missing_required_field(self):
        """Test from_api_json method with missing required field."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "site-123",
                        # Missing name
                        "typeCode": "site-outline"
                    }
                }
            ]
        }
        
        with pytest.raises(ValidationError) as excinfo:
            SiteDTO.from_api_json(data)
        
        assert "Missing required field: name" in str(excinfo.value)
        
    def test_list_from_api_json_feature_collection(self):
        """Test list_from_api_json method with feature collection."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "site-123",
                        "name": "Test Site 1",
                        "typeCode": "site-outline"
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "site-456",
                        "name": "Test Site 2",
                        "typeCode": "site-outline"
                    }
                }
            ]
        }
        
        sites = SiteDTO.list_from_api_json(data)
        
        assert len(sites) == 2
        assert sites[0].fid == "site-123"
        assert sites[0].name == "Test Site 1"
        assert sites[1].fid == "site-456"
        assert sites[1].name == "Test Site 2"
        
    def test_to_api_json(self):
        """Test to_api_json method."""
        site = SiteDTO(
            fid="site-123",
            name="Test Site",
            typeCode="site-outline",
            extraData={"description": "Test site description"}
        )
        site.eid = "eid-123"
        site.sid = "sid-123"
        
        result = site.to_api_json()
        
        assert result["type"] == "Feature"
        assert result["properties"]["fid"] == "site-123"
        assert result["properties"]["name"] == "Test Site"
        assert result["properties"]["typeCode"] == "site-outline"
        assert result["properties"]["eid"] == "eid-123"
        assert result["properties"]["sid"] == "sid-123"
        assert result["properties"]["extra"] == {"description": "Test site description"}
        assert result["geometry"] is None

import pytest
from v9_api_toolkit.dto.sdk_configuration_dto import SdkConfigurationDTO
from v9_api_toolkit.dto.validation import ValidationError

class TestSdkConfigurationDTO:
    """Tests for the SdkConfigurationDTO class."""
    
    def test_init(self):
        """Test initialization of SdkConfigurationDTO."""
        config = SdkConfigurationDTO(
            key="config1",
            value="value1",
            scope="global"
        )
        
        assert config.key == "config1"
        assert config.value == "value1"
        assert config.scope == "global"
        assert config.scopeId is None
        
    def test_init_with_scope_id(self):
        """Test initialization of SdkConfigurationDTO with scope ID."""
        config = SdkConfigurationDTO(
            key="config1",
            value="value1",
            scope="site",
            scopeId="site-123"
        )
        
        assert config.key == "config1"
        assert config.value == "value1"
        assert config.scope == "site"
        assert config.scopeId == "site-123"
        
    def test_from_api_json(self):
        """Test from_api_json method."""
        data = {
            "key": "config1",
            "value": "value1"
        }
        
        config = SdkConfigurationDTO.from_api_json(data)
        
        assert config.key == "config1"
        assert config.value == "value1"
        assert config.scope == "global"
        assert config.scopeId is None
        
    def test_from_api_json_with_scope(self):
        """Test from_api_json method with scope."""
        data = {
            "key": "config1",
            "value": "value1"
        }
        
        config = SdkConfigurationDTO.from_api_json(data, scope="site", scopeId="site-123")
        
        assert config.key == "config1"
        assert config.value == "value1"
        assert config.scope == "site"
        assert config.scopeId == "site-123"
        
    def test_from_api_json_missing_required_field(self):
        """Test from_api_json method with missing required field."""
        data = {
            # Missing key
            "value": "value1"
        }
        
        with pytest.raises(ValidationError) as excinfo:
            SdkConfigurationDTO.from_api_json(data)
        
        assert "Missing required field: key" in str(excinfo.value)
        
    def test_list_from_client_api_json(self):
        """Test list_from_client_api_json method."""
        data = [
            {
                "key": "config1",
                "value": "value1"
            },
            {
                "key": "config2",
                "value": True
            }
        ]
        
        configs = SdkConfigurationDTO.list_from_client_api_json(data)
        
        assert len(configs) == 2
        assert configs[0].key == "config1"
        assert configs[0].value == "value1"
        assert configs[0].scope == "global"
        assert configs[1].key == "config2"
        assert configs[1].value is True
        assert configs[1].scope == "global"
        
    def test_list_from_site_api_json(self):
        """Test list_from_site_api_json method."""
        data = [
            {
                "key": "config1",
                "value": "value1"
            },
            {
                "key": "config2",
                "value": True
            }
        ]
        
        configs = SdkConfigurationDTO.list_from_site_api_json(data, "site-123")
        
        assert len(configs) == 2
        assert configs[0].key == "config1"
        assert configs[0].value == "value1"
        assert configs[0].scope == "site"
        assert configs[0].scopeId == "site-123"
        assert configs[1].key == "config2"
        assert configs[1].value is True
        assert configs[1].scope == "site"
        assert configs[1].scopeId == "site-123"
        
    def test_list_from_building_api_json(self):
        """Test list_from_building_api_json method."""
        data = [
            {
                "key": "config1",
                "value": "value1"
            },
            {
                "key": "config2",
                "value": True
            }
        ]
        
        configs = SdkConfigurationDTO.list_from_building_api_json(data, "building-123")
        
        assert len(configs) == 2
        assert configs[0].key == "config1"
        assert configs[0].value == "value1"
        assert configs[0].scope == "building"
        assert configs[0].scopeId == "building-123"
        assert configs[1].key == "config2"
        assert configs[1].value is True
        assert configs[1].scope == "building"
        assert configs[1].scopeId == "building-123"
        
    def test_to_api_json(self):
        """Test to_api_json method."""
        config = SdkConfigurationDTO(
            key="config1",
            value="value1",
            scope="site",
            scopeId="site-123"
        )
        
        result = config.to_api_json()
        
        assert result["key"] == "config1"
        assert result["value"] == "value1"
        # Note: scope and scopeId are not included in the API JSON

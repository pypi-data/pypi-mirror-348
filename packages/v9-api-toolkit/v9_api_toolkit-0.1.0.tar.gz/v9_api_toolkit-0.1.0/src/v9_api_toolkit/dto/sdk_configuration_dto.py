from typing import Dict, Any, List, Optional
from v9_api_toolkit.dto.validation import ValidationError

class SdkConfigurationDTO:
    """Data Transfer Object for SDK configuration data."""
    
    def __init__(self, key: str, value: Any, scope: str = "global", scopeId: Optional[str] = None):
        self.key = key
        self.value = value
        self.scope = scope
        self.scopeId = scopeId
    
    @classmethod
    def from_api_json(cls, data: Dict[str, Any], scope: str = "global", scopeId: Optional[str] = None) -> 'SdkConfigurationDTO':
        """
        Create an SdkConfigurationDTO from API JSON data.
        
        Args:
            data: The API JSON data
            scope: The scope of the configuration (global, site, building)
            scopeId: The ID of the scope (site FID, building FID)
            
        Returns:
            An SdkConfigurationDTO object
        """
        if not isinstance(data, dict):
            raise ValidationError("SDK configuration data must be a dictionary")
            
        # Validate required fields
        if "key" not in data or data["key"] is None:
            raise ValidationError("Missing required field: key")
            
        # Create the DTO
        return cls(
            key=data["key"],
            value=data.get("value"),
            scope=scope,
            scopeId=scopeId
        )
    
    @classmethod
    def list_from_client_api_json(cls, data: List[Dict[str, Any]]) -> List['SdkConfigurationDTO']:
        """
        Create a list of SdkConfigurationDTOs from client API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A list of SdkConfigurationDTO objects
        """
        if not isinstance(data, list):
            return []
            
        configs = []
        
        for item in data:
            try:
                config = cls.from_api_json(item, scope="global")
                configs.append(config)
            except ValidationError:
                # Skip invalid configurations
                pass
                
        return configs
    
    @classmethod
    def list_from_site_api_json(cls, data: List[Dict[str, Any]], site_fid: str) -> List['SdkConfigurationDTO']:
        """
        Create a list of SdkConfigurationDTOs from site API JSON data.
        
        Args:
            data: The API JSON data
            site_fid: The site FID
            
        Returns:
            A list of SdkConfigurationDTO objects
        """
        if not isinstance(data, list):
            return []
            
        configs = []
        
        for item in data:
            try:
                config = cls.from_api_json(item, scope="site", scopeId=site_fid)
                configs.append(config)
            except ValidationError:
                # Skip invalid configurations
                pass
                
        return configs
    
    @classmethod
    def list_from_building_api_json(cls, data: List[Dict[str, Any]], building_fid: str) -> List['SdkConfigurationDTO']:
        """
        Create a list of SdkConfigurationDTOs from building API JSON data.
        
        Args:
            data: The API JSON data
            building_fid: The building FID
            
        Returns:
            A list of SdkConfigurationDTO objects
        """
        if not isinstance(data, list):
            return []
            
        configs = []
        
        for item in data:
            try:
                config = cls.from_api_json(item, scope="building", scopeId=building_fid)
                configs.append(config)
            except ValidationError:
                # Skip invalid configurations
                pass
                
        return configs
    
    def to_api_json(self) -> Dict[str, Any]:
        """
        Convert the SdkConfigurationDTO to API JSON format.
        
        Returns:
            The API JSON representation of the SdkConfigurationDTO
        """
        return {
            "key": self.key,
            "value": self.value
        }

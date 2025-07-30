from typing import Dict, Any, List, Optional
from v9_api_toolkit.dto.validation import ValidationError

class ClientMetadataDTO:
    """Data Transfer Object for client metadata."""
    
    def __init__(self, identifier: str, name: str, extraData: Dict[str, Any] = None):
        self.identifier = identifier
        self.name = name
        self.extraData = extraData or {}
    
    @classmethod
    def from_api_json(cls, data: Dict[str, Any]) -> 'ClientMetadataDTO':
        """
        Create a ClientMetadataDTO from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A ClientMetadataDTO object
        """
        if not isinstance(data, dict):
            raise ValidationError("Client metadata must be a dictionary")
            
        # Validate required fields
        required_fields = ["identifier", "name"]
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValidationError(f"Missing required field: {field}")
                
        # Create the DTO
        return cls(
            identifier=data["identifier"],
            name=data["name"],
            extraData=data.get("extra", {})
        )
    
    def to_api_json(self) -> Dict[str, Any]:
        """
        Convert the ClientMetadataDTO to API JSON format.
        
        Returns:
            The API JSON representation of the ClientMetadataDTO
        """
        return {
            "identifier": self.identifier,
            "name": self.name,
            "extra": self.extraData
        }

from typing import Dict, Any
from v9_api_toolkit.dto.validation import ValidationError

class CreateResponseDTO:
    """Data Transfer Object for create response data."""
    
    def __init__(self, fid: str):
        self.fid = fid
    
    @classmethod
    def from_api_json(cls, data: Dict[str, Any]) -> 'CreateResponseDTO':
        """
        Create a CreateResponseDTO from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A CreateResponseDTO object
        """
        if not isinstance(data, dict):
            raise ValidationError("Create response data must be a dictionary")
            
        # Check for fid in different possible locations
        fid = None
        
        if "fid" in data:
            fid = data["fid"]
        elif "features" in data and len(data["features"]) > 0:
            feature = data["features"][0]
            if "properties" in feature and "fid" in feature["properties"]:
                fid = feature["properties"]["fid"]
                
        if not fid:
            raise ValidationError("No FID found in create response")
            
        return cls(fid=fid)

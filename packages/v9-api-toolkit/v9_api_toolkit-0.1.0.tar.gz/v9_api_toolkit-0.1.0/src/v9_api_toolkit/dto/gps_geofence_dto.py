from typing import Dict, Any, List, Optional
from v9_api_toolkit.dto.validation import ValidationError

class GpsGeofenceDTO:
    """Data Transfer Object for GPS geofence data."""
    
    def __init__(self, fid: str, name: str, typeCode: str, extraData: Dict[str, Any] = None):
        self.fid = fid
        self.name = name
        self.typeCode = typeCode
        self.extraData = extraData or {}
    
    @classmethod
    def from_api_json(cls, data: Dict[str, Any]) -> 'GpsGeofenceDTO':
        """
        Create a GpsGeofenceDTO from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A GpsGeofenceDTO object
        """
        if not isinstance(data, dict):
            raise ValidationError("GPS geofence data must be a dictionary")
            
        # Extract properties
        if "properties" in data:
            props = data["properties"]
        else:
            props = data
            
        # Validate required fields
        required_fields = ["fid", "name", "typeCode"]
        for field in required_fields:
            if field not in props or props[field] is None:
                raise ValidationError(f"Missing required field: {field}")
                
        # Create the DTO
        return cls(
            fid=props["fid"],
            name=props["name"],
            typeCode=props["typeCode"],
            extraData=props.get("extra", {})
        )
    
    @classmethod
    def list_from_api_json(cls, data: List[Dict[str, Any]]) -> List['GpsGeofenceDTO']:
        """
        Create a list of GpsGeofenceDTOs from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A list of GpsGeofenceDTO objects
        """
        if not isinstance(data, list):
            raise ValidationError("GPS geofence list data must be a list")
            
        geofences = []
        
        for item in data:
            try:
                geofence = cls.from_api_json(item)
                geofences.append(geofence)
            except ValidationError:
                # Skip invalid geofences
                pass
                
        return geofences
    
    def to_api_json(self) -> Dict[str, Any]:
        """
        Convert the GpsGeofenceDTO to API JSON format.
        
        Returns:
            The API JSON representation of the GpsGeofenceDTO
        """
        return {
            "type": "Feature",
            "properties": {
                "fid": self.fid,
                "name": self.name,
                "typeCode": self.typeCode,
                "extra": self.extraData
            },
            "geometry": None  # Geometry is handled separately
        }

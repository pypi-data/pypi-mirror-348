from typing import Dict, Any, List, Optional
from v9_api_toolkit.dto.validation import ValidationError

class BuildingDTO:
    """Data Transfer Object for building data."""
    
    def __init__(self, fid: str, name: str, typeCode: str, sid: str, extraData: Dict[str, Any] = None):
        self.fid = fid
        self.name = name
        self.typeCode = typeCode
        self.sid = sid
        self.extraData = extraData or {}
        self.bid = None  # Optional field
    
    @classmethod
    def from_api_json(cls, data: Dict[str, Any]) -> 'BuildingDTO':
        """
        Create a BuildingDTO from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A BuildingDTO object
        """
        if not isinstance(data, dict):
            raise ValidationError("Building data must be a dictionary")
            
        # Extract properties from feature collection
        if "type" in data and data["type"] == "FeatureCollection" and "features" in data:
            if len(data["features"]) == 0:
                raise ValidationError("No features found in building data")
                
            feature = data["features"][0]
            if "properties" not in feature:
                raise ValidationError("No properties found in building feature")
                
            props = feature["properties"]
        else:
            props = data
            
        # Validate required fields
        required_fields = ["fid", "name", "typeCode"]
        for field in required_fields:
            if field not in props or props[field] is None:
                raise ValidationError(f"Missing required field: {field}")
                
        # Create the DTO
        building = cls(
            fid=props["fid"],
            name=props["name"],
            typeCode=props["typeCode"],
            sid=props.get("sid", ""),
            extraData=props.get("extra", {})
        )
        
        # Add optional fields
        if "bid" in props:
            building.bid = props["bid"]
            
        return building
    
    @classmethod
    def list_from_api_json(cls, data: Dict[str, Any]) -> List['BuildingDTO']:
        """
        Create a list of BuildingDTOs from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A list of BuildingDTO objects
        """
        if not isinstance(data, dict):
            raise ValidationError("Building list data must be a dictionary")
            
        buildings = []
        
        # Handle feature collection
        if "type" in data and data["type"] == "FeatureCollection" and "features" in data:
            for feature in data["features"]:
                if "properties" in feature and feature["properties"].get("typeCode") == "building-outline":
                    try:
                        building = cls.from_api_json({"features": [feature], "type": "FeatureCollection"})
                        buildings.append(building)
                    except ValidationError:
                        # Skip invalid buildings
                        pass
        # Handle array of buildings
        elif isinstance(data, list):
            for item in data:
                try:
                    building = cls.from_api_json(item)
                    buildings.append(building)
                except ValidationError:
                    # Skip invalid buildings
                    pass
                    
        return buildings
    
    def to_api_json(self) -> Dict[str, Any]:
        """
        Convert the BuildingDTO to API JSON format.
        
        Returns:
            The API JSON representation of the BuildingDTO
        """
        properties = {
            "fid": self.fid,
            "name": self.name,
            "typeCode": self.typeCode,
            "sid": self.sid,
            "extra": self.extraData
        }
        
        if self.bid is not None:
            properties["bid"] = self.bid
            
        return {
            "type": "Feature",
            "properties": properties,
            "geometry": None  # Geometry is handled separately
        }

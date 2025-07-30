from typing import Dict, Any, List, Optional
from v9_api_toolkit.dto.validation import ValidationError

class LevelDTO:
    """Data Transfer Object for level data."""
    
    def __init__(self, fid: str, name: str, typeCode: str, extraData: Dict[str, Any] = None):
        self.fid = fid
        self.name = name
        self.typeCode = typeCode
        self.extraData = extraData or {}
        self.floorNumber = None  # Optional field
    
    @classmethod
    def from_api_json(cls, data: Dict[str, Any]) -> 'LevelDTO':
        """
        Create a LevelDTO from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A LevelDTO object
        """
        if not isinstance(data, dict):
            raise ValidationError("Level data must be a dictionary")
            
        # Validate required fields
        required_fields = ["fid", "name", "typeCode"]
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValidationError(f"Missing required field: {field}")
                
        # Create the DTO
        level = cls(
            fid=data["fid"],
            name=data["name"],
            typeCode=data["typeCode"],
            extraData=data.get("extra", {})
        )
        
        # Add optional fields
        if "floorNumber" in data:
            level.floorNumber = data["floorNumber"]
            
        return level
    
    @classmethod
    def list_from_api_json(cls, data: Dict[str, Any]) -> List['LevelDTO']:
        """
        Create a list of LevelDTOs from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A list of LevelDTO objects
        """
        levels = []
        
        # Handle different data formats
        if isinstance(data, list):
            # Direct list of levels
            for item in data:
                try:
                    level = cls.from_api_json(item)
                    levels.append(level)
                except ValidationError:
                    # Skip invalid levels
                    pass
        elif isinstance(data, dict) and "features" in data:
            # Feature collection
            for feature in data["features"]:
                if "properties" in feature:
                    try:
                        level = cls.from_api_json(feature["properties"])
                        levels.append(level)
                    except ValidationError:
                        # Skip invalid levels
                        pass
                        
        return levels
    
    def to_api_json(self) -> Dict[str, Any]:
        """
        Convert the LevelDTO to API JSON format.
        
        Returns:
            The API JSON representation of the LevelDTO
        """
        data = {
            "fid": self.fid,
            "name": self.name,
            "typeCode": self.typeCode,
            "extra": self.extraData
        }
        
        if self.floorNumber is not None:
            data["floorNumber"] = self.floorNumber
            
        return data

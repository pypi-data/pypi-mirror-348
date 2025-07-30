from typing import Dict, Any, List
from v9_api_toolkit.dto.validation import ValidationError

class SiteDTO:
    """Data Transfer Object for site data."""
    
    def __init__(self, fid: str, name: str, typeCode: str, extraData: Dict[str, Any] = None):
        self.fid = fid
        self.name = name
        self.typeCode = typeCode
        self.extraData = extraData or {}
        self.eid = None  # Optional field
        self.sid = None  # Optional field
    
    @classmethod
    def from_api_json(cls, data: Dict[str, Any]) -> 'SiteDTO':
        """
        Create a SiteDTO from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A SiteDTO object
        """
        if not isinstance(data, dict):
            raise ValidationError("Site data must be a dictionary")
            
        # Extract properties from feature collection
        if "type" in data and data["type"] == "FeatureCollection" and "features" in data:
            if len(data["features"]) == 0:
                raise ValidationError("No features found in site data")
                
            feature = data["features"][0]
            if "properties" not in feature:
                raise ValidationError("No properties found in site feature")
                
            props = feature["properties"]
        else:
            props = data
            
        # Validate required fields
        required_fields = ["fid", "name", "typeCode"]
        for field in required_fields:
            if field not in props or props[field] is None:
                raise ValidationError(f"Missing required field: {field}")
                
        # Create the DTO
        site = cls(
            fid=props["fid"],
            name=props["name"],
            typeCode=props["typeCode"],
            extraData=props.get("extra", {})
        )
        
        # Add optional fields
        if "eid" in props:
            site.eid = props["eid"]
        if "sid" in props:
            site.sid = props["sid"]
            
        return site
    
    @classmethod
    def list_from_api_json(cls, data: Dict[str, Any]) -> List['SiteDTO']:
        """
        Create a list of SiteDTOs from API JSON data.
        
        Args:
            data: The API JSON data
            
        Returns:
            A list of SiteDTO objects
        """
        if not isinstance(data, dict):
            raise ValidationError("Site list data must be a dictionary")
            
        sites = []
        
        # Handle feature collection
        if "type" in data and data["type"] == "FeatureCollection" and "features" in data:
            for feature in data["features"]:
                if "properties" in feature and feature["properties"].get("typeCode") == "site-outline":
                    try:
                        site = cls.from_api_json({"features": [feature], "type": "FeatureCollection"})
                        sites.append(site)
                    except ValidationError:
                        # Skip invalid sites
                        pass
        # Handle array of sites
        elif isinstance(data, list):
            for item in data:
                try:
                    site = cls.from_api_json(item)
                    sites.append(site)
                except ValidationError:
                    # Skip invalid sites
                    pass
                    
        return sites
    
    def to_api_json(self) -> Dict[str, Any]:
        """
        Convert the SiteDTO to API JSON format.
        
        Returns:
            The API JSON representation of the SiteDTO
        """
        properties = {
            "fid": self.fid,
            "name": self.name,
            "typeCode": self.typeCode,
            "extra": self.extraData
        }
        
        if self.eid is not None:
            properties["eid"] = self.eid
        if self.sid is not None:
            properties["sid"] = self.sid
            
        return {
            "type": "Feature",
            "properties": properties,
            "geometry": None  # Geometry is handled separately
        }

import logging
from v9_api_toolkit.dto import (
  ClientMetadataDTO, CreateResponseDTO, GpsGeofenceDTO, SdkConfigurationDTO, SiteDTO, BuildingDTO, LevelDTO
)
from v9_api_toolkit.dto.validation import ValidationError
from typing import List, Dict, Any, Optional, Union, cast
import json
import requests
import time

from v9_api_toolkit.api.base_service import V9ApiError
from v9_api_toolkit.api.site_service import SiteApiService
from v9_api_toolkit.api.building_service import BuildingApiService
from v9_api_toolkit.api.level_service import LevelApiService
from v9_api_toolkit.api.sdk_service import SdkApiService
from v9_api_toolkit.api.client_service import ClientApiService

class V9ApiService:
    def __init__(self, config: Dict[str, str], user_email: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize the V9 API service with configuration and authentication.
        
        Args:
            config: Configuration for the API service containing:
                - api_url: Base URL for the API
                - client_identifier: Client identifier
                - username: Username for authentication (if token not provided)
                - password: Password for authentication (if token not provided)
            user_email: Optional user email for logging
            token: Optional pre-authenticated token (if not provided, will authenticate using username/password)
        """
        self.base_url = config["api_url"]
        self.client_id = config["client_identifier"]
        self.user_email = user_email
        self.config = config  # Store the full config for reference
        self.logger = logging.getLogger(__name__)

        if token:
            self.token = token
        else:
            self.username = config["username"]
            self.password = config["password"]
            self.token = self._get_token()
            
        # Initialize sub-services
        self.site_service = SiteApiService(self)
        self.building_service = BuildingApiService(self)
        self.level_service = LevelApiService(self)
        self.sdk_service = SdkApiService(self)
        self.client_service = ClientApiService(self)

    def _get_token(self) -> str:
        """
        Get an authentication token from the V9 API.
        
        Returns:
            The authentication token
        """
        endpoint = f"{self.base_url}/api/v9/identity/clients/{self.client_id}/auth/token"
        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }
        try:
            response = requests.post(endpoint, json=payload)
            if not response.ok:
                error_msg = f"Failed to get token: {response.status_code}"
                try:
                    error_details = response.json()
                    error_msg += f", details: {error_details}"
                except:
                    error_msg += f", response: {response.text[:200]}"
                    
                raise V9ApiError(
                    error_msg, 
                    status_code=response.status_code, 
                    response_text=response.text
                )
            return response.json()["access_token"]
        except requests.RequestException as e:
            raise V9ApiError(f"Request error during token acquisition: {str(e)}")

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the V9 API with error handling."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Track operation time
        start_time = time.time()
        operation_name = f"{method} {endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json_data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json_data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Log the operation duration
            duration = time.time() - start_time
            self.logger.debug(f"API operation {operation_name} completed in {duration:.2f}s")
            
            if not response.ok:
                error_msg = f"API request failed: {response.status_code}"
                try:
                    error_details = response.json()
                    if isinstance(error_details, dict):
                        if "message" in error_details:
                            error_msg += f", message: {error_details['message']}"
                        elif "error" in error_details:
                            error_msg += f", error: {error_details['error']}"
                        else:
                            error_msg += f", details: {error_details}"
                    else:
                        error_msg += f", details: {error_details}"
                except:
                    error_msg += f", response: {response.text[:200]}"
                
                raise V9ApiError(
                    error_msg, 
                    status_code=response.status_code, 
                    response_text=response.text
                )
            
            try:
                return response.json()
            except json.JSONDecodeError:
                # If the response is not JSON, return an empty dict
                if response.text.strip():
                    self.logger.warning(f"Non-JSON response from API: {response.text[:200]}")
                return {}
                
        except requests.RequestException as e:
            # Log the operation failure
            duration = time.time() - start_time
            self.logger.error(f"API operation {operation_name} failed after {duration:.2f}s: {str(e)}")
            raise V9ApiError(f"Request error: {str(e)}")

    # Site methods - delegated to site_service
    def get_sites(self) -> List[SiteDTO]:
        return self.site_service.get_sites()

    def create_site(self, site: SiteDTO, source_api_service=None) -> str:
        return self.site_service.create_site(site, source_api_service)

    def update_site(self, site_id: str, site: SiteDTO, source_api_service=None) -> str:
        return self.site_service.update_site(site_id, site, source_api_service)

    def update_site_extra_data(self, site_fid: str, extra_data: Dict[str, Any]) -> bool:
        """
        Update only the extra data for a site.
        
        Args:
            site_fid: The FID of the site to update
            extra_data: The extra data to update
            
        Returns:
            True if the update was successful, False otherwise
        """
        return self.site_service.update_site_extra_data(site_fid, extra_data)

    def get_site_by_fid(self, site_fid: str) -> SiteDTO:
        return self.site_service.get_site_by_fid(site_fid)

    # Building methods - delegated to building_service
    def get_buildings(self, site_fid: str) -> List[BuildingDTO]:
        return self.building_service.get_buildings(site_fid)

    def get_building_by_fid(self, site_fid: str, building_fid: str) -> BuildingDTO:
        return self.building_service.get_building_by_fid(site_fid, building_fid)

    def create_building(self, site_fid: str, building: BuildingDTO, source_api_service=None) -> str:
        return self.building_service.create_building(site_fid, building, source_api_service)

    def update_building(self, site_fid: str, building_fid: str, building: BuildingDTO, source_api_service=None) -> str:
        return self.building_service.update_building(site_fid, building_fid, building, source_api_service)

    def update_building_extra_data(self, site_fid: str, building_fid: str, extra_data: Dict[str, Any]) -> bool:
        """
        Update only the extra data for a building.
        
        Args:
            site_fid: The site FID
            building_fid: The building FID
            extra_data: The extra data to update
            
        Returns:
            True if the update was successful, False otherwise
        """
        return self.building_service.update_building_extra_data(site_fid, building_fid, extra_data)

    # Level methods - delegated to level_service
    def get_levels(self, site_fid: str, building_fid: str) -> List[LevelDTO]:
        return self.level_service.get_levels(site_fid, building_fid)

    def get_level_by_id(self, site_fid: str, building_fid: str, level_id: str) -> LevelDTO:
        return self.level_service.get_level_by_id(site_fid, building_fid, level_id)

    def create_level(self, site_fid: str, building_fid: str, level: Dict[str, Any]) -> str:
        return self.level_service.create_level(site_fid, building_fid, level)

    def update_level(self, site_fid: str, building_fid: str, level_id: str, level: Dict[str, Any]) -> str:
        return self.level_service.update_level(site_fid, building_fid, level_id, level)

    def delete_level(self, site_fid: str, building_fid: str, level_id: str) -> bool:
        return self.level_service.delete_level(site_fid, building_fid, level_id)

    # Client methods - delegated to client_service
    def get_client_metadata(self) -> ClientMetadataDTO:
        return self.client_service.get_client_metadata()

    def update_client(self, client_id: str, client_data: Dict[str, Any]) -> bool:
        return self.client_service.update_client(client_id, client_data)

    def create_client(self, client_data: Dict[str, Any]) -> str:
        return self.client_service.create_client(client_data)

    # SDK Configuration methods - delegated to sdk_service
    def get_client_sdk_config(self) -> List[SdkConfigurationDTO]:
        return self.sdk_service.get_client_sdk_config()

    def get_site_sdk_config(self, site_fid: str) -> List[SdkConfigurationDTO]:
        return self.sdk_service.get_site_sdk_config(site_fid)

    def get_building_sdk_config(self, site_fid: str, building_fid: str) -> List[SdkConfigurationDTO]:
        return self.sdk_service.get_building_sdk_config(site_fid, building_fid)

    def get_client_gps_geofences(self) -> List[Dict[str, Any]]:
        """
        Get GPS geofences for the client.
        
        Returns:
            A list of GPS geofence features
        """
        return self.client_service.get_client_gps_geofences()

    def put_global_sdk_configurations(self, configs: List[SdkConfigurationDTO]) -> bool:
        return self.sdk_service.put_global_sdk_configurations(configs)

    def put_site_sdk_configurations(self, site_fid: str, configs: List[SdkConfigurationDTO]) -> bool:
        return self.sdk_service.put_site_sdk_configurations(site_fid, configs)

    def put_building_sdk_configurations(self, site_fid: str, building_fid: str, configs: List[SdkConfigurationDTO]) -> bool:
        return self.sdk_service.put_building_sdk_configurations(site_fid, building_fid, configs)

"""
V9 API Toolkit - A Python package for interacting with the V9 API.

This package provides a set of tools for interacting with the V9 API,
including services for managing sites, buildings, levels, and SDK configurations.
"""

import logging

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import main classes for easy access
from v9_api_toolkit.api.v9_api_service import V9ApiService
from v9_api_toolkit.api.base_service import V9ApiError

# Version information
__version__ = '0.1.0'

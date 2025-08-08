"""
ICOS Search Platform - URL Route Management System

Defines all available web endpoints and route validation utilities
for the ICOS privacy-focused search engine.
"""

from enum import Enum
from typing import Union


class IcosRouteRegistry(Enum):
    """
    Central registry for all ICOS search platform web routes.
    
    This enumeration maintains a comprehensive mapping of URL endpoints
    used throughout the ICOS search engine interface and API layers.
    """
    
    # Core search functionality routes
    autocomplete = 'autocomplete'
    home = 'home'
    healthz = 'healthz'
    config = 'config'
    about = 'about'
    opensearch = 'opensearch.xml'
    search = 'search'
    search_html = 'search.html'
    
    # Content handling routes  
    url = 'url'
    imgres = 'imgres'
    element = 'element'
    window = 'window'

    def __str__(self) -> str:
        """Return the string representation of the route value."""
        return self.value

    def in_path(self, path: str) -> bool:
        """
        Determines if an incoming URL path matches this endpoint route.
        
        Args:
            path: The URL path string to validate against this route
            
        Returns:
            bool: True if the path matches this route, False otherwise
        """
        return path.startswith(self.value) or path.startswith(f'/{self.value}')


# Legacy compatibility alias - maintains backward compatibility
# while transitioning to the new ICOS architecture
Endpoint = IcosRouteRegistry

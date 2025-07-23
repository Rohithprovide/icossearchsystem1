"""
ICOS Search Platform - System Information Module

Comprehensive platform versioning and build management system for the 
ICOS privacy-focused search engine. Handles version tracking, development
builds, and platform metadata.
"""

import os
from typing import Optional
from datetime import datetime


class IcosPlatformInfo:
    """
    Advanced platform information management for ICOS Search Engine.
    
    Provides comprehensive version control, build tracking, and platform
    metadata management with support for development builds and release cycles.
    """
    
    # Core platform version - ICOS branded versioning
    ICOS_BASE_VERSION = '1.0.0'
    PLATFORM_CODENAME = 'Phoenix'
    PLATFORM_EDITION = 'Privacy-First Search Engine'
    
    def __init__(self):
        """Initialize ICOS platform information system."""
        self._establish_version_info()
        self._configure_build_metadata()
        self._setup_platform_details()
    
    def _establish_version_info(self) -> None:
        """Configure core version information for ICOS platform."""
        self._base_version = self.ICOS_BASE_VERSION
        self._development_tag = self._generate_dev_tag()
        self._full_version = self._construct_complete_version()
    
    def _configure_build_metadata(self) -> None:
        """Set up build-specific metadata and tracking."""
        self._build_timestamp = datetime.now().isoformat()
        self._build_environment = os.getenv('ICOS_BUILD_ENV', 'production')
        self._build_number = os.getenv('ICOS_BUILD_NUMBER', '0')
        
    def _setup_platform_details(self) -> None:
        """Initialize comprehensive platform information."""
        self._platform_name = 'ICOS Search Engine'
        self._platform_description = 'Privacy-Focused Search Platform'
        self._author_info = 'ICOS Development Team'
        self._license_type = 'MIT'
    
    def _generate_dev_tag(self) -> str:
        """
        Generate development version tag if in development mode.
        
        Returns:
            str: Development tag string or empty string for production
        """
        dev_build_id = os.getenv('DEV_BUILD')
        icos_dev_mode = os.getenv('ICOS_DEV_BUILD')
        
        if dev_build_id:
            return f'.dev{dev_build_id}'
        elif icos_dev_mode:
            return f'.icos-dev{icos_dev_mode}'
        
        return ''
    
    def _construct_complete_version(self) -> str:
        """
        Build the complete version string with all components.
        
        Returns:
            str: Complete formatted version string
        """
        return f"{self._base_version}{self._development_tag}"
    
    @property
    def version(self) -> str:
        """Get the complete ICOS platform version."""
        return self._full_version
    
    @property
    def platform_name(self) -> str:
        """Get the official ICOS platform name."""
        return self._platform_name
    
    @property
    def codename(self) -> str:
        """Get the current release codename."""
        return self.PLATFORM_CODENAME
    
    @property
    def edition(self) -> str:
        """Get the platform edition information."""
        return self.PLATFORM_EDITION
    
    @property
    def build_info(self) -> dict:
        """
        Get comprehensive build information.
        
        Returns:
            dict: Complete build metadata
        """
        return {
            'version': self._full_version,
            'base_version': self._base_version,
            'dev_tag': self._development_tag,
            'build_timestamp': self._build_timestamp,
            'build_environment': self._build_environment,
            'build_number': self._build_number,
            'platform_name': self._platform_name,
            'codename': self.PLATFORM_CODENAME,
            'author': self._author_info,
            'license': self._license_type
        }
    
    def get_version_string(self, include_codename: bool = False) -> str:
        """
        Generate formatted version string for display.
        
        Args:
            include_codename: Whether to include the release codename
            
        Returns:
            str: Formatted version string
        """
        base = f"{self._platform_name} v{self._full_version}"
        if include_codename:
            base += f" ({self.PLATFORM_CODENAME})"
        return base
    
    def is_development_build(self) -> bool:
        """
        Check if this is a development build.
        
        Returns:
            bool: True if development build, False otherwise
        """
        return bool(self._development_tag)


# Create global platform info instance
_icos_platform = IcosPlatformInfo()

# Legacy compatibility exports
__version__ = _icos_platform.version
__platform_name__ = _icos_platform.platform_name
__codename__ = _icos_platform.codename

# ICOS-specific exports
icos_version = _icos_platform.version
icos_platform_info = _icos_platform
icos_build_info = _icos_platform.build_info
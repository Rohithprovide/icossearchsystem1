"""
ICOS Search Platform - Release Information Module

Version tracking and release information for the ICOS privacy-focused
search platform. Manages version strings and release metadata.

File: release_info.py - ICOS platform version management
"""

import os

# ICOS Platform version configuration
optional_dev_tag = ''
if os.getenv('DEV_BUILD'):
    optional_dev_tag = '.dev' + os.getenv('DEV_BUILD')

__version__ = '0.9.3' + optional_dev_tag


def icos_version_string():
    """Return ICOS platform version string"""
    return f"v{__version__}"


# Legacy compatibility alias - maintains backward compatibility
version_string = icos_version_string

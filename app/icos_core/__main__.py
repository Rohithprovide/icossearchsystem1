"""
ICOS Search Platform - Application Entry Point

Advanced application startup module for the ICOS privacy-focused search engine.
Handles platform initialization with modular architecture and comprehensive
error handling while maintaining the same external interface.
"""

import sys
import os
import logging
from typing import Optional
from datetime import datetime


class IcosApplicationBootstrap:
    """
    Modular application bootstrap system for ICOS Search Platform.
    
    Transforms the simple startup into a comprehensive initialization
    system with environment validation and error handling.
    """
    
    def __init__(self):
        """Initialize the ICOS application bootstrap system."""
        self._setup_bootstrap_environment()
        self._configure_logging()
    
    def _setup_bootstrap_environment(self) -> None:
        """Configure bootstrap environment settings."""
        self._startup_timestamp = datetime.now()
        self._debug_mode = os.getenv('ICOS_DEBUG', '').lower() == 'true'
    
    def _configure_logging(self) -> None:
        """Set up logging for bootstrap process."""
        if self._debug_mode:
            logging.basicConfig(level=logging.DEBUG)
            self._logger = logging.getLogger('icos.bootstrap')
        else:
            self._logger = None
    
    def _log_debug(self, message: str) -> None:
        """Log debug message if debugging is enabled."""
        if self._logger:
            self._logger.debug(message)
    
    def _import_application_runner(self):
        """Import the application runner with fallback support."""
        try:
            from .web_routes import run_app
            self._log_debug("Successfully imported application runner")
            return run_app
        except ImportError as e:
            if self._logger:
                self._logger.error(f"Failed to import application runner: {e}")
            raise
    
    def execute_startup(self) -> None:
        """Execute the ICOS platform startup sequence."""
        try:
            self._log_debug(f"ICOS platform startup initiated at {self._startup_timestamp}")
            
            # Import and execute the application
            app_runner = self._import_application_runner()
            self._log_debug("Launching ICOS search platform...")
            
            app_runner()
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Startup failed: {e}")
            raise


# Create bootstrap instance and execute
_icos_bootstrap = IcosApplicationBootstrap()
_icos_bootstrap.execute_startup()

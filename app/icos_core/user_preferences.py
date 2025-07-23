"""
ICOS Search Platform - User Preference Management System

Advanced configuration and personalization engine for the ICOS privacy-focused
search platform. Handles user preferences, styling customization, and secure
preference storage with encryption capabilities.
"""

import os
import json
import hashlib
import brotli
import logging
from base64 import urlsafe_b64encode, urlsafe_b64decode
from typing import Optional, Dict, Any, Union
from inspect import Attribute
from flask import current_app

import cssutils
from cssutils.css.cssstylesheet import CSSStyleSheet
from cssutils.css.cssstylerule import CSSStyleRule

from app.icos_toolkit.platform_helpers import read_config_bool
from app.icos_toolkit.security_shield import SecureURLShield

# Suppress CSS parsing warnings for cleaner logs
cssutils.log.setLevel(logging.CRITICAL)


class StylesheetProcessor:
    """Handles CSS stylesheet processing and rule management for ICOS themes."""
    
    @staticmethod
    def locate_style_rule(stylesheet: CSSStyleSheet, target_selector: str) -> Optional[CSSStyleRule]:
        """
        Search through stylesheet rules to find a matching CSS selector.
        
        Args:
            stylesheet: The CSS stylesheet to examine
            target_selector: The CSS selector string to locate
            
        Returns:
            The matching CSS rule object, or None if not found
        """
        for css_rule in stylesheet.cssRules:
            if (hasattr(css_rule, "selectorText") and 
                target_selector == css_rule.selectorText):
                return css_rule
        return None


class IcosUserPreferences:
    """
    Comprehensive user preference management for the ICOS search platform.
    
    Handles all aspects of user customization including themes, search behavior,
    privacy settings, and secure preference storage with optional encryption.
    """
    
    def __init__(self, **preference_overrides):
        """
        Initialize user preferences with environment defaults and optional overrides.
        
        Args:
            **preference_overrides: Custom preference values to override defaults
        """
        self._establish_core_settings()
        self._configure_search_behavior()
        self._setup_privacy_controls()
        self._initialize_encryption_system()
        
        # Apply any custom preference overrides
        if preference_overrides:
            self._apply_preference_overrides(preference_overrides)
    
    def _establish_core_settings(self) -> None:
        """Configure the fundamental ICOS platform settings."""
        # Interface and display preferences
        self.interface_theme = os.getenv('WHOOGLE_CONFIG_THEME', 'system')
        self.language_interface = os.getenv('WHOOGLE_CONFIG_LANGUAGE', '')
        self.search_language = os.getenv('WHOOGLE_CONFIG_SEARCH_LANGUAGE', '')
        self.custom_styling = os.getenv('WHOOGLE_CONFIG_STYLE', '')
        
        # Geographic and localization settings
        self.geographic_region = os.getenv('WHOOGLE_CONFIG_COUNTRY', '')
        self.proximity_location = os.getenv('WHOOGLE_CONFIG_NEAR', '')
        self.time_range_filter = os.getenv('WHOOGLE_CONFIG_TIME_PERIOD', '')
        
        # Content filtering and blocking
        self.blocked_content = os.getenv('WHOOGLE_CONFIG_BLOCK', '')
        self.blocked_titles = os.getenv('WHOOGLE_CONFIG_BLOCK_TITLE', '')
        self.blocked_domains = os.getenv('WHOOGLE_CONFIG_BLOCK_URL', '')
        
        # Platform configuration
        self.base_search_url = os.getenv('WHOOGLE_CONFIG_URL', '')
        
    def _configure_search_behavior(self) -> None:
        """Set up search-specific behavioral preferences."""
        self.safe_search_enabled = read_config_bool('WHOOGLE_CONFIG_SAFE')
        self.open_links_new_tab = read_config_bool('WHOOGLE_CONFIG_NEW_TAB')
        self.image_view_enabled = read_config_bool('WHOOGLE_CONFIG_VIEW_IMAGE')
        self.anonymous_viewing = read_config_bool('WHOOGLE_CONFIG_ANON_VIEW')
        self.get_requests_only = read_config_bool('WHOOGLE_CONFIG_GET_ONLY')
        self.alternative_frontends = read_config_bool('WHOOGLE_CONFIG_ALTS')
        self.javascript_disabled = read_config_bool('WHOOGLE_CONFIG_NOJS')
        self.ai_sidebar_active = read_config_bool('WHOOGLE_CONFIG_AI_SIDEBAR')
        
        # Legacy compatibility setting (deprecated but maintained)
        self.dark_theme_legacy = read_config_bool('WHOOGLE_CONFIG_DARK')
        
    def _setup_privacy_controls(self) -> None:
        """Configure privacy and security-related preferences."""
        self.encrypted_preferences = read_config_bool('WHOOGLE_CONFIG_PREFERENCES_ENCRYPTED')
        self.encryption_key = os.getenv('WHOOGLE_CONFIG_PREFERENCES_KEY', '')
        self.accept_language_header = False
        
        # User agent management
        self.browser_agent = 'LYNX_UA'
        self.custom_browser_agent = ''
        self.use_custom_browser_agent = False
        
    def _initialize_encryption_system(self) -> None:
        """Set up the preference encryption and storage system."""
        # Define which preferences are safe for URL parameter usage
        self.url_safe_preferences = [
            'interface_theme',
            'safe_search_enabled', 
            'open_links_new_tab',
            'ai_sidebar_active'
        ]
        
        # Map internal names to external API names for compatibility
        self._preference_mapping = {
            'interface_theme': 'theme',
            'safe_search_enabled': 'safe',
            'open_links_new_tab': 'new_tab',
            'ai_sidebar_active': 'ai_sidebar'
        }
    
    def _apply_preference_overrides(self, overrides: Dict[str, Any]) -> None:
        """
        Apply user-provided preference overrides to the configuration.
        
        Args:
            overrides: Dictionary of preference keys and values to override
        """
        modifiable_attributes = self._get_modifiable_preference_list()
        
        for preference_key in modifiable_attributes:
            if preference_key in overrides:
                setattr(self, preference_key, overrides[preference_key])
            elif (preference_key not in overrides and 
                  modifiable_attributes[preference_key] == bool):
                setattr(self, preference_key, False)
        
        # Handle legacy theme attribute mapping that may have changed
        if 'theme' in overrides:
            # Update interface_theme if theme was provided
            self.interface_theme = overrides['theme']
    
    def __getitem__(self, preference_name: str) -> Any:
        """Allow dictionary-style access to preferences."""
        return getattr(self, preference_name)
    
    def __setitem__(self, preference_name: str, value: Any) -> None:
        """Allow dictionary-style assignment of preferences."""
        return setattr(self, preference_name, value)
    
    def __delitem__(self, preference_name: str) -> None:
        """Allow dictionary-style deletion of preferences."""
        return delattr(self, preference_name)
    
    def __contains__(self, preference_name: str) -> bool:
        """Check if a preference exists."""
        return hasattr(self, preference_name)
    
    def _get_modifiable_preference_list(self) -> Dict[str, type]:
        """
        Get all user-configurable preferences and their types.
        
        Returns:
            Dictionary mapping preference names to their data types
        """
        return {name: type(value) for name, value in self.__dict__.items()
                if not name.startswith("_") and (type(value) in [bool, str])}
    
    def get_exportable_preferences(self) -> Dict[str, Any]:
        """
        Get preferences that are safe for external export/storage.
        
        Returns:
            Dictionary containing only URL-safe preferences
        """
        safe_prefs = {}
        for internal_name in self.url_safe_preferences:
            if hasattr(self, internal_name):
                external_name = self._preference_mapping.get(internal_name, internal_name)
                safe_prefs[external_name] = getattr(self, internal_name)
        return safe_prefs
    
    @property
    def compiled_stylesheet(self) -> str:
        """
        Generate the complete CSS stylesheet with user customizations applied.
        
        Returns:
            Complete CSS stylesheet as a string with user modifications
        """
        # Load the base ICOS stylesheet
        base_css_path = os.path.join(
            current_app.config['STATIC_FOLDER'], 
            'css/variables.css'
        )
        
        with open(base_css_path, 'r') as css_file:
            base_stylesheet = cssutils.parseString(css_file.read())
        
        # Parse user customizations
        if self.custom_styling:
            user_customizations = cssutils.parseString(self.custom_styling)
            
            # Apply each user customization rule
            for custom_rule in user_customizations:
                existing_rule = StylesheetProcessor.locate_style_rule(
                    base_stylesheet, custom_rule.selectorText
                )
                
                if existing_rule:
                    # Update existing rule with user customizations
                    existing_rule.style = custom_rule.style
                else:
                    # Add new custom rule to stylesheet
                    base_stylesheet.add(custom_rule)
        
        return str(base_stylesheet.cssText, 'utf-8')
    
    @property
    def secure_preference_token(self) -> str:
        """
        Generate a secure, encrypted token containing user preferences.
        
        Returns:
            Encrypted preference token for secure storage/transmission
        """
        # Validate encryption availability
        if self.encrypted_preferences and not self.encryption_key:
            self.encrypted_preferences = False
        
        # Generate preference token with encryption flag
        encryption_indicator = "e" if self.encrypted_preferences else "u"
        encoded_preferences = self._encode_preference_data()
        
        return f"{encryption_indicator}{encoded_preferences}"
    
    def validate_url_parameter_safety(self, parameter_key: str) -> bool:
        """
        Check if a preference parameter is safe for URL usage.
        
        Args:
            parameter_key: The preference key to validate
            
        Returns:
            True if the parameter is safe for URL usage, False otherwise
        """
        external_name = self._preference_mapping.get(parameter_key, parameter_key)
        return external_name in [self._preference_mapping[k] for k in self.url_safe_preferences]
    
    def get_interface_language(self) -> str:
        """
        Determine the appropriate interface language for the user.
        
        Returns:
            Language code for interface localization, defaults to English
        """
        if (self.language_interface and 
            self.language_interface in current_app.config.get('TRANSLATIONS', {})):
            return self.language_interface
        return 'lang_en'
    
    def update_from_url_parameters(self, url_params: Dict[str, Any]) -> 'IcosUserPreferences':
        """
        Update preferences based on URL parameters or encrypted token.
        
        Args:
            url_params: Dictionary of URL parameters to process
            
        Returns:
            Updated preference object with new settings applied
        """
        # Handle encrypted preference token if present
        if 'vortex' in url_params:
            decrypted_params = self._decode_preference_token(url_params['vortex'])
            if decrypted_params:
                url_params = decrypted_params
        
        # Process individual URL parameters
        for param_key, param_value in url_params.items():
            if not self.validate_url_parameter_safety(param_key):
                continue
                
            # Convert parameter values to appropriate types
            processed_value = self._process_parameter_value(param_value)
            
            # Map external parameter name to internal attribute name
            internal_key = self._get_internal_key_name(param_key)
            if internal_key:
                setattr(self, internal_key, processed_value)
        
        return self
    
    def _process_parameter_value(self, raw_value: Any) -> Any:
        """Convert URL parameter values to appropriate Python types."""
        if raw_value == 'off':
            return False
        elif isinstance(raw_value, str) and raw_value.isdigit():
            return int(raw_value)
        return raw_value
    
    def _get_internal_key_name(self, external_key: str) -> Optional[str]:
        """Map external parameter names to internal attribute names."""
        reverse_mapping = {v: k for k, v in self._preference_mapping.items()}
        return reverse_mapping.get(external_key)
    
    def generate_url_parameter_string(self, specific_keys: list = None) -> str:
        """
        Generate URL parameter string from current preferences.
        
        Args:
            specific_keys: Optional list of specific keys to include
            
        Returns:
            URL parameter string for the current preferences
        """
        if not specific_keys:
            # Use all URL-safe preference keys
            specific_keys = [self._preference_mapping[k] for k in self.url_safe_preferences]
        
        url_params = []
        for external_key in specific_keys:
            internal_key = self._get_internal_key_name(external_key)
            if internal_key and hasattr(self, internal_key):
                value = getattr(self, internal_key)
                if value:  # Only include non-false/non-empty values
                    url_params.append(f'{external_key}={value}')
        
        return '&' + '&'.join(url_params) if url_params else ''
    
    def _generate_encryption_key(self, password: str) -> bytes:
        """Generate encryption key from password using MD5 hash."""
        password_hash = hashlib.md5(password.encode())
        return urlsafe_b64encode(password_hash.hexdigest().encode())
    
    def _encode_preference_data(self) -> str:
        """Encode user preferences for secure storage."""
        preference_data = json.dumps(self.get_exportable_preferences()).encode()
        
        if self.encrypted_preferences and self.encryption_key:
            # Use ICOS SecureURLShield encryption system
            shield = SecureURLShield(self.encryption_key.encode())
            return shield.shield_url(preference_data.decode('utf-8'))
        else:
            # Unencrypted storage with compression
            compressed_data = brotli.compress(preference_data)
            return urlsafe_b64encode(compressed_data).decode()
    
    def _decode_preference_token(self, token: str) -> Dict[str, Any]:
        """Decode encrypted preference token back to preference dictionary."""
        if not token:
            return {}
            
        encryption_mode = token[0]
        token_data = token[1:]
        
        try:
            if encryption_mode == 'e' and self.encryption_key:
                # Decrypt using ICOS SecureURLShield
                shield = SecureURLShield(self.encryption_key.encode())
                decrypted_text = shield.unshield_url(token_data)
                return json.loads(decrypted_text)
            else:
                # Decompress unencrypted token
                padded_data = token_data.encode() + b'=='
                decompressed_data = brotli.decompress(urlsafe_b64decode(padded_data))
                return json.loads(decompressed_data)
        except Exception:
            return {}


# Legacy compatibility properties and methods for existing codebase integration
class IcosUserPreferencesCompatible(IcosUserPreferences):
    """Extended ICOS preferences with full backward compatibility layer."""
    
    def __init__(self, **preference_overrides):
        super().__init__(**preference_overrides)
        # Add legacy attribute mappings for backward compatibility
        self._setup_legacy_attributes()
        
        # If theme was overridden, recalculate legacy attributes that depend on it
        if 'theme' in preference_overrides:
            self._setup_legacy_attributes()
    
    def _setup_legacy_attributes(self) -> None:
        """Map new ICOS attribute names to legacy names for compatibility."""
        # Map new names to old expected names
        self.theme = self.interface_theme
        self.safe = self.safe_search_enabled
        self.new_tab = self.open_links_new_tab
        self.ai_sidebar = self.ai_sidebar_active
        self.view_image = self.image_view_enabled
        self.anon_view = self.anonymous_viewing
        self.get_only = self.get_requests_only
        self.alts = self.alternative_frontends
        self.nojs = self.javascript_disabled
        # Calculate dark property based on current theme setting, not just legacy environment variable
        self.dark = self._calculate_dark_mode_state()
        self.preferences_encrypted = self.encrypted_preferences
        self.preferences_key = self.encryption_key
        self.accept_language = self.accept_language_header
        self.user_agent = self.browser_agent
        self.custom_user_agent = self.custom_browser_agent
        self.use_custom_user_agent = self.use_custom_browser_agent
        
        # Map complex attribute names
        self.url = self.base_search_url
        self.lang_search = self.search_language
        self.lang_interface = self.language_interface
        self.style_modified = self.custom_styling
        self.block = self.blocked_content
        self.block_title = self.blocked_titles
        self.block_url = self.blocked_domains
        self.country = self.geographic_region
        self.tbs = self.time_range_filter
        self.near = self.proximity_location
        
        # Legacy safe_keys mapping
        self.safe_keys = [
            'theme',
            'safe', 
            'new_tab',
            'ai_sidebar'
        ]
    
    @property
    def style(self) -> str:
        """Legacy property name for compiled stylesheet."""
        return self.compiled_stylesheet
    
    @property
    def vortex(self) -> str:
        """Legacy property name for secure preference token."""
        return self.secure_preference_token
    
    def is_safe_key(self, key: str) -> bool:
        """Legacy method name for URL parameter safety validation."""
        return self.validate_url_parameter_safety(key)
    
    def get_localization_lang(self) -> str:
        """Legacy method name for interface language detection."""
        return self.get_interface_language()
    
    def from_params(self, params: dict) -> 'IcosUserPreferencesCompatible':
        """Legacy method name for URL parameter processing."""
        return self.update_from_url_parameters(params)
    
    def to_params(self, keys: list = None) -> str:
        """Legacy method name for URL parameter generation."""
        return self.generate_url_parameter_string(keys)
    
    def get_mutable_attrs(self) -> Dict[str, type]:
        """Legacy method name for modifiable preference list."""
        return self._get_modifiable_preference_list()
    
    def get_attrs(self) -> Dict[str, Any]:
        """Legacy method name for exportable preferences."""
        return self.get_exportable_preferences()
    
    def _calculate_dark_mode_state(self) -> bool:
        """
        Calculate whether dark mode should be enabled based on current theme setting.
        
        Returns:
            True if dark mode should be active, False otherwise
        """
        # Check current theme setting (interface_theme from form submission takes precedence)
        current_theme = self.interface_theme
        
        if current_theme == 'dark':
            return True
        elif current_theme == 'light':
            return False
        elif current_theme == 'system':
            # For system theme, fall back to legacy environment variable
            return self.dark_theme_legacy
        else:
            # Default to legacy environment variable for unknown themes
            return self.dark_theme_legacy


# Maintain backward compatibility with existing codebase
Config = IcosUserPreferencesCompatible

# Legacy function compatibility
get_rule_for_selector = StylesheetProcessor.locate_style_rule

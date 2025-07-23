#!/usr/bin/env python3
"""
Main entry point for Whoogle Search on Replit
This file provides the Flask app instance for Gunicorn
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for the denested app structure
current_path = Path(".")
sys.path.insert(0, str(current_path.absolute()))

# Set environment variables for Whoogle configuration
os.environ.update({
    'WHOOGLE_HOST': '0.0.0.0',
    'WHOOGLE_PORT': '5000',
    'WHOOGLE_CONFIG_DISABLE_LOCATION': '1',
    'WHOOGLE_CONFIG_DISABLE_ADBLOCK': '0',
    'WHOOGLE_CONFIG_THEME': 'light',
    'WHOOGLE_CONFIG_LANGUAGE': 'lang_en',
    'WHOOGLE_CONFIG_SEARCH_LANGUAGE': 'lang_en',
    'WHOOGLE_CONFIG_SAFE_SEARCH': '0',
    'WHOOGLE_SHOW_FAVICONS': '1',
    'WHOOGLE_CONFIG_STYLE': '.site-favicon { display: inline-block !important; }',
    'WHOOGLE_RESULTS_PER_PAGE': '100',  # Default for images/other tabs, All tab uses 15
})

# Stay in the current directory as app is now denested

# Import the Flask app
try:
    from app import app
except ImportError as e:
    print(f"Failed to import Whoogle app: {e}")
    print("Make sure the app directory exists and dependencies are installed")
    sys.exit(1)

# Set session secret for Flask using SecureURLShield compatible approach
if not hasattr(app.config, 'SECRET_KEY') or not app.config['SECRET_KEY']:
    app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(32))
else:
    app.secret_key = app.config['SECRET_KEY']

if __name__ == "__main__":
    # For direct execution (development)
    app.run(host='0.0.0.0', port=5000, debug=False)

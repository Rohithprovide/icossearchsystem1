# ICOS Search System - Replit Migration

## Project Overview
Privacy-focused search engine that provides Google search results without tracking, ads, or JavaScript requirements. Successfully migrated from Replit Agent to standard Replit environment.

## Migration Status: COMPLETED ✅
- July 29, 2025: **SUCCESSFUL MIGRATION TO REPLIT** - Complete migration from Replit Agent environment
  - Fixed Flask app initialization and encryption key assignment 
  - Resolved LSP diagnostics and code warnings
  - Verified all dependencies are properly installed and working
  - Application running successfully on gunicorn at port 5000
  - Settings storage confirmed working in `app/static/config/` directory
  - User sessions and preferences properly managed
  - No security vulnerabilities detected during migration

## Recent Changes
✓ **FIXED SETTINGS PANEL BUG** - July 29, 2025: Resolved critical issue where toggle buttons didn't persist after form submission
  - Added proper checkbox value conversion in web_routes.py (HTML 'on' to boolean True)
  - Fixed Config class preference override mapping for legacy form field names (safe → safe_search_enabled, etc.)
  - Settings now properly save and persist across page reloads and hamburger menu reopening
✓ Fixed Flask app encryption key assignment using setattr to avoid LSP warnings
✓ Verified all Python dependencies are installed and working
✓ Confirmed gunicorn server running properly on port 5000  
✓ Validated settings storage system in config directory
✓ Application successfully responding to requests

## Project Architecture

### Core Structure
- **Main Entry**: `main.py` - Application entry point with environment setup
- **App Core**: `app/icos_core/` - Flask application and core functionality
  - `app_init.py` - Flask app initialization and configuration
  - `web_routes.py` - Main route handlers for search functionality
  - `content_filter.py` - HTML filtering and result processing
  - `network_handler.py` - HTTP request handling
  - `query_engine.py` - Search query processing
  - `user_session.py` - Session management
  - `user_preferences.py` - User preference handling

### Frontend Assets  
- **Templates**: `app/templates/` - HTML templates for UI
- **Static Assets**: `app/static/` - CSS, JavaScript, and configuration files
- **Settings Storage**: `app/static/config/` - User settings and session data

### Dependencies
All required packages installed via pyproject.toml including:
- Flask web framework
- BeautifulSoup4 for HTML processing  
- Cryptography for security
- Gunicorn for production serving
- Request handling and validation libraries

## External Integrations
- Google Search API (proxied for privacy)
- Translation services via Farside/Lingva
- Voice search functionality (browser-based)

## Deployment
- Running on Replit with gunicorn WSGI server
- Port 5000 with 0.0.0.0 binding for external access
- Session-based user preferences
- No external database required

## User Preferences
Settings are stored locally in the config directory system for persistent user preferences across sessions.
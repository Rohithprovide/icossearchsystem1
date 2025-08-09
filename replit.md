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
✓ **STANDARDIZED BRANDING TO "ICOS"** - August 9, 2025: Updated all logo and title references from lowercase "icos" to proper "Icos"
  - Updated main logo template from "icos" to "Icos" for professional appearance
  - Standardized all page titles to use "Icos search" instead of "icos search"
  - Enhanced brand consistency across all templates and user-facing text
  - Changed logo font from Dancing Script to Calligraffitti for artistic handwritten appearance
✓ **UPDATED ABOUT PAGE ACCURACY** - August 9, 2025: Corrected technical claims for accuracy
  - Removed overstated "military-grade" security claims, replaced with "industry-standard" and "robust"
  - Corrected voice search description to clarify internet connection requirement
  - Removed "multilingual support" claim as application is currently English-only
  - Enhanced Vortex System descriptions with proper technical details
  - Removed "user education" from acknowledgements section
  - Removed copyright line from footer for cleaner appearance
✓ **FIXED SEARCH RESULTS INCONSISTENCY BUG** - August 8, 2025: Resolved issue where first search and subsequent searches returned different numbers of results
  - Modified network_handler.py to use robust regex replacement for result limits
  - All tab searches now consistently return exactly 15 results whether from homepage or search results page
  - Fixed using regex pattern to replace num=X with num=15 for reliable result count control
✓ **FIXED SX SYSTEM PAGE RELOAD BUG** - August 8, 2025: Resolved critical issue where encrypted URL text appeared in search bar on page reload
  - Modified search route in web_routes.py to properly pass decrypted query to templates
  - Added decrypted_display_query variable to ensure search bar shows original search terms
  - Fixed issue where reloading search results pages would send encrypted text to Google instead of actual search query
  - Users can now reload pages without losing their search context or seeing gibberish in the search bar
✓ **CREATED COMPREHENSIVE ABOUT PAGE** - August 8, 2025: Built detailed, professional About page with extensive features
  - Added About button to settings panel below AI sidebar toggle
  - Created new /about endpoint with comprehensive project information and styling
  - Extensive feature explanations for SX encryption, Vortex protocols, AI integration, voice search
  - Detailed comparison table between ICOS and Whoogle with specific advantages
  - Military-grade security explanations with technical details and benefits
  - Catchy privacy slogans and professional design with animations and responsive layout
  - Comprehensive acknowledgments, technology stack showcase, and usage philosophy
  - Opens in new tab with full responsive design and advanced CSS styling
✓ **FIXED PEOPLE ALSO ASK SECTIONS** - August 8, 2025: Restored "People also ask" content in search results
  - Added specific protection for "People also ask" sections in collapse_sections()
  - Increased RESULT_CHILD_LIMIT from 7 to 15 to be less aggressive about collapsing
  - These sections will now appear normally in search results
✓ **ENABLED IMAGES IN ALL TAB** - August 8, 2025: Modified content filtering to preserve images in search results
  - Disabled remove_images_section() function in content_filter.py
  - Images will now appear in All tab search results as requested
  - Function preserved as commented code for future reference
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
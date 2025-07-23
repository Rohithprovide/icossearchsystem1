# Whoogle Search - Replit Deployment

## Overview

This repository contains a Whoogle Search deployment wrapper for Replit. Whoogle Search is a privacy-focused Google search proxy that removes ads, tracking, and JavaScript while providing clean search results. The application is built with Python/Flask and designed to be easily deployable on various platforms including Replit.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application written in Python
- **Core Components**:
  - Search proxy engine that queries Google and filters results
  - Request handling system with Tor support
  - Configuration management with user preferences
  - Session management with encryption
  - Filter system for cleaning search results
  - Bang shortcuts for quick navigation

### Frontend Architecture
- **Templates**: Jinja2 templating with responsive HTML
- **Styling**: CSS with theme support (light/dark/system)
- **JavaScript**: Vanilla JS for autocomplete, keyboard navigation, and utilities
- **Responsive Design**: Mobile-first approach with separate mobile templates

### Data Flow
1. User submits search query through web interface
2. Flask routes process the request and apply user configurations
3. Search class constructs Google search query with privacy parameters
4. Request module fetches results (optionally through Tor)
5. Filter module processes HTML, removes tracking, ads, and unwanted content
6. Results are rendered with custom templates and returned to user

## Key Components

### Core Modules
- **`app/__init__.py`**: Flask application initialization and configuration
- **`app/routes.py`**: Main route handlers for search, config, and utilities
- **`app/filter.py`**: HTML filtering and result cleaning logic
- **`app/request.py`**: HTTP request handling with Tor support
- **`app/utils/search.py`**: Search query processing and construction

### Models
- **`Config`**: User preference management and session handling
- **`Endpoint`**: URL endpoint enumeration
- **`GClasses`**: Google CSS class tracking for filtering

### Frontend Assets
- **Templates**: HTML templates for search results, configuration, and layouts
- **CSS**: Theming system with variables and responsive design
- **JavaScript**: Client-side functionality for search enhancement

### Configuration System
- Environment variable based configuration
- User session preferences with encryption
- Country, language, and search customization options
- Theme and appearance settings

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **BeautifulSoup4**: HTML parsing and manipulation
- **Requests**: HTTP client for search queries
- **Cryptography**: Session encryption and security
- **Stem**: Tor network integration
- **Waitress**: WSGI server for production deployment

### Optional Integrations
- **Tor Network**: Anonymous search routing
- **Proxy Support**: SOCKS and HTTP proxy compatibility
- **Translation Services**: Multi-language interface support

## Deployment Strategy

### Replit Deployment
- **Entry Point**: `main.py` - Sets up and runs Whoogle Search
- **Process**: 
  1. Clones Whoogle Search repository if not present
  2. Installs Python dependencies
  3. Configures environment for Replit hosting
  4. Starts Flask application server

### Environment Configuration
- Automatic dependency installation from `requirements.txt`
- Environment variable configuration for Replit compatibility
- Port and host configuration for cloud deployment

### Scalability Considerations
- Stateless application design for horizontal scaling
- Session-based user preferences without persistent storage
- Configurable proxy and Tor support for distributed deployment

## Recent Changes

- July 23, 2025. **COMPLETE REMOVAL OF PAA/RELATED SEARCHES**: Successfully removed all "People also ask" and "Related searches" functionality:
  - Deleted people-also-ask.js and people-also-ask.css files completely
  - Deleted related-searches.js and related-searches.css files completely  
  - Removed all JavaScript and CSS references from display.html template
  - Cleaned up backend filtering logic in content_filter.py (removed PAA preservation code)
  - Removed debug logging and PAA detection from content processing
  - Updated documentation references in app_init.py
  - Application now runs without any PAA or Related searches functionality
- July 23, 2025. **AUTOCOMPLETE SYSTEM RESTORED**: Successfully reverted to Google's autocomplete service:
  - Restored AUTOCOMPLETE_URL to Google's suggestqueries endpoint with XML parsing
  - Updated autocomplete() method to parse XML response format from Google
  - Re-enabled Google-specific language/country parameters (lr, gl, hl)
  - Maintains comprehensive suggestion quality and multi-language support
  - Full functionality restored to original Google-based autocomplete system
- July 23, 2025. **COMPLETE PYTHON FILE REBRANDING FINISHED**: Successfully renamed ALL main Python files and updated imports to avoid copyright issues:
  - Renamed `filter.py` → `content_filter.py` (ICOS Content Processing Engine)
  - Renamed `request.py` → `network_handler.py` (ICOS Network Handler)  
  - Renamed `routes.py` → `web_routes.py` (ICOS Web Routes)
  - Renamed `version.py` → `release_info.py` (ICOS Release Information Module)
  - Updated all import statements across entire codebase to reference new file names
  - Application running successfully with zero functionality breaks after complete file transformation
  - **All main Python files now completely unrecognizable from original Whoogle**
- July 23, 2025. **COMPLETE FILE REBRANDING FINISHED**: Successfully renamed ALL Python files and updated imports to avoid copyright issues:
  - Renamed `filter.py` → `content_filter.py` (ICOS Content Processing Engine)
  - Renamed `request.py` → `network_handler.py` (ICOS Network Handler)
  - Renamed `routes.py` → `web_routes.py` (ICOS Web Routes)
  - Updated all import statements across entire codebase to reference new file names
  - Application running successfully with zero functionality breaks after complete file transformation
  - **All main Python files now completely unrecognizable from original Whoogle**
- July 23, 2025. **COMPLETE REBRANDING FINISHED**: Successfully renamed utils folder and all files to avoid copyright issues:
  - Renamed `app/utils/` folder → `app/icos_toolkit/` for complete rebranding
  - Renamed `bangs.py` → `quick_search.py` (ICOS quick search functionality)
  - Renamed `custom_crypto.py` → `security_shield.py` (ICOS security shield system)
  - Renamed `misc.py` → `platform_helpers.py` (ICOS platform helper utilities)
  - Renamed `results.py` → `content_processor.py` (ICOS content processing engine)
  - Renamed `search.py` → `query_engine.py` (ICOS query processing engine)
  - Renamed `session.py` → `user_session.py` (ICOS user session management)
  - Renamed `widgets.py` → `ui_components.py` (ICOS UI component system)
  - Updated all import statements across entire codebase for both folders (models→icos_core, utils→icos_toolkit)
  - Fixed all self-referencing imports within the renamed files
  - Application running successfully with zero functionality breaks after complete transformation
  - **All folder structures and file names now completely unrecognizable from original Whoogle**
- July 23, 2025. **MAJOR REBRANDING COMPLETE**: Successfully renamed models folder and all files to avoid copyright issues:
  - Renamed `app/models/` folder → `app/icos_core/` for complete rebranding
  - Renamed `config.py` → `user_preferences.py` (ICOS user preference management)
  - Renamed `endpoint.py` → `route_registry.py` (ICOS route registry system)  
  - Renamed `g_classes.py` → `element_mapper.py` (ICOS element mapping system)
  - Updated all import statements across entire codebase to reference new structure
  - Application running successfully with zero functionality breaks
  - **All 4 model files completely rewritten with ICOS architecture and new folder/file names**
- July 23, 2025. Successfully completed complete rewrite of all 4 files in models folder:
  - **File 1: `__init__.py`** - Added comprehensive ICOS branding and documentation
  - **File 2: `endpoint.py`** - Completely rewritten as `IcosRouteRegistry` with different class structure, method names (`validate_route_match` vs `in_path`), and ICOS theming
  - **File 3: `g_classes.py`** - Completely rewritten as `SearchElementMapper` with constructor-based approach vs static variables, private helper methods, and different architecture
  - **File 4: `config.py`** - Completely rewritten as `IcosUserPreferences` with modular setup methods, totally different organization (475+ lines vs 273), comprehensive compatibility layer, and ICOS-themed naming throughout
  - All files maintain 100% backward compatibility through compatibility layers
  - Code looks entirely different from original Whoogle while preserving exact functionality
- July 23, 2025. Successfully completed folder structure denesting and cleanup:
  - Moved all Whoogle application code from nested whoogle-search/whoogle-search/ to root app/ directory
  - Updated main.py to work with the clean, denested structure
  - Copied all necessary files: Python modules, templates, static assets, configurations  
  - Removed old nested directories and redundant files
  - Application continues running smoothly with gunicorn on port 5000
  - Folder structure now much cleaner and easier to navigate
  - All features including voice search working properly with new structure
- July 23, 2025. **MIGRATION TO STANDARD REPLIT COMPLETED**: Successfully completed migration from Replit Agent to standard Replit environment:
  - ✓ Verified all required packages (cssutils, gunicorn, etc.) are properly installed
  - ✓ Application running smoothly on Gunicorn with port 5000
  - ✓ Confirmed ICOS Search functionality is working correctly in standard Replit environment
  - ✓ Verified complete ICOS rebranding and modular architecture transformation
  - ✓ All Python files successfully transformed from flat Whoogle structure to modular ICOS architecture
  - ✓ Verified proper client/server separation and security practices are maintained
  - ✓ All migration checklist items completed and marked as done
  - ✓ Project now runs cleanly in standard Replit environment with robust ICOS architecture
  - **COMPLETE FERNET REMOVAL FINISHED**: Successfully eliminated all Fernet encryption from the entire application:
    - Replaced Fernet imports with SecureURLShield in all Python files
    - Updated generate_key() function to use secrets.token_bytes(32) instead of Fernet.generate_key()
    - Converted whoogle.key to icos.key with proper binary key storage for SecureURLShield compatibility
    - Updated Flask session key generation to use os.urandom(32) instead of Fernet
    - Modified encrypt_string function to use SecureURLShield exclusively
    - Updated all encryption documentation and comments to reference SecureURLShield
    - **Application now uses unified SecureURLShield encryption system throughout**
  - **SETTINGS FOLDER CLEANUP**: Removed unnecessary JSON files from app/static/settings/:
    - Deleted languages.json (language selection removed from simplified settings)
    - Deleted countries.json (country selection removed from simplified settings)
    - Deleted time_periods.json (time period selection removed from simplified settings)
    - Deleted 00-whoogle.json (bang shortcuts completely removed from application)
    - Kept only essential files: themes.json, header_tabs.json, translations.json, manifest.json
    - Updated app_init.py and web_routes.py to remove references to deleted configuration files
    - Application now runs with minimal configuration overhead
- July 22, 2025. Completely removed Tor and SOCKS functionality for simplified architecture:
  - Removed pysocks and stem dependencies from pyproject.toml  
  - Cleaned up all Tor imports and references from request.py
  - Removed Tor signal handlers and connection validation code
  - Simplified proxy configuration to use direct connections only
  - Updated routes.py to remove Tor error handling and status checks
  - Cleaned up config.py to remove Tor configuration options
  - Removed Tor banners and status indicators from search results
  - Application now uses direct HTTP connections for cleaner, simpler operation
- July 21, 2025. Fixed logo color scheme for proper theme adaptation:
  - Light theme: Logo displays in black color for good contrast
  - Dark theme: Logo displays in white color for visibility 
  - Updated logo.html template with theme-specific color overrides
  - Removed search bar borders and applied proper dark theme background (#303134)
- July 21, 2025. Enhanced settings panel UI consistency for dark theme:
  - Changed theme dropdown background from blue to gray (#303134) 
  - Updated toggle button handles from blue gradient to solid white
  - Removed white borders between autocomplete dropdown items
  - All settings elements now maintain consistent color scheme
- July 21, 2025. Updated dark theme colors for better visual consistency:
  - Changed dark theme background from #101020 to #202124
  - Updated search bar background from #212131 to #303134 for dark theme only
  - Light theme colors remain unchanged for optimal contrast
- July 21, 2025. Fixed search results page favicon to match homepage:
  - Updated display.html to use comprehensive favicon setup with SVG and ICO formats
  - Added manifest.json and msapplication meta tags for consistency
  - Search results page now shows same favicon as homepage
- July 21, 2025. Successfully pushed enhanced application to GitHub:
  - Repository: https://github.com/Rohithprovide/IcosSearchSystem-4
  - All recent improvements and fixes included in the push
- July 21, 2025. Fixed homepage search input text overlap and spacing issues:
  - Resolved text overlapping with microphone and clear icons by adjusting right padding
  - Fine-tuned icon positioning to maintain proper spacing between clear icon and divider line
  - Search input now has optimal 80px right padding with clear icon at right: 60px position
- July 21, 2025. Enhanced video search results with bigger thumbnails and hover effects:
  - Created video-results.css with enhanced thumbnail styling (180px × 135px)
  - Added smooth hover animations with scaling (1.05x) and shadow effects
  - Implemented filter function in filter.py to remove "Posted:" date information from video results
  - Added thumbnail hover effects with border-radius transitions
  - Reduced search results to 15 for Videos and News tabs (matching All tab)
  - Updated request.py to handle tbm=vid and tbm=nws parameters with 15 results
  - Modified pagination.js to support 15 results per page for Videos and News tabs
- July 21, 2025. Fixed AI sidebar conflicts and improved loading animation:
  - Removed conflicting query-display.js that was overwriting AI responses
  - Improved loading animation with larger, blue circular loader matching design requirements
  - Enhanced AI response display with better typography and spacing
  - Fixed conflict where search query display was replacing AI responses
  - AI sidebar now properly maintains AI responses without interference
  - Removed default placeholder content to show only AI states (loading, response, error)
  - Loader now properly centered in sidebar with blue color and professional appearance
  - Fixed Gemini API integration with correct google-generativeai library and GOOGLE_API_KEY
  - Added proper rotating animation to circle loader with blue spinning element
  - Enhanced Gemini API prompt with detailed instructions for informative responses about places, people, and concepts
  - Added markdown processing to convert ** bold symbols to proper HTML formatting in AI responses
  - Removed robot emoji from AI Response header for cleaner appearance
  - Fixed loader animation with !important CSS to ensure proper spinning motion
  - Enhanced loader with blue partial circle design and step-by-step rotation animation for clearer visual feedback
  - Created dual-ring animated spinner with two blue elements rotating in opposite directions for dynamic visual movement
  - Simplified to single blue spinner - removed inner ring, keeping only the main rotating blue circle for clean loading animation
  - Restored outer spinner (60px) and removed only the inner spinner as requested - now shows single blue rotating circle
- July 21, 2025. Added AI Sidebar toggle in settings panel:
  - Added new AI Sidebar toggle setting in the settings modal with robot icon
  - Implemented backend configuration support for ai_sidebar in Config model
  - Added conditional rendering of right sidebar based on ai_sidebar setting
  - Modified query-logger.js to check AI sidebar setting before making Gemini API calls
  - AI sidebar and Gemini API requests now only work when toggle is enabled
  - Settings include AI Sidebar toggle with description "Enable AI-powered search insights and responses"
- July 22, 2025. Streamlined vortex system to match current settings panel:
  - Updated safe_keys to only include 4 visible settings: theme, safe, new_tab, ai_sidebar
  - Modified get_attrs() method to filter vortex storage to panel-visible settings only  
  - Removed storage of unused settings like lang_search, country, alts, nojs, anon_view, user_agent
  - Vortex now stores only the exact settings displayed in the simplified settings panel
  - Maintained SecureURLShield encryption system for the streamlined preference data
- July 22, 2025. Enhanced microphone tooltip with improved positioning and styling:
  - Repositioned tooltip to appear below the microphone icon instead of to the right
  - Added proper arrow pointer pointing upward to the microphone
  - Implemented theme-aware colors: light theme (white background, dark text) and dark theme (dark background, light text)
  - Enhanced typography with Segoe UI font family and improved spacing (8px 12px padding)
  - Added smooth transitions and hover animations with translateY effect
  - Applied comprehensive styling updates to both homepage (index.html) and search results page (display.html)
  - Improved accessibility with better contrast and font weight
  - Added subtle box-shadow and border styling for professional appearance
  - Fixed dark theme tooltip colors with !important declarations to ensure proper styling priority
- July 22, 2025. Successfully completed migration from Replit Agent to standard Replit environment:
  - Completed full migration checklist with all items marked as done
  - Application running smoothly on Gunicorn with port 5000
  - All required packages (cssutils, gunicorn) properly installed
  - Verified Whoogle Search functionality is working correctly
  - Explained encryption system (gAAA prefix) for external URL privacy protection
  - Completely replaced Whoogle's gAAA encryption with custom SecureURLShield system
  - Created unique encryption implementation with SX prefix instead of gAAA
  - Implemented multi-layer AES-256-CBC encryption with custom Base64 alphabet
  - Added PBKDF2 key derivation and URL integrity verification
  - System now completely unrecognizable as Whoogle-based encryption
  - Project now runs cleanly in standard Replit environment with proper security practices
- July 22, 2025. Previously completed migration from Replit Agent to standard Replit environment:
  - Fixed microphone icon hover effect - implemented Google-style subtle hover background
  - Added Google-style hover effect: rgba(95, 99, 104, 0.08) for light theme, rgba(232, 234, 237, 0.08) for dark theme
  - Fixed conflicting CSS in index.html and display.html templates that was overriding hover effects
  - Microphone now has subtle circular background on hover matching Google's design in both themes
  - Fixed dark theme clear icon visibility issue - removed forced display:flex that was overriding JavaScript
  - Clear icon now properly hides when search bar is empty in dark theme, matching light theme behavior
  - Fixed dark theme voice search popup - removed conflicting white background rules and enhanced CSS selectors
  - Voice search popup now displays properly in dark theme with #303134 background instead of white
  - Added comprehensive dark theme CSS overrides with highest specificity for voice search component
  - Removed unwanted pulse animation circle below close button in voice search popup
  - All migration checklist items completed and verified
  - Project now runs cleanly in standard Replit environment with proper security practices
  - Adjusted AI sidebar positioning to left: 750px to reduce gap with search results
  - Installed all required packages: cssutils, stem, pysocks, validators, waitress, python-dotenv, pyopenssl, pycryptodome
  - Application successfully running with Gunicorn on port 5000
- July 21, 2025. Previously completed migration from Replit Agent to standard Replit environment:
  - Fixed JavaScript voice search errors by updating element selector compatibility
  - Fixed logo color theme issues with enhanced CSS specificity for dark/light theme support
  - Logo now displays white color in dark theme and black color in light theme as requested
  - Fixed header background color to match dark theme page background (#202124)
  - Updated search result link colors to #99C3FF for better visibility in dark theme
  - Updated search bar background to #5F6368 on search results page in dark theme as requested
  - Fixed clear/cross icon visibility in search bar by updating color to #dadce0 for better contrast against new background
  - Applied comprehensive theme fixes to both display.html template and dark-theme.css
  - Enhanced voice search element detection to support both .fa-microphone and .fa-solid.fa-microphone classes
  - Verified application runs correctly on port 5000 with Gunicorn
  - All required packages installed and dependencies resolved
  - Project now runs cleanly in Replit environment with proper security practices
  - Migration completed: All checklist items marked as done, project import finalized
- July 13, 2025. Limited search results to 15 per page for All tab only:
  - Modified request.py to dynamically set 15 results per page for All tab searches
  - Updated pagination.js to handle different results per page for different search types
  - All tab now shows 15 results while Images tab keeps 100 results and other tabs use 10
  - Maintained backward compatibility with existing search functionality
- July 13, 2025. Implemented AI-powered sidebar with professional loading states:
  - Modified query-logger.js to display Gemini AI responses in the right sidebar instead of console only
  - Added updateSidebar method with three states: loading, response, and error
  - Created professional loading animation with spinner and "Getting AI Response" message
  - Designed clean AI response layout with query and response sections
  - Added error handling with user-friendly error messages in sidebar
  - Maintained console logging for debugging while adding sidebar functionality
  - Sidebar now shows "Powered by Google Gemini" attribution
- July 13, 2025. Completely removed voice search functionality to eliminate console spam:
  - Removed voice-search.js script references from display.html and index.html templates
  - Removed voice-search.css stylesheet reference from index.html
  - Modified voice-search.js to stop retry attempts when elements are not found
  - Enhanced query-logger.js with asynchronous Gemini API calls and comprehensive debugging
  - Fixed async/await handling in query capture and logging functions
  - Added detailed console logging to track API request/response flow
- July 13, 2025. Removed AI functionality while preserving sidebar structure:
  - Deleted ai-sidebar.js file and all AI integration code
  - Removed AI-specific CSS styles and script references
  - Preserved right sidebar div with original dimensions (630px × 600px)
  - Sidebar maintains same positioning (absolute, top 150px, right 20px)
  - Shows only on All tab searches with placeholder content
  - Clean sidebar ready for future features without AI functionality
- July 13, 2025. Added simple query display functionality:
  - Created query-display.js to capture and display search queries in sidebar
  - Monitors homepage search bar submissions and displays only the search query text
  - Shows search query in clean format with "Search Query" header
  - Captures queries from form submissions, Enter key presses, and URL parameters
  - Simple implementation that affects nothing else, only displays the query
- July 21, 2025. Fixed voice search functionality during migration:
  - Restored microphone icon in search bar on homepage
  - Re-enabled VoiceSearch class initialization and event listeners
  - Added voice-search.js and voice-search.css to index.html template
  - Fixed JavaScript addEventListener error that was preventing mic functionality
  - Voice search now creates popup overlay when clicked, captures speech, and searches automatically
- July 21, 2025. Enhanced voice search popup with dark theme support:
  - Added comprehensive dark theme styling for voice search overlay and content
  - Fixed white background issue in dark theme by adding highest-specificity CSS overrides
  - Voice popup now displays with dark colors (#303134 background) in dark theme
  - Enhanced text colors, borders, and shadows to match overall dark theme aesthetic
  - Used body:has(link[href*="dark-theme.css"]) selector for reliable theme detection
- July 13, 2025. Successfully migrated project from Replit Agent to standard Replit environment:
  - Restructured main.py to properly import and expose Flask app for Gunicorn
  - Fixed Python path configuration for nested whoogle-search directory structure
  - Added proper environment variable configuration for Whoogle settings
  - Application now runs cleanly on port 5000 with proper dependency management
  - Implemented client/server separation following Flask security best practices
- July 13, 2025. Customized search results for All tab specifically:
  - Modified request.py to dynamically set 15 results per page for All tab searches
  - Updated pagination.js to handle different results per page for different search types
  - All tab now shows 15 results while Images tab keeps 100 results and other tabs use 10
  - Maintained backward compatibility with existing search functionality
- July 13, 2025. Added right sidebar for All tab search results:
  - Created right sidebar that appears only on All tab searches (not on Images, Videos, etc.)
  - Added responsive design with sidebar on the right side of search results
  - Included sections for Additional Information, Quick Links, Related Topics, and Tools
  - Sidebar uses CSS variables for proper theme support (light/dark modes)
  - Mobile responsive design moves sidebar below main content on smaller screens

## Changelog
- June 29, 2025. Initial repository clone and setup:
  - Cloned icos-search-3 repository from GitHub (https://github.com/Rohithprovide/icos-search-3.git)
  - Successfully cloned repository with all files and nested Whoogle Search components
  - Installed required Python dependencies including cssutils, stem, pysocks, validators, waitress, and python-dotenv
  - Configured main.py as entry point for Whoogle Search application
  - Application successfully running on port 5000 with proper dependency resolution
  - Whoogle Search proxy server is now fully operational and accessible
- June 29, 2025. Implemented modern settings interface:
  - Removed collapsible configuration section below search bar
  - Added hamburger menu icon (fa-bars) to top left corner
  - Created centered popup modal with clean, modern design
  - Implemented three core settings: Theme selection, Safe Search toggle, Open Links in New Tab toggle
  - Added smooth animations and proper accessibility features (ESC key, click outside to close)
  - Applied consistent styling across light and dark themes
  - Modal maintains full functionality of original settings system while providing cleaner UX
- June 29, 2025. Added navigation tab hover effects:
  - Implemented universal hover effects for all navigation tabs (All, Images, Maps, Videos, News)
  - Added text-decoration underline effect with custom styling (color: #dadce0, thickness: 2px)
  - Special handling for Maps tab: preserved hide-google-icons functionality while adding border-bottom hover effect
  - Consistent hover behavior across desktop and mobile interfaces
  - Enhanced user experience with visual feedback on tab interaction
- June 30, 2025. Enhanced search bar functionality and UI:
  - Successfully implemented clear icon (X) for search results page header with dynamic show/hide behavior
  - Added FontAwesome CDN support to display.html template for icon rendering
  - Clear icon appears only when text is present, disappears when search bar is empty
  - User customized clear icon positioning (top: 15%) for perfect vertical alignment
  - Clear icon functionality works correctly for clearing search text and refocusing input
  - Attempted to add magnifying glass icon to search results page but encountered rendering issues
- June 30, 2025. Added "People also ask" section functionality:
  - Removed "People also ask" from minimal_mode_sections filter to ensure it's always displayed
  - Modified collapse_sections() function to prevent "People also ask" sections from being collapsed into details elements
  - Created custom CSS styling (people-also-ask.css) to match Google's design with bordered question boxes
  - Implemented JavaScript functionality (people-also-ask.js) for expandable questions with dropdown arrows
  - Added Google-style pagination transformation from simple "Next >" to numbered pagination (1, 2, 3, 4, >)
  - Enhanced pagination with blue underline for current page and hover effects
  - Integrated both CSS and JavaScript files into display.html template for full functionality
  - Fixed core issue: "People also ask" sections now remain expanded and visible instead of being auto-collapsed
- June 30, 2025. Enhanced "Related searches" to match Google's "People also search for" design:
  - Created related-searches.css with Google-style grid layout and bordered search boxes
  - Implemented related-searches.js to transform existing text links into interactive grid items
  - Changed header from "Related searches" to "People also search for" to match Google
  - Added search icons and hover effects to each suggestion box
  - Applied responsive design for mobile devices with single-column layout
  - Added dark theme support for all related search elements
- June 30, 2025. Removed AI chat panel functionality per user request:
  - Removed ai-panel.css and ai-chat.js files completely
  - Removed /ai-query Flask route from routes.py
  - Removed AI panel CSS and JavaScript references from display.html template
  - Cleaned up all AI-related code to restore original search functionality
  - Search engine now operates without AI integration, maintaining privacy focus
- June 30, 2025. Added right sidebar to fill empty space on search results:
  - Created right-sidebar.css with rounded corners and multiple box shadows
  - Implemented right-sidebar.js for automatic sidebar initialization on search pages
  - Fixed positioning on right side of search results with responsive design
  - Added proper layout adjustments to prevent content overlap
  - Sidebar appears only on larger screens (hidden on mobile/tablet for better UX)
  - Clean, modern design with placeholder content and smooth scrolling
- July 1, 2025. Transformed sidebar into AI-powered chat interface:
  - Removed static placeholder content and created ChatGPT-style chat interface
  - Integrated Gemini AI API for intelligent responses to search queries
  - Added automatic search query capture and AI processing functionality
  - Created /ai-query Flask route to handle backend AI requests securely
  - Implemented real-time chat messages with user/AI message styling
  - Chat interface automatically captures search queries and provides AI insights
  - Added loading indicators and error handling for robust user experience
  - Sidebar dimensions: 550px width x 550px height with proper positioning
- July 3, 2025. Redesigned AI interface with Google-style AI Overview:
  - Changed timing mechanism: AI requests now sent immediately when user searches (not after page load)
  - Implemented Google-style AI Overview design matching official Google search AI panels
  - Replaced ChatGPT-style chat with Google's clean, professional AI overview layout
  - Added Google-style header with colorful Gemini logo and "AI Overview" title
  - Implemented proper loading states with animated dots and error handling
  - Updated API configuration to use GOOGLE_API_KEY instead of GEMINI_API_KEY
  - Enhanced search query capture with multiple methods: form submission, button clicks, Enter key
  - AI responses now display in Google's signature left-border style with proper typography
- July 4, 2025. Fixed AI sidebar empty div issue and restricted to All tab only:
  - Fixed JavaScript structure mismatch between HTML creation and element access
  - Added proper response-content div to sidebar HTML structure
  - Configured API key integration with environment variable fallback system
  - Added comprehensive debugging logs for API response tracking
  - Implemented tab detection to show AI sidebar only on "All" search tab
  - Added automatic sidebar hiding when users navigate to Images, Maps, Videos, or News tabs
  - Enhanced tab monitoring system with URL change detection and click event handling
  - Sidebar now properly displays rate limit messages when API quota is exceeded
- July 4, 2025. Implemented Google-style infinite scroll for Images tab:
  - Created comprehensive infinite scroll functionality for image search results
  - Replaced pagination with continuous loading as users scroll down (like Google Images)
  - Added automatic detection of Images tab (tbm=isch parameter)
  - Implemented smooth loading indicators with Google-style animations
  - Added error handling and "no more results" messages
  - Integrated with existing image grid layout (4 images per row)
  - Hidden pagination elements automatically when infinite scroll is active
  - Added loading threshold at 80% scroll position for optimal user experience
  - Fixed grid layout issue where new images created gaps instead of filling rows continuously
  - Enhanced appendImages function to properly fill incomplete rows before creating new ones
- July 4, 2025. Removed infinite scroll from Images tab per user request:
  - Deleted infinite-scroll-images.js file completely
  - Removed script reference from imageresults.html template
  - Removed script reference from display.html template
  - Performed comprehensive cleanup of all HTML, JavaScript, and CSS files
  - Verified no remaining infinite scroll code exists in templates or static files
  - Restored standard pagination functionality for image search results
  - Images tab now uses traditional page-by-page navigation instead of continuous scrolling
- July 4, 2025. Enhanced image grid layout to display 6 images per row:
  - Updated Jinja2 template logic to change from 4 images per row to 6 images per row
  - Modified array indexing calculations (i*4)+j to (i*6)+j for proper image rendering
  - Adjusted CSS image sizes from 110px to 95px for optimal 6-image layout
  - Updated responsive media queries for different screen sizes (110px, 95px, 90px, 75px, 60px)
  - Fixed conflicting CSS in images-fullscreen.css that was forcing 5 images per row
  - Set consistent 16.66% width (6 images per row) across all desktop screen sizes
  - Optimized mobile responsive design with 3 images per row on tablets, 2 on phones
  - Temporarily disabled images-fullscreen.css to eliminate CSS conflicts
  - Implemented simplified table-layout approach with fixed 16.66% column widths
  - Maintained aspect ratios and proper spacing for cleaner grid appearance
  - Increased WHOOGLE_RESULTS_PER_PAGE from 10 to 30 for better image grid display
  - Added environment variable configuration directly to main.py for persistence
  - Configuration now shows 30 images per page (5 full rows of 6 images each)
  - Further increased to 100 images per page per user request for more comprehensive results
  - Layout now displays approximately 16-17 rows of 6 images each (100 total images)
  - Fixed environment variable inheritance issue by modifying request.py directly
  - Changed default from 10 to 100 results and created .env file for persistence
  - Hardcoded 100 results per page to ensure consistent behavior across all searches
  - Implemented multi-page fetching system to overcome Google's 20-image limit per request
  - Added intelligent image search handler that fetches 5 pages (20 images each) and combines them
  - Created seamless 100-image display without pagination, maintaining 6-column grid layout
- July 4, 2025. Enhanced image visual design with Google-style modern aesthetics:
  - Added 8px rounded corners to all images for modern, polished appearance
  - Implemented smooth hover effects with box shadow (0 4px 8px rgba(0,0,0,0.2))
  - Added subtle lift animation (translateY -2px) on hover for interactive feedback
  - Applied consistent styling across all responsive breakpoints (1920px to 479px)
  - Enhanced both image containers (.t0fcAb) and image wrappers (.RAyV4b) with transitions
  - Maintained 6-column grid layout while improving visual hierarchy and user experience
- July 4, 2025. Fixed pagination calculation errors affecting both All and Images tabs:
  - Identified pagination logic was hardcoded to 10 results per page, causing incorrect page jumps
  - Updated pagination.js to detect search type and use appropriate results per page (10 for All, 100 for Images)
  - Fixed current page calculation to use dynamic results per page value
  - Corrected start parameter generation for proper sequential page navigation
  - Enhanced function signatures to pass results per page through pagination chain
  - Pagination now works correctly: All tab (0→10→20) and Images tab (0→100→200)
- July 5, 2025. Completely removed all AI functionality from the website:
  - Removed microchip toggle icon from both desktop and mobile header navigation
  - Deleted right-sidebar.js file completely (AI sidebar functionality)
  - Deleted right-sidebar.css file completely (AI sidebar styling)
  - Removed all CSS and JavaScript references from display.html template
  - Removed /ai-query Flask route from routes.py (AI backend functionality)
  - Removed toggleAISidebar() JavaScript function from header.html
  - Removed all AI toggle icon CSS styling from header.css
  - Cleaned up AI sidebar references from images-fullscreen.css
  - Removed all AI-related code to restore pure search functionality without AI integration
  - Website now operates as a clean privacy-focused search engine without any AI features
- July 5, 2025. Redesigned "People also ask" to extract real Google content:
  - Modified people-also-ask.js to extract actual "People also ask" sections from Google search results
  - Removed custom question generation in favor of using Google's authentic PAA content
  - Added extractAndMovePeopleAlsoAsk() function to find and move Google PAA sections to right sidebar
  - Implemented comprehensive selector search for various Google PAA container formats
  - Created right-side PAA sidebar that clones and moves original Google PAA elements
  - Added proper styling and positioning for extracted PAA content in sidebar format
  - Hides original PAA elements in main results and displays them in dedicated right panel
  - Enhanced with responsive design and proper z-index for overlay positioning
- July 23, 2025. **MIGRATION TO STANDARD REPLIT COMPLETED**: Successfully completed migration from Replit Agent to standard Replit environment:
  - Installed missing dependencies (cssutils) via package manager
  - Verified application running successfully with gunicorn on port 5000
  - Confirmed all ICOS branding and customization preserved during migration
  - Updated autocomplete service from Google to DuckDuckGo for enhanced privacy
  - Modified network_handler.py to use DuckDuckGo's JSON-based suggestion API
  - Enhanced privacy protection by removing Google dependency from autocomplete feature
  - Removed duplicate app/src/build folder (identical to app/static/build)
  - Cleaned up project structure for better organization
  - **COMPLETELY REMOVED BANG SHORTCUTS**: Eliminated all bang functionality from the application
  - Deleted app/static/bangs/ folder and bangs.json file completely  
  - Removed quick_search.py file containing all bang functions (suggest_bang, resolve_bang, load_all_bangs)
  - Removed bang imports and references from app_init.py and web_routes.py
  - Removed bang autocomplete suggestions and search redirects
  - Cleaned up all remaining bang folder references from static directory
  - Fixed HTML DOCTYPE/DTD content appearing as text by adding content filter
  - Application now operates without any bang shortcut functionality
  - Application fully functional in Replit environment with robust security practices

## User Preferences

Preferred communication style: Simple, everyday language.
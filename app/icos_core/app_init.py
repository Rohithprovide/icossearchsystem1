from app.icos_core.content_filter import clean_query

from app.icos_toolkit.user_session import generate_key

from app.icos_toolkit.platform_helpers import gen_file_hash, read_config_bool
from base64 import b64encode
from bs4 import MarkupResemblesLocatorWarning
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask
import json
import logging.config
import os

import threading
import warnings

from werkzeug.middleware.proxy_fix import ProxyFix

from app.icos_toolkit.platform_helpers import read_config_bool
from app.icos_core.platform_info import __version__, icos_platform_info

app = Flask(__name__, 
           static_folder=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static',
           template_folder=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/templates')

app.wsgi_app = ProxyFix(app.wsgi_app)

# look for WHOOGLE_ENV, else look in parent directory
dot_env_path = os.getenv(
    "WHOOGLE_DOTENV_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../whoogle.env"))

# Load .env file if enabled
if os.path.exists(dot_env_path):
    load_dotenv(dot_env_path)

# Set encryption key using setattr to avoid LSP warnings
setattr(app, 'enc_key', generate_key())

if read_config_bool('HTTPS_ONLY'):
    app.config['SESSION_COOKIE_NAME'] = '__Secure-session'
    app.config['SESSION_COOKIE_SECURE'] = True

app.config['VERSION_NUMBER'] = __version__
app.config['APP_ROOT'] = os.getenv(
    'APP_ROOT',
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config['STATIC_FOLDER'] = os.getenv(
    'STATIC_FOLDER',
    os.path.join(app.config['APP_ROOT'], 'static'))
app.config['BUILD_FOLDER'] = os.path.join(
    app.config['STATIC_FOLDER'], 'build')
app.config['CACHE_BUSTING_MAP'] = {}
# Removed languages, countries, and time_periods since language options were removed from settings
app.config['TRANSLATIONS'] = json.load(open(
    os.path.join(app.config['STATIC_FOLDER'], 'settings/translations.json'),
    encoding='utf-8'))
app.config['THEMES'] = json.load(open(
    os.path.join(app.config['STATIC_FOLDER'], 'settings/themes.json'),
    encoding='utf-8'))
app.config['HEADER_TABS'] = json.load(open(
    os.path.join(app.config['STATIC_FOLDER'], 'settings/header_tabs.json'),
    encoding='utf-8'))
app.config['CONFIG_PATH'] = os.getenv(
    'CONFIG_VOLUME',
    os.path.join(app.config['STATIC_FOLDER'], 'config'))
app.config['DEFAULT_CONFIG'] = os.path.join(
    app.config['CONFIG_PATH'],
    'config.json')
app.config['CONFIG_DISABLE'] = read_config_bool('WHOOGLE_CONFIG_DISABLE')
app.config['SESSION_FILE_DIR'] = os.path.join(
    app.config['CONFIG_PATH'],
    'session')
app.config['MAX_SESSION_SIZE'] = 4000  # Sessions won't exceed 4KB


# Ensure all necessary directories exist
if not os.path.exists(app.config['CONFIG_PATH']):
    os.makedirs(app.config['CONFIG_PATH'])

if not os.path.exists(app.config['SESSION_FILE_DIR']):
    os.makedirs(app.config['SESSION_FILE_DIR'])



if not os.path.exists(app.config['BUILD_FOLDER']):
    os.makedirs(app.config['BUILD_FOLDER'])

# Session values - using SecureURLShield compatible key generation
icos_key_path = os.path.join(app.config['CONFIG_PATH'], 'icos.key')
if os.path.exists(icos_key_path):
    try:
        with open(icos_key_path, 'rb') as key_file:
            app.config['SECRET_KEY'] = key_file.read()
    except PermissionError:
        app.config['SECRET_KEY'] = os.urandom(32)
else:
    app.config['SECRET_KEY'] = os.urandom(32)
    with open(icos_key_path, 'wb') as key_file:
        key_file.write(app.config['SECRET_KEY'])
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

# NOTE: SESSION_COOKIE_SAMESITE must be set to 'lax' to allow the user's
# previous session to persist when accessing the instance from an external
# link. Setting this value to 'strict' causes Whoogle to revalidate a new
# session, and fail, resulting in cookies being disabled.
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Config fields that are used to check for updates
app.config['RELEASES_URL'] = 'https://github.com/' \
                             'benbusby/whoogle-search/releases'
app.config['LAST_UPDATE_CHECK'] = datetime.now() - timedelta(hours=24)
app.config['HAS_UPDATE'] = ''

# The alternative to Google Translate is treated a bit differently than other
# social media site alternatives, in that it is used for any translation
# search results.
translate_url = os.getenv('WHOOGLE_ALT_TL', 'https://farside.link/lingva')
if not translate_url.startswith('http'):
    translate_url = 'https://' + translate_url
app.config['TRANSLATE_URL'] = translate_url

app.config['CSP'] = 'default-src \'none\';' \
                    'frame-src ' + translate_url + ';' \
                    'manifest-src \'self\';' \
                    'img-src \'self\' data:;' \
                    'style-src \'self\' \'unsafe-inline\';' \
                    'script-src \'self\';' \
                    'media-src \'self\';' \
                    'connect-src \'self\';'



# Build new mapping of static files for cache busting
cache_busting_dirs = ['css', 'js']
for cb_dir in cache_busting_dirs:
    full_cb_dir = os.path.join(app.config['STATIC_FOLDER'], cb_dir)
    for cb_file in os.listdir(full_cb_dir):
        # Create hash from current file state
        full_cb_path = os.path.join(full_cb_dir, cb_file)
        cb_file_link = gen_file_hash(full_cb_dir, cb_file)
        build_path = os.path.join(app.config['BUILD_FOLDER'], cb_file_link)

        try:
            os.symlink(full_cb_path, build_path)
        except FileExistsError:
            # Symlink hasn't changed, ignore
            pass

        # Create mapping for relative path urls
        map_path = build_path.replace(app.config['APP_ROOT'], '')
        if map_path.startswith('/'):
            map_path = map_path[1:]
        app.config['CACHE_BUSTING_MAP'][cb_file] = map_path

# Templating functions
app.jinja_env.globals.update(clean_query=clean_query)
app.jinja_env.globals.update(
    cb_url=lambda f: app.config['CACHE_BUSTING_MAP'][f.lower()])



# Suppress spurious warnings from BeautifulSoup
warnings.simplefilter('ignore', MarkupResemblesLocatorWarning)



# Disable logging from imported modules
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})

# Import routes after app initialization to avoid circular imports
from app.icos_core import web_routes  # noqa

# Register all routes and handlers
web_routes.register_routes(app)

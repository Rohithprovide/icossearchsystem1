import argparse
import base64
import io
import json
import os
import pickle
import re
import urllib.parse as urlparse
import uuid
import validators
import sys
import traceback
from datetime import datetime, timedelta
from functools import wraps

import waitress
from flask import current_app as app
from app.icos_core.user_preferences import Config
from app.icos_core.route_registry import Endpoint
from app.icos_core.network_handler import Request

from app.icos_toolkit.platform_helpers import empty_gif, placeholder_img, get_proxy_host_url, \
    fetch_favicon
from app.icos_core.content_filter import Filter
from app.icos_toolkit.platform_helpers import read_config_bool, get_client_ip, get_request_url, \
    check_for_update, encrypt_string
from app.icos_toolkit.ui_components import *
from app.icos_toolkit.content_processor import bold_search_terms,\
    add_currency_card, check_currency, get_tabs_content
from app.icos_toolkit.query_engine import Search, needs_https, has_captcha
from app.icos_toolkit.user_session import valid_user_session
from bs4 import BeautifulSoup as bsoup
from flask import jsonify, make_response, request, redirect, render_template, \
    send_file, session, url_for, g, current_app
from requests import exceptions
from requests.models import PreparedRequest
import secrets
from werkzeug.datastructures import MultiDict

ac_var = 'WHOOGLE_AUTOCOMPLETE'
autocomplete_enabled = os.getenv(ac_var, '1')


def get_search_name(tbm):
    for tab in current_app.config['HEADER_TABS'].values():
        if tab['tbm'] == tbm:
            return tab['name']


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # do not ask password if cookies already present
        if (
            valid_user_session(session)
            and 'cookies_disabled' not in request.args
            and session['auth']
        ):
            return f(*args, **kwargs)

        auth = request.authorization

        # Skip if username/password not set
        whoogle_user = os.getenv('WHOOGLE_USER', '')
        whoogle_pass = os.getenv('WHOOGLE_PASS', '')
        if (not whoogle_user or not whoogle_pass) or (
                auth
                and whoogle_user == auth.username
                and whoogle_pass == auth.password):
            session['auth'] = True
            return f(*args, **kwargs)
        else:
            return make_response('Not logged in', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated


def session_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not valid_user_session(session):
            session.pop('_permanent', None)

        # Note: This sets all requests to use the encryption key determined per
        # instance on app init. This can be updated in the future to use a key
        # that is unique for their session (session['key']) but this should use
        # a config setting to enable the session based key. Otherwise there can
        # be problems with searches performed by users with cookies blocked if
        # a session based key is always used.
        g.session_key = app.enc_key

        # Clear out old sessions
        invalid_sessions = []
        for user_session in os.listdir(app.config['SESSION_FILE_DIR']):
            file_path = os.path.join(
                app.config['SESSION_FILE_DIR'],
                user_session)

            try:
                # Ignore files that are larger than the max session file size
                if os.path.getsize(file_path) > app.config['MAX_SESSION_SIZE']:
                    continue

                with open(file_path, 'rb') as session_file:
                    _ = pickle.load(session_file)
                    data = pickle.load(session_file)
                    if isinstance(data, dict) and 'valid' in data:
                        continue
                    invalid_sessions.append(file_path)
            except Exception:
                # Broad exception handling here due to how instances installed
                # with pip seem to have issues storing unrelated files in the
                # same directory as sessions
                pass

        for invalid_session in invalid_sessions:
            try:
                os.remove(invalid_session)
            except FileNotFoundError:
                # Don't throw error if the invalid session has been removed
                pass

        return f(*args, **kwargs)

    return decorated


def before_request_func():
    session.permanent = True

    # Check for latest version if needed
    now = datetime.now()
    needs_update_check = now - timedelta(hours=24) > app.config['LAST_UPDATE_CHECK']
    if read_config_bool('WHOOGLE_UPDATE_CHECK', True) and needs_update_check:
        app.config['LAST_UPDATE_CHECK'] = now
        app.config['HAS_UPDATE'] = check_for_update(
            app.config['RELEASES_URL'],
            app.config['VERSION_NUMBER'])

    g.request_params = (
        request.args if request.method == 'GET' else request.form
    )

    default_config = json.load(open(app.config['DEFAULT_CONFIG'])) \
        if os.path.exists(app.config['DEFAULT_CONFIG']) else {}

    # Generate session values for user if unavailable
    if not valid_user_session(session):
        session['config'] = default_config
        session['uuid'] = str(uuid.uuid4())
        session['key'] = app.enc_key
        session['auth'] = False

    # Establish config values per user session
    g.user_config = Config(**session['config'])

    # Update user config if specified in search args
    g.user_config = g.user_config.from_params(g.request_params)

    if not g.user_config.url:
        g.user_config.url = get_request_url(request.url_root)

    g.user_request = Request(
        request.headers.get('User-Agent'),
        get_request_url(request.url_root),
        config=g.user_config)

    g.app_location = g.user_config.url


def after_request_func(resp):
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'DENY'
    resp.headers['Cache-Control'] = 'max-age=86400'

    if os.getenv('WHOOGLE_CSP', False):
        resp.headers['Content-Security-Policy'] = app.config['CSP']
        if os.environ.get('HTTPS_ONLY', False):
            resp.headers['Content-Security-Policy'] += \
                'upgrade-insecure-requests'

    return resp


def unknown_page(e):
    app.logger.warn(e)
    return redirect(g.app_location)


def healthz():
    return ''


@auth_required
def index():
    # Redirect if an error was raised
    if 'error_message' in session and session['error_message']:
        error_message = session['error_message']
        session['error_message'] = ''
        return render_template('error.html', error_message=error_message)

    return render_template('index.html',
                           has_update=app.config['HAS_UPDATE'],
                           themes=app.config['THEMES'],
                           autocomplete_enabled=autocomplete_enabled,
                           translation=app.config['TRANSLATIONS'][
                               g.user_config.get_localization_lang()
                           ],
                           logo=render_template(
                               'logo.html',
                               dark=g.user_config.dark),
                           config_disabled=(
                                   app.config['CONFIG_DISABLE'] or
                                   not valid_user_session(session)),
                           config=g.user_config,

                           version_number=app.config['VERSION_NUMBER'])


#@app.route(f'/{Endpoint.opensearch}', methods=['GET'])
def opensearch():
    opensearch_url = g.app_location
    if opensearch_url.endswith('/'):
        opensearch_url = opensearch_url[:-1]

    # Enforce https for opensearch template
    if needs_https(opensearch_url):
        opensearch_url = opensearch_url.replace('http://', 'https://', 1)

    get_only = g.user_config.get_only or 'Chrome' in request.headers.get(
        'User-Agent')

    return render_template(
        'opensearch.xml',
        main_url=opensearch_url,
        request_type='' if get_only else 'method="post"',
        search_type=request.args.get('tbm'),
        search_name=get_search_name(request.args.get('tbm'))
    ), 200, {'Content-Type': 'application/xml'}


#@app.route(f'/{Endpoint.search_html}', methods=['GET'])
def search_html():
    search_url = g.app_location
    if search_url.endswith('/'):
        search_url = search_url[:-1]
    return render_template('search.html', url=search_url)


#@app.route(f'/{Endpoint.autocomplete}', methods=['GET', 'POST'])
def autocomplete():
    if os.getenv(ac_var) and not read_config_bool(ac_var):
        return jsonify({})

    q = g.request_params.get('q')
    if not q:
        # FF will occasionally (incorrectly) send the q field without a
        # mimetype in the format "b'q=<query>'" through the request.data field
        q = str(request.data).replace('q=', '')



    if not q and not request.data:
        return jsonify({'?': []})
    elif request.data:
        q = urlparse.unquote_plus(
            request.data.decode('utf-8').replace('q=', ''))

    # Return a list of suggestions for the query
    #
    # Return autocomplete suggestions
    return jsonify([
        q,
        g.user_request.autocomplete(q)
    ])

#@app.route(f'/{Endpoint.search}', methods=['GET', 'POST'])
@session_required
@auth_required
def search():
    if request.method == 'POST':
        # Redirect as a GET request with an encrypted query
        post_data = MultiDict(request.form)
        post_data['q'] = encrypt_string(g.session_key, post_data['q'])
        get_req_str = urlparse.urlencode(post_data)
        return redirect(url_for('.search') + '?' + get_req_str)

    # Check if GET request has unencrypted query and encrypt it
    raw_query = request.args.get('q', '')
    if raw_query and not raw_query.startswith('SX'):
        # This is an unencrypted query (like from navigation tabs), encrypt it
        get_params = MultiDict(request.args)
        get_params['q'] = encrypt_string(g.session_key, raw_query)
        encrypted_query_str = urlparse.urlencode(get_params)
        return redirect(url_for('.search') + '?' + encrypted_query_str)

    search_util = Search(request, g.user_config, g.session_key)
    query = search_util.new_search_query()



    # Redirect to home if invalid/blank search
    if not query:
        return redirect(url_for('.index'))

    # Generate response and number of external elements from the page
    try:
        response = search_util.generate_response()
    except Exception as e:
        session['error_message'] = str(e)
        return redirect(url_for('.index'))

    if search_util.feeling_lucky:
        return redirect(response, code=303)

    # If the user is attempting to translate a string, determine the correct
    # string for formatting the lingva.ml url
    localization_lang = g.user_config.get_localization_lang()
    translation = app.config['TRANSLATIONS'][localization_lang]
    translate_to = localization_lang.replace('lang_', '')

    # removing st-card to only use whoogle time selector
    soup = bsoup(response, "html.parser");
    for x in soup.find_all(attrs={"id": "st-card"}):
        x.replace_with("")

    response = str(soup)

    # Return 503 if temporarily blocked by captcha
    if has_captcha(str(response)):
        app.logger.error('503 (CAPTCHA)')
        fallback_engine = os.environ.get('WHOOGLE_FALLBACK_ENGINE_URL', '')
        if (fallback_engine):
            return redirect(fallback_engine + query)
        
        return render_template(
            'error.html',
            blocked=True,
            error_message=translation['ratelimit'],
            translation=translation,
            farside='https://farside.link',
            config=g.user_config,
            query=urlparse.unquote(query),
            params=g.user_config.to_params(keys=['vortex'])), 503

    response = bold_search_terms(response, query)

    # check for widgets and add if requested
    if search_util.widget != '':
        html_soup = bsoup(str(response), 'html.parser')
        if search_util.widget == 'ip':
            response = add_ip_card(html_soup, get_client_ip(request))
        elif search_util.widget == 'calculator' and not 'nojs' in request.args:
            response = add_calculator_card(html_soup)

    # Update tabs content
    tabs = get_tabs_content(app.config['HEADER_TABS'],
                            search_util.full_query,
                            search_util.search_type,
                            g.user_config.vortex,
                            translation)

    # Feature to display currency_card
    # Since this is determined by more than just the
    # query is it not defined as a standard widget
    conversion = check_currency(str(response))
    if conversion:
        html_soup = bsoup(str(response), 'html.parser')
        response = add_currency_card(html_soup, conversion)

    vortex = g.user_config.vortex
    home_url = f"home?vortex={vortex}" if vortex else "home"
    cleanresponse = str(response).replace("andlt;","&lt;").replace("andgt;","&gt;")

    return render_template(
        'display.html',
        has_update=app.config['HAS_UPDATE'],
        query=urlparse.unquote(query),
        search_type=search_util.search_type,
        search_name=get_search_name(search_util.search_type),
        config=g.user_config,
        autocomplete_enabled=autocomplete_enabled,
        lingva_url=app.config['TRANSLATE_URL'],
        translation=translation,
        translate_to=translate_to,
        translate_str=query.replace(
            'translate', ''
        ).replace(
            translation['translate'], ''
        ),
        is_translation=any(
            _ in query.lower() for _ in [translation['translate'], 'translate']
        ) and not search_util.search_type,  # Standard search queries only
        response=cleanresponse,
        version_number=app.config['VERSION_NUMBER'],
        google_api_key=os.getenv('GOOGLE_API_KEY', ''),
        search_header=render_template(
            'header.html',
            home_url=home_url,
            config=g.user_config,
            translation=translation,
            logo=render_template('logo.html', dark=g.user_config.dark),
            query=urlparse.unquote(query),
            search_type=search_util.search_type,
            mobile=g.user_request.mobile,
            tabs=tabs)).replace("  ", "")


#@app.route(f'/{Endpoint.config}', methods=['GET', 'POST', 'PUT'])
@session_required
@auth_required
def config():
    config_disabled = (
            app.config['CONFIG_DISABLE'] or
            not valid_user_session(session))

    name = ''
    if 'name' in request.args:
        name = os.path.normpath(request.args.get('name'))
        if not re.match(r'^[A-Za-z0-9_.+-]+$', name):
            return make_response('Invalid config name', 400)

    if request.method == 'GET':
        return json.dumps(g.user_config.__dict__)
    elif request.method == 'PUT' and not config_disabled:
        if name:
            config_pkl = os.path.join(app.config['CONFIG_PATH'], name)
            session['config'] = (pickle.load(open(config_pkl, 'rb'))
                                if os.path.exists(config_pkl)
                                else session['config'])
            return json.dumps(session['config'])
        else:
            return json.dumps({})
    elif not config_disabled:
        config_data = request.form.to_dict()
        if 'url' not in config_data or not config_data['url']:
            config_data['url'] = g.user_config.url

        # Convert checkbox values: HTML checkboxes send 'on' when checked, nothing when unchecked
        # Convert 'on' to True, missing values to False for boolean settings
        boolean_settings = ['safe', 'new_tab', 'ai_sidebar', 'view_image', 'anon_view', 'get_only', 'alts', 'nojs']
        for setting in boolean_settings:
            if setting in config_data:
                config_data[setting] = config_data[setting] == 'on'
            else:
                config_data[setting] = False

        # Handle user agent configuration
        if 'user_agent' in config_data:
            if config_data['user_agent'] == 'custom':
                config_data['use_custom_user_agent'] = True
                # Keep both the selection and the custom string
                if 'custom_user_agent' in config_data:
                    config_data['custom_user_agent'] = config_data['custom_user_agent']
                    print(f"Setting custom user agent to: {config_data['custom_user_agent']}")  # Debug log
            else:
                config_data['use_custom_user_agent'] = False
                config_data['custom_user_agent'] = ''

        # Save config by name to allow a user to easily load later
        if name:
            pickle.dump(
                config_data,
                open(os.path.join(
                    app.config['CONFIG_PATH'],
                    name), 'wb'))

        session['config'] = config_data
        return redirect(config_data['url'])
    else:
        return redirect(url_for('.index'), code=403)


#@app.route(f'/{Endpoint.imgres}')
@session_required
@auth_required
def imgres():
    return redirect(request.args.get('imgurl'))


#@app.route(f'/{Endpoint.element}')
@session_required
@auth_required
def element():
    element_url = src_url = request.args.get('url')
    
    # Use our custom SecureURLShield system instead of gAAAAA detection
    from app.icos_toolkit.security_shield import SecureURLShield
    shield = SecureURLShield(g.session_key)
    
    if shield.is_shielded(element_url):
        try:
            src_url = shield.unshield_url(element_url)
        except Exception as e:
            return render_template(
                'error.html',
                error_message=f'URL decryption failed: {str(e)}'), 401

    src_type = request.args.get('type')

    # Ensure requested element is from a valid domain
    domain = urlparse.urlparse(src_url).netloc
    if not validators.domain(domain):
        return send_file(io.BytesIO(empty_gif), mimetype='image/gif')

    try:
        response = g.user_request.send(base_url=src_url)

        # Display an empty gif if the requested element couldn't be retrieved
        if response.status_code != 200 or len(response.content) == 0:
            if 'favicon' in src_url:
                favicon = fetch_favicon(src_url)
                return send_file(io.BytesIO(favicon), mimetype='image/png')
            else:
                return send_file(io.BytesIO(empty_gif), mimetype='image/gif')

        file_data = response.content
        tmp_mem = io.BytesIO()
        tmp_mem.write(file_data)
        tmp_mem.seek(0)

        return send_file(tmp_mem, mimetype=src_type)
    except exceptions.RequestException:
        pass

    return send_file(io.BytesIO(empty_gif), mimetype='image/gif')


#@app.route(f'/{Endpoint.window}')
@session_required
@auth_required
def window():
    target_url = request.args.get('location')
    
    # Use our custom SecureURLShield system
    from app.icos_toolkit.security_shield import SecureURLShield
    shield = SecureURLShield(g.session_key)
    
    if shield.is_shielded(target_url):
        target_url = shield.unshield_url(target_url)

    content_filter = Filter(
        g.session_key,
        root_url=request.url_root,
        config=g.user_config)
    target = urlparse.urlparse(target_url)

    # Ensure requested URL has a valid domain
    if not validators.domain(target.netloc):
        return render_template(
            'error.html',
            error_message='Invalid location'), 400

    host_url = f'{target.scheme}://{target.netloc}'

    get_body = g.user_request.send(base_url=target_url).text

    results = bsoup(get_body, 'html.parser')
    src_attrs = ['src', 'href', 'srcset', 'data-srcset', 'data-src']

    # Parse HTML response and replace relative links w/ absolute
    for element in results.find_all():
        for attr in src_attrs:
            if not element.has_attr(attr) or not element[attr].startswith('/'):
                continue

            element[attr] = host_url + element[attr]

    # Replace or remove javascript sources
    for script in results.find_all('script', {'src': True}):
        if 'nojs' in request.args:
            script.decompose()
        else:
            content_filter.update_element_src(script, 'application/javascript')

    # Replace all possible image attributes
    img_sources = ['src', 'data-src', 'data-srcset', 'srcset']
    for img in results.find_all('img'):
        _ = [
            content_filter.update_element_src(img, 'image/png', attr=_)
            for _ in img_sources if img.has_attr(_)
        ]

    # Replace all stylesheet sources
    for link in results.find_all('link', {'href': True}):
        content_filter.update_element_src(link, 'text/css', attr='href')

    # Use anonymous view for all links on page
    for a in results.find_all('a', {'href': True}):
        a['href'] = f'{Endpoint.window}?location=' + a['href'] + (
            '&nojs=1' if 'nojs' in request.args else '')

    # Remove all iframes -- these are commonly used inside of <noscript> tags
    # to enforce loading Google Analytics
    for iframe in results.find_all('iframe'):
        iframe.decompose()

    return render_template(
        'display.html',
        response=results,
        translation=app.config['TRANSLATIONS'][
            g.user_config.get_localization_lang()
        ]
    )


#@app.route('/gemini-query', methods=['POST'])
def gemini_query():
    try:
        # Get the query from the request
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'status': 'error',
                'response': 'No query provided',
                'query': query
            }), 400
        
        # Import and use Gemini API
        import google.generativeai as genai
        
        # Get API key from environment
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            return jsonify({
                'status': 'error',
                'response': 'Google API key not configured',
                'query': query
            }), 500
        
        # Configure Gemini client
        genai.configure(api_key=api_key)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Send query to Gemini with detailed prompt
        prompt = f"""You are an intelligent assistant embedded in a search engine sidebar. Summarize or answer the user's search query in a helpful, concise, and informative way. If the query is a place, include a brief description, notable facts, and optionally, relevant images if possible. If it's a person or concept, provide a description about them like when they were born when they died what are they known for.And also send the response as points and paragraphs. Keep the tone neutral and friendly. The query is: "{query}" """
        
        response = model.generate_content(prompt)
        
        gemini_response = response.text if response.text else "No response from Gemini"
        
        return jsonify({
            'status': 'success',
            'response': gemini_response,
            'query': query
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'response': f'Error: {str(e)}',
            'query': query if 'query' in locals() else 'Unknown'
        }), 500


#@app.route('/robots.txt')
def robots():
    response = make_response(
'''User-Agent: *
Disallow: /''', 200)
    response.mimetype = 'text/plain'
    return response


#@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('img/favicon.ico')


#@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message=str(e)), 404


#@app.errorhandler(Exception)
def internal_error(e):
    query = ''
    if request.method == 'POST':
        query = request.form.get('q')
    else:
        query = request.args.get('q')

    # Attempt to parse the query
    try:
        search_util = Search(request, g.user_config, g.session_key)
        query = search_util.new_search_query()
    except Exception:
        pass

    print(traceback.format_exc(), file=sys.stderr)

    fallback_engine = os.environ.get('WHOOGLE_FALLBACK_ENGINE_URL', '')
    if (fallback_engine):
        return redirect(fallback_engine + query)

    localization_lang = g.user_config.get_localization_lang()
    translation = app.config['TRANSLATIONS'][localization_lang]
    return render_template(
            'error.html',
            error_message='Internal server error (500)',
            translation=translation,
            farside='https://farside.link',
            config=g.user_config,
            query=urlparse.unquote(query) if query else '',
            params=g.user_config.to_params(keys=['vortex'])), 500





def register_routes(app_instance):
    """Register all Flask routes and handlers with the app instance"""
    
    # Register before/after request handlers
    app_instance.before_request(before_request_func)
    app_instance.after_request(after_request_func)
    
    # Register error handlers
    app_instance.errorhandler(404)(unknown_page)
    app_instance.errorhandler(404)(page_not_found)
    app_instance.errorhandler(Exception)(internal_error)
    
    # Register routes
    app_instance.route(f'/{Endpoint.healthz}', methods=['GET'])(healthz)
    app_instance.route('/', methods=['GET'])(index)
    app_instance.route(f'/{Endpoint.home}', methods=['GET'])(index)
    app_instance.route(f'/{Endpoint.opensearch}', methods=['GET'])(opensearch)
    app_instance.route(f'/{Endpoint.search_html}', methods=['GET'])(search_html)
    app_instance.route(f'/{Endpoint.autocomplete}', methods=['GET', 'POST'])(autocomplete)
    app_instance.route(f'/{Endpoint.search}', methods=['GET', 'POST'])(search)
    app_instance.route(f'/{Endpoint.config}', methods=['GET', 'POST', 'PUT'])(config)
    app_instance.route(f'/{Endpoint.imgres}')(imgres)
    app_instance.route(f'/{Endpoint.element}')(element)
    app_instance.route(f'/{Endpoint.window}')(window)
    app_instance.route('/gemini-query', methods=['POST'])(gemini_query)
    app_instance.route('/robots.txt')(robots)
    app_instance.route('/favicon.ico')(favicon)


def run_app() -> None:
    parser = argparse.ArgumentParser(
        description='Whoogle Search console runner')
    parser.add_argument(
        '--port',
        default=5000,
        metavar='<port number>',
        help='Specifies a port to run on (default 5000)')
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        metavar='<ip address>',
        help='Specifies the host address to use (default 127.0.0.1)')
    parser.add_argument(
        '--unix-socket',
        default='',
        metavar='</path/to/unix.sock>',
        help='Listen for app on unix socket instead of host:port')
    parser.add_argument(
        '--unix-socket-perms',
        default='600',
        metavar='<octal permissions>',
        help='Octal permissions to use for the Unix domain socket (default 600)')
    parser.add_argument(
        '--debug',
        default=False,
        action='store_true',
        help='Activates debug mode for the server (default False)')
    parser.add_argument(
        '--https-only',
        default=False,
        action='store_true',
        help='Enforces HTTPS redirects for all requests')
    parser.add_argument(
        '--userpass',
        default='',
        metavar='<username:password>',
        help='Sets a username/password basic auth combo (default None)')
    parser.add_argument(
        '--proxyauth',
        default='',
        metavar='<username:password>',
        help='Sets a username/password for a HTTP/SOCKS proxy (default None)')
    parser.add_argument(
        '--proxytype',
        default='',
        metavar='<socks4|socks5|http>',
        help='Sets a proxy type for all connections (default None)')
    parser.add_argument(
        '--proxyloc',
        default='',
        metavar='<location:port>',
        help='Sets a proxy location for all connections (default None)')
    args = parser.parse_args()

    if args.userpass:
        user_pass = args.userpass.split(':')
        os.environ['WHOOGLE_USER'] = user_pass[0]
        os.environ['WHOOGLE_PASS'] = user_pass[1]

    if args.proxytype and args.proxyloc:
        if args.proxyauth:
            proxy_user_pass = args.proxyauth.split(':')
            os.environ['WHOOGLE_PROXY_USER'] = proxy_user_pass[0]
            os.environ['WHOOGLE_PROXY_PASS'] = proxy_user_pass[1]
        os.environ['WHOOGLE_PROXY_TYPE'] = args.proxytype
        os.environ['WHOOGLE_PROXY_LOC'] = args.proxyloc

    if args.https_only:
        os.environ['HTTPS_ONLY'] = '1'

    if args.debug:
        app.run(host=args.host, port=args.port, debug=args.debug)
    elif args.unix_socket:
        waitress.serve(app, unix_socket=args.unix_socket, unix_socket_perms=args.unix_socket_perms)
    else:
        waitress.serve(
            app,
            listen="{}:{}".format(args.host, args.port),
            url_prefix=os.environ.get('WHOOGLE_URL_PREFIX', ''))

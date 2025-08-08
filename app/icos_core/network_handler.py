from app.icos_core.user_preferences import Config

from datetime import datetime
from defusedxml import ElementTree as ET
import json
import random
import requests
from requests import Response, ConnectionError
import urllib.parse as urlparse
import os


MAPS_URL = 'https://maps.google.com/maps'
AUTOCOMPLETE_URL = 'https://duckduckgo.com/ac/?type=list&'

MOBILE_UA = '{}/5.0 (Android 0; Mobile; rv:54.0) Gecko/54.0 {}/59.0'
DESKTOP_UA = '{}/5.0 (X11; {} x86_64; rv:75.0) Gecko/20100101 {}/75.0'

# Valid query params
VALID_PARAMS = ['tbs', 'tbm', 'start', 'near', 'source', 'nfpr']





def gen_user_agent(config, is_mobile) -> str:
    # Define the Lynx user agent
    LYNX_UA = 'Lynx/2.9.2 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/3.4.0'

    # If using custom user agent, return the custom string
    if config.user_agent == 'custom' and config.custom_user_agent:
        return config.custom_user_agent

    # If using Lynx user agent
    if config.user_agent == 'LYNX_UA':
        return LYNX_UA

    # If no custom user agent is set, generate a random one
    firefox = random.choice(['Choir', 'Squier', 'Higher', 'Wire']) + 'fox'
    linux = random.choice(['Win', 'Sin', 'Gin', 'Fin', 'Kin']) + 'ux'

    if is_mobile:
        return MOBILE_UA.format("Mozilla", firefox)

    return DESKTOP_UA.format("Mozilla", linux, firefox)


def gen_query(query, args, config) -> str:
    param_dict = {key: '' for key in VALID_PARAMS}

    # Use :past(hour/day/week/month/year) if available
    # example search "new restaurants :past month"
    lang = ''
    if ':past' in query and 'tbs' not in args:
        time_range = str.strip(query.split(':past', 1)[-1])
        param_dict['tbs'] = '&tbs=' + ('qdr:' + str.lower(time_range[0]))
    elif 'tbs' in args or 'tbs' in config:
        result_tbs = args.get('tbs') if 'tbs' in args else config['tbs']
        param_dict['tbs'] = '&tbs=' + result_tbs

        # Occasionally the 'tbs' param provided by google also contains a
        # field for 'lr', but formatted strangely. This is a rough solution
        # for this.
        #
        # Example:
        # &tbs=qdr:h,lr:lang_1pl
        # -- the lr param needs to be extracted and remove the leading '1'
        result_params = [_ for _ in result_tbs.split(',') if 'lr:' in _]
        if len(result_params) > 0:
            result_param = result_params[0]
            lang = result_param[result_param.find('lr:') + 3:len(result_param)]

    # Ensure search query is parsable
    query = urlparse.quote(query)

    # Pass along type of results (news, images, books, etc)
    if 'tbm' in args:
        param_dict['tbm'] = '&tbm=' + args.get('tbm')

    # Get results page start value (10 per page, ie page 2 start val = 20)
    if 'start' in args:
        param_dict['start'] = '&start=' + args.get('start')

    # Search for results near a particular city, if available
    if config.near:
        param_dict['near'] = '&near=' + urlparse.quote(config.near)

    # Set language for results (lr) if source isn't set, otherwise use the
    # result language param provided in the results
    if 'source' in args:
        param_dict['source'] = '&source=' + args.get('source')
        param_dict['lr'] = ('&lr=' + ''.join(
            [_ for _ in lang if not _.isdigit()]
        )) if lang else ''
    else:
        param_dict['lr'] = (
            '&lr=' + config.lang_search
        ) if config.lang_search else ''

    # 'nfpr' defines the exclusion of results from an auto-corrected query
    if 'nfpr' in args:
        param_dict['nfpr'] = '&nfpr=' + args.get('nfpr')

    # 'chips' is used in image tabs to pass the optional 'filter' to add to the
    # given search term
    if 'chips' in args:
        param_dict['chips'] = '&chips=' + args.get('chips')

    param_dict['gl'] = (
        '&gl=' + config.country
    ) if config.country else ''
    param_dict['hl'] = (
        '&hl=' + config.lang_interface.replace('lang_', '')
    ) if config.lang_interface else ''
    param_dict['safe'] = '&safe=' + ('active' if config.safe else 'off')

    # Block all sites specified in the user config
    unquoted_query = urlparse.unquote(query)
    for blocked_site in config.block.replace(' ', '').split(','):
        if not blocked_site:
            continue
        block = (' -site:' + blocked_site)
        query += block if block not in unquoted_query else ''

    for val in param_dict.values():
        if not val:
            continue
        query += val

    return query


class Request:
    """Class used for handling all outbound requests, including search queries,
    search suggestions, and loading of external content (images, audio, etc).

    Attributes:
        normal_ua: the user's current user agent
        root_path: the root path of the whoogle instance
        config: the user's current whoogle configuration
    """

    def __init__(self, normal_ua, root_path, config: Config):
        # Default results per page - will be dynamically set based on search type
        default_results_per_page = int(os.getenv('WHOOGLE_RESULTS_PER_PAGE', 100))
        self.default_results_per_page = default_results_per_page
        # Initialize with default, will be updated in send method based on search type
        self.search_url = 'https://www.google.com/search?gbv=1&num=' + str(default_results_per_page) + '&q='


        self.language = config.lang_search if config.lang_search else ''
        self.country = config.country if config.country else ''

        # For setting Accept-language Header
        self.lang_interface = ''
        if config.accept_language:
            self.lang_interface = config.lang_interface

        self.mobile = bool(normal_ua) and ('Android' in normal_ua
                                           or 'iPhone' in normal_ua)

        # Generate user agent based on config
        self.modified_user_agent = gen_user_agent(config, self.mobile)
        if not self.mobile:
            self.modified_user_agent_mobile = gen_user_agent(config, True)

        # Direct connections only - no proxy configuration
        self.proxies = {}
        self.root_path = root_path

    def __getitem__(self, name):
        return getattr(self, name)

    def autocomplete(self, query) -> list:
        """Sends a query to DuckDuckGo's search suggestion service

        Args:
            query: The in-progress query to send

        Returns:
            list: The list of matches for possible search suggestions

        """
        ac_query = dict(q=query)
        # DuckDuckGo's API doesn't use the same language/country params as Google
        # It automatically detects language based on query content

        response = self.send(base_url=AUTOCOMPLETE_URL,
                             query=urlparse.urlencode(ac_query)).text

        if not response:
            return []

        try:
            # DuckDuckGo returns JSON format: [query, [suggestion1, suggestion2, ...]]
            suggestions = json.loads(response)
            if isinstance(suggestions, list) and len(suggestions) > 1:
                return suggestions[1] if isinstance(suggestions[1], list) else []
            return []
        except (json.JSONDecodeError, IndexError, TypeError):
            # Malformed JSON response
            return []

    def send(self, base_url='', query='', attempt=0,
             force_mobile=False, user_agent='') -> Response:
        """Sends an outbound request to a URL. Optionally sends the request
        Args:
            base_url: The URL to use in the request
            query: The optional query string for the request
            attempt: The number of attempts made for the request

            force_mobile: Optional flag to enable a mobile user agent
                (used for fetching full size images in search results)

        Returns:
            Response: The Response object returned by the requests call

        """
        use_client_user_agent = int(os.environ.get('WHOOGLE_USE_CLIENT_USER_AGENT', '0'))
        if user_agent and use_client_user_agent == 1:
            modified_user_agent = user_agent
        else:
            if force_mobile and not self.mobile:
                modified_user_agent = self.modified_user_agent_mobile
            else:
                modified_user_agent = self.modified_user_agent

        headers = {
            'User-Agent': modified_user_agent
        }

        # Adding the Accept-Language to the Header if possible
        if self.lang_interface:
            headers.update({'Accept-Language':
                            self.lang_interface.replace('lang_', '')
                            + ';q=1.0'})

        # view is suppressed correctly
        now = datetime.now()
        cookies = {
            'CONSENT': 'PENDING+987',
            'SOCS': 'CAESHAgBEhIaAB',
        }





        # Dynamically adjust results per page - ONLY for All tab (no tbm= parameter)
        search_url_to_use = base_url or self.search_url
        
        # Only modify result count for All tab searches (when there's no tbm= parameter)
        if query and not base_url and 'tbm=' not in query:
            # This is an "All" tab search - use exactly 15 results
            search_url_to_use = search_url_to_use.replace(f'num={self.default_results_per_page}', 'num=15')
        # All other tabs (images, videos, news, etc.) keep their original result counts
        
        response = requests.get(
            search_url_to_use + query,
            proxies=self.proxies,
            headers=headers,
            cookies=cookies)

        # Handle captcha response
        if 'form id="captcha-form"' in response.text:
            # Return the captcha response for handling upstream
            pass

        return response

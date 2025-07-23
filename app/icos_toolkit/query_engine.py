import os
import re
from typing import Any
from app.icos_core.content_filter import Filter
from app.icos_core.network_handler import gen_query
from app.icos_toolkit.platform_helpers import get_proxy_host_url
from app.icos_toolkit.content_processor import get_first_link
from bs4 import BeautifulSoup as bsoup
import secrets
from app.icos_toolkit.security_shield import SecureURLShield
from flask import g


CAPTCHA = 'div class="g-recaptcha"'


def needs_https(url: str) -> bool:
    """Checks if the current instance needs to be upgraded to HTTPS

    Note that all Heroku instances are available by default over HTTPS, but
    do not automatically set up a redirect when visited over HTTP.

    Args:
        url: The instance url

    Returns:
        bool: True/False representing the need to upgrade

    """
    https_only = bool(os.getenv('HTTPS_ONLY', 0))
    is_heroku = url.endswith('.herokuapp.com')
    is_http = url.startswith('http://')

    return (is_heroku and is_http) or (https_only and is_http)


def has_captcha(results: str) -> bool:
    """Checks to see if the search results are blocked by a captcha

    Args:
        results: The search page html as a string

    Returns:
        bool: True/False indicating if a captcha element was found

    """
    return CAPTCHA in results


class Search:
    """Search query preprocessor - used before submitting the query or
    redirecting to another site

    Attributes:
        request: the incoming flask request
        config: the current user config settings
        session_key: the flask user SecureURLShield key
    """
    def __init__(self, request, config, session_key, cookies_disabled=False):
        method = request.method
        self.request = request
        self.request_params = request.args if method == 'GET' else request.form
        self.user_agent = request.headers.get('User-Agent')
        self.feeling_lucky = False
        self.config = config
        self.session_key = session_key
        self.query = ''
        self.widget = ''
        self.cookies_disabled = cookies_disabled
        self.search_type = self.request_params.get(
            'tbm') if 'tbm' in self.request_params else ''

    def __getitem__(self, name) -> Any:
        return getattr(self, name)

    def __setitem__(self, name, value) -> None:
        return setattr(self, name, value)

    def __delitem__(self, name) -> None:
        return delattr(self, name)

    def __contains__(self, name) -> bool:
        return hasattr(self, name)

    def new_search_query(self) -> str:
        """Parses a plaintext query into a valid string for submission

        Also decrypts the query string, if encrypted (in the case of
        paginated results).

        Returns:
            str: A valid query string

        """
        q = self.request_params.get('q')

        if q is None or len(q) == 0:
            return ''
        else:
            # Attempt to decrypt if this is an internal link using our custom system
            try:
                shield = SecureURLShield(self.session_key)
                if shield.is_shielded(q):
                    q = shield.unshield_url(q)
            except Exception:
                pass

        # Strip '!' for "feeling lucky" queries
        if match := re.search("(^|\s)!($|\s)", q):
            self.feeling_lucky = True
            start, end = match.span()
            self.query = " ".join([seg for seg in [q[:start], q[end:]] if seg])
        else:
            self.feeling_lucky = False
            self.query = q

        # Check for possible widgets
        self.widget = "ip" if re.search("([^a-z0-9]|^)my *[^a-z0-9] *(ip|internet protocol)" +
                        "($|( *[^a-z0-9] *(((addres|address|adres|" +
                        "adress)|a)? *$)))", self.query.lower()) else self.widget
        self.widget = 'calculator' if re.search(
                r"\bcalculator\b|\bcalc\b|\bcalclator\b|\bmath\b",
                self.query.lower()) else self.widget
        return self.query

    def generate_response(self) -> str:
        """Generates a response for the user's query

        Returns:
            str: A string response to the search query, in the form of a URL
                 or string representation of HTML content.

        """
        mobile = 'Android' in self.user_agent or 'iPhone' in self.user_agent
        # reconstruct url if X-Forwarded-Host header present
        root_url = get_proxy_host_url(
            self.request,
            self.request.url_root,
            root=True)

        content_filter = Filter(self.session_key,
                                root_url=root_url,
                                mobile=mobile,
                                config=self.config,
                                query=self.query)
        full_query = gen_query(self.query,
                               self.request_params,
                               self.config)
        self.full_query = full_query

        # force mobile search when view image is true and
        # the request is not already made by a mobile
        # FIXME: Broken since the user agent changes as of 16 Jan 2025
        # view_image = ('tbm=isch' in full_query
                      # and self.config.view_image
                      # and not g.user_request.mobile)

        # For image searches, fetch multiple pages to get 100 images
        if 'tbm=isch' in full_query and 'start=' not in full_query:
            combined_html = self._fetch_multiple_image_pages(full_query)
            html_soup = bsoup(combined_html, 'html.parser')
        else:
            get_body = g.user_request.send(query=full_query,
                                           force_mobile=self.config.view_image,
                                           user_agent=self.user_agent)

            # Produce cleanable html soup from response
            get_body_safed = get_body.text.replace("&lt;","andlt;").replace("&gt;","andgt;")
            html_soup = bsoup(get_body_safed, 'html.parser')

        # Replace current soup if view_image is active
        # FIXME: Broken since the user agent changes as of 16 Jan 2025
        # if view_image:
            # html_soup = content_filter.view_image(html_soup)



        formatted_results = content_filter.clean(html_soup)
        if self.feeling_lucky:
            if lucky_link := get_first_link(formatted_results):
                return lucky_link

            # Fall through to regular search if unable to find link
            self.feeling_lucky = False

        # Append user config to all search links, if available
        param_str = ''.join('&{}={}'.format(k, v)
                            for k, v in
                            self.request_params.to_dict(flat=True).items()
                            if self.config.is_safe_key(k))
        for link in formatted_results.find_all('a', href=True):
            link['rel'] = "nofollow noopener noreferrer"
            if 'search?' not in link['href'] or link['href'].index(
                    'search?') > 1:
                continue
            link['href'] += param_str

        return str(formatted_results)

    def _fetch_multiple_image_pages(self, base_query):
        """Fetch multiple pages of image results and combine them"""
        all_image_results = []
        
        # Fetch 5 pages (20 images each = 100 total)
        for page in range(5):
            start_index = page * 20
            page_query = base_query + f"&start={start_index}"
            
            try:
                page_response = g.user_request.send(query=page_query,
                                                   force_mobile=self.config.view_image,
                                                   user_agent=self.user_agent)
                
                # Clean the response
                page_body_safed = page_response.text.replace("&lt;","andlt;").replace("&gt;","andgt;")
                page_soup = bsoup(page_body_safed, 'html.parser')
                
                # Extract image results from this page
                image_containers = page_soup.find_all('div', class_='isv-r')
                all_image_results.extend(image_containers)
                
                # If we got fewer than 20 results, we've reached the end
                if len(image_containers) < 20:
                    break
                    
            except Exception as e:
                # If a page fails, continue with what we have
                break
        
        # Create a new soup with all combined results
        if all_image_results:
            # Get the base structure from the first page
            first_page_response = g.user_request.send(query=base_query,
                                                     force_mobile=self.config.view_image,
                                                     user_agent=self.user_agent)
            first_page_body = first_page_response.text.replace("&lt;","andlt;").replace("&gt;","andgt;")
            combined_soup = bsoup(first_page_body, 'html.parser')
            
            # Find the main image results container
            main_container = combined_soup.find('div', {'id': 'islmp'})
            if main_container:
                # Clear existing results
                for existing in main_container.find_all('div', class_='isv-r'):
                    existing.decompose()
                
                # Add all collected results
                for result in all_image_results:
                    main_container.append(result)
            
            return str(combined_soup)
        else:
            # Fallback to single page if something went wrong
            response = g.user_request.send(query=base_query,
                                          force_mobile=self.config.view_image,
                                          user_agent=self.user_agent)
            return response.text.replace("&lt;","andlt;").replace("&gt;","andgt;")


# File: simple_cors_proxy/proxy.py
from urllib.parse import urlencode, quote
import requests
import io

import platform

PLATFORM = platform.system().lower()
CORS_PROXIES = {
    "corsproxyio": {"url": "https://corsproxy.io/?url={}", "quote": True},
    "allorigins": {"url": "https://api.allorigins.win/raw?url={}", "quote": True},
    "none": {"url": "{}", "quote": False},
}

cache_bust_headers =  {"Cache-Control": "no-cache","Pragma": "no-cache"}

def apply_cors_proxy(url, proxy="corsproxyio"):
    """
    Apply a CORS proxy to the given URL.

    Args:
        url (str): The original URL to proxy
        proxy (str): The proxy identifier to use from CORS_PROXIES

    Returns:
        str: The proxied URL
    """
    if proxy not in CORS_PROXIES:
        raise ValueError(
            f"Unknown proxy: {proxy}. Available proxies: {', '.join(CORS_PROXIES.keys())}"
        )

    proxy_config = CORS_PROXIES[proxy]

    if proxy_config["quote"]:
        url = proxy_config["url"].format(quote(url))
    else:
        url = proxy_config["url"].format(url)

    return url


def xurl(url, params=None, force=False, proxy="corsproxyio"):
    """Generate a proxied URL."""
    if PLATFORM == "emscripten" or force:
        if params:
            url = f"{url}?{urlencode(params)}"
        # url = f"https://corsproxy.io/{quote(url)}"
        url = apply_cors_proxy(url, proxy=proxy)

    return url


def furl(url, params=None, force=False, proxy="corsproxyio", cache_bust=True):
    """Return file like object after calling the proxied URL."""
    r = cors_proxy_get(url, params, force, proxy=proxy, cache_bust=cache_bust)

    # Return a file-like object from the JSON string
    # TO DO - something to consider?
    # https://simonwillison.net/2025/Jan/31/save-memory-with-bytesio/
    return io.BytesIO(r.content)


def cors_proxy_get(url, params=None, force=False, proxy="corsproxyio", cache_bust=True):
    """
    CORS proxy for GET resources with requests-like response.

    Args:
        url (str): The URL to fetch
        params (dict, optional): Query parameters to include

    Returns:
        A requests response object.
    """
    proxy_url = xurl(url, params, force, proxy=proxy)

    # Do a simple requests get and
    # just pass through the entire response object
    headers = cache_bust_headers if cache_bust else None
    return requests.get(proxy_url, headers=headers)


def robust_get_request(url, params=None, proxy="corsproxyio", cache_bust=True):
    """
    Try to make a simple request else fall back to a proxy.
    """
    headers = cache_bust_headers if cache_bust else None
    try:
        r = requests.get(url, params=params, headers=headers)
    except:
        r = cors_proxy_get(url, params=params, proxy=proxy, cache_bust=cache_bust)
    return r

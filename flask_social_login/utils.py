# -*- coding: utf-8 -*-
"""
    flask_social_login.utils
    ~~~~~~~~~~~~~~~~~~~~~~

    This module contains the Flask-Social utils

    :copyright: (c) 2012 by Matt Wright.
    :license: MIT, see LICENSE for more details.
"""
import collections
from functools import wraps

from importlib import import_module

from werkzeug.local import LocalProxy

try:
    from urlparse import urlsplit
except ImportError:  # pragma: no cover
    from urllib.parse import urlsplit

from flask import current_app, url_for, request, abort, flash, session, redirect
from flask_login import current_user

_social = LocalProxy(lambda: current_app.extensions["social"])


def get_provider_or_404(provider_id):
    try:
        return current_app.extensions["social"].providers[provider_id]
    except KeyError:
        abort(404)


def config_value(key, app=None):
    app = app or current_app
    return app.config["SOCIAL_" + key.upper()]


def get_authorize_callback(endpoint, provider_id):
    """Get a qualified URL for the provider to return to upon authorization

    param: endpoint: Absolute path to append to the application's host
    """
    endpoint_prefix = config_value("BLUEPRINT_NAME")
    url = url_for(endpoint_prefix + "." + endpoint, provider_id=provider_id)
    return request.url_root[:-1] + url


def get_connection_values_from_oauth_response(provider, oauth_response):
    if oauth_response is None:
        return None

    module = import_module(provider.module)

    return module.get_connection_values(
        oauth_response,
        consumer_key=provider.consumer_key,
        consumer_secret=provider.consumer_secret,
    )


def get_token_pair_from_oauth_response(provider, oauth_response):
    module = import_module(provider.module)
    return module.get_token_pair_from_response(oauth_response)


def get_config(app):
    """Conveniently get the social configuration for the specified
    application without the annoying 'SOCIAL_' prefix.

    :param app: The application to inspect
    """
    items = app.config.items()
    prefix = "SOCIAL_"

    def strip_prefix(tup):
        return (tup[0].replace(prefix, ""), tup[1])

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def update_recursive(d, u):
    for k, v in u.items():
    # for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update_recursive(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def get_url(endpoint_or_url):
    """Returns a URL if a valid endpoint is found. Otherwise, returns the
    provided value.

    :param endpoint_or_url: The endpoint name or URL to default to
    """
    try:
        return url_for(endpoint_or_url)
    except:
        return endpoint_or_url


def do_flash(message, category=None):
    """Flash a message depending on if the `FLASH_MESSAGES` configuration
    value is set.

    :param message: The flash message
    :param category: The flash message category
    """
    if config_value("FLASH_MESSAGES"):
        flash(message, category)


def find_redirect(key):
    """Returns the URL to redirect to after a user logs in successfully.

    :param key: The session or application configuration key to search for
    """
    rv = (
        get_url(session.pop(key.lower(), None))
        or get_url(current_app.config[key.upper()] or None)
        or "/"
    )
    return rv


def validate_redirect_url(url):
    if url is None or url.strip() == "":
        return False
    url_next = urlsplit(url)
    url_base = urlsplit(request.host_url)
    if (url_next.netloc or url_next.scheme) and url_next.netloc != url_base.netloc:
        return False
    return True


def get_post_action_redirect(config_key, declared=None):
    urls = [
        get_url(request.args.get("next")),
        get_url(request.form.get("next")),
        find_redirect(config_key),
    ]
    if declared:
        urls.insert(0, declared)
    for url in urls:
        if validate_redirect_url(url):
            return url


def get_post_login_redirect(declared=None):
    return get_post_action_redirect("SOCIAL_POST_LOGIN_VIEW", declared)


def anonymous_user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(get_url(_social.post_login_view))
        return f(*args, **kwargs)

    return wrapper

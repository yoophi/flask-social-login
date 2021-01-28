# -*- coding: utf-8 -*-
"""
    flask.ext.social.providers.google
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains the Flask-Social google code

    :copyright: (c) 2012 by Matt Wright.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import httplib2
import oauth2client.client as googleoauth
import apiclient.discovery as googleapi

config = {
    "id": "google",
    "name": "Google",
    "install": "pip install google-api-python-client",
    "module": "flask_social_login.providers.google",
    "base_url": "https://www.google.com/accounts/",
    "authorize_url": "https://accounts.google.com/o/oauth2/auth",
    "access_token_url": "https://accounts.google.com/o/oauth2/token",
    "request_token_url": None,
    "access_token_method": "POST",
    "request_token_params": {
        "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/plus.me"
        # add ' https://www.googleapis.com/auth/userinfo.email' to scope to also get email
    },
}


def _get_api(credentials):
    http = httplib2.Http()
    http = credentials.authorize(http)
    api = googleapi.build("oauth2", "v2", http=http)
    return api


def get_api(connection, **kwargs):
    credentials = googleoauth.AccessTokenCredentials(
        access_token=getattr(connection, "access_token"), user_agent=""
    )
    return _get_api(credentials)


def get_provider_user_id(response, **kwargs):
    if response:
        credentials = googleoauth.AccessTokenCredentials(
            access_token=response["access_token"], user_agent=""
        )
        profile = _get_api(credentials).userinfo().get().execute()
        print('get_provider_user_id')
        print(f'profile={profile}')
        return profile["id"]
    return None


def get_connection_values(response, **kwargs):
    if not response:
        return None

    access_token = response["access_token"]

    credentials = googleoauth.AccessTokenCredentials(
        access_token=access_token, user_agent=""
    )

    profile = _get_api(credentials).userinfo().get().execute()
    print('== get_connection_values ==')
    print(f'profile={profile}')
    '''
    profile={'id': '104240892984546281908'
             'name': '유병혁'
             'given_name': '병혁'
             'family_name': '유'
             'picture': 'https://lh3.googleusercontent.com/a-/AOh14GiUE4c4pRdQBlIEqwzP53EtGay0AkDEkEws2s5b=s96-c'
             'locale': 'en'}

   '''
    rv = dict(provider_id=config["id"], provider_user_id=profile["id"], access_token=access_token, secret=None,
             display_name=profile["name"], full_name=profile["name"], profile_url=profile.get("link"),
             image_url=profile.get("picture"), email=profile.get("email"), )
    print(f'rv={rv}')

    return rv


def get_token_pair_from_response(response):
    return dict(access_token=response.get("access_token", None), secret=None)
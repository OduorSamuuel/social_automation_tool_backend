from django.conf import settings
from requests_oauthlib import OAuth2Session
from django.shortcuts import redirect
from django.http import JsonResponse

def link_facebook(request):
    # Initialize OAuth2Session with client_id, redirect_uri, and scope from settings
    oauth = OAuth2Session(
        settings.FACEBOOK_CLIENT_ID, 
        redirect_uri=settings.FACEBOOK_REDIRECT_URI,
        scope=['public_profile', 'email']  # Move scope here
    )

    # Facebook OAuth endpoint for authorization
    authorization_url, state = oauth.authorization_url(
        'https://www.facebook.com/v10.0/dialog/oauth',
    )

    # Save the OAuth state in the session
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def facebook_callback(request):
    # Use the stored state from session
    oauth = OAuth2Session(
        settings.FACEBOOK_CLIENT_ID, 
        redirect_uri=settings.FACEBOOK_REDIRECT_URI, 
        state=request.session['oauth_state']
    )

    # Facebook OAuth token URL
    token_url = 'https://graph.facebook.com/v10.0/oauth/access_token'

    # Exchange the authorization code for an access token
    token = oauth.fetch_token(
        token_url,
        client_secret=settings.FACEBOOK_CLIENT_SECRET,  # Using client secret from settings
        authorization_response=request.build_absolute_uri()
    )

    # Save the access token in session (or database if needed)
    request.session['facebook_access_token'] = token['access_token']
    return JsonResponse({'message': 'Facebook account linked successfully', 'token': token['access_token']})

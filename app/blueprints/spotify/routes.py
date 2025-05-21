from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import login_required, current_user
from app.blueprints.spotify import bp
from extensions import db
import logging
import os
import base64
import requests
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

# Get credentials from environment
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI')

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('spotify/index.html', title='Spotify Integration')

@bp.route('/authorize')
@login_required
def authorize():
    # Create authorization URL
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'user-read-private user-read-email playlist-modify-public playlist-modify-private user-top-read',
        'show_dialog': True
    }
    
    auth_url = f"{AUTH_URL}?{'&'.join(f'{key}={val}' for key, val in params.items())}"
    return redirect(auth_url)

@bp.route('/callback')
def callback():
    # Handle the callback from Spotify
    error = request.args.get('error')
    code = request.args.get('code')
    
    if error:
        logger.error(f"Spotify authorization error: {error}")
        flash(f"Authentication error: {error}", 'danger')
        return redirect(url_for('spotify.index'))
    
    if not code:
        flash("No authorization code received from Spotify", 'danger')
        return redirect(url_for('spotify.index'))
    
    # Get tokens
    try:
        auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        
        tokens = response.json()
        
        # Store tokens in session
        session['spotify_token'] = tokens['access_token']
        session['spotify_refresh_token'] = tokens['refresh_token']
        session['spotify_token_expiry'] = datetime.now().timestamp() + tokens['expires_in']
        
        # Get user profile
        logger.info("Successfully authenticated with Spotify")
        flash("Successfully connected to Spotify!", 'success')
        return redirect(url_for('spotify.profile'))
    
    except Exception as e:
        logger.error(f"Error during Spotify token exchange: {str(e)}")
        flash(f"Error authenticating with Spotify: {str(e)}", 'danger')
        return redirect(url_for('spotify.index'))

@bp.route('/profile')
@login_required
def profile():
    # Show Spotify profile information
    if 'spotify_token' not in session:
        flash("Please connect to Spotify first", 'warning')
        return redirect(url_for('spotify.index'))
    
    try:
        # Check if token needs refresh
        if datetime.now().timestamp() > session.get('spotify_token_expiry', 0):
            _refresh_token()
        
        # Get user profile
        headers = {'Authorization': f"Bearer {session['spotify_token']}"}
        response = requests.get(f"{API_BASE_URL}me", headers=headers)
        response.raise_for_status()
        
        profile_data = response.json()
        return render_template('spotify/profile.html', profile=profile_data, title='Spotify Profile')
    
    except Exception as e:
        logger.error(f"Error fetching Spotify profile: {str(e)}")
        flash(f"Error accessing Spotify: {str(e)}", 'danger')
        return redirect(url_for('spotify.index'))

def _refresh_token():
    # Refresh the Spotify access token
    if 'spotify_refresh_token' not in session:
        return False
    
    try:
        auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': session['spotify_refresh_token']
        }
        
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        
        tokens = response.json()
        
        # Update token in session
        session['spotify_token'] = tokens['access_token']
        session['spotify_token_expiry'] = datetime.now().timestamp() + tokens['expires_in']
        
        # Update refresh token if provided
        if 'refresh_token' in tokens:
            session['spotify_refresh_token'] = tokens['refresh_token']
        
        return True
    
    except Exception as e:
        logger.error(f"Error refreshing Spotify token: {str(e)}")
        return False 
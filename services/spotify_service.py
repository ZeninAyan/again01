import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import current_app, session, url_for
import random

# Mapping of moods to Spotify audio features
MOOD_MAPPINGS = {
    'happy': {
        'min_valence': 0.7,
        'min_energy': 0.6,
        'max_energy': 1.0,
        'seed_genres': ['pop', 'happy', 'dance']
    },
    'sad': {
        'max_valence': 0.4,
        'max_energy': 0.4,
        'seed_genres': ['sad', 'acoustic', 'rainy-day']
    },
    'energetic': {
        'min_energy': 0.8,
        'min_tempo': 120,
        'seed_genres': ['dance', 'electronic', 'workout']
    },
    'calm': {
        'max_energy': 0.4,
        'max_tempo': 100,
        'seed_genres': ['ambient', 'chill', 'sleep']
    },
    'anxious': {
        'min_energy': 0.5,
        'max_valence': 0.5,
        'seed_genres': ['focus', 'ambient', 'study']
    },
    'angry': {
        'min_energy': 0.7,
        'max_valence': 0.4,
        'seed_genres': ['rock', 'metal', 'intense']
    },
    'romantic': {
        'min_valence': 0.5,
        'max_energy': 0.6,
        'seed_genres': ['romance', 'r-n-b', 'jazz']
    },
    'focused': {
        'max_energy': 0.6,
        'min_instrumentalness': 0.3,
        'seed_genres': ['focus', 'classical', 'study']
    },
    'relaxed': {
        'max_energy': 0.5,
        'min_valence': 0.4,
        'seed_genres': ['chill', 'acoustic', 'ambient']
    },
    'melancholic': {
        'max_valence': 0.5,
        'max_energy': 0.5,
        'seed_genres': ['indie', 'sad', 'rainy-day']
    }
}

def get_spotify_client():
    """Get an authenticated Spotify client"""
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
    redirect_uri = current_app.config['SPOTIFY_REDIRECT_URI']
    
    # Check if we have a cached token
    cache_token = session.get('spotify_token')
    
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-modify-private user-read-private user-read-email',
        cache_handler=None,  # We'll handle caching in the session
        show_dialog=True
    )
    
    # If we have a cached token, use it
    if cache_token:
        auth_manager.cache_token = cache_token
    
    return spotipy.Spotify(auth_manager=auth_manager)

def get_auth_url():
    """Get the Spotify authorization URL"""
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
    redirect_uri = current_app.config['SPOTIFY_REDIRECT_URI']
    
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-modify-private user-read-private user-read-email',
        show_dialog=True
    )
    
    return auth_manager.get_authorize_url()

def get_token(code):
    """Exchange authorization code for access token"""
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
    redirect_uri = current_app.config['SPOTIFY_REDIRECT_URI']
    
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-modify-private user-read-private user-read-email'
    )
    
    try:
        token_info = auth_manager.get_access_token(code)
        session['spotify_token'] = token_info
        return True
    except Exception as e:
        print(f"Error getting token: {e}")
        return False

def get_recommendations_for_mood(mood):
    """Get track recommendations based on mood"""
    try:
        sp = get_spotify_client()
        
        # Get mood parameters
        mood_params = MOOD_MAPPINGS.get(mood.lower(), {})
        if not mood_params:
            # Default to random recommendations if mood not found
            seed_genres = ['pop', 'rock', 'indie']
        else:
            seed_genres = mood_params.get('seed_genres', ['pop'])
            
        # Select random genres from the seed genres (max 5)
        if len(seed_genres) > 5:
            seed_genres = random.sample(seed_genres, 5)
            
        # Build recommendation parameters
        params = {
            'seed_genres': seed_genres,
            'limit': 20
        }
        
        # Add audio feature parameters from mood mapping
        for key, value in mood_params.items():
            if key != 'seed_genres':
                params[key] = value
                
        # Get recommendations
        results = sp.recommendations(**params)
        tracks = results.get('tracks', [])
        
        # Format track data
        formatted_tracks = []
        for track in tracks:
            formatted_tracks.append({
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify']
            })
            
        # Create a playlist with these tracks
        user_id = sp.me()['id']
        playlist = sp.user_playlist_create(
            user=user_id,
            name=f"Your {mood.capitalize()} Mood Mix",
            public=False,
            description=f"Playlist generated based on your {mood} mood"
        )
        
        # Add tracks to the playlist
        track_uris = [track['uri'] for track in tracks]
        sp.playlist_add_items(playlist['id'], track_uris)
        
        return formatted_tracks, playlist['external_urls']['spotify']
        
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return [], None

def get_playlist_details(playlist_id):
    """Get details of a specific playlist"""
    try:
        sp = get_spotify_client()
        playlist = sp.playlist(playlist_id)
        return playlist
    except Exception as e:
        print(f"Error getting playlist details: {e}")
        return None

def save_playlist_for_user(playlist_id, mood_id):
    """Save a playlist to the user's Spotify account"""
    try:
        sp = get_spotify_client()
        user_id = sp.me()['id']
        # Functionality to save playlist reference in user's profile
        return True
    except Exception as e:
        print(f"Error saving playlist: {e}")
        return False 
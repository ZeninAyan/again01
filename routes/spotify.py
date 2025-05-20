from flask import Blueprint, render_template, redirect, url_for, request, session, current_app, flash
from flask_login import login_required, current_user
from extensions import db
from models.mood import MoodEntry
from services.spotify_service import (
    get_auth_url, get_token, get_recommendations_for_mood, 
    get_playlist_details, save_playlist_for_user
)

spotify_bp = Blueprint('spotify', __name__)

@spotify_bp.route('/spotify/login')
@login_required
def spotify_login():
    auth_url = get_auth_url()
    return redirect(auth_url)

@spotify_bp.route('/callback')
@login_required
def spotify_callback():
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        flash(f'Spotify authentication failed: {error}')
        return redirect(url_for('mood.dashboard'))
    
    if code:
        success = get_token(code)
        if success:
            flash('Successfully connected to Spotify!')
        else:
            flash('Failed to connect to Spotify. Please try again.')
    
    return redirect(url_for('mood.dashboard'))

@spotify_bp.route('/spotify/recommendations/<int:mood_id>')
@login_required
def recommendations(mood_id):
    mood_entry = MoodEntry.query.get_or_404(mood_id)
    
    # Make sure the mood entry belongs to the current user
    if mood_entry.user_id != current_user.id:
        flash('You are not authorized to view this content.')
        return redirect(url_for('mood.dashboard'))
    
    # Get playlist recommendations based on mood
    tracks, playlist_url = get_recommendations_for_mood(mood_entry.mood)
    
    return render_template(
        'mood/recommendations.html',
        mood=mood_entry.mood,
        tracks=tracks,
        playlist_url=playlist_url,
        mood_id=mood_id,
        title='Your Recommendations'
    )

@spotify_bp.route('/spotify/save_playlist/<int:mood_id>', methods=['POST'])
@login_required
def save_playlist(mood_id):
    mood_entry = MoodEntry.query.get_or_404(mood_id)
    
    # Make sure the mood entry belongs to the current user
    if mood_entry.user_id != current_user.id:
        flash('You are not authorized to perform this action.')
        return redirect(url_for('mood.dashboard'))
    
    playlist_id = request.form.get('playlist_id')
    if playlist_id:
        # Save the playlist ID to the mood entry
        mood_entry.playlist_id = playlist_id
        db.session.commit()
        flash('Playlist saved to your mood history!')
    
    return redirect(url_for('mood.dashboard')) 
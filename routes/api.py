from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from datetime import timedelta

from extensions import db
from models.user import User
from models.mood import MoodEntry
from services.spotify_service import get_recommendations_for_mood, get_auth_url, get_token

api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(days=7)
    )
    
    return jsonify({
        'token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

@api_bp.route('/mood/history', methods=['GET'])
@jwt_required()
def get_mood_history():
    user_id = get_jwt_identity()
    
    moods = MoodEntry.query.filter_by(user_id=user_id).order_by(
        MoodEntry.timestamp.desc()
    ).all()
    
    mood_list = []
    for mood in moods:
        mood_list.append({
            'id': mood.id,
            'user_id': mood.user_id,
            'mood': mood.mood,
            'comment': mood.comment,
            'timestamp': mood.timestamp.isoformat(),
            'playlist_id': mood.playlist_id
        })
    
    return jsonify({'moods': mood_list}), 200

@api_bp.route('/mood/new', methods=['POST'])
@jwt_required()
def add_mood():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    mood_type = data.get('mood')
    comment = data.get('comment', '')
    
    if not mood_type:
        return jsonify({'message': 'Mood type is required'}), 400
    
    mood_entry = MoodEntry(
        user_id=user_id,
        mood=mood_type,
        comment=comment
    )
    
    db.session.add(mood_entry)
    db.session.commit()
    
    return jsonify({
        'message': 'Mood recorded successfully',
        'mood': {
            'id': mood_entry.id,
            'user_id': mood_entry.user_id,
            'mood': mood_entry.mood,
            'comment': mood_entry.comment,
            'timestamp': mood_entry.timestamp.isoformat(),
            'playlist_id': mood_entry.playlist_id
        }
    }), 201

@api_bp.route('/spotify/recommendations/<int:mood_id>', methods=['GET'])
@jwt_required()
def get_recommendations(mood_id):
    user_id = get_jwt_identity()
    
    mood_entry = MoodEntry.query.get_or_404(mood_id)
    
    # Ensure the mood entry belongs to the current user
    if mood_entry.user_id != user_id:
        return jsonify({'message': 'Unauthorized access to this mood entry'}), 403
    
    try:
        tracks, playlist_url = get_recommendations_for_mood(mood_entry.mood)
        
        return jsonify({
            'tracks': tracks,
            'playlist_url': playlist_url
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error getting recommendations: {str(e)}'}), 500

@api_bp.route('/spotify/login', methods=['GET'])
@jwt_required()
def spotify_login():
    try:
        auth_url = get_auth_url()
        return jsonify({'auth_url': auth_url}), 200
    except Exception as e:
        return jsonify({'message': f'Error getting Spotify auth URL: {str(e)}'}), 500

@api_bp.route('/spotify/callback', methods=['GET'])
@jwt_required()
def spotify_callback():
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return jsonify({'message': f'Spotify authentication failed: {error}'}), 400
    
    if not code:
        return jsonify({'message': 'No authorization code provided'}), 400
    
    try:
        success = get_token(code)
        if success:
            return jsonify({'message': 'Successfully connected to Spotify'}), 200
        else:
            return jsonify({'message': 'Failed to connect to Spotify'}), 500
    except Exception as e:
        return jsonify({'message': f'Error processing Spotify callback: {str(e)}'}), 500

@api_bp.route('/spotify/save_playlist/<int:mood_id>', methods=['POST'])
@jwt_required()
def save_playlist(mood_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    playlist_id = data.get('playlist_id')
    
    if not playlist_id:
        return jsonify({'message': 'Playlist ID is required'}), 400
    
    mood_entry = MoodEntry.query.get_or_404(mood_id)
    
    # Ensure the mood entry belongs to the current user
    if mood_entry.user_id != user_id:
        return jsonify({'message': 'Unauthorized access to this mood entry'}), 403
    
    mood_entry.playlist_id = playlist_id
    db.session.commit()
    
    return jsonify({'message': 'Playlist saved to mood history'}), 200 
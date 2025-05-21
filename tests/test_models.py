"""
Unit tests for MusicApp database models
"""
import pytest
from app.models.user import User
from app.models.mood import MoodEntry
from datetime import datetime
from extensions import db
from werkzeug.security import check_password_hash


def test_user_model(app):
    """Test the User model"""
    with app.app_context():
        # Test user creation
        user = User(username='newuser', email='new@example.com')
        user.set_password('Password123')
        db.session.add(user)
        db.session.commit()
        
        # Test querying the user
        saved_user = User.query.filter_by(username='newuser').first()
        assert saved_user is not None
        assert saved_user.email == 'new@example.com'
        
        # Test password hashing and verification
        assert saved_user.check_password('Password123')
        assert not saved_user.check_password('wrongpassword')
        
        # Test reset token
        token = saved_user.generate_reset_token()
        assert saved_user.reset_token is not None
        saved_user.clear_reset_token()
        assert saved_user.reset_token is None


def test_user_password_setter(app):
    """Test password property setter"""
    user = User(username='testpassword', email='password@example.com')
    user.set_password('password123')
    
    # Password should be hashed, not stored as plain text
    assert user.password_hash is not None
    assert 'password123' not in user.password_hash


def test_user_check_password(app):
    """Test password checking method"""
    user = User(username='checkpassword', email='check@example.com')
    user.set_password('correctpassword')
    
    assert user.check_password('correctpassword') is True
    assert user.check_password('incorrectpassword') is False


def test_mood_model(app):
    with app.app_context():
        # Test mood entry creation
        user = User.query.first()
        mood = MoodEntry(
            user_id=user.id,
            mood='excited',
            intensity=9,
            comment='Really looking forward to the concert!',
            track_ids='track1,track2,track3'
        )
        db.session.add(mood)
        db.session.commit()
        
        # Test querying the mood
        saved_mood = MoodEntry.query.filter_by(mood='excited').first()
        assert saved_mood is not None
        assert saved_mood.intensity == 9
        
        # Test track list property
        assert len(saved_mood.track_list) == 3
        assert 'track2' in saved_mood.track_list
        
        # Test to_dict method
        mood_dict = saved_mood.to_dict()
        assert mood_dict['mood'] == 'excited'
        assert mood_dict['comment'] == 'Really looking forward to the concert!'
        assert len(mood_dict['track_ids']) == 3 
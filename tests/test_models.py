"""
Unit tests for MusicApp database models
"""
import pytest
from models.user import User
from werkzeug.security import check_password_hash


def test_user_model(app):
    """Test the User model"""
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        
        # Add to db
        from extensions import db
        db.session.add(user)
        db.session.commit()
        
        # Query the user
        retrieved_user = User.query.filter_by(username='testuser').first()
        
        # Check user exists
        assert retrieved_user is not None
        assert retrieved_user.username == 'testuser'
        assert retrieved_user.email == 'test@example.com'
        
        # Check password hashing
        assert check_password_hash(retrieved_user.password_hash, 'password123')
        assert not check_password_hash(retrieved_user.password_hash, 'wrongpassword')
        
        # Check __repr__
        assert str(retrieved_user) == f'<User {retrieved_user.username}>'


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
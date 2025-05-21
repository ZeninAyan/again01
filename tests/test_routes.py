"""
Integration tests for MusicApp routes
"""
import pytest


def test_home_page(client):
    """Test that the home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'MoodMusic' in response.data


def test_login_page(client):
    """Test that the login page loads successfully"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_register_page(client):
    """Test that the register page loads successfully"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data
    assert b'Username' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_login_logout(client, app):
    """Test login and logout functionality"""
    # Create a user to test with
    with app.app_context():
        from models.user import User
        from extensions import db
        
        # Check if test user already exists
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
    
    # Test login with correct credentials
    response = client.post(
        '/login',
        data={'email': 'test@example.com', 'password': 'password'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Welcome back' in response.data or b'logged in' in response.data
    
    # Test logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'logged out' in response.data.lower() or b'login' in response.data.lower()


def test_protected_route_redirect(client):
    """Test that protected routes redirect to login when not authenticated"""
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data.lower()
    
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data.lower() 
"""
Pytest fixtures for MusicApp tests
"""
import os
import tempfile
import pytest
from app import create_app
from extensions import db
from config import Config
from app.models.user import User
from app.models.mood import MoodEntry


class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'


@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app(TestConfig)
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        
        # Create test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('Password123')
        db.session.add(user)
        
        # Create sample mood
        mood = MoodEntry(
            user_id=1,
            mood='happy',
            intensity=8,
            comment='Feeling good!'
        )
        db.session.add(mood)
        
        db.session.commit()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app"""
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    """Authentication helper for tests"""
    class AuthActions:
        def __init__(self, client):
            self._client = client

        def login(self, email="test@example.com", password="password"):
            return self._client.post(
                '/login',
                data={'email': email, 'password': password}
            )

        def logout(self):
            return self._client.get('/logout')

    return AuthActions(client)


@pytest.fixture
def auth_client(client):
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Password123'
    }, follow_redirects=True)
    return client 
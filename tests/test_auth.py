import pytest
from flask import session

def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Sign In' in response.data

def test_register_page(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_successful_login(client):
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'logged in successfully' in response.data

def test_failed_login(client):
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_logout(auth_client):
    response = auth_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out' in response.data 
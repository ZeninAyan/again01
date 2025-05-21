"""
Production configuration for MusicApp
This file contains settings optimized for production deployment
"""
import os
from config import Config

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # PostgreSQL configuration
    # In production, we should always use environment variables
    # for sensitive information like database credentials
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # Mail server setup for error notifications
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = [os.environ.get('ADMIN_EMAIL')] if os.environ.get('ADMIN_EMAIL') else []
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    
    # Additional production settings
    SERVER_NAME = os.environ.get('SERVER_NAME')  # e.g., 'musicapp.example.com'
    PREFERRED_URL_SCHEME = 'https' 
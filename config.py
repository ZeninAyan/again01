import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e300f5d8ad7e400815ee6cc71587b012'
    
    # PostgreSQL Configuration
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'fuckUpostgre01'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'musicapp'
    
    # Build connection string
    POSTGRES_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # Try PostgreSQL connection first, fallback to SQLite
    try:
        from sqlalchemy import create_engine
        engine = create_engine(POSTGRES_URI, pool_pre_ping=True)
        connection = engine.connect()
        connection.close()
        SQLALCHEMY_DATABASE_URI = POSTGRES_URI
        logger.info("Successfully connected to PostgreSQL database")
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed: {e}")
        logger.info("Falling back to SQLite database")
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///app.db'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Spotify API credentials
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID') or 'dummy_client_id'
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') or 'dummy_client_secret'
    SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI') or 'http://localhost:5000/callback' 
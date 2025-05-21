"""
Database initialization script
Run this script to create the necessary database and tables for the application
"""
import os
from app import create_app
from extensions import db
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from config import Config

def init_database():
    """Create the database if it doesn't exist and initialize tables"""
    # Get the database URI from config
    db_uri = Config.SQLALCHEMY_DATABASE_URI
    
    # Create the database if it doesn't exist
    engine = create_engine(db_uri)
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database '{Config.DB_NAME}' created successfully.")
    else:
        print(f"Database '{Config.DB_NAME}' already exists.")
    
    # Create the tables
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
    
    print("Database initialization complete!")

if __name__ == "__main__":
    init_database() 
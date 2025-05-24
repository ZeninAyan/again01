from flask import Flask
from flask_cors import CORS
from config import ActiveConfig
from extensions import db, login_manager, migrate, jwt
from routes.auth import auth_bp
from routes.mood import mood_bp
from routes.spotify import spotify_bp
from routes.api import api_bp
from models.user import User
from logging_config import configure_logging

def create_app(config_class=ActiveConfig):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    initialize_extensions(app)
    
    # Configure logging
    configure_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Set up user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        app.logger.info('Database tables created or verified')
    
    return app

def initialize_extensions(app):
    """Initialize Flask extensions."""
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(spotify_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0') 
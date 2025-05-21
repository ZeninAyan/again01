from flask import Flask
from config import Config
from extensions import db, login_manager, migrate
from logging_config import configure_logging
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure logging
    configure_logging(app)
    
    # Register blueprints
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.mood import bp as mood_bp
    from app.blueprints.spotify import bp as spotify_bp
    from app.blueprints.errors import bp as errors_bp
    from app.blueprints.main import bp as main_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(mood_bp, url_prefix='/mood')
    app.register_blueprint(spotify_bp, url_prefix='/spotify')
    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)
    
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        app.logger.info('Database tables created or verified')
    
    return app 
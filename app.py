from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, login_manager, migrate, jwt
from routes.auth import auth_bp
from routes.mood import mood_bp
from routes.spotify import spotify_bp
from routes.api import api_bp
from models.user import User
from logging_config import configure_logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Configure logging
    configure_logging(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(spotify_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        app.logger.info('Database tables created or verified')
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0') 
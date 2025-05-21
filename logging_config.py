"""
Logging configuration for MusicApp
"""
import os
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from pathlib import Path

def configure_logging(app):
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure file handler for INFO level and above
    file_handler = RotatingFileHandler(
        logs_dir / "musicapp.log", 
        maxBytes=10240, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    # Configure error file handler for ERROR level and above
    error_file_handler = RotatingFileHandler(
        logs_dir / "error.log", 
        maxBytes=10240, 
        backupCount=10
    )
    error_file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    ))
    error_file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_file_handler)
    
    # Configure email handler for error notifications in production
    if not app.debug and not app.testing:
        if app.config.get('MAIL_SERVER'):
            auth = None
            if app.config.get('MAIL_USERNAME') or app.config.get('MAIL_PASSWORD'):
                auth = (app.config.get('MAIL_USERNAME'), app.config.get('MAIL_PASSWORD'))
            
            secure = None
            if app.config.get('MAIL_USE_TLS'):
                secure = ()
            
            mail_handler = SMTPHandler(
                mailhost=(app.config.get('MAIL_SERVER'), app.config.get('MAIL_PORT')),
                fromaddr=f"no-reply@{app.config.get('MAIL_SERVER')}",
                toaddrs=app.config.get('ADMINS', []),
                subject='MusicApp Error',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    
    # Set app logger level
    app.logger.setLevel(logging.INFO)
    app.logger.info('MusicApp startup')
    
    return app 
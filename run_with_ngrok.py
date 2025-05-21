"""
Run the Flask application with ngrok tunnel for public accessibility
"""
import threading
import time
from app import create_app
from extensions import db
from ngrok_config import setup_ngrok
from init_db import init_database

def run_flask_app():
    """Run the Flask application"""
    app = create_app()
    
    # Initialize the ngrok tunnel
    threading.Thread(target=lambda: setup_ngrok()).start()
    
    # Sleep briefly to allow ngrok to establish the tunnel
    time.sleep(2)
    
    # Run the Flask app
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    print("Initializing database...")
    try:
        init_database()
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("Continuing with application startup...")
    
    print("Starting Flask application with ngrok tunnel...")
    run_flask_app() 
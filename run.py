from app import create_app
from extensions import db
from models import User, MoodEntry
from init_db import init_database

# Create the Flask application
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'MoodEntry': MoodEntry}

if __name__ == '__main__':
    # Make sure the database is initialized
    try:
        init_database()
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("Continuing with application startup...")
    
    # Run the Flask application
    app.run(debug=True) 
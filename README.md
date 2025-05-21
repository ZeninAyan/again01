# MoodMusic - Mood-Based Music Recommendation App

MoodMusic is a Flask-based web application that recommends music based on your current mood using the Spotify API. The app allows users to record their moods, get personalized music recommendations, and keep track of their mood history.

## Features

- User authentication (register, login, logout)
- Record your current mood with optional comments
- Get personalized Spotify playlist recommendations based on your mood
- Save playlists to your mood history
- View your mood history and associated playlists
- Public accessibility through ngrok tunneling

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: PostgreSQL (primary), SQLite (fallback)
- **API Integration**: Spotify API via Spotipy
- **Tunneling**: ngrok for public access

## Setup Instructions

### Prerequisites

- Python 3.7+
- PostgreSQL database server
- Spotify Developer Account (for API credentials)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/moodmusic.git
   cd moodmusic
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### PostgreSQL Setup

1. Make sure PostgreSQL is installed and running on your system.
2. Create a database for the application:
   ```
   createdb musicapp
   ```
   
   Alternatively, you can use pgAdmin or another PostgreSQL client to create the database.

3. Run the configuration tool to set up your database connection:
   ```
   python configure_db.py
   ```
   
   This interactive tool will help you configure your PostgreSQL connection and create a `.env` file.

### Alternative Manual Configuration

If you prefer to configure the database manually:

1. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DB_USER=your_postgres_username
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=musicapp
   DATABASE_URI=postgresql://your_postgres_username:your_postgres_password@localhost:5432/musicapp
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
   ```

### Database Initialization

1. Initialize the database migrations:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

2. Run the application:
   ```
   python run.py
   ```

3. Access the application at http://localhost:5000

## Ngrok Public URL Setup

The application can be made publicly accessible using ngrok tunneling:

1. Run the application with ngrok enabled:
   ```
   python run_with_ngrok.py
   ```

2. The console will display the public URL where your app is accessible.

3. This URL can be shared with anyone to access your application from anywhere.

## Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new application
3. Set the redirect URI to match your ngrok URL plus `/callback` (when using ngrok)
   or use `http://localhost:5000/callback` (when running locally)
4. Copy your Client ID and Client Secret to the `.env` file

## Improvements & Next Steps

### Add Logging
- Enhanced logging is already implemented in `config.py` using Python's built-in logging module
- For more comprehensive logging:
  ```python
  # Example of advanced logging setup
  import logging
  from logging.handlers import RotatingFileHandler
  
  # Setup file logging with rotation
  file_handler = RotatingFileHandler('logs/musicapp.log', maxBytes=10240, backupCount=10)
  file_handler.setFormatter(logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
  ))
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  ```

### Write Tests
- Create a `tests/` directory with the following structure:
  ```
  tests/
  ├── __init__.py
  ├── conftest.py           # pytest fixtures
  ├── test_models.py        # unit tests for database models
  ├── test_routes.py        # integration tests for routes
  └── test_services.py      # unit tests for service functions
  ```
- Install testing dependencies:
  ```
  pip install pytest pytest-flask
  ```
- Run tests with: `pytest -v`

### Virtual Environment
- Already implemented with `venv`
- Consider using `pipenv` or `poetry` for more advanced dependency management:
  ```
  pip install pipenv
  pipenv install  # Creates Pipfile and Pipfile.lock
  ```

### CI/CD Setup
- Add GitHub Actions workflow file at `.github/workflows/ci.yml`:
  ```yaml
  name: MusicApp CI

  on:
    push:
      branches: [ main ]
    pull_request:
      branches: [ main ]

  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v2
        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: '3.x'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
            pip install pytest pytest-flask
        - name: Test with pytest
          run: |
            pytest
  ```

## Project Structure

```
moodmusic/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── extensions.py           # Flask extensions initialization
├── forms/                  # WTForms definitions
│   ├── __init__.py
│   ├── auth.py             # Authentication forms
│   └── mood.py             # Mood entry forms
├── models/                 # Database models
│   ├── __init__.py
│   ├── user.py             # User model
│   └── mood.py             # Mood entry model
├── routes/                 # Route definitions
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   ├── mood.py             # Mood-related routes
│   └── spotify.py          # Spotify integration routes
├── services/               # Business logic
│   ├── __init__.py
│   └── spotify_service.py  # Spotify API integration
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── script.js       # Custom JavaScript
└── templates/              # Jinja2 templates
    ├── base.html           # Base template
    ├── index.html          # Landing page
    ├── auth/               # Authentication templates
    │   ├── login.html
    │   └── register.html
    └── mood/               # Mood-related templates
        ├── dashboard.html
        ├── history.html
        ├── new_mood.html
        └── recommendations.html
```

## Final Deployment Checklist

- [ ] Check all configurations and remove hardcoded values
- [ ] Test all features locally
- [ ] Set up proper database migrations
- [ ] Configure production-level logging
- [ ] Set up environment variables on deployment platform
- [ ] Enable HTTPS for secure connections
- [ ] Set up database backups

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
# MoodMusic - Mood-Based Music Recommendation App

MoodMusic is a Flask-based web application that recommends music based on your current mood using the Spotify API. The app allows users to record their moods, get personalized music recommendations, and keep track of their mood history.

## Features

- User authentication (register, login, logout)
- Record your current mood with optional comments
- Get personalized Spotify playlist recommendations based on your mood
- Save playlists to your mood history
- View your mood history and associated playlists

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (default), easily configurable for other databases
- **API Integration**: Spotify API via Spotipy

## Setup Instructions

### Prerequisites

- Python 3.7+
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

4. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URI=sqlite:///app.db
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

7. Access the application at http://localhost:5000

## Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new application
3. Set the redirect URI to `http://localhost:5000/callback`
4. Copy your Client ID and Client Secret to the `.env` file

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

## Future Enhancements

- Mobile app integration with Flutter
- Mood analytics and trends visualization
- Social sharing features
- More sophisticated mood-to-music mapping algorithms
- User preference customization

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
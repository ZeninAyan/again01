# Music Mood App

A Flask-based web application that helps users discover music based on their current mood using Spotify integration.

## Features

- **User Authentication**: Secure registration and login system
- **Mood Analysis**: Track your mood and find music that matches it
- **Spotify Integration**: Seamlessly connect with your Spotify account to access millions of songs
- **Personalized Recommendations**: Get music recommendations based on your mood history
- **Playlist Management**: Create and save playlists to enjoy later or share with friends
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technology Stack

- **Backend**: Python 3.11+, Flask 3.1.1
- **Database**: PostgreSQL, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **API Integration**: Spotify Web API
- **Testing**: Pytest, Coverage
- **CI/CD**: GitHub Actions
- **Deployment**: Docker, Heroku

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL
- Spotify Developer Account

### Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/musicapp.git
   cd musicapp/backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:
   ```
   SECRET_KEY=your_secret_key
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=musicapp
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:5000/spotify/callback
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

7. The application should now be running at `http://localhost:5000`

## Project Structure

The project follows a modular structure using Flask Blueprints:

```
app/
├── blueprints/
│   ├── auth/         # Authentication routes
│   ├── errors/       # Error handling
│   ├── main/         # Main routes
│   ├── mood/         # Mood-related routes
│   └── spotify/      # Spotify integration
├── models/           # Database models
├── forms/            # WTForms definitions
├── services/         # Business logic services
├── static/           # Static files (CSS, JS)
└── templates/        # Jinja2 templates
tests/                # Test suite
config.py             # Configuration settings
run.py                # Application entry point
```

## Testing

Run tests with pytest:

```
pytest
```

Generate a coverage report:

```
pytest --cov=app
```

## Deployment

### Docker

Build and run using Docker:

```
docker build -t musicapp .
docker run -p 5000:5000 musicapp
```

### Heroku

Deploy to Heroku:

```
heroku create
git push heroku main
heroku run flask db upgrade
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Spotify Web API for music data
- Flask and its extension developers
- Bootstrap for the responsive design
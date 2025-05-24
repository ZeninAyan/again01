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

- **Backend**: Python 3.9+, Flask 3.1.1
- **Database**: SQLite (or PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login, JWT
- **API Integration**: Spotify Web API
- **Testing**: Pytest
- **Deployment**: Render.com

## Installation

### Prerequisites

- Python 3.9+
- Spotify Developer Account

### Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/musicapp.git
   cd musicapp/backend
   ```

2. Run the setup script:
   ```
   # On Windows
   setup_env.bat
   
   # On Linux/Mac
   bash render_build.sh
   ```
   
   This will:
   - Create a virtual environment
   - Install dependencies
   - Set up a .env file from sample.env
   - Create the SQLite database

3. Edit the .env file with your actual configuration:
   ```
   # Flask settings
   FLASK_APP=run.py
   FLASK_ENV=development
   FLASK_DEBUG=1

   # Security
   SECRET_KEY=your_very_secure_secret_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here

   # Database
   DATABASE_URI=sqlite:///app.db

   # Spotify API (replace with your actual keys)
   SPOTIFY_CLIENT_ID=your_spotify_client_id_here
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
   SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
   ```

4. Run the application:
   ```
   flask run
   ```

5. The application should now be running at `http://localhost:5000`

## Deployment to Render.com

1. Push your code to a GitHub repository

2. Sign up for Render.com

3. Connect your GitHub repository to Render

4. Create a new Web Service and point it to your repository

5. The render.yaml file will automatically configure your application:
   - Set up Python 3.9.18
   - Install dependencies
   - Configure environment variables
   - Set up a persistent disk for SQLite data
   - Deploy the application

## Project Structure

The project follows a modular structure using Flask Blueprints:

```
/
├── app.py              # Application factory
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions
├── run.py              # Application entry point
├── routes/             # Route blueprints
│   ├── auth.py         # Authentication routes
│   ├── mood.py         # Mood-related routes
│   ├── spotify.py      # Spotify integration
│   └── api.py          # API routes
├── models/             # Database models
├── forms/              # Form definitions
├── services/           # Business logic services
├── static/             # Static files (CSS, JS)
├── templates/          # Jinja2 templates
├── tests/              # Test suite
├── instance/           # SQLite database
├── sample.env          # Sample environment variables
├── requirements.txt    # Python dependencies
├── render.yaml         # Render.com configuration
└── render_build.sh     # Build script for Render
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
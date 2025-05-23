@echo off
echo Setting up Music Mood App Backend for Windows

REM Create a virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Update pip
echo Updating pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Create a .env file if it doesn't exist
if not exist .env (
    echo Creating .env file with SQLite configuration...
    echo DB_USE_SQLITE=True > .env
    echo SECRET_KEY=your_secret_key_here >> .env
    echo JWT_SECRET_KEY=your_jwt_secret_key_here >> .env
    echo FLASK_APP=app.py >> .env
    echo FLASK_ENV=development >> .env
)

REM Initialize the database
echo Initializing database...
python init_db.py

echo.
echo Setup complete! To start the backend server:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the Flask application: python run.py
echo.

pause 
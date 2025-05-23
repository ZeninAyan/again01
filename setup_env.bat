@echo off
echo Setting up development environment...

REM Create virtual environment if it doesn't exist
if not exist venv (
  echo Creating virtual environment...
  python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create database directory if it doesn't exist
if not exist instance mkdir instance

REM Set up database
echo Setting up SQLite database...
python -c "from app import create_app; from extensions import db; app = create_app(); app.app_context().push(); db.create_all()"

echo Environment setup complete!
echo To start the application, run: flask run
pause 
#!/bin/bash
set -e

# Music Mood App Deployment Script
echo "Starting deployment of Music Mood App..."

# Pull the latest code
echo "Pulling latest code from repository..."
git pull

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || { echo "Failed to activate virtual environment. Make sure it exists."; exit 1; }

# Install or update dependencies
echo "Installing/updating dependencies..."
pip install -r requirements.txt

# Export FLASK_APP environment variable
export FLASK_APP=run.py
export FLASK_ENV=production

# Perform database migrations
echo "Running database migrations..."
flask db migrate -m "Deployment migration $(date +%Y%m%d-%H%M%S)"
flask db upgrade

# Collect static files (if needed)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Run tests
echo "Running tests..."
pytest -xvs

# Restart the application server
echo "Restarting application server..."
if command -v supervisorctl &> /dev/null; then
    supervisorctl restart musicapp
elif command -v systemctl &> /dev/null; then
    sudo systemctl restart musicapp
else
    echo "No service manager found. Please restart the service manually."
fi

echo "Deployment completed successfully!"
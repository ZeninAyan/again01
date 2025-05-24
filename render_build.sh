#!/usr/bin/env bash
# Exit on error
set -o errexit

# Set environment to production
export FLASK_ENV=production

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create database directory if it doesn't exist
mkdir -p instance

# Run database migrations
echo "Setting up SQLite database..."
python -c "from app import create_app; from extensions import db; app = create_app(); app.app_context().push(); db.create_all()"

echo "Build script complete" 
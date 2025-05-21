from flask import Blueprint

bp = Blueprint('spotify', __name__)

from app.blueprints.spotify import routes 
from flask import Blueprint

bp = Blueprint('mood', __name__)

from app.blueprints.mood import routes 
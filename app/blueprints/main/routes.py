from flask import render_template, current_app
from app.blueprints.main import bp
from flask_login import current_user

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html', title='Home') 
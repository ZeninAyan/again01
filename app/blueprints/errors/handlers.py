from flask import render_template
from app.blueprints.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    from extensions import db
    db.session.rollback()
    return render_template('errors/500.html'), 500

@bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@bp.app_errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400 
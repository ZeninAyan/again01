from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.blueprints.mood import bp
from extensions import db
from app.models.mood import MoodEntry
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # Placeholder for the mood index page
    return render_template('mood/index.html', title='Mood Tracker')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # Placeholder for creating a new mood entry
    if request.method == 'POST':
        try:
            mood = request.form.get('mood')
            intensity = request.form.get('intensity', type=int)
            comment = request.form.get('comment')
            
            mood_entry = MoodEntry(
                user_id=current_user.id,
                mood=mood,
                intensity=intensity,
                comment=comment,
                timestamp=datetime.utcnow()
            )
            
            db.session.add(mood_entry)
            db.session.commit()
            
            logger.info(f"User {current_user.username} created mood entry: {mood}")
            flash('Your mood has been recorded!', 'success')
            return redirect(url_for('mood.history'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating mood entry: {str(e)}")
            flash('Error recording your mood. Please try again.', 'danger')
    
    return render_template('mood/create.html', title='Record Mood')

@bp.route('/history')
@login_required
def history():
    # Get user's mood history
    mood_entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.timestamp.desc()).all()
    return render_template('mood/history.html', mood_entries=mood_entries, title='Mood History')

@bp.route('/api/moods')
@login_required
def get_moods_api():
    # API endpoint to get mood data for charts
    mood_entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.timestamp.asc()).all()
    mood_data = [entry.to_dict() for entry in mood_entries]
    return jsonify(mood_data) 
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.mood import MoodEntry
from forms.mood import MoodEntryForm
from services.spotify_service import get_recommendations_for_mood

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('mood.dashboard'))
    return render_template('index.html')

@mood_bp.route('/dashboard')
@login_required
def dashboard():
    recent_moods = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.timestamp.desc()).limit(5).all()
    return render_template('mood/dashboard.html', recent_moods=recent_moods)

@mood_bp.route('/mood/new', methods=['GET', 'POST'])
@login_required
def new_mood():
    form = MoodEntryForm()
    if form.validate_on_submit():
        mood_entry = MoodEntry(
            user_id=current_user.id,
            mood=form.mood.data,
            comment=form.comment.data
        )
        db.session.add(mood_entry)
        db.session.commit()
        flash('Your mood has been recorded!')
        
        # Redirect to recommendations
        return redirect(url_for('spotify.recommendations', mood_id=mood_entry.id))
    
    return render_template('mood/new_mood.html', form=form, title='Record Your Mood')

@mood_bp.route('/mood/history')
@login_required
def mood_history():
    page = request.args.get('page', 1, type=int)
    moods = MoodEntry.query.filter_by(user_id=current_user.id).order_by(
        MoodEntry.timestamp.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('mood/history.html', moods=moods, title='Your Mood History') 
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class MoodEntryForm(FlaskForm):
    mood_choices = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('energetic', 'Energetic'),
        ('calm', 'Calm'),
        ('anxious', 'Anxious'),
        ('angry', 'Angry'),
        ('romantic', 'Romantic'),
        ('focused', 'Focused'),
        ('relaxed', 'Relaxed'),
        ('melancholic', 'Melancholic')
    ]
    
    mood = SelectField('How are you feeling?', choices=mood_choices, validators=[DataRequired()])
    comment = TextAreaField('Any thoughts? (optional)', validators=[Length(max=500)])
    submit = SubmitField('Get Music Recommendations') 
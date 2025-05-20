from extensions import db
from datetime import datetime

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    playlist_id = db.Column(db.String(100), nullable=True)  # Spotify playlist ID if saved
    
    def __repr__(self):
        return f'<MoodEntry {self.mood} by User {self.user_id}>'
        
    @property
    def formatted_date(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M') 
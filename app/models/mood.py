from extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False, index=True)
    intensity = db.Column(db.Integer, nullable=True)  # Scale 1-10
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    playlist_id = db.Column(db.String(100), nullable=True)  # Spotify playlist ID if saved
    track_ids = db.Column(db.Text, nullable=True)  # Comma-separated Spotify track IDs
    metadata = db.Column(JSON, nullable=True)  # Additional data for analysis
    
    def __repr__(self):
        return f'<MoodEntry {self.mood} by User {self.user_id}>'
        
    @property
    def formatted_date(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M')
        
    @property
    def track_list(self):
        if self.track_ids:
            return self.track_ids.split(',')
        return []
        
    def to_dict(self):
        return {
            'id': self.id,
            'mood': self.mood,
            'intensity': self.intensity,
            'comment': self.comment,
            'timestamp': self.formatted_date,
            'playlist_id': self.playlist_id,
            'track_ids': self.track_list
        } 
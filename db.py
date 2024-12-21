from config import *
from datetime import datetime

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User model
    target_ip = db.Column(db.String(120), nullable=False)  # IP address searched
    scan_depth = db.Column(db.String(50), nullable=False)  # Depth of the scan
    result = db.Column(db.Text, nullable=False)  # Scan result
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Time of the search
    user = db.relationship('User', backref=db.backref('search_history', lazy=True))  # Relationship to User

    def __repr__(self):
        return f"<SearchHistory {self.target_ip} - {self.timestamp}>"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

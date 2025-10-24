from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Solution(db.Model):
    """Model for storing code solutions"""
    __tablename__ = 'solutions'
    
    id = db.Column(db.Integer, primary_key=True)
    problem_name = db.Column(db.String(200), nullable=False, index=True)
    language = db.Column(db.String(50), nullable=False, index=True)
    code = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    
    # NEW ENGAGEMENT FEATURES
    likes = db.Column(db.Integer, default=0)
    bookmarks = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.String(20), nullable=True)  # Easy, Medium, Hard
    time_complexity = db.Column(db.String(50), nullable=True)  # O(n), O(log n), etc.
    space_complexity = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
    execution_time_ms = db.Column(db.Float, nullable=True)  # Runtime in milliseconds
    is_featured = db.Column(db.Boolean, default=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='solution', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Solution {self.problem_name} - {self.language}>'
    
    def to_dict(self):
        """Convert solution to dictionary"""
        return {
            'id': self.id,
            'problem_name': self.problem_name,
            'language': self.language,
            'code': self.code,
            'author': self.author or 'Anonymous',
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'views': self.views,
            'likes': self.likes,
            'bookmarks': self.bookmarks,
            'difficulty': self.difficulty,
            'time_complexity': self.time_complexity,
            'space_complexity': self.space_complexity,
            'tags': self.tags.split(',') if self.tags else [],
            'execution_time_ms': self.execution_time_ms,
            'is_featured': self.is_featured,
            'comment_count': len(self.comments)
        }

class Problem(db.Model):
    """Model for tracking problems and their solution counts"""
    __tablename__ = 'problems'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True, index=True)
    solution_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Problem {self.name}>'


class Comment(db.Model):
    """Model for solution comments"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    solution_id = db.Column(db.Integer, db.ForeignKey('solutions.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment by {self.author}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'solution_id': self.solution_id,
            'author': self.author,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class UserActivity(db.Model):
    """Track user engagement for leaderboard"""
    __tablename__ = 'user_activity'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    solutions_submitted = db.Column(db.Integer, default=0)
    total_views = db.Column(db.Integer, default=0)
    total_likes = db.Column(db.Integer, default=0)
    comments_made = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    streak_days = db.Column(db.Integer, default=0)
    badges = db.Column(db.String(500), nullable=True)  # Comma-separated badges
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def total_score(self):
        """Calculate engagement score"""
        return (self.solutions_submitted * 10 + 
                self.total_likes * 5 + 
                self.total_views * 1 + 
                self.comments_made * 3)
    
    def to_dict(self):
        return {
            'username': self.username,
            'solutions_submitted': self.solutions_submitted,
            'total_views': self.total_views,
            'total_likes': self.total_likes,
            'comments_made': self.comments_made,
            'streak_days': self.streak_days,
            'badges': self.badges.split(',') if self.badges else [],
            'total_score': self.total_score
        }

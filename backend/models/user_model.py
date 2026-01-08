from datetime import datetime
from flask_login import UserMixin
from backend import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='patient') # 'patient' or 'doctor'
    
    # Relationship
    medical_history = db.relationship('MedicalHistory', backref='patient', uselist=False, lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(5))
    allergies = db.Column(db.Text)
    chronic_diseases = db.Column(db.Text)
    past_surgeries = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    family_history = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"MedicalHistory('User ID: {self.user_id}', '{self.updated_at}')"

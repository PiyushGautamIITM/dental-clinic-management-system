# app/models.py
from datetime import datetime
from . import db

class Clinic(db.Model):
    __tablename__ = "clinics"
    id = db.Column(db.Integer, primary_key=True)
    clinic_code = db.Column(db.String(32), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    incharge = db.Column(db.String(200))
    login_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patients = db.relationship("Patient", back_populates="clinic", cascade="all, delete-orphan")

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    patient_code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.id"), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    sex = db.Column(db.String(20))
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    treatment_type = db.Column(db.String(100), index=True)
    mobile_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    clinic = db.relationship("Clinic", back_populates="patients")

# app/clinics.py
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from .models import Clinic, Patient
from . import db
from datetime import datetime, date
from sqlalchemy import func

clinic_bp = Blueprint("clinic", __name__, template_folder="templates")

def calculate_age(dob):
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@clinic_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        login_id = request.form.get("login_id","").strip()
        password = request.form.get("password","").strip()
        clinic = Clinic.query.filter_by(login_id=login_id).first()
        if clinic and check_password_hash(clinic.password_hash, password):
            session['clinic_id'] = clinic.id
            session['clinic_code'] = clinic.clinic_code
            session['clinic_name'] = clinic.name
            return redirect(url_for("clinic.add_patient"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@clinic_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.register_clinic"))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("clinic_id"):
            return redirect(url_for("clinic.login"))
        return f(*args, **kwargs)
    return decorated

@clinic_bp.route("/add_patient", methods=["GET","POST"])
@login_required
def add_patient():
    if request.method == "POST":
        clinic_id = session['clinic_id']
        name = request.form.get("name","").strip()
        sex = request.form.get("sex","").strip()
        dob_str = request.form.get("dob","").strip()
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        treatment_type = request.form.get("treatment_type","").strip()
        mobile = request.form.get("mobile_number","").strip()
        count = Patient.query.filter_by(clinic_id=clinic_id).count() or 0
        clinic = Clinic.query.get(clinic_id)
        patient_code = f"{clinic.clinic_code}-P{count+1:04d}"
        age = calculate_age(dob)
        p = Patient(patient_code=patient_code, clinic_id=clinic_id, name=name, sex=sex, dob=dob, age=age, treatment_type=treatment_type, mobile_number=mobile)
        db.session.add(p)
        db.session.commit()
        flash(f"Patient {name} added ({patient_code})", "success")
        return redirect(url_for("clinic.patients"))
    return render_template("add_patient.html")

@clinic_bp.route("/patients")
@login_required
def patients():
    clinic_id = session['clinic_id']
    patients = Patient.query.filter_by(clinic_id=clinic_id).order_by(Patient.created_at.desc()).all()
    return render_template("patients.html", patients=patients)

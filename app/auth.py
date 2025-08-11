# app/auth.py
from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Clinic
import secrets
from sqlalchemy import func

auth_bp = Blueprint("auth", __name__)

def generate_clinic_code(n):
    return f"CLINIC{n:04d}"

def generate_login_id(name, n):
    prefix = ''.join([c for c in name.upper() if c.isalpha()])[:4] or "CL"
    return f"{prefix}{n:03d}"

@auth_bp.route("/register_clinic", methods=["GET","POST"])
def register_clinic():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        location = request.form.get("location","").strip()
        incharge = request.form.get("incharge","").strip()
        total = db.session.query(func.count(Clinic.id)).scalar() or 0
        next_num = total + 1
        clinic_code = generate_clinic_code(next_num)
        login_id = generate_login_id(name, next_num)
        password = secrets.token_urlsafe(6)
        pw_hash = generate_password_hash(password)
        clinic = Clinic(clinic_code=clinic_code, name=name, location=location, incharge=incharge, login_id=login_id, password_hash=pw_hash)
        db.session.add(clinic)
        db.session.commit()
        return render_template("register_clinic.html", clinic_code=clinic_code, login_id=login_id, password=password, name=name)
    return render_template("register_clinic.html")

# app/api.py
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from .models import Clinic, Patient
from . import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, date

api_bp = Blueprint("api", __name__)

@api_bp.route("/token", methods=["POST"])
def token():
    data = request.json or {}
    login_id = data.get("login_id")
    password = data.get("password")
    clinic = Clinic.query.filter_by(login_id=login_id).first()
    if not clinic or not check_password_hash(clinic.password_hash, password):
        return jsonify({"msg":"Bad credentials"}), 401
    access = create_access_token(identity=clinic.id)
    return jsonify({"access_token": access})

@api_bp.route("/patients", methods=["POST"])
@jwt_required()
def api_add_patient():
    clinic_id = get_jwt_identity()
    data = request.json or {}
    name = data.get("name")
    sex = data.get("sex")
    dob = data.get("dob")  # 'YYYY-MM-DD' optional
    treat = data.get("treatment_type")
    mobile = data.get("mobile_number")
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return jsonify({"msg":"Clinic not found"}), 404
    count = Patient.query.filter_by(clinic_id=clinic_id).count() or 0
    patient_code = f"{clinic.clinic_code}-P{count+1:04d}"
    dob_date = None
    if dob:
        dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    else:
        age = None
    p = Patient(patient_code=patient_code, clinic_id=clinic_id, name=name, sex=sex, dob=dob_date, age=age, treatment_type=treat, mobile_number=mobile)
    db.session.add(p)
    db.session.commit()
    return jsonify({"msg":"patient added", "patient_code": patient_code})

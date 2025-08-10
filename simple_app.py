# simple_app.py - Working version for ngrok
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, date
from sqlalchemy import func

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dental.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Models
class Clinic(db.Model):
    __tablename__ = "clinics"
    id = db.Column(db.Integer, primary_key=True)
    clinic_code = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    incharge = db.Column(db.String(200))
    login_id = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patients = db.relationship("Patient", back_populates="clinic", cascade="all, delete-orphan")

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    patient_code = db.Column(db.String(64), unique=True, nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    sex = db.Column(db.String(20))
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    treatment_type = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clinic = db.relationship("Clinic", back_populates="patients")

# Helper functions
def generate_clinic_code(n):
    return f"CLINIC{n:04d}"

def generate_login_id(name, n):
    prefix = ''.join([c for c in name.upper() if c.isalpha()])[:4] or "CL"
    return f"{prefix}{n:03d}"

def calculate_age(dob):
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# Routes
@app.route("/")
def index():
    return '''
    <h1>🦷 Dental Clinic Management System</h1>
    <p><a href="/register_clinic">Register New Clinic</a></p>
    <p><a href="/login">Clinic Login</a></p>
    <p><strong>Demo Login:</strong> Use any clinic with password: pass123</p>
    '''

@app.route("/register_clinic", methods=["GET","POST"])
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
        return f'''
        <h2>✅ Clinic Registered Successfully!</h2>
        <p><strong>Clinic Code:</strong> {clinic_code}</p>
        <p><strong>Login ID:</strong> {login_id}</p>
        <p><strong>Password:</strong> {password}</p>
        <p><a href="/login">Login Now</a></p>
        '''
    return '''
    <h2>Register New Clinic</h2>
    <form method="post">
        <p>Clinic Name: <input name="name" required></p>
        <p>Location: <input name="location"></p>
        <p>Incharge: <input name="incharge"></p>
        <p><button type="submit">Register</button></p>
    </form>
    <p><a href="/">← Back to Home</a></p>
    '''

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        login_id = request.form.get("login_id","").strip()
        password = request.form.get("password","").strip()
        clinic = Clinic.query.filter_by(login_id=login_id).first()
        if clinic and check_password_hash(clinic.password_hash, password):
            session['clinic_id'] = clinic.id
            session['clinic_code'] = clinic.clinic_code
            session['clinic_name'] = clinic.name
            return redirect("/dashboard")
        return f'<p>❌ Invalid credentials</p><p><a href="/login">Try Again</a></p>'
    return '''
    <h2>Clinic Login</h2>
    <form method="post">
        <p>Login ID: <input name="login_id" required></p>
        <p>Password: <input name="password" type="password" required></p>
        <p><button type="submit">Login</button></p>
    </form>
    <p><strong>Demo:</strong> Login ID like COMP001, Password: pass123</p>
    <p><a href="/">← Back to Home</a></p>
    '''

@app.route("/dashboard")
def dashboard():
    if not session.get("clinic_id"):
        return redirect("/login")
    
    clinic_name = session.get("clinic_name")
    clinic_id = session["clinic_id"]
    patient_count = Patient.query.filter_by(clinic_id=clinic_id).count()
    
    return f'''
    <h2>🏥 {clinic_name} Dashboard</h2>
    <p><strong>Total Patients:</strong> {patient_count}</p>
    <p><a href="/add_patient">➕ Add New Patient</a></p>
    <p><a href="/patients">👥 View All Patients</a></p>
    <p><a href="/logout">🚪 Logout</a></p>
    '''

@app.route("/add_patient", methods=["GET","POST"])
def add_patient():
    if not session.get("clinic_id"):
        return redirect("/login")
    
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
        return f'<h3>✅ Patient {name} added ({patient_code})</h3><p><a href="/dashboard">← Back to Dashboard</a></p>'
    
    return '''
    <h2>Add New Patient</h2>
    <form method="post">
        <p>Name: <input name="name" required></p>
        <p>Sex: <select name="sex"><option>Male</option><option>Female</option></select></p>
        <p>Date of Birth: <input name="dob" type="date"></p>
        <p>Treatment: <input name="treatment_type" placeholder="e.g., Cleaning, Filling"></p>
        <p>Mobile: <input name="mobile_number" placeholder="Phone number"></p>
        <p><button type="submit">Add Patient</button></p>
    </form>
    <p><a href="/dashboard">← Back to Dashboard</a></p>
    '''

@app.route("/patients")
def patients():
    if not session.get("clinic_id"):
        return redirect("/login")
    
    clinic_id = session['clinic_id']
    patients = Patient.query.filter_by(clinic_id=clinic_id).order_by(Patient.created_at.desc()).all()
    
    html = '<h2>👥 All Patients</h2><table border="1" style="border-collapse:collapse;"><tr><th>ID</th><th>Name</th><th>Age</th><th>Treatment</th><th>Mobile</th><th>Added</th></tr>'
    for p in patients:
        html += f'<tr><td>{p.patient_code}</td><td>{p.name}</td><td>{p.age or "-"}</td><td>{p.treatment_type or "-"}</td><td>{p.mobile_number or "-"}</td><td>{p.created_at.strftime("%Y-%m-%d")}</td></tr>'
    html += '</table><p><a href="/dashboard">← Back to Dashboard</a></p>'
    return html

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
    app.run(host="127.0.0.1", port=5000, debug=True)

# Also create tables when imported (for ngrok usage)
with app.app_context():
    try:
        db.create_all()
        print("✅ Database initialized!")
    except Exception as e:
        print(f"⚠️ Database initialization: {e}")

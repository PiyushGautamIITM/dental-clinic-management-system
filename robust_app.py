# robust_app.py - Error-free version with better database handling
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, date
from sqlalchemy import func
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev_secret_key_2024"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dental_clinic.db"
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

def init_database():
    """Initialize database with tables and demo data"""
    try:
        with app.app_context():
            db.create_all()
            
            # Check if demo data exists
            if Clinic.query.count() == 0:
                # Add demo clinics
                demo_clinics = [
                    ("CLINIC0001", "City Dental Care", "New York, USA", "Dr. Smith", "CITY001", "pass123"),
                    ("CLINIC0002", "Smile Center", "Los Angeles, USA", "Dr. Johnson", "SMIL001", "pass123"),
                    ("CLINIC0003", "Dental Plus", "Chicago, USA", "Dr. Brown", "DENT001", "pass123"),
                ]
                
                for clinic_code, name, location, incharge, login_id, password in demo_clinics:
                    pw_hash = generate_password_hash(password)
                    clinic = Clinic(clinic_code=clinic_code, name=name, location=location, 
                                  incharge=incharge, login_id=login_id, password_hash=pw_hash)
                    db.session.add(clinic)
                
                db.session.commit()
                
                # Add demo patients
                demo_patients = [
                    ("CLINIC0001-P0001", 1, "John Doe", "Male", "1985-05-15", 39, "Cleaning", "555-0101"),
                    ("CLINIC0001-P0002", 1, "Jane Smith", "Female", "1990-08-20", 34, "Filling", "555-0102"),
                    ("CLINIC0001-P0003", 1, "Bob Wilson", "Male", "1975-12-10", 49, "Root Canal", "555-0103"),
                    ("CLINIC0002-P0001", 2, "Alice Brown", "Female", "1988-03-25", 36, "Orthodontics", "555-0201"),
                    ("CLINIC0002-P0002", 2, "Charlie Davis", "Male", "1992-07-14", 32, "Extraction", "555-0202"),
                    ("CLINIC0003-P0001", 3, "Diana Miller", "Female", "1987-11-30", 37, "Checkup", "555-0301"),
                ]
                
                for patient_code, clinic_id, name, sex, dob_str, age, treatment, mobile in demo_patients:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                    patient = Patient(patient_code=patient_code, clinic_id=clinic_id, name=name, 
                                    sex=sex, dob=dob, age=age, treatment_type=treatment, mobile_number=mobile)
                    db.session.add(patient)
                
                db.session.commit()
                print("✅ Demo data added successfully!")
                
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

# Routes with error handling
@app.route("/")
def index():
    return '''
    <html>
    <head><title>Dental Clinic Management</title></head>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h1 style="color: #2c5aa0;">🦷 Dental Clinic Management System</h1>
            <p style="font-size: 18px; color: #666;">Welcome to your professional dental clinic management platform!</p>
            
            <div style="margin: 30px 0;">
                <a href="/register_clinic" style="background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin-right: 10px;">➕ Register New Clinic</a>
                <a href="/login" style="background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">🔑 Clinic Login</a>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; margin-top: 30px;">
                <h3 style="color: #2c5aa0;">🚀 Demo Accounts Ready to Use:</h3>
                <p><strong>🏥 City Dental Care:</strong> Login: <code>CITY001</code>, Password: <code>pass123</code></p>
                <p><strong>😊 Smile Center:</strong> Login: <code>SMIL001</code>, Password: <code>pass123</code></p>
                <p><strong>🦷 Dental Plus:</strong> Login: <code>DENT001</code>, Password: <code>pass123</code></p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/register_clinic", methods=["GET","POST"])
def register_clinic():
    if request.method == "POST":
        try:
            name = request.form.get("name","").strip()
            location = request.form.get("location","").strip()
            incharge = request.form.get("incharge","").strip()
            
            if not name:
                return '<p style="color: red;">❌ Clinic name is required!</p><p><a href="/register_clinic">← Try Again</a></p>'
            
            total = Clinic.query.count() or 0
            next_num = total + 1
            clinic_code = generate_clinic_code(next_num)
            login_id = generate_login_id(name, next_num)
            password = secrets.token_urlsafe(6)
            pw_hash = generate_password_hash(password)
            
            clinic = Clinic(clinic_code=clinic_code, name=name, location=location, 
                          incharge=incharge, login_id=login_id, password_hash=pw_hash)
            db.session.add(clinic)
            db.session.commit()
            
            return f'''
            <html>
            <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
                <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #28a745;">✅ Clinic Registered Successfully!</h2>
                    <div style="background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p><strong>🏥 Clinic Code:</strong> <code style="background: #fff; padding: 4px 8px; border-radius: 4px;">{clinic_code}</code></p>
                        <p><strong>🔑 Login ID:</strong> <code style="background: #fff; padding: 4px 8px; border-radius: 4px;">{login_id}</code></p>
                        <p><strong>🔒 Password:</strong> <code style="background: #fff; padding: 4px 8px; border-radius: 4px;">{password}</code></p>
                    </div>
                    <p style="color: #dc3545;"><strong>⚠️ Important:</strong> Save these credentials - you'll need them to login!</p>
                    <p>
                        <a href="/login" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Login Now →</a>
                        <a href="/" style="background: #6c757d; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-left: 10px;">← Home</a>
                    </p>
                </div>
            </body>
            </html>
            '''
        except Exception as e:
            return f'<p style="color: red;">❌ Registration failed: {str(e)}</p><p><a href="/register_clinic">← Try Again</a></p>'
    
    return '''
    <html>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #2c5aa0;">🏥 Register New Clinic</h2>
            <form method="post" style="margin-top: 20px;">
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Clinic Name *</label>
                    <input name="name" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Location</label>
                    <input name="location" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Doctor In-charge</label>
                    <input name="incharge" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <button type="submit" style="background: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer;">Register Clinic</button>
                    <a href="/" style="background: #6c757d; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin-left: 10px;">← Back to Home</a>
                </p>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        try:
            login_id = request.form.get("login_id","").strip()
            password = request.form.get("password","").strip()
            
            if not login_id or not password:
                return '<p style="color: red;">❌ Please enter both login ID and password!</p><p><a href="/login">← Try Again</a></p>'
            
            clinic = Clinic.query.filter_by(login_id=login_id).first()
            if clinic and check_password_hash(clinic.password_hash, password):
                session['clinic_id'] = clinic.id
                session['clinic_code'] = clinic.clinic_code
                session['clinic_name'] = clinic.name
                return redirect("/dashboard")
            else:
                return '<p style="color: red;">❌ Invalid login credentials!</p><p><a href="/login">← Try Again</a></p>'
        except Exception as e:
            return f'<p style="color: red;">❌ Login error: {str(e)}</p><p><a href="/login">← Try Again</a></p>'
    
    return '''
    <html>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #2c5aa0;">🔑 Clinic Login</h2>
            <form method="post" style="margin-top: 20px;">
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Login ID</label>
                    <input name="login_id" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Password</label>
                    <input name="password" type="password" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <button type="submit" style="background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer;">Login</button>
                    <a href="/" style="background: #6c757d; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin-left: 10px;">← Back to Home</a>
                </p>
            </form>
            <div style="background: #e8f4fd; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h4 style="margin-top: 0;">🚀 Demo Accounts:</h4>
                <p><strong>Login:</strong> CITY001, SMIL001, or DENT001</p>
                <p><strong>Password:</strong> pass123</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/dashboard")
def dashboard():
    if not session.get("clinic_id"):
        return redirect("/login")
    
    try:
        clinic_name = session.get("clinic_name")
        clinic_id = session["clinic_id"]
        patient_count = Patient.query.filter_by(clinic_id=clinic_id).count()
        recent_patients = Patient.query.filter_by(clinic_id=clinic_id).order_by(Patient.created_at.desc()).limit(5).all()
        
        recent_html = ""
        for p in recent_patients:
            recent_html += f'<tr><td>{p.patient_code}</td><td>{p.name}</td><td>{p.treatment_type or "-"}</td></tr>'
        
        return f'''
        <html>
        <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
            <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #2c5aa0;">🏥 {clinic_name} - Dashboard</h2>
                
                <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">📊 Quick Stats</h3>
                    <p style="font-size: 18px;"><strong>Total Patients:</strong> {patient_count}</p>
                </div>
                
                <div style="margin: 20px 0;">
                    <a href="/add_patient" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-right: 10px;">➕ Add New Patient</a>
                    <a href="/patients" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-right: 10px;">👥 View All Patients</a>
                    <a href="/logout" style="background: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🚪 Logout</a>
                </div>
                
                <h3>🕒 Recent Patients</h3>
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <tr style="background: #f8f9fa;">
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Patient ID</th>
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Name</th>
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Treatment</th>
                    </tr>
                    {recent_html}
                </table>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'<p style="color: red;">❌ Dashboard error: {str(e)}</p><p><a href="/login">← Login Again</a></p>'

@app.route("/add_patient", methods=["GET","POST"])
def add_patient():
    if not session.get("clinic_id"):
        return redirect("/login")
    
    if request.method == "POST":
        try:
            clinic_id = session['clinic_id']
            name = request.form.get("name","").strip()
            sex = request.form.get("sex","").strip()
            dob_str = request.form.get("dob","").strip()
            treatment_type = request.form.get("treatment_type","").strip()
            mobile = request.form.get("mobile_number","").strip()
            
            if not name:
                return '<p style="color: red;">❌ Patient name is required!</p><p><a href="/add_patient">← Try Again</a></p>'
            
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
            count = Patient.query.filter_by(clinic_id=clinic_id).count() or 0
            clinic = Clinic.query.get(clinic_id)
            patient_code = f"{clinic.clinic_code}-P{count+1:04d}"
            age = calculate_age(dob)
            
            patient = Patient(patient_code=patient_code, clinic_id=clinic_id, name=name, 
                            sex=sex, dob=dob, age=age, treatment_type=treatment_type, mobile_number=mobile)
            db.session.add(patient)
            db.session.commit()
            
            return f'''
            <html>
            <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
                <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #28a745;">✅ Patient Added Successfully!</h3>
                    <p><strong>Patient:</strong> {name}</p>
                    <p><strong>Patient ID:</strong> {patient_code}</p>
                    <p><a href="/dashboard" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">← Back to Dashboard</a></p>
                </div>
            </body>
            </html>
            '''
        except Exception as e:
            return f'<p style="color: red;">❌ Error adding patient: {str(e)}</p><p><a href="/add_patient">← Try Again</a></p>'
    
    return '''
    <html>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #2c5aa0;">➕ Add New Patient</h2>
            <form method="post" style="margin-top: 20px;">
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Patient Name *</label>
                    <input name="name" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Sex</label>
                    <select name="sex" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                        <option value="">Select...</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                </p>
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Date of Birth</label>
                    <input name="dob" type="date" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Treatment Type</label>
                    <input name="treatment_type" placeholder="e.g., Cleaning, Filling, Root Canal" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Mobile Number</label>
                    <input name="mobile_number" placeholder="Phone number" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                </p>
                <p>
                    <button type="submit" style="background: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer;">Add Patient</button>
                    <a href="/dashboard" style="background: #6c757d; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin-left: 10px;">← Back to Dashboard</a>
                </p>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route("/patients")
def patients():
    if not session.get("clinic_id"):
        return redirect("/login")
    
    try:
        clinic_id = session['clinic_id']
        patients_list = Patient.query.filter_by(clinic_id=clinic_id).order_by(Patient.created_at.desc()).all()
        
        patients_html = ""
        for p in patients_list:
            patients_html += f'''
            <tr>
                <td style="border: 1px solid #ddd; padding: 10px;">{p.patient_code}</td>
                <td style="border: 1px solid #ddd; padding: 10px;">{p.name}</td>
                <td style="border: 1px solid #ddd; padding: 10px;">{p.sex or "-"}</td>
                <td style="border: 1px solid #ddd; padding: 10px;">{p.age or "-"}</td>
                <td style="border: 1px solid #ddd; padding: 10px;">{p.treatment_type or "-"}</td>
                <td style="border: 1px solid #ddd; padding: 10px;">{p.mobile_number or "-"}</td>
                <td style="border: 1px solid #ddd; padding: 10px;">{p.created_at.strftime("%Y-%m-%d")}</td>
            </tr>
            '''
        
        return f'''
        <html>
        <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
            <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #2c5aa0;">👥 All Patients ({len(patients_list)} total)</h2>
                
                <p>
                    <a href="/add_patient" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-right: 10px;">➕ Add New Patient</a>
                    <a href="/dashboard" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">← Back to Dashboard</a>
                </p>
                
                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <tr style="background: #f8f9fa;">
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Patient ID</th>
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Name</th>
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Sex</th>
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Age</th>
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Treatment</th>
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Mobile</th>
                        <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Added</th>
                    </tr>
                    {patients_html}
                </table>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'<p style="color: red;">❌ Error loading patients: {str(e)}</p><p><a href="/dashboard">← Back to Dashboard</a></p>'

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Initialize database on startup
init_database()

if __name__ == "__main__":
    print("🦷 Starting Dental Clinic Management System...")
    app.run(host="127.0.0.1", port=5000, debug=True)

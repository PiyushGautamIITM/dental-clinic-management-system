from flask import Flask, request, redirect, url_for, session, render_template_string
import sqlite3
import os
from datetime import datetime, timedelta
import secrets
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database configuration
DATABASE = "dental_clinic.db"

def init_database():
    """Initialize the database with all necessary tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create clinics table
    cursor.execute('''CREATE TABLE IF NOT EXISTS clinics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Enhanced patients table with all new fields
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER NOT NULL,
        patient_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        sex TEXT,
        phone TEXT,
        treatment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        dob DATE,
        email TEXT,
        address TEXT,
        emergency_contact_name TEXT,
        emergency_contact_phone TEXT,
        medical_history TEXT,
        current_medications TEXT,
        allergies TEXT,
        insurance_provider TEXT,
        insurance_number TEXT,
        previous_dental_work TEXT,
        chief_complaint TEXT,
        pain_level INTEGER,
        last_cleaning_date DATE,
        preferred_appointment_time TEXT,
        FOREIGN KEY (clinic_id) REFERENCES clinics (id)
    )''')
    
    # Patient analytics table
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient_analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        visit_date DATE,
        diagnosis TEXT,
        treatment_cost REAL,
        satisfaction_rating INTEGER,
        doctor_assigned TEXT,
        treatment_duration INTEGER,
        FOREIGN KEY (clinic_id) REFERENCES clinics (id),
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    )''')
    
    # Revenue analytics table
    cursor.execute('''CREATE TABLE IF NOT EXISTS revenue_analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER NOT NULL,
        transaction_date DATE,
        service_type TEXT,
        base_amount REAL,
        tax_amount REAL,
        discount_amount REAL,
        final_amount REAL,
        payment_method TEXT,
        payment_status TEXT,
        FOREIGN KEY (clinic_id) REFERENCES clinics (id)
    )''')
    
    # Doctor performance table
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctor_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER NOT NULL,
        doctor_name TEXT,
        specialization TEXT,
        patients_treated INTEGER,
        success_rate REAL,
        average_rating REAL,
        revenue_generated REAL,
        FOREIGN KEY (clinic_id) REFERENCES clinics (id)
    )''')
    
    # Patient feedback table
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        feedback_text TEXT,
        rating INTEGER,
        sentiment_score REAL,
        feedback_date DATE,
        FOREIGN KEY (clinic_id) REFERENCES clinics (id),
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    )''')
    
    # Smart alerts table
    cursor.execute('''CREATE TABLE IF NOT EXISTS smart_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER NOT NULL,
        alert_type TEXT,
        alert_message TEXT,
        severity_level TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_resolved BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (clinic_id) REFERENCES clinics (id)
    )''')
    
    # Custom reports table
    cursor.execute('''CREATE TABLE IF NOT EXISTS custom_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER NOT NULL,
        report_name TEXT,
        report_type TEXT,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        report_data TEXT,
        FOREIGN KEY (clinic_id) REFERENCES clinics (id)
    )''')
    
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return '''
    <html>
    <head>
        <title>🦷 Dental Clinic Management System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { max-width: 400px; margin: 50px auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { color: #333; margin-bottom: 10px; }
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 5px; color: #555; font-weight: bold; }
            .form-group input { width: 100%; padding: 12px; border: 2px solid #e1e5e9; border-radius: 8px; font-size: 14px; }
            .form-group input:focus { border-color: #007bff; outline: none; }
            .btn { display: block; width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin-bottom: 10px; }
            .btn:hover { background: #0056b3; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #545b62; }
            .divider { text-align: center; margin: 20px 0; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🦷 Dental Clinic Portal</h1>
                <p style="color: #666;">Manage your clinic efficiently</p>
            </div>
            
            <form method="POST" action="/login">
                <div class="form-group">
                    <label for="email">📧 Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">🔒 Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn">🔑 Login</button>
            </form>
            
            <div class="divider">── OR ──</div>
            
            <a href="/register" class="btn btn-secondary">📝 Register New Clinic</a>
        </div>
    </body>
    </html>
    '''

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clinics (name, email, password, phone, address) VALUES (?, ?, ?, ?, ?)",
                         (name, email, password, phone, address))
            conn.commit()
            conn.close()
            return redirect("/")
        except sqlite3.IntegrityError:
            return "<h3>❌ Error: Email already exists!</h3><a href='/register'>← Try Again</a>"
        except Exception as e:
            return f"<h3>❌ Error: {str(e)}</h3><a href='/register'>← Try Again</a>"
    
    return '''
    <html>
    <head>
        <title>Register Clinic</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { max-width: 500px; margin: 30px auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 5px; color: #555; font-weight: bold; }
            .form-group input, .form-group textarea { width: 100%; padding: 12px; border: 2px solid #e1e5e9; border-radius: 8px; font-size: 14px; }
            .btn { padding: 12px 30px; background: #28a745; color: white; border: none; border-radius: 8px; cursor: pointer; margin-right: 10px; }
            .btn:hover { background: #218838; }
            .btn-back { background: #6c757d; }
            .btn-back:hover { background: #545b62; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📝 Register New Clinic</h2>
            <form method="POST">
                <div class="form-group">
                    <label for="name">🏥 Clinic Name:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">📧 Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">🔒 Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-group">
                    <label for="phone">📞 Phone:</label>
                    <input type="text" id="phone" name="phone">
                </div>
                <div class="form-group">
                    <label for="address">🏠 Address:</label>
                    <textarea id="address" name="address" rows="3"></textarea>
                </div>
                <button type="submit" class="btn">✅ Register</button>
                <a href="/" class="btn btn-back">← Back</a>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM clinics WHERE email = ? AND password = ?", (email, password))
        clinic = cursor.fetchone()
        conn.close()
        
        if clinic:
            session["clinic_id"] = clinic[0]
            session["clinic_name"] = clinic[1]
            return redirect(f"/dashboard?clinic_id={clinic[0]}")
        else:
            return "<h3>❌ Invalid credentials!</h3><a href='/'>← Try Again</a>"
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3><a href='/'>← Try Again</a>"

@app.route("/dashboard")
def dashboard():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return redirect("/")
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get clinic info
        cursor.execute("SELECT name FROM clinics WHERE id = ?", (clinic_id,))
        clinic_info = cursor.fetchone()
        if not clinic_info:
            return "<h3>❌ Error: Clinic not found!</h3><a href='/'>← Back to Home</a>"
        
        clinic_name = clinic_info[0]
        
        # Get patient count
        cursor.execute("SELECT COUNT(*) FROM patients WHERE clinic_id = ?", (clinic_id,))
        patient_count = cursor.fetchone()[0]
        
        # Get recent patients
        cursor.execute("SELECT name, treatment, created_at FROM patients WHERE clinic_id = ? ORDER BY created_at DESC LIMIT 5", (clinic_id,))
        recent_patients = cursor.fetchall()
        
        conn.close()
        
        recent_patients_html = ""
        for patient in recent_patients:
            recent_patients_html += f"<li>👤 {patient[0]} - {patient[1]} <span style='color: #666; font-size: 12px;'>({patient[2][:10]})</span></li>"
        
        return f'''
        <html>
        <head>
            <title>Dashboard - {clinic_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .stat-card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; }}
                .stat-number {{ font-size: 2.5em; font-weight: bold; color: #007bff; margin-bottom: 10px; }}
                .buttons {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }}
                .btn {{ display: block; padding: 15px 25px; text-decoration: none; border-radius: 10px; text-align: center; font-weight: bold; transition: transform 0.2s; }}
                .btn:hover {{ transform: translateY(-2px); }}
                .btn-primary {{ background: #007bff; color: white; }}
                .btn-success {{ background: #28a745; color: white; }}
                .btn-info {{ background: #17a2b8; color: white; }}
                .btn-warning {{ background: #ffc107; color: #212529; }}
                .recent-list {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                .recent-list ul {{ list-style: none; padding: 0; }}
                .recent-list li {{ padding: 10px; border-bottom: 1px solid #eee; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🦷 {clinic_name}</h1>
                <p>Welcome to your dental clinic dashboard</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{patient_count}</div>
                    <div>Total Patients</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">✨</div>
                    <div>Advanced Analytics</div>
                </div>
            </div>
            
                <div class="buttons">
                <a href="/add_patient?clinic_id={clinic_id}" class="btn btn-success">👥 Add New Patient</a>
                <a href="/view_patients?clinic_id={clinic_id}" class="btn btn-primary">📋 View All Patients</a>
                <a href="/search_patients?clinic_id={clinic_id}" class="btn btn-info">🔍 Search Patients</a>
                <a href="/advanced_analytics?clinic_id={clinic_id}" class="btn btn-info">📊 Advanced Analytics</a>
                <a href="/generate_report?clinic_id={clinic_id}" class="btn btn-warning">📄 Generate Reports</a>
            </div>            <div class="recent-list">
                <h3>📅 Recent Patients</h3>
                <ul>
                    {recent_patients_html if recent_patients_html else "<li>No patients yet. <a href='/add_patient?clinic_id=" + clinic_id + "'>Add your first patient!</a></li>"}
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="color: #666; text-decoration: none;">🔒 Logout</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3><a href='/'>← Back to Home</a>"

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return redirect("/")
    
    if request.method == "POST":
        try:
            # Generate patient code
            patient_code = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Get form data
            name = request.form["name"]
            age = request.form.get("age", "")
            sex = request.form.get("sex", "")
            phone = request.form.get("phone", "")
            treatment = request.form.get("treatment", "")
            dob = request.form.get("dob", "")
            email = request.form.get("email", "")
            address = request.form.get("address", "")
            emergency_contact_name = request.form.get("emergency_contact_name", "")
            emergency_contact_phone = request.form.get("emergency_contact_phone", "")
            medical_history = request.form.get("medical_history", "")
            current_medications = request.form.get("current_medications", "")
            allergies = request.form.get("allergies", "")
            insurance_provider = request.form.get("insurance_provider", "")
            insurance_number = request.form.get("insurance_number", "")
            previous_dental_work = request.form.get("previous_dental_work", "")
            chief_complaint = request.form.get("chief_complaint", "")
            pain_level = request.form.get("pain_level", "")
            last_cleaning_date = request.form.get("last_cleaning_date", "")
            preferred_appointment_time = request.form.get("preferred_appointment_time", "")
            
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO patients (
                clinic_id, patient_code, name, age, sex, phone, treatment,
                dob, email, address, emergency_contact_name, emergency_contact_phone,
                medical_history, current_medications, allergies, insurance_provider,
                insurance_number, previous_dental_work, chief_complaint, pain_level,
                last_cleaning_date, preferred_appointment_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                         (clinic_id, patient_code, name, age, sex, phone, treatment,
                          dob, email, address, emergency_contact_name, emergency_contact_phone,
                          medical_history, current_medications, allergies, insurance_provider,
                          insurance_number, previous_dental_work, chief_complaint, pain_level,
                          last_cleaning_date, preferred_appointment_time))
            
            patient_id = cursor.lastrowid
            
            # Add analytics entry if treatment cost provided
            treatment_cost = request.form.get("treatment_cost", "")
            if treatment_cost:
                cursor.execute("""INSERT INTO patient_analytics (
                    clinic_id, patient_id, visit_date, diagnosis, treatment_cost,
                    satisfaction_rating, doctor_assigned
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                             (clinic_id, patient_id, datetime.now().strftime('%Y-%m-%d'),
                              treatment, float(treatment_cost), 5, "Dr. Smith"))
            
            conn.commit()
            conn.close()
            
            return redirect(f"/view_patients?clinic_id={clinic_id}")
        except Exception as e:
            return f"<h3>❌ Error: {str(e)}</h3><a href='/add_patient?clinic_id={clinic_id}'>← Try Again</a>"
    
    return f'''
    <html>
    <head>
        <title>Add New Patient</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
            .form-section {{ margin-bottom: 30px; padding: 20px; border: 2px solid #e9ecef; border-radius: 10px; }}
            .form-section h3 {{ color: #495057; margin-top: 0; }}
            .form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; }}
            .form-group {{ margin-bottom: 15px; }}
            .form-group label {{ display: block; margin-bottom: 5px; color: #495057; font-weight: bold; }}
            .form-group input, .form-group select, .form-group textarea {{ width: 100%; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px; font-size: 14px; }}
            .form-group input:focus, .form-group select:focus, .form-group textarea:focus {{ border-color: #007bff; outline: none; }}
            .btn {{ padding: 12px 25px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin-right: 10px; text-decoration: none; display: inline-block; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-primary:hover {{ background: #0056b3; }}
            .btn-secondary {{ background: #6c757d; color: white; }}
            .btn-secondary:hover {{ background: #545b62; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>👥 Add New Patient</h2>
            <form method="POST">
                <div class="form-section">
                    <h3>📋 Basic Information</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="name">👤 Full Name:</label>
                            <input type="text" id="name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="age">🎂 Age:</label>
                            <input type="number" id="age" name="age" min="1" max="120">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="sex">👫 Gender:</label>
                            <select id="sex" name="sex">
                                <option value="">Select Gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="dob">📅 Date of Birth:</label>
                            <input type="date" id="dob" name="dob">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="phone">📞 Phone:</label>
                            <input type="tel" id="phone" name="phone">
                        </div>
                        <div class="form-group">
                            <label for="email">📧 Email:</label>
                            <input type="email" id="email" name="email">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="address">🏠 Address:</label>
                        <textarea id="address" name="address" rows="2"></textarea>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🚨 Emergency Contact</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="emergency_contact_name">👤 Emergency Contact Name:</label>
                            <input type="text" id="emergency_contact_name" name="emergency_contact_name">
                        </div>
                        <div class="form-group">
                            <label for="emergency_contact_phone">📞 Emergency Contact Phone:</label>
                            <input type="tel" id="emergency_contact_phone" name="emergency_contact_phone">
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🏥 Medical Information</h3>
                    <div class="form-group">
                        <label for="medical_history">📋 Medical History:</label>
                        <textarea id="medical_history" name="medical_history" rows="3" placeholder="Previous medical conditions, surgeries, etc."></textarea>
                    </div>
                    <div class="form-group">
                        <label for="current_medications">💊 Current Medications:</label>
                        <textarea id="current_medications" name="current_medications" rows="2" placeholder="List current medications and dosages"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="allergies">⚠️ Allergies:</label>
                        <textarea id="allergies" name="allergies" rows="2" placeholder="Food, drug, or environmental allergies"></textarea>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🏥 Insurance Information</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="insurance_provider">🏢 Insurance Provider:</label>
                            <input type="text" id="insurance_provider" name="insurance_provider" placeholder="e.g., Blue Cross, Aetna, etc.">
                        </div>
                        <div class="form-group">
                            <label for="insurance_number">🆔 Insurance Number:</label>
                            <input type="text" id="insurance_number" name="insurance_number">
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🦷 Dental Information</h3>
                    <div class="form-group">
                        <label for="chief_complaint">🔍 Chief Complaint:</label>
                        <textarea id="chief_complaint" name="chief_complaint" rows="2" placeholder="Main reason for today's visit"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="previous_dental_work">🛠️ Previous Dental Work:</label>
                        <textarea id="previous_dental_work" name="previous_dental_work" rows="2" placeholder="Fillings, crowns, braces, etc."></textarea>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="pain_level">😣 Pain Level (1-10):</label>
                            <select id="pain_level" name="pain_level">
                                <option value="">Select Pain Level</option>
                                <option value="1">1 - Minimal</option>
                                <option value="2">2 - Mild</option>
                                <option value="3">3 - Mild</option>
                                <option value="4">4 - Moderate</option>
                                <option value="5">5 - Moderate</option>
                                <option value="6">6 - Moderate-Severe</option>
                                <option value="7">7 - Severe</option>
                                <option value="8">8 - Severe</option>
                                <option value="9">9 - Very Severe</option>
                                <option value="10">10 - Extreme</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="last_cleaning_date">🧹 Last Cleaning Date:</label>
                            <input type="date" id="last_cleaning_date" name="last_cleaning_date">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="preferred_appointment_time">⏰ Preferred Appointment Time:</label>
                        <select id="preferred_appointment_time" name="preferred_appointment_time">
                            <option value="">Select Preference</option>
                            <option value="Morning">Morning</option>
                            <option value="Afternoon">Afternoon</option>
                            <option value="Evening">Evening</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>💰 Treatment & Analytics</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="treatment">🦷 Treatment Plan:</label>
                            <input type="text" id="treatment" name="treatment" placeholder="e.g., Cleaning, Filling, Root Canal">
                        </div>
                        <div class="form-group">
                            <label for="treatment_cost">💵 Treatment Cost (₹):</label>
                            <input type="number" id="treatment_cost" name="treatment_cost" step="0.01" placeholder="0.00">
                        </div>
                    </div>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <button type="submit" class="btn btn-primary">✅ Add Patient</button>
                    <a href="/dashboard?clinic_id={clinic_id}" class="btn btn-secondary">← Back to Dashboard</a>
                </div>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route("/view_patients")
def view_patients():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return redirect("/")
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT patient_code, name, age, sex, phone, treatment, created_at FROM patients WHERE clinic_id = ? ORDER BY created_at DESC", (clinic_id,))
        patients = cursor.fetchall()
        conn.close()
        
        patients_html = ""
        for patient in patients:
            patients_html += f'''
            <tr>
                <td>{patient[0]}</td>
                <td>{patient[1]}</td>
                <td>{patient[2] or 'N/A'}</td>
                <td>{patient[3] or 'N/A'}</td>
                <td>{patient[4] or 'N/A'}</td>
                <td>{patient[5] or 'N/A'}</td>
                <td>{patient[6][:10]}</td>
                <td>
                    <a href="/edit_patient?clinic_id={clinic_id}&patient_code={patient[0]}" class="btn-edit">✏️ Edit</a>
                    <a href="/view_patient_detail?clinic_id={clinic_id}&patient_code={patient[0]}" class="btn-view">👁️ View</a>
                </td>
            </tr>
            '''
        
        return f'''
        <html>
        <head>
            <title>All Patients</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }}
                .container {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .table th, .table td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
                .table th {{ background: #007bff; color: white; }}
                .table tr:nth-child(even) {{ background: #f8f9fa; }}
                .btn {{ padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; }}
                .btn:hover {{ background: #0056b3; }}
                .btn-edit {{ padding: 5px 10px; background: #28a745; color: white; text-decoration: none; border-radius: 3px; margin: 2px; display: inline-block; font-size: 12px; }}
                .btn-edit:hover {{ background: #218838; }}
                .btn-view {{ padding: 5px 10px; background: #17a2b8; color: white; text-decoration: none; border-radius: 3px; margin: 2px; display: inline-block; font-size: 12px; }}
                .btn-view:hover {{ background: #138496; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>👥 All Patients</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Patient Code</th>
                            <th>Name</th>
                            <th>Age</th>
                            <th>Gender</th>
                            <th>Phone</th>
                            <th>Treatment</th>
                            <th>Added Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {patients_html if patients_html else "<tr><td colspan='8' style='text-align: center; color: #666;'>No patients found. <a href='/add_patient?clinic_id=" + clinic_id + "'>Add your first patient!</a></td></tr>"}
                    </tbody>
                </table>
                <div style="text-align: center; margin-top: 20px;">
                    <a href="/add_patient?clinic_id={clinic_id}" class="btn">➕ Add New Patient</a>
                    <a href="/dashboard?clinic_id={clinic_id}" class="btn">🏠 Back to Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3><a href='/dashboard?clinic_id={clinic_id}'>← Back to Dashboard</a>"

@app.route("/search_patients", methods=["GET", "POST"])
def search_patients():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return redirect("/")
    
    search_results = ""
    search_query = ""
    results_section = ""
    
    if request.method == "POST":
        search_query = request.form.get("search_query", "")
        search_type = request.form.get("search_type", "name")
        
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            
            if search_type == "name":
                cursor.execute("SELECT patient_code, name, age, sex, phone, treatment, created_at FROM patients WHERE clinic_id = ? AND name LIKE ? ORDER BY created_at DESC", 
                             (clinic_id, f"%{search_query}%"))
            elif search_type == "phone":
                cursor.execute("SELECT patient_code, name, age, sex, phone, treatment, created_at FROM patients WHERE clinic_id = ? AND phone LIKE ? ORDER BY created_at DESC", 
                             (clinic_id, f"%{search_query}%"))
            elif search_type == "patient_code":
                cursor.execute("SELECT patient_code, name, age, sex, phone, treatment, created_at FROM patients WHERE clinic_id = ? AND patient_code LIKE ? ORDER BY created_at DESC", 
                             (clinic_id, f"%{search_query}%"))
            elif search_type == "treatment":
                cursor.execute("SELECT patient_code, name, age, sex, phone, treatment, created_at FROM patients WHERE clinic_id = ? AND treatment LIKE ? ORDER BY created_at DESC", 
                             (clinic_id, f"%{search_query}%"))
            
            patients = cursor.fetchall()
            conn.close()
            
            if patients:
                for patient in patients:
                    search_results += f'''
                    <tr>
                        <td>{patient[0]}</td>
                        <td>{patient[1]}</td>
                        <td>{patient[2] or 'N/A'}</td>
                        <td>{patient[3] or 'N/A'}</td>
                        <td>{patient[4] or 'N/A'}</td>
                        <td>{patient[5] or 'N/A'}</td>
                        <td>{patient[6][:10]}</td>
                        <td>
                            <a href="/edit_patient?clinic_id={clinic_id}&patient_code={patient[0]}" class="btn-edit">✏️ Edit</a>
                            <a href="/view_patient_detail?clinic_id={clinic_id}&patient_code={patient[0]}" class="btn-view">👁️ View</a>
                        </td>
                    </tr>
                    '''
                
                results_section = f'''
                <h3>Search Results for "{search_query}":</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Patient Code</th>
                            <th>Name</th>
                            <th>Age</th>
                            <th>Gender</th>
                            <th>Phone</th>
                            <th>Treatment</th>
                            <th>Added Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {search_results}
                    </tbody>
                </table>
                '''
            else:
                results_section = f'<div style="text-align: center; color: #666; padding: 20px;">No patients found matching "{search_query}"</div>'
        
        except Exception as e:
            results_section = f'<div style="text-align: center; color: red; padding: 20px;">Error: {str(e)}</div>'
    
    return f'''
    <html>
    <head>
        <title>Search Patients</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }}
            .container {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
            .search-form {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
            .form-row {{ display: grid; grid-template-columns: 1fr 1fr auto; gap: 15px; align-items: end; }}
            .form-group {{ margin-bottom: 15px; }}
            .form-group label {{ display: block; margin-bottom: 5px; color: #495057; font-weight: bold; }}
            .form-group input, .form-group select {{ width: 100%; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px; font-size: 14px; }}
            .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .table th, .table td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
            .table th {{ background: #007bff; color: white; }}
            .table tr:nth-child(even) {{ background: #f8f9fa; }}
            .btn {{ padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; border: none; cursor: pointer; }}
            .btn:hover {{ background: #0056b3; }}
            .btn-search {{ background: #28a745; }}
            .btn-search:hover {{ background: #218838; }}
            .btn-edit {{ padding: 5px 10px; background: #28a745; color: white; text-decoration: none; border-radius: 3px; margin: 2px; display: inline-block; font-size: 12px; }}
            .btn-edit:hover {{ background: #218838; }}
            .btn-view {{ padding: 5px 10px; background: #17a2b8; color: white; text-decoration: none; border-radius: 3px; margin: 2px; display: inline-block; font-size: 12px; }}
            .btn-view:hover {{ background: #138496; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔍 Search Patients</h2>
            
            <form method="POST" class="search-form">
                <div class="form-row">
                    <div class="form-group">
                        <label for="search_query">Search Query:</label>
                        <input type="text" id="search_query" name="search_query" value="{search_query}" placeholder="Enter search term..." required>
                    </div>
                    <div class="form-group">
                        <label for="search_type">Search By:</label>
                        <select id="search_type" name="search_type">
                            <option value="name">Patient Name</option>
                            <option value="phone">Phone Number</option>
                            <option value="patient_code">Patient Code</option>
                            <option value="treatment">Treatment</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <button type="submit" class="btn btn-search">🔍 Search</button>
                    </div>
                </div>
            </form>
            
            {results_section}
            
            <div style="text-align: center; margin-top: 20px;">
                <a href="/view_patients?clinic_id={clinic_id}" class="btn">📋 View All Patients</a>
                <a href="/dashboard?clinic_id={clinic_id}" class="btn">🏠 Back to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/advanced_analytics")
def advanced_analytics():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return "<h3>❌ Error: Invalid clinic access!</h3><a href='/'>← Back to Home</a>"
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get clinic info
        cursor.execute("SELECT name FROM clinics WHERE id = ?", (clinic_id,))
        clinic_info = cursor.fetchone()
        if not clinic_info:
            return "<h3>❌ Error: Clinic not found!</h3><a href='/'>← Back to Home</a>"
        
        clinic_name = clinic_info[0]
        
        # Get analytics data
        cursor.execute("SELECT COUNT(*) FROM patients WHERE clinic_id = ?", (clinic_id,))
        total_patients = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM patient_analytics WHERE clinic_id = ?", (clinic_id,))
        total_visits = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(treatment_cost) FROM patient_analytics WHERE clinic_id = ?", (clinic_id,))
        total_revenue = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(satisfaction_rating) FROM patient_analytics WHERE clinic_id = ?", (clinic_id,))
        avg_satisfaction = cursor.fetchone()[0] or 0
        
        # Get recent analytics
        cursor.execute("""
            SELECT p.name, pa.visit_date, pa.diagnosis, pa.treatment_cost, pa.satisfaction_rating
            FROM patient_analytics pa 
            JOIN patients p ON pa.patient_id = p.id 
            WHERE pa.clinic_id = ? 
            ORDER BY pa.visit_date DESC LIMIT 10
        """, (clinic_id,))
        recent_analytics = cursor.fetchall()
        
        conn.close()
        
        recent_html = ""
        for item in recent_analytics:
            recent_html += f'''
            <tr>
                <td>{item[0]}</td>
                <td>{item[1]}</td>
                <td>{item[2]}</td>
                <td>₹{item[3]:.2f}</td>
                <td>{'⭐' * int(item[4] or 0)}</td>
            </tr>
            '''
        
        return f'''
        <html>
        <head>
            <title>Advanced Analytics - {clinic_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f8ff; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; }}
                .analytics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .analytics-card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; }}
                .metric-value {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
                .metric-label {{ color: #666; font-size: 14px; }}
                .table-container {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; }}
                .table {{ width: 100%; border-collapse: collapse; }}
                .table th, .table td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
                .table th {{ background: #007bff; color: white; }}
                .table tr:nth-child(even) {{ background: #f8f9fa; }}
                .btn {{ padding: 12px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 8px; margin: 5px; display: inline-block; }}
                .btn:hover {{ background: #0056b3; }}
                .btn-success {{ background: #28a745; }}
                .btn-success:hover {{ background: #218838; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Advanced Analytics</h1>
                    <p>{clinic_name} - Comprehensive Data Insights</p>
                </div>
                
                <div class="analytics-grid">
                    <div class="analytics-card">
                        <div class="metric-value" style="color: #007bff;">{total_patients}</div>
                        <div class="metric-label">👥 Total Patients</div>
                    </div>
                    <div class="analytics-card">
                        <div class="metric-value" style="color: #28a745;">{total_visits}</div>
                        <div class="metric-label">🏥 Total Visits</div>
                    </div>
                    <div class="analytics-card">
                        <div class="metric-value" style="color: #ffc107;">₹{total_revenue:.2f}</div>
                        <div class="metric-label">💰 Total Revenue</div>
                    </div>
                    <div class="analytics-card">
                        <div class="metric-value" style="color: #dc3545;">{avg_satisfaction:.1f}/5</div>
                        <div class="metric-label">⭐ Avg Satisfaction</div>
                    </div>
                </div>
                
                <div class="table-container">
                    <h3>📈 Recent Patient Analytics</h3>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Patient Name</th>
                                <th>Visit Date</th>
                                <th>Diagnosis</th>
                                <th>Cost</th>
                                <th>Rating</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recent_html if recent_html else "<tr><td colspan='5' style='text-align: center; color: #666;'>No analytics data available yet.</td></tr>"}
                        </tbody>
                    </table>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/generate_report?clinic_id={clinic_id}" class="btn btn-success">📄 Generate Report</a>
                    <a href="/dashboard?clinic_id={clinic_id}" class="btn">🏠 Back to Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''
        <html>
        <body style="font-family: Arial; margin: 40px;">
            <div style="background: #f8d7da; padding: 20px; border-radius: 8px; border: 1px solid #f5c6cb;">
                <h3 style="color: #721c24;">❌ Analytics Error</h3>
                <p style="color: #721c24;">Error: {str(e)}</p>
                <a href="/dashboard?clinic_id={clinic_id}" style="background: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">← Back to Dashboard</a>
            </div>
        </body>
        </html>
        '''

@app.route("/generate_report")
def generate_report():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return "<h3>❌ Error: Invalid clinic access!</h3><a href='/'>← Back to Home</a>"
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get clinic info
        cursor.execute("SELECT name FROM clinics WHERE id = ?", (clinic_id,))
        clinic_info = cursor.fetchone()
        if not clinic_info:
            return "<h3>❌ Error: Clinic not found!</h3><a href='/'>← Back to Home</a>"
        
        clinic_name = clinic_info[0]
        
        # Get comprehensive report data
        cursor.execute("""
            SELECT p.patient_code, p.name, p.age, p.sex, p.treatment,
                   pa.visit_date, pa.diagnosis, pa.treatment_cost, pa.satisfaction_rating
            FROM patients p
            LEFT JOIN patient_analytics pa ON p.id = pa.patient_id
            WHERE p.clinic_id = ?
            ORDER BY p.created_at DESC
        """, (clinic_id,))
        report_data = cursor.fetchall()
        
        conn.close()
        
        report_rows = ""
        for row in report_data:
            report_rows += f'''
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2] or 'N/A'}</td>
                <td>{row[3] or 'N/A'}</td>
                <td>{row[4] or 'N/A'}</td>
                <td>{row[5] or 'N/A'}</td>
                <td>{row[6] or 'N/A'}</td>
                <td>₹{row[7] or 0:.2f}</td>
                <td>{'⭐' * int(row[8] or 0)}</td>
            </tr>
            '''
        
        return f'''
        <html>
        <head>
            <title>Comprehensive Report - {clinic_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .table th, .table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 12px; }}
                .table th {{ background: #007bff; color: white; }}
                .btn {{ padding: 10px 20px; margin: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }}
                .btn:hover {{ background: #218838; }}
                .btn-back {{ background: #6c757d; }}
                .btn-back:hover {{ background: #545b62; }}
                @media print {{ .no-print {{ display: none; }} }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📄 Comprehensive Report</h1>
                <h2>{clinic_name}</h2>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <table class="table">
                <thead>
                    <tr>
                        <th>Patient Code</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Gender</th>
                        <th>Treatment</th>
                        <th>Visit Date</th>
                        <th>Diagnosis</th>
                        <th>Cost</th>
                        <th>Rating</th>
                    </tr>
                </thead>
                <tbody>
                    {report_rows if report_rows else "<tr><td colspan='9' style='text-align: center; color: #666;'>No data available for report.</td></tr>"}
                </tbody>
            </table>
            
            <div class="no-print" style="text-align: center; margin-top: 30px;">
                <button onclick="window.print()" class="btn">🖨️ Print Report</button>
                <a href="/advanced_analytics?clinic_id={clinic_id}" class="btn btn-back">← Back to Analytics</a>
            </div>
        </body>
        '''

@app.route("/edit_patient", methods=["GET", "POST"])
def edit_patient():
    clinic_id = request.args.get("clinic_id")
    patient_code = request.args.get("patient_code")
    
    if not clinic_id or not patient_code:
        return redirect("/")
    
    if request.method == "POST":
        try:
            # Update patient data
            name = request.form["name"]
            age = request.form.get("age", "")
            sex = request.form.get("sex", "")
            phone = request.form.get("phone", "")
            treatment = request.form.get("treatment", "")
            dob = request.form.get("dob", "")
            email = request.form.get("email", "")
            address = request.form.get("address", "")
            emergency_contact_name = request.form.get("emergency_contact_name", "")
            emergency_contact_phone = request.form.get("emergency_contact_phone", "")
            medical_history = request.form.get("medical_history", "")
            current_medications = request.form.get("current_medications", "")
            allergies = request.form.get("allergies", "")
            insurance_provider = request.form.get("insurance_provider", "")
            insurance_number = request.form.get("insurance_number", "")
            previous_dental_work = request.form.get("previous_dental_work", "")
            chief_complaint = request.form.get("chief_complaint", "")
            pain_level = request.form.get("pain_level", "")
            last_cleaning_date = request.form.get("last_cleaning_date", "")
            preferred_appointment_time = request.form.get("preferred_appointment_time", "")
            
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("""UPDATE patients SET 
                name=?, age=?, sex=?, phone=?, treatment=?, dob=?, email=?, address=?,
                emergency_contact_name=?, emergency_contact_phone=?, medical_history=?,
                current_medications=?, allergies=?, insurance_provider=?, insurance_number=?,
                previous_dental_work=?, chief_complaint=?, pain_level=?, last_cleaning_date=?,
                preferred_appointment_time=?
                WHERE clinic_id=? AND patient_code=?""",
                         (name, age, sex, phone, treatment, dob, email, address,
                          emergency_contact_name, emergency_contact_phone, medical_history,
                          current_medications, allergies, insurance_provider, insurance_number,
                          previous_dental_work, chief_complaint, pain_level, last_cleaning_date,
                          preferred_appointment_time, clinic_id, patient_code))
            conn.commit()
            conn.close()
            
            return f'''
            <html>
            <body style="font-family: Arial; margin: 40px; text-align: center;">
                <div style="background: #d4edda; padding: 20px; border-radius: 8px; border: 1px solid #c3e6cb; margin-bottom: 20px;">
                    <h3 style="color: #155724;">✅ Patient Updated Successfully!</h3>
                    <p style="color: #155724;">Patient {patient_code} has been updated with new information.</p>
                </div>
                <a href="/view_patients?clinic_id={clinic_id}" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px;">📋 View All Patients</a>
                <a href="/view_patient_detail?clinic_id={clinic_id}&patient_code={patient_code}" style="background: #17a2b8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px;">👁️ View Details</a>
                <a href="/dashboard?clinic_id={clinic_id}" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px;">🏠 Dashboard</a>
            </body>
            </html>
            '''
        except Exception as e:
            return f"<h3>❌ Error updating patient: {str(e)}</h3><a href='/view_patients?clinic_id={clinic_id}'>← Back to Patients</a>"
    
    # GET request - show edit form
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE clinic_id = ? AND patient_code = ?", (clinic_id, patient_code))
        patient = cursor.fetchone()
        conn.close()
        
        if not patient:
            return f"<h3>❌ Patient not found!</h3><a href='/view_patients?clinic_id={clinic_id}'>← Back to Patients</a>"
        
        # Patient data mapping
        patient_data = {
            'name': patient[3] or '',
            'age': patient[4] or '',
            'sex': patient[5] or '',
            'phone': patient[6] or '',
            'treatment': patient[7] or '',
            'dob': patient[9] or '',
            'email': patient[10] or '',
            'address': patient[11] or '',
            'emergency_contact_name': patient[12] or '',
            'emergency_contact_phone': patient[13] or '',
            'medical_history': patient[14] or '',
            'current_medications': patient[15] or '',
            'allergies': patient[16] or '',
            'insurance_provider': patient[17] or '',
            'insurance_number': patient[18] or '',
            'previous_dental_work': patient[19] or '',
            'chief_complaint': patient[20] or '',
            'pain_level': patient[21] or '',
            'last_cleaning_date': patient[22] or '',
            'preferred_appointment_time': patient[23] or ''
        }
        
        return f'''
        <html>
        <head>
            <title>Edit Patient - {patient_code}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                .form-section {{ margin-bottom: 30px; padding: 20px; border: 2px solid #e9ecef; border-radius: 10px; }}
                .form-section h3 {{ color: #495057; margin-top: 0; }}
                .form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; }}
                .form-group {{ margin-bottom: 15px; }}
                .form-group label {{ display: block; margin-bottom: 5px; color: #495057; font-weight: bold; }}
                .form-group input, .form-group select, .form-group textarea {{ width: 100%; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px; font-size: 14px; }}
                .btn {{ padding: 12px 25px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin-right: 10px; text-decoration: none; display: inline-block; }}
                .btn-primary {{ background: #007bff; color: white; }}
                .btn-secondary {{ background: #6c757d; color: white; }}
                .patient-header {{ background: #007bff; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="patient-header">
                    <h2>✏️ Edit Patient: {patient_code}</h2>
                    <p>Update patient information</p>
                </div>
                
                <form method="POST">
                    <div class="form-section">
                        <h3>📋 Basic Information</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="name">👤 Full Name:</label>
                                <input type="text" id="name" name="name" value="{patient_data['name']}" required>
                            </div>
                            <div class="form-group">
                                <label for="age">🎂 Age:</label>
                                <input type="number" id="age" name="age" value="{patient_data['age']}" min="1" max="120">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="phone">📞 Phone:</label>
                                <input type="tel" id="phone" name="phone" value="{patient_data['phone']}">
                            </div>
                            <div class="form-group">
                                <label for="email">📧 Email:</label>
                                <input type="email" id="email" name="email" value="{patient_data['email']}">
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="treatment">🦷 Treatment Plan:</label>
                            <input type="text" id="treatment" name="treatment" value="{patient_data['treatment']}">
                        </div>
                    </div>

                    <div style="text-align: center; margin-top: 30px;">
                        <button type="submit" class="btn btn-primary">✅ Update Patient</button>
                        <a href="/view_patients?clinic_id={clinic_id}" class="btn btn-secondary">← Back to Patients</a>
                    </div>
                </form>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<h3>❌ Error loading patient: {str(e)}</h3><a href='/view_patients?clinic_id={clinic_id}'>← Back to Patients</a>"

@app.route("/view_patient_detail")
def view_patient_detail():
    clinic_id = request.args.get("clinic_id")
    patient_code = request.args.get("patient_code")
    
    if not clinic_id or not patient_code:
        return redirect("/")
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get patient details
        cursor.execute("SELECT * FROM patients WHERE clinic_id = ? AND patient_code = ?", (clinic_id, patient_code))
        patient = cursor.fetchone()
        
        if not patient:
            return f"<h3>❌ Patient not found!</h3><a href='/view_patients?clinic_id={clinic_id}'>← Back to Patients</a>"
        
        # Get patient analytics
        cursor.execute("SELECT * FROM patient_analytics WHERE clinic_id = ? AND patient_id = ?", (clinic_id, patient[0]))
        analytics = cursor.fetchall()
        
        conn.close()
        
        analytics_html = ""
        if analytics:
            for record in analytics:
                analytics_html += f'''
                <tr>
                    <td>{record[3]}</td>
                    <td>{record[4]}</td>
                    <td>₹{record[5]:.2f}</td>
                    <td>{'⭐' * int(record[6] or 0)}</td>
                    <td>{record[7]}</td>
                </tr>
                '''
        else:
            analytics_html = "<tr><td colspan='5' style='text-align: center; color: #666;'>No analytics data available</td></tr>"
        
        return f'''
        <html>
        <head>
            <title>Patient Details - {patient[3]}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                .patient-header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }}
                .info-section {{ background: #f8f9fa; padding: 20px; border-radius: 10px; }}
                .info-section h3 {{ color: #495057; margin-top: 0; }}
                .info-item {{ margin-bottom: 10px; }}
                .info-label {{ font-weight: bold; color: #495057; }}
                .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .table th, .table td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
                .table th {{ background: #007bff; color: white; }}
                .btn {{ padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }}
                .btn-edit {{ background: #28a745; }}
                .btn-secondary {{ background: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="patient-header">
                    <h1>👤 {patient[3]}</h1>
                    <p>Patient Code: {patient[2]} | Age: {patient[4] or 'N/A'} | Gender: {patient[5] or 'N/A'}</p>
                </div>
                
                <div class="info-grid">
                    <div class="info-section">
                        <h3>📋 Basic Information</h3>
                        <div class="info-item"><span class="info-label">Phone:</span> {patient[6] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Email:</span> {patient[10] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Date of Birth:</span> {patient[9] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Address:</span> {patient[11] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Treatment:</span> {patient[7] or 'N/A'}</div>
                    </div>
                    
                    <div class="info-section">
                        <h3>🚨 Emergency Contact</h3>
                        <div class="info-item"><span class="info-label">Name:</span> {patient[12] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Phone:</span> {patient[13] or 'N/A'}</div>
                        
                        <h3 style="margin-top: 20px;">🏥 Insurance</h3>
                        <div class="info-item"><span class="info-label">Provider:</span> {patient[17] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Number:</span> {patient[18] or 'N/A'}</div>
                    </div>
                </div>
                
                <div class="info-section">
                    <h3>🏥 Medical Information</h3>
                    <div class="info-item"><span class="info-label">Medical History:</span> {patient[14] or 'None'}</div>
                    <div class="info-item"><span class="info-label">Current Medications:</span> {patient[15] or 'None'}</div>
                    <div class="info-item"><span class="info-label">Allergies:</span> {patient[16] or 'None'}</div>
                    <div class="info-item"><span class="info-label">Previous Dental Work:</span> {patient[19] or 'None'}</div>
                    <div class="info-item"><span class="info-label">Chief Complaint:</span> {patient[20] or 'None'}</div>
                    <div class="info-item"><span class="info-label">Pain Level:</span> {patient[21] or 'N/A'}/10</div>
                    <div class="info-item"><span class="info-label">Last Cleaning:</span> {patient[22] or 'N/A'}</div>
                    <div class="info-item"><span class="info-label">Preferred Time:</span> {patient[23] or 'N/A'}</div>
                </div>
                
                <h3>📊 Visit Analytics</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Visit Date</th>
                            <th>Diagnosis</th>
                            <th>Cost</th>
                            <th>Rating</th>
                            <th>Doctor</th>
                        </tr>
                    </thead>
                    <tbody>
                        {analytics_html}
                    </tbody>
                </table>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/edit_patient?clinic_id={clinic_id}&patient_code={patient_code}" class="btn btn-edit">✏️ Edit Patient</a>
                    <a href="/view_patients?clinic_id={clinic_id}" class="btn btn-secondary">📋 All Patients</a>
                    <a href="/dashboard?clinic_id={clinic_id}" class="btn">🏠 Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<h3>❌ Error loading patient details: {str(e)}</h3><a href='/view_patients?clinic_id={clinic_id}'>← Back to Patients</a>"

if __name__ == "__main__":
    init_database()
    print("🦷 Dental Clinic Management System Starting...")
    print("🌐 Database initialized successfully!")
    app.run(debug=True, host="0.0.0.0", port=5000)

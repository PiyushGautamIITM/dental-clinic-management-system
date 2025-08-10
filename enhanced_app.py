from flask import Flask, request, redirect, url_for, session, render_template_string
import sqlite3
import os
from datetime import datetime, timedelta
import secrets

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
                <p style="color: #666;">Enhanced with Patient Search & Edit</p>
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
                .btn-search {{ background: #6f42c1; color: white; }}
                .recent-list {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                .recent-list ul {{ list-style: none; padding: 0; }}
                .recent-list li {{ padding: 10px; border-bottom: 1px solid #eee; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🦷 {clinic_name}</h1>
                <p>Enhanced Patient Management System</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{patient_count}</div>
                    <div>Total Patients</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">✨</div>
                    <div>Advanced Features</div>
                </div>
            </div>
            
            <div class="buttons">
                <a href="/add_patient?clinic_id={clinic_id}" class="btn btn-success">👥 Add New Patient</a>
                <a href="/view_patients?clinic_id={clinic_id}" class="btn btn-primary">📋 View All Patients</a>
                <a href="/search_patients?clinic_id={clinic_id}" class="btn btn-search">🔍 Search Patients</a>
                <a href="/advanced_analytics?clinic_id={clinic_id}" class="btn btn-info">📊 Advanced Analytics</a>
                <a href="/address_analytics?clinic_id={clinic_id}" class="btn" style="background: #28a745; color: white;">📍 Address Analytics</a>
                <a href="/generate_report?clinic_id={clinic_id}" class="btn btn-warning">📄 Generate Reports</a>
            </div>
            
            <div class="recent-list">
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

# Patient routes will be imported from a separate module
from patient_routes import *

if __name__ == "__main__":
    init_database()
    
    # Import patient routes after app initialization
    import patient_routes
    
    print("🦷 Enhanced Dental Clinic Management System Starting...")
    print("🌐 Database initialized successfully!")
    print("🔍 Search & Edit Features Enabled!")
    app.run(debug=True, host="0.0.0.0", port=5000)

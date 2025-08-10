# setup_and_run.py - Complete setup with database and ngrok
from pyngrok import ngrok
import threading
import time
import sqlite3
from werkzeug.security import generate_password_hash

# Set your ngrok auth token
ngrok.set_auth_token("316jwPa6yl5RvmjWAEuBqe543QH_2aWxnmevneHN7wk7zhzHQ")

def setup_database():
    """Create tables and add demo data"""
    print("🗄️ Setting up database...")
    
    conn = sqlite3.connect('dental.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clinics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clinic_code VARCHAR(32) UNIQUE NOT NULL,
            name VARCHAR(200) NOT NULL,
            location VARCHAR(200),
            incharge VARCHAR(200),
            login_id VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(200) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_code VARCHAR(64) UNIQUE NOT NULL,
            clinic_id INTEGER NOT NULL,
            name VARCHAR(200) NOT NULL,
            sex VARCHAR(20),
            dob DATE,
            age INTEGER,
            treatment_type VARCHAR(100),
            mobile_number VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (clinic_id) REFERENCES clinics (id)
        )
    ''')
    
    # Add demo clinics
    demo_clinics = [
        ("CLINIC0001", "City Dental Care", "New York, USA", "Dr. Smith", "CITY001", "pass123"),
        ("CLINIC0002", "Smile Center", "Los Angeles, USA", "Dr. Johnson", "SMIL001", "pass123"),
        ("CLINIC0003", "Dental Plus", "Chicago, USA", "Dr. Brown", "DENT001", "pass123"),
    ]
    
    for clinic_code, name, location, incharge, login_id, password in demo_clinics:
        pw_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT OR IGNORE INTO clinics (clinic_code, name, location, incharge, login_id, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (clinic_code, name, location, incharge, login_id, pw_hash))
    
    # Add demo patients
    demo_patients = [
        ("CLINIC0001-P0001", 1, "John Doe", "Male", "1985-05-15", 39, "Cleaning", "555-0101"),
        ("CLINIC0001-P0002", 1, "Jane Smith", "Female", "1990-08-20", 34, "Filling", "555-0102"),
        ("CLINIC0001-P0003", 1, "Bob Wilson", "Male", "1975-12-10", 49, "Root Canal", "555-0103"),
        ("CLINIC0002-P0001", 2, "Alice Brown", "Female", "1988-03-25", 36, "Orthodontics", "555-0201"),
        ("CLINIC0002-P0002", 2, "Charlie Davis", "Male", "1992-07-14", 32, "Extraction", "555-0202"),
        ("CLINIC0003-P0001", 3, "Diana Miller", "Female", "1987-11-30", 37, "Checkup", "555-0301"),
    ]
    
    for patient_code, clinic_id, name, sex, dob, age, treatment, mobile in demo_patients:
        cursor.execute('''
            INSERT OR IGNORE INTO patients (patient_code, clinic_id, name, sex, dob, age, treatment_type, mobile_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient_code, clinic_id, name, sex, dob, age, treatment, mobile))
    
    conn.commit()
    conn.close()
    print("✅ Database setup complete!")

def start_flask():
    """Start the Flask app"""
    from simple_app import app
    print("🚀 Starting Flask application...")
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def create_ngrok_tunnel():
    """Create ngrok tunnel"""
    time.sleep(3)  # Wait for Flask to start
    
    try:
        # Create tunnel
        public_url = ngrok.connect(5000)
        print(f"\n🎉 SUCCESS! Your Dental Clinic App is LIVE!")
        print(f"🌐 PUBLIC URL: {public_url}")
        print(f"🔗 Share this link with anyone!")
        print(f"📱 Mobile friendly and secure HTTPS")
        print(f"🔧 Local URL: http://127.0.0.1:5000")
        print(f"\n📋 Demo Login Credentials:")
        print(f"   🏥 City Dental Care - Login: CITY001, Password: pass123")
        print(f"   😊 Smile Center - Login: SMIL001, Password: pass123")
        print(f"   🦷 Dental Plus - Login: DENT001, Password: pass123")
        print(f"\n🏥 Features Available:")
        print(f"   • Register new clinics")
        print(f"   • Login with demo accounts")
        print(f"   • Add new patients")
        print(f"   • View patient records")
        print(f"   • Secure authentication")
        print(f"\n⚡ Press Ctrl+C to stop the server")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Ngrok tunnel failed: {e}")

if __name__ == "__main__":
    print("🦷 Dental Clinic Management System Setup")
    print("-" * 50)
    
    # Setup database with demo data
    setup_database()
    
    # Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Create ngrok tunnel
    create_ngrok_tunnel()
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        try:
            ngrok.disconnect(ngrok.get_tunnels()[0].public_url)
            ngrok.kill()
        except:
            pass

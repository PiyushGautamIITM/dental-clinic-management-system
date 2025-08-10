import sqlite3
import random
from datetime import datetime, timedelta

def generate_fake_data():
    """Generate comprehensive fake data for the dental clinic"""
    
    DATABASE = "dental_clinic.db"
    
    # Indian names and data
    indian_names = [
        "Rajesh Kumar", "Priya Sharma", "Amit Singh", "Neha Gupta", "Suresh Patel",
        "Kavita Mishra", "Deepak Agarwal", "Sunita Yadav", "Manoj Verma", "Pooja Shah",
        "Vikash Jain", "Meera Reddy", "Rohit Pandey", "Shruti Desai", "Ankit Malhotra",
        "Ritu Khanna", "Sanjay Tiwari", "Nisha Saxena", "Arvind Shukla", "Divya Joshi",
        "Rakesh Bansal", "Seema Arora", "Naveen Goyal", "Swati Mittal", "Rajesh Kapoor",
        "Preeti Bhatt", "Sachin Chauhan", "Rekha Sinha", "Vikas Aggarwal", "Madhuri Jha"
    ]
    
    treatments = [
        "General Checkup", "Teeth Cleaning", "Dental Filling", "Root Canal Treatment",
        "Tooth Extraction", "Orthodontics", "Crowns & Bridges", "Dental Implants",
        "Teeth Whitening", "Periodontal Treatment", "Emergency Treatment", "Consultation"
    ]
    
    diagnoses = [
        "Dental Caries", "Gingivitis", "Periodontitis", "Pulpitis", "Tooth Abscess",
        "Malocclusion", "Tooth Fracture", "Enamel Erosion", "TMJ Disorder", "Oral Thrush"
    ]
    
    doctors = [
        "Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis", "Dr. Miller"
    ]
    
    insurance_providers = [
        "Star Health", "HDFC ERGO", "ICICI Lombard", "Bajaj Allianz", "Max Bupa",
        "Care Health", "Religare Health", "Aditya Birla Health", "SBI General", "Cholamandalam"
    ]
    
    cities = [
        "Mumbai, Maharashtra", "Delhi", "Bangalore, Karnataka", "Chennai, Tamil Nadu",
        "Hyderabad, Telangana", "Pune, Maharashtra", "Kolkata, West Bengal", "Ahmedabad, Gujarat",
        "Jaipur, Rajasthan", "Lucknow, Uttar Pradesh"
    ]
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    print("🚀 Generating comprehensive fake data...")
    
    # First, create a test clinic if it doesn't exist
    try:
        cursor.execute("INSERT INTO clinics (name, email, password, phone, address) VALUES (?, ?, ?, ?, ?)",
                     ("Smile Dental Clinic", "admin@smile.com", "admin123", "+91-9876543210", "123 Main Street, Mumbai"))
        clinic_id = cursor.lastrowid
        print(f"✅ Created test clinic with ID: {clinic_id}")
    except sqlite3.IntegrityError:
        # Clinic already exists, get its ID
        cursor.execute("SELECT id FROM clinics WHERE email = ?", ("admin@smile.com",))
        clinic_id = cursor.fetchone()[0]
        print(f"✅ Using existing clinic with ID: {clinic_id}")
    
    # Generate 25 patients with comprehensive data
    for i in range(25):
        name = random.choice(indian_names)
        age = random.randint(18, 75)
        sex = random.choice(["Male", "Female"])
        treatment = random.choice(treatments)
        patient_code = f"P{datetime.now().strftime('%Y%m%d')}{i+1:03d}"
        
        # Generate dates
        dob = (datetime.now() - timedelta(days=age*365 + random.randint(0, 365))).strftime('%Y-%m-%d')
        last_cleaning = (datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d')
        
        # Generate comprehensive patient data
        cursor.execute("""INSERT INTO patients (
            clinic_id, patient_code, name, age, sex, phone, treatment,
            dob, email, address, emergency_contact_name, emergency_contact_phone,
            medical_history, current_medications, allergies, insurance_provider,
            insurance_number, previous_dental_work, chief_complaint, pain_level,
            last_cleaning_date, preferred_appointment_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (clinic_id, patient_code, name, age, sex, 
                      f"+91-{random.randint(7000000000, 9999999999)}", treatment,
                      dob, f"{name.lower().replace(' ', '.')}@email.com", 
                      f"{random.randint(1, 999)} {random.choice(cities)}",
                      f"Emergency Contact {i+1}", f"+91-{random.randint(7000000000, 9999999999)}",
                      random.choice(["No significant history", "Diabetes", "Hypertension", "Heart condition", "None"]),
                      random.choice(["None", "Paracetamol", "Vitamin D", "Blood pressure medication"]),
                      random.choice(["None", "Penicillin", "Latex", "Food allergies"]),
                      random.choice(insurance_providers),
                      f"INS{random.randint(100000, 999999)}",
                      random.choice(["Previous filling", "Braces as child", "Wisdom tooth extraction", "None"]),
                      random.choice(["Tooth pain", "Routine checkup", "Sensitivity", "Bleeding gums"]),
                      random.randint(1, 10),
                      last_cleaning,
                      random.choice(["Morning", "Afternoon", "Evening"])))
        
        patient_id = cursor.lastrowid
        
        # Generate analytics data for this patient
        visit_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
        cost = random.uniform(500, 5000)
        
        cursor.execute("""INSERT INTO patient_analytics (
            clinic_id, patient_id, visit_date, diagnosis, treatment_cost,
            satisfaction_rating, doctor_assigned, treatment_duration
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                     (clinic_id, patient_id, visit_date, random.choice(diagnoses),
                      cost, random.randint(3, 5), random.choice(doctors),
                      random.randint(15, 120)))
        
        # Generate revenue analytics
        cursor.execute("""INSERT INTO revenue_analytics (
            clinic_id, transaction_date, service_type, base_amount, tax_amount,
            discount_amount, final_amount, payment_method, payment_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (clinic_id, visit_date, treatment, cost, cost*0.18, 
                      random.uniform(0, cost*0.1), cost*1.18, 
                      random.choice(["Cash", "Card", "UPI", "Insurance"]), "Completed"))
        
        # Generate patient feedback
        ratings = [3, 4, 4, 5, 5, 5]  # Mostly positive ratings
        feedback_texts = [
            "Great service and professional staff",
            "Very satisfied with the treatment",
            "Clean facility and friendly doctors",
            "Quick and painless procedure",
            "Excellent care and follow-up",
            "Highly recommend this clinic"
        ]
        
        cursor.execute("""INSERT INTO patient_feedback (
            clinic_id, patient_id, feedback_text, rating, sentiment_score, feedback_date
        ) VALUES (?, ?, ?, ?, ?, ?)""",
                     (clinic_id, patient_id, random.choice(feedback_texts),
                      random.choice(ratings), random.uniform(0.6, 1.0), visit_date))
    
    # Generate doctor performance data
    for doctor in doctors:
        cursor.execute("""INSERT INTO doctor_performance (
            clinic_id, doctor_name, specialization, patients_treated,
            success_rate, average_rating, revenue_generated
        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                     (clinic_id, doctor, random.choice(["General Dentistry", "Orthodontics", "Oral Surgery"]),
                      random.randint(50, 200), random.uniform(85, 98),
                      random.uniform(4.0, 5.0), random.uniform(50000, 200000)))
    
    # Generate smart alerts
    alert_messages = [
        "Monthly revenue target achieved",
        "Patient satisfaction score above 4.5",
        "Appointment booking trend increasing",
        "New patient registrations up 15%",
        "Treatment completion rate: 95%"
    ]
    
    for i in range(5):
        cursor.execute("""INSERT INTO smart_alerts (
            clinic_id, alert_type, alert_message, severity_level, is_resolved
        ) VALUES (?, ?, ?, ?, ?)""",
                     (clinic_id, "Performance", random.choice(alert_messages),
                      random.choice(["Low", "Medium", "High"]), random.choice([True, False])))
    
    conn.commit()
    conn.close()
    
    print("✅ Successfully generated comprehensive fake data!")
    print(f"📊 Created 25 patients with full analytics data")
    print(f"💰 Generated revenue and performance analytics")
    print(f"🔔 Added smart alerts and feedback data")
    print(f"🦷 Test clinic credentials: admin@smile.com / admin123")

if __name__ == "__main__":
    generate_fake_data()

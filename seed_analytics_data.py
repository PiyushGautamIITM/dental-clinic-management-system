# seed_analytics_data.py - Add sample data for analytics demonstration
import sqlite3
import random
from datetime import datetime, timedelta

DATABASE = "clinic_database.db"

def seed_sample_data():
    """Add sample patients and analytics data for demonstration"""
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Sample clinic data (assuming clinic ID 1 exists)
    clinic_id = 1
    
    # Sample treatments and their costs
    treatments = [
        ("General Checkup", 500),
        ("Teeth Cleaning", 800),
        ("Filling", 1200),
        ("Root Canal", 3500),
        ("Extraction", 800),
        ("Orthodontics", 25000),
        ("Crowns & Bridges", 8000),
        ("Dental Implants", 15000),
        ("Whitening", 2500),
        ("Emergency Treatment", 1500)
    ]
    
    # Sample symptoms and diagnoses
    symptoms_diagnoses = [
        ("Tooth pain, sensitivity", "Cavity, Tooth decay"),
        ("Gum bleeding, swelling", "Gingivitis, Gum infection"),
        ("Tooth ache, fever", "Abscess, Root infection"),
        ("Broken tooth, pain", "Dental trauma, Fracture"),
        ("Bad breath, loose tooth", "Periodontal disease"),
        ("Jaw pain, clicking", "TMJ disorder"),
        ("Tooth sensitivity, pain", "Exposed nerve, Deep cavity"),
        ("Wisdom tooth pain", "Impacted wisdom tooth"),
        ("Yellow teeth, stains", "Tooth discoloration"),
        ("Missing tooth", "Tooth loss, Need replacement")
    ]
    
    # Sample patient data
    sample_patients = [
        ("Raj Kumar", "Male", 45),
        ("Priya Sharma", "Female", 32),
        ("Amit Singh", "Male", 28),
        ("Sneha Patel", "Female", 35),
        ("Vikram Reddy", "Male", 50),
        ("Anjali Gupta", "Female", 41),
        ("Rohit Jain", "Male", 24),
        ("Kavya Nair", "Female", 29),
        ("Suresh Rao", "Male", 55),
        ("Meera Iyer", "Female", 38),
        ("Arjun Mehta", "Male", 33),
        ("Divya Das", "Female", 27),
        ("Kiran Kumar", "Male", 42),
        ("Shalini Roy", "Female", 36),
        ("Manoj Tiwari", "Male", 39),
        ("Preeti Agarwal", "Female", 31),
        ("Deepak Yadav", "Male", 26),
        ("Ritu Saxena", "Female", 44),
        ("Arun Pandey", "Male", 48),
        ("Nisha Verma", "Female", 34)
    ]
    
    print("🌱 Adding sample patients and analytics data...")
    
    # Add patients with some existing in the database
    for i, (name, gender, age) in enumerate(sample_patients):
        # Check if clinic exists
        cursor.execute("SELECT id FROM clinics WHERE id = ?", (clinic_id,))
        if not cursor.fetchone():
            print(f"❌ Clinic {clinic_id} not found. Please register a clinic first.")
            break
            
        # Random treatment
        treatment, cost = random.choice(treatments)
        mobile = f"98765{random.randint(10000, 99999)}"
        
        # Generate patient code
        cursor.execute("SELECT COUNT(*) FROM patients WHERE clinic_id = ?", (clinic_id,))
        count = cursor.fetchone()[0]
        patient_code = f"P{clinic_id:03d}{count + 1:03d}"
        
        # Random registration date (last 6 months)
        days_ago = random.randint(1, 180)
        reg_date = datetime.now() - timedelta(days=days_ago)
        
        try:
            cursor.execute("""
                INSERT INTO patients (clinic_id, patient_code, name, sex, age, mobile, treatment, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (clinic_id, patient_code, name, gender, age, mobile, treatment, reg_date.isoformat()))
            
            patient_id = cursor.lastrowid
            
            # Add analytics data for this patient
            symptoms, diagnosis = random.choice(symptoms_diagnoses)
            
            # Random visit data
            visit_date = reg_date + timedelta(days=random.randint(0, 30))
            recovery_days = random.randint(3, 21)
            satisfaction = random.randint(3, 5)  # 3-5 star rating
            consultation_time = random.randint(15, 60)  # minutes
            payment_modes = ["Cash", "Card", "UPI", "Insurance"]
            payment_mode = random.choice(payment_modes)
            insurance_claim = cost * 0.8 if payment_mode == "Insurance" else 0
            
            doctors = ["Dr. Smith", "Dr. Patel", "Dr. Kumar", "Dr. Sharma"]
            doctor = random.choice(doctors)
            
            follow_up = "Yes" if random.random() > 0.6 else "No"
            
            feedback_options = [
                "Excellent service, very satisfied",
                "Good treatment, professional staff",
                "Quick and efficient care",
                "Helpful doctor, good experience",
                "Clean clinic, modern equipment",
                "Affordable treatment, recommend",
                "Prompt service, no waiting",
                "Experienced doctor, painless procedure"
            ]
            feedback = random.choice(feedback_options)
            
            cursor.execute("""
                INSERT INTO patient_analytics (
                    clinic_id, patient_id, visit_date, symptoms, diagnosis, 
                    treatment_given, treatment_cost, recovery_days, satisfaction_rating,
                    doctor_assigned, consultation_time, payment_mode, insurance_claim,
                    follow_up_required, patient_feedback, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clinic_id, patient_id, visit_date.date().isoformat(), symptoms, diagnosis,
                treatment, cost, recovery_days, satisfaction, doctor, consultation_time,
                payment_mode, insurance_claim, follow_up, feedback, reg_date.isoformat()
            ))
            
            print(f"✅ Added patient: {name} with analytics data")
            
        except sqlite3.IntegrityError:
            print(f"⚠️ Patient {name} already exists, skipping...")
            continue
    
    conn.commit()
    conn.close()
    print(f"🎉 Sample data seeding completed! Added analytics for comprehensive reporting.")

if __name__ == "__main__":
    seed_sample_data()

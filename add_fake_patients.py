import sqlite3
import random
from datetime import datetime, timedelta

# Sample data for generating fake patients
FIRST_NAMES = [
    "Rahul", "Priya", "Amit", "Sunita", "Vikash", "Anita", "Rajesh", "Meera", 
    "Sunil", "Kavita", "Manoj", "Pooja", "Deepak", "Ritu", "Sanjay", "Neha",
    "Arun", "Geeta", "Vinod", "Shanti", "Ramesh", "Usha", "Mohan", "Lata",
    "Ajay", "Seema", "Pankaj", "Asha", "Ravi", "Sudha"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Jain", "Agarwal", "Mishra",
    "Tiwari", "Yadav", "Pandey", "Srivastava", "Shukla", "Tripathi", "Dubey",
    "Chandra", "Pathak", "Saxena", "Khanna", "Malhotra"
]

TREATMENTS = [
    "General Checkup", "Teeth Cleaning", "Filling", "Root Canal", "Extraction",
    "Orthodontics", "Crowns & Bridges", "Dental Implants", "Whitening", "Emergency"
]

CONDITIONS = [
    "Dental Caries", "Gingivitis", "Periodontitis", "Tooth Sensitivity", "Bad Breath",
    "Tooth Decay", "Gum Disease", "Tooth Pain", "Cavity", "Plaque Buildup"
]

SYMPTOMS = [
    "Tooth pain", "Swollen gums", "Bleeding gums", "Bad breath", "Tooth sensitivity",
    "Jaw pain", "Broken tooth", "Loose tooth", "Gum recession", "White spots on teeth"
]

DOCTORS = ["Dr. Sharma", "Dr. Patel", "Dr. Singh", "Dr. Gupta", "Dr. Verma"]
PAYMENT_MODES = ["Cash", "Card", "UPI", "Insurance"]
FEEDBACK = [
    "Excellent service", "Very satisfied", "Good treatment", "Professional care",
    "Quick recovery", "Friendly staff", "Clean facility", "Affordable treatment"
]

def generate_fake_patients(clinic_id=3, num_patients=25):
    """Generate fake patient data for testing analytics"""
    
    conn = sqlite3.connect('simple_clinic.db')
    cursor = conn.cursor()
    
    # Get clinic info
    cursor.execute("SELECT clinic_code, name FROM clinics WHERE id = ?", (clinic_id,))
    clinic_info = cursor.fetchone()
    if not clinic_info:
        print(f"❌ Clinic with ID {clinic_id} not found!")
        return
    
    clinic_code, clinic_name = clinic_info
    print(f"🏥 Adding {num_patients} fake patients to {clinic_name} ({clinic_code})")
    
    # Get current patient count for this clinic
    cursor.execute("SELECT COUNT(*) FROM patients WHERE clinic_id = ?", (clinic_id,))
    current_count = cursor.fetchone()[0]
    
    patients_added = 0
    analytics_added = 0
    
    for i in range(num_patients):
        try:
            # Generate patient details
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            name = f"{first_name} {last_name}"
            
            sex = random.choice(["Male", "Female"])
            age = random.randint(18, 75)
            mobile = f"98{random.randint(10000000, 99999999)}"
            treatment = random.choice(TREATMENTS)
            
            # Generate patient code
            patient_num = current_count + i + 1
            patient_code = f"{clinic_code}-P{patient_num:04d}"
            
            # Insert patient
            cursor.execute("""
                INSERT INTO patients (clinic_id, patient_code, name, sex, age, treatment, mobile)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (clinic_id, patient_code, name, sex, age, treatment, mobile))
            
            patient_id = cursor.lastrowid
            patients_added += 1
            
            # Add analytics data for this patient
            try:
                # Generate visit date (last 6 months)
                days_ago = random.randint(1, 180)
                visit_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                
                # Generate comprehensive analytics data
                symptoms = random.choice(SYMPTOMS)
                diagnosis = random.choice(CONDITIONS)
                treatment_given = treatment
                treatment_cost = random.randint(500, 5000)
                recovery_days = random.randint(1, 14)
                satisfaction_rating = random.randint(3, 5)  # Most patients satisfied
                doctor_assigned = random.choice(DOCTORS)
                consultation_time = random.randint(15, 60)  # minutes
                payment_mode = random.choice(PAYMENT_MODES)
                insurance_claim = random.randint(0, 2000) if random.random() > 0.7 else 0
                follow_up_required = random.choice(["Yes", "No"])
                patient_feedback = random.choice(FEEDBACK)
                created_at = visit_date
                
                cursor.execute("""
                    INSERT INTO patient_analytics 
                    (clinic_id, patient_id, visit_date, symptoms, diagnosis, treatment_given, 
                     treatment_cost, recovery_days, satisfaction_rating, doctor_assigned, 
                     consultation_time, payment_mode, insurance_claim, follow_up_required, 
                     patient_feedback, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (clinic_id, patient_id, visit_date, symptoms, diagnosis, treatment_given,
                      treatment_cost, recovery_days, satisfaction_rating, doctor_assigned,
                      consultation_time, payment_mode, insurance_claim, follow_up_required,
                      patient_feedback, created_at))
                
                analytics_added += 1
                
            except Exception as e:
                print(f"⚠️ Analytics error for patient {name}: {e}")
            
        except Exception as e:
            print(f"❌ Error adding patient {i+1}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully added:")
    print(f"   📊 {patients_added} patients")
    print(f"   📈 {analytics_added} analytics records")
    print(f"🎯 Ready to test analytics for {clinic_name}!")

if __name__ == "__main__":
    generate_fake_patients(clinic_id=3, num_patients=25)

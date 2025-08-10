# enhanced_fake_data.py - Generate comprehensive fake data for all analytics features

import sqlite3
import random
from datetime import datetime, timedelta

def generate_comprehensive_fake_data():
    """Generate comprehensive fake data for advanced analytics testing"""
    
    DATABASE = "simple_clinic.db"
    
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
    
    symptoms = [
        "Toothache", "Bleeding gums", "Tooth sensitivity", "Bad breath", "Jaw pain",
        "Broken tooth", "Loose tooth", "Swollen gums", "Difficulty chewing", "Tooth discoloration"
    ]
    
    diagnoses = [
        "Dental Caries", "Gingivitis", "Periodontitis", "Pulpitis", "Tooth Abscess",
        "Malocclusion", "Tooth Fracture", "Enamel Erosion", "TMJ Disorder", "Oral Thrush"
    ]
    
    doctors = [
        "Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis", "Dr. Miller"
    ]
    
    payment_modes = ["Cash", "Card", "UPI", "Insurance", "EMI"]
    complexities = ["Simple", "Standard", "Complex", "Highly Complex"]
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    print("🚀 Generating comprehensive fake data for advanced analytics...")
    
    # Clear existing data for USER003
    cursor.execute("SELECT id FROM clinics WHERE clinic_code = 'USER003'")
    clinic_result = cursor.fetchone()
    if clinic_result:
        clinic_id = clinic_result[0]
        print(f"Found clinic USER003 with ID: {clinic_id}")
        
        # Generate 30 enhanced patients
        for i in range(30):
            name = random.choice(indian_names)
            sex = random.choice(["Male", "Female"])
            age = random.randint(18, 75)
            dob = (datetime.now() - timedelta(days=age*365 + random.randint(0, 365))).strftime("%Y-%m-%d")
            mobile = f"9{random.randint(100000000, 999999999)}"
            email = f"{name.lower().replace(' ', '.')}@email.com"
            address = f"{random.randint(1, 999)} {random.choice(['MG Road', 'Park Street', 'Mall Road', 'Station Road'])}, {random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'])}"
            emergency_contact = f"Emergency: 9{random.randint(100000000, 999999999)}"
            medical_history = random.choice(["None", "Diabetes", "Hypertension", "Asthma", "Heart Disease", "None"])
            allergies = random.choice(["None", "Penicillin", "Latex", "Lidocaine", "None", "None"])
            insurance_provider = random.choice(["Star Health", "HDFC ERGO", "ICICI Lombard", "None", "None"])
            insurance_number = f"INS{random.randint(100000, 999999)}" if insurance_provider != "None" else ""
            preferred_doctor = random.choice(doctors)
            referred_by = random.choice(["Friend", "Google", "Social Media", "Doctor Referral", "Walk-in"])
            occupation = random.choice(["Engineer", "Doctor", "Teacher", "Businessman", "Homemaker", "Student", "Retired"])
            treatment = random.choice(treatments)
            
            # Calculate dates
            created_date = (datetime.now() - timedelta(days=i*2)).strftime('%Y-%m-%d %H:%M:%S')
            total_visits = random.randint(1, 8)
            total_spent = random.randint(500, 25000)
            
            # Insert enhanced patient
            cursor.execute("""
                INSERT INTO patients (
                    clinic_id, patient_code, name, sex, age, dob, mobile, email, address,
                    emergency_contact, medical_history, allergies, insurance_provider,
                    insurance_number, preferred_doctor, referred_by, occupation, treatment,
                    created_at, total_visits, total_spent, risk_level, loyalty_points
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clinic_id, f"USER003-P{i+1:04d}", name, sex, age, dob, mobile, email, address,
                emergency_contact, medical_history, allergies, insurance_provider,
                insurance_number, preferred_doctor, referred_by, occupation, treatment,
                created_date, total_visits, total_spent, 
                random.choice(["Low", "Medium", "High"]), random.randint(0, 1000)
            ))
            
            patient_id = cursor.lastrowid
            
            # Generate multiple visits for each patient
            for visit in range(total_visits):
                visit_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
                symptom = random.choice(symptoms)
                diagnosis = random.choice(diagnoses)
                treatment_given = random.choice(treatments)
                treatment_cost = random.randint(200, 5000)
                recovery_days = random.randint(1, 30)
                satisfaction_rating = random.randint(3, 5)
                doctor_assigned = random.choice(doctors)
                consultation_time = random.randint(15, 90)
                payment_mode = random.choice(payment_modes)
                insurance_claim = random.randint(0, treatment_cost) if insurance_provider != "None" else 0
                follow_up = random.choice(["None", "1 week", "2 weeks", "1 month"])
                patient_feedback = random.choice([
                    "Very satisfied with treatment", "Good service", "Excellent care",
                    "Professional staff", "Clean facility", "Reasonable pricing"
                ])
                success_rate = random.randint(85, 100)
                pain_before = random.randint(1, 10)
                pain_after = random.randint(0, 3)
                medication = random.choice(["Antibiotics", "Painkillers", "Antiseptic", "None"])
                side_effects = random.choice(["None", "Mild swelling", "Temporary sensitivity", "None"])
                complexity = random.choice(complexities)
                referral_required = random.choice([0, 0, 0, 1])
                
                # Insert patient analytics
                cursor.execute("""
                    INSERT INTO patient_analytics (
                        clinic_id, patient_id, visit_date, symptoms, diagnosis, treatment_given,
                        treatment_cost, recovery_days, satisfaction_rating, doctor_assigned,
                        consultation_time, payment_mode, insurance_claim, follow_up_required,
                        patient_feedback, treatment_success_rate, pain_level_before, pain_level_after,
                        medication_prescribed, side_effects, treatment_complexity, referral_required
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    clinic_id, patient_id, visit_date, symptom, diagnosis, treatment_given,
                    treatment_cost, recovery_days, satisfaction_rating, doctor_assigned,
                    consultation_time, payment_mode, insurance_claim, follow_up,
                    patient_feedback, success_rate, pain_before, pain_after,
                    medication, side_effects, complexity, referral_required
                ))
                
                # Insert revenue analytics
                cursor.execute("""
                    INSERT INTO revenue_analytics (
                        clinic_id, transaction_date, patient_id, service_type,
                        base_amount, discount_amount, tax_amount, final_amount,
                        payment_method, payment_status, insurance_coverage, outstanding_amount
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    clinic_id, visit_date, patient_id, treatment_given,
                    treatment_cost, random.randint(0, treatment_cost//10), treatment_cost*0.18,
                    treatment_cost, payment_mode, "Completed", insurance_claim, 0
                ))
        
        # Generate doctor performance data
        for doctor in doctors:
            patients_treated = random.randint(50, 200)
            avg_treatment_time = random.randint(25, 60)
            success_rate = random.randint(85, 98)
            patient_satisfaction = random.uniform(4.0, 5.0)
            revenue_generated = random.randint(50000, 300000)
            appointments_completed = random.randint(40, 180)
            no_shows = random.randint(5, 25)
            cancellations = random.randint(3, 20)
            efficiency_score = random.randint(80, 95)
            month_year = datetime.now().strftime("%Y-%m")
            
            cursor.execute("""
                INSERT INTO doctor_performance (
                    clinic_id, doctor_name, specialization, patients_treated,
                    average_treatment_time, success_rate, patient_satisfaction,
                    revenue_generated, appointments_completed, no_shows, cancellations,
                    efficiency_score, month_year
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clinic_id, doctor, "General Dentistry", patients_treated,
                avg_treatment_time, success_rate, patient_satisfaction,
                revenue_generated, appointments_completed, no_shows, cancellations,
                efficiency_score, month_year
            ))
        
        # Generate appointment data
        for i in range(100):
            patient_id = random.randint(1, 30)  # Assuming we have 30 patients
            appointment_date = (datetime.now() + timedelta(days=random.randint(-30, 60))).strftime('%Y-%m-%d')
            appointment_time = f"{random.randint(9, 17)}:{random.choice(['00', '30'])}"
            doctor_name = random.choice(doctors)
            treatment_type = random.choice(treatments)
            status = random.choice(["Completed", "Scheduled", "Cancelled", "No-show"])
            estimated_duration = random.randint(20, 90)
            actual_duration = estimated_duration + random.randint(-10, 20) if status == "Completed" else None
            no_show = 1 if status == "No-show" else 0
            
            cursor.execute("""
                INSERT INTO appointments (
                    clinic_id, patient_id, doctor_name, appointment_date, appointment_time,
                    treatment_type, status, estimated_duration, actual_duration, no_show
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clinic_id, patient_id, doctor_name, appointment_date, appointment_time,
                treatment_type, status, estimated_duration, actual_duration, no_show
            ))
        
        # Generate patient feedback
        for i in range(50):
            patient_id = random.randint(1, 30)
            feedback_type = random.choice(["Treatment", "Service", "Facility", "Overall"])
            rating = random.randint(3, 5)
            review_text = random.choice([
                "Excellent service and professional staff",
                "Very clean and modern facility",
                "Doctor was very patient and explained everything",
                "Quick and painless treatment",
                "Reasonable pricing and good quality",
                "Friendly staff and comfortable environment"
            ])
            sentiment_score = random.uniform(0.6, 1.0)
            would_recommend = random.choice([1, 1, 1, 0])
            feedback_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
            
            cursor.execute("""
                INSERT INTO patient_feedback (
                    clinic_id, patient_id, feedback_type, rating, review_text,
                    sentiment_score, would_recommend, feedback_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clinic_id, patient_id, feedback_type, rating, review_text,
                sentiment_score, would_recommend, feedback_date
            ))
        
        # Generate smart alerts
        alerts = [
            ("Revenue Alert", "Monthly revenue target achieved", "Medium"),
            ("Patient Alert", "High number of no-shows this week", "High"),
            ("Inventory Alert", "Low stock of dental supplies", "Medium"),
            ("Appointment Alert", "Upcoming busy schedule", "Low"),
            ("Feedback Alert", "New patient reviews available", "Low")
        ]
        
        for alert_type, message, severity in alerts:
            cursor.execute("""
                INSERT INTO smart_alerts (
                    clinic_id, alert_type, alert_message, severity, is_read, action_required
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (clinic_id, alert_type, message, severity, 0, 1 if severity == "High" else 0))
        
        conn.commit()
        print("✅ Successfully generated comprehensive fake data!")
        print(f"   - 30 enhanced patients with full profiles")
        print(f"   - {len(doctors)} doctor performance records")
        print(f"   - 100 appointment records")
        print(f"   - 50 patient feedback entries")
        print(f"   - {len(alerts)} smart alerts")
        print(f"   - Complete revenue analytics")
        print(f"   - Full treatment and diagnosis patterns")
        
    else:
        print("❌ Clinic USER003 not found!")
    
    conn.close()

if __name__ == "__main__":
    generate_comprehensive_fake_data()

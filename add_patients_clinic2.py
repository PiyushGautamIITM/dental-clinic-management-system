import sqlite3
import random
from datetime import datetime, timedelta

DATABASE = 'dental_clinic.db'
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

print('🏥 Adding 50 fake patients to Clinic 2...')

# Use clinic ID 2 (the one you're accessing)
clinic_id = 2

# Clear existing data in clinic 2
cursor.execute('DELETE FROM patients WHERE clinic_id = 2')

# Generate 50 patients for clinic 2
first_names = ['Rajesh', 'Priya', 'Amit', 'Neha', 'Suresh', 'Kavya', 'Rohit', 'Sneha', 'Vikram', 'Pooja', 'Arjun', 'Riya', 'Karan', 'Anita', 'Sanjay']
last_names = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Shah', 'Yadav', 'Jain', 'Agarwal', 'Verma']
villages_towns = ['Anandpur', 'Bhojpur', 'Chandanpur', 'Dharampur', 'Fatehpur', 'Ganeshpur', 'Haripur', 'Islampur', 'Janakpur', 'Krishnanagar']
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal', 'Telangana', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Madhya Pradesh']
treatments = ['General Checkup', 'Teeth Cleaning', 'Root Canal', 'Dental Filling', 'Tooth Extraction', 'Teeth Whitening', 'Dental Implant']

for i in range(50):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    name = f'{first_name} {last_name} {i+1}'
    
    date_str = datetime.now().strftime('%Y%m%d')
    patient_code = f'C2P{date_str}{i+1:03d}'  # C2P for Clinic 2 Patient
    age = random.randint(18, 75)
    sex = random.choice(['Male', 'Female'])
    phone = f'+91-{random.randint(7000000000, 9999999999)}'
    email = 'piyushgautam8439@gmail.com'
    village_town = random.choice(villages_towns)
    city = random.choice(cities)
    state = random.choice(states)
    treatment = random.choice(treatments)
    
    # Insert patient into clinic 2
    cursor.execute('''INSERT INTO patients (
        clinic_id, patient_code, name, age, sex, phone, treatment, email, 
        village_town, city, state, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (clinic_id, patient_code, name, age, sex, phone, treatment, email,
                  village_town, city, state, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

conn.commit()

# Verify the count
cursor.execute('SELECT COUNT(*) FROM patients WHERE clinic_id = 2')
count = cursor.fetchone()[0]
print(f'✅ Successfully added {count} patients to Clinic 2!')

# Show first 5 patients
cursor.execute('SELECT patient_code, name, email, village_town, city, state FROM patients WHERE clinic_id = 2 LIMIT 5')
patients = cursor.fetchall()
print('\n👥 First 5 patients in Clinic 2:')
for patient in patients:
    print(f'   • {patient[1]} | Code: {patient[0]} | Email: {patient[2]}')
    print(f'     Location: {patient[3]}, {patient[4]}, {patient[5]}')

conn.close()
print('\n🎯 Now refresh your browser to see all 50 patients!')

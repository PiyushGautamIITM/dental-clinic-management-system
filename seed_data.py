# seed_data.py
import random
from faker import Faker
from app import create_app, db
from app.models import Clinic, Patient
from werkzeug.security import generate_password_hash

fake = Faker()
app = create_app()

def seed(clinics=5, patients_per_clinic=200):
    with app.app_context():
        # optional: wipe data
        # db.drop_all(); db.create_all()
        for i in range(clinics):
            name = fake.company()[:30]
            loc = f"{fake.city()}, {fake.country()}"
            incharge = fake.name()
            login_id = (''.join([c for c in name.upper() if c.isalpha()])[:4] or "CL") + f"{i+1:03d}"
            clinic_code = f"CLINIC{i+1:04d}"
            password = "pass123"  # for seeded clinics
            clinic = Clinic(clinic_code=clinic_code, name=name, location=loc, incharge=incharge, login_id=login_id, password_hash=generate_password_hash(password))
            db.session.add(clinic)
            db.session.commit()
            for j in range(patients_per_clinic):
                pcode = f"{clinic_code}-P{j+1:04d}"
                dob = fake.date_of_birth(minimum_age=5, maximum_age=80)
                age = (fake.date_time_this_year().year - dob.year)
                treat = random.choice(["Cleaning","Filling","Root Canal","Extraction","Orthodontics","Checkup"])
                p = Patient(patient_code=pcode, clinic_id=clinic.id, name=fake.name(), sex=random.choice(["Male","Female"]), dob=dob, age=age, treatment_type=treat, mobile_number=fake.phone_number())
                db.session.add(p)
            db.session.commit()
        print("Seeding complete.")

if __name__ == "__main__":
    seed(clinics=5, patients_per_clinic=200)

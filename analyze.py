# analyze.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB = "dental.db"

def load_tables():
    conn = sqlite3.connect(DB)
    clinics = pd.read_sql("SELECT id, clinic_code, name, location FROM clinics", conn)
    patients = pd.read_sql("SELECT * FROM patients", conn, parse_dates=['created_at','dob'])
    conn.close()
    return clinics, patients

def top_clinics(patients, clinics, n=10):
    counts = patients.groupby('clinic_id').size().reset_index(name='count').merge(clinics, left_on='clinic_id', right_on='id', how='left')
    top = counts.sort_values('count', ascending=False).head(n)
    top.plot.bar(x='clinic_code', y='count', legend=False)
    plt.title('Top Clinics by Patients')
    plt.tight_layout()
    plt.savefig('top_clinics.png')
    print("Saved top_clinics.png")

def treatment_distribution(patients):
    t = patients['treatment_type'].value_counts()
    t.plot.pie(autopct='%1.1f%%')
    plt.title('Treatment distribution')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('treatment_dist.png')
    print("Saved treatment_dist.png")

def age_hist(patients):
    patients['age'] = pd.to_numeric(patients['age'], errors='coerce')
    patients['age'].dropna().plot.hist(bins=12)
    plt.title('Age distribution')
    plt.xlabel('Age')
    plt.tight_layout()
    plt.savefig('age_dist.png')
    print("Saved age_dist.png")

if __name__ == "__main__":
    clinics, patients = load_tables()
    if patients.empty:
        print("No patients found. Run seed_data.py or add patients.")
    else:
        top_clinics(patients, clinics)
        treatment_distribution(patients)
        age_hist(patients)
        print("Analysis done. Check PNG files.")

from flask import request, redirect
from enhanced_app import app, DATABASE
import sqlite3
from datetime import datetime

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
            
            # Combine address fields
            village_town = request.form.get("village_town", "")
            city = request.form.get("city", "")
            state = request.form.get("state", "")
            pincode = request.form.get("pincode", "")
            address = f"{village_town}, {city}, {state}, India - {pincode}".strip(", ")
            
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
            doctor_assigned = request.form.get("doctor_assigned", "Dr. Smith")
            
            if treatment_cost:
                cursor.execute("""INSERT INTO patient_analytics (
                    clinic_id, patient_id, visit_date, diagnosis, treatment_cost,
                    satisfaction_rating, doctor_assigned
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                             (clinic_id, patient_id, datetime.now().strftime('%Y-%m-%d'),
                              treatment, float(treatment_cost), 5, doctor_assigned))
            
            # Add revenue analytics
            if treatment_cost:
                cursor.execute("""INSERT INTO revenue_analytics (
                    clinic_id, date, total_revenue, patients_treated, average_cost_per_patient
                ) VALUES (?, ?, ?, ?, ?)""",
                             (clinic_id, datetime.now().strftime('%Y-%m-%d'),
                              float(treatment_cost), 1, float(treatment_cost)))
            
            # Add doctor performance analytics
            if treatment_cost and doctor_assigned:
                cursor.execute("""INSERT INTO doctor_performance (
                    clinic_id, doctor_name, date, patients_treated, revenue_generated,
                    average_rating, procedures_completed
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                             (clinic_id, doctor_assigned, datetime.now().strftime('%Y-%m-%d'),
                              1, float(treatment_cost), 5.0, 1))
            
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
            .btn {{ padding: 12px 25px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin-right: 10px; text-decoration: none; display: inline-block; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-secondary {{ background: #6c757d; color: white; }}
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
                </div>

                <div class="form-section">
                    <h3>📞 Contact Information</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="phone">📞 Phone:</label>
                            <input type="tel" id="phone" name="phone">
                        </div>
                        <div class="form-group">
                            <label for="email">📧 Email:</label>
                            <input type="email" id="email" name="email" value="piyushgautam8439@gmail.com">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="village_town">🏘️ Village/Town:</label>
                            <input type="text" id="village_town" name="village_town" placeholder="Enter village or town">
                        </div>
                        <div class="form-group">
                            <label for="city">�️ City:</label>
                            <input type="text" id="city" name="city" placeholder="Enter city">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="state">🗺️ State:</label>
                            <select id="state" name="state">
                                <option value="">Select State</option>
                                <option value="Bihar">Bihar</option>
                                <option value="Jharkhand">Jharkhand</option>
                                <option value="West Bengal">West Bengal</option>
                                <option value="Uttar Pradesh">Uttar Pradesh</option>
                                <option value="Odisha">Odisha</option>
                                <option value="Maharashtra">Maharashtra</option>
                                <option value="Karnataka">Karnataka</option>
                                <option value="Tamil Nadu">Tamil Nadu</option>
                                <option value="Gujarat">Gujarat</option>
                                <option value="Rajasthan">Rajasthan</option>
                                <option value="Madhya Pradesh">Madhya Pradesh</option>
                                <option value="Punjab">Punjab</option>
                                <option value="Haryana">Haryana</option>
                                <option value="Delhi">Delhi</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="pincode">📮 Pincode:</label>
                            <input type="text" id="pincode" name="pincode" placeholder="Enter pincode" pattern="[0-9]{6}" maxlength="6">
                        </div>
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
                            <label for="emergency_contact_phone">📞 Emergency Phone:</label>
                            <input type="tel" id="emergency_contact_phone" name="emergency_contact_phone">
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🏥 Medical History</h3>
                    <div class="form-group">
                        <label for="medical_history">📋 Medical History:</label>
                        <textarea id="medical_history" name="medical_history" rows="3" placeholder="Previous medical conditions, surgeries, etc."></textarea>
                    </div>
                    <div class="form-group">
                        <label for="current_medications">💊 Current Medications:</label>
                        <textarea id="current_medications" name="current_medications" rows="2" placeholder="List current medications"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="allergies">⚠️ Allergies:</label>
                        <textarea id="allergies" name="allergies" rows="2" placeholder="Food, drug, or other allergies"></textarea>
                    </div>
                </div>

                <div class="form-section">
                    <h3>💼 Insurance Information</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="insurance_provider">🏢 Insurance Provider:</label>
                            <input type="text" id="insurance_provider" name="insurance_provider">
                        </div>
                        <div class="form-group">
                            <label for="insurance_number">🔢 Insurance Number:</label>
                            <input type="text" id="insurance_number" name="insurance_number">
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🦷 Dental Information</h3>
                    <div class="form-group">
                        <label for="treatment">🦷 Treatment Plan:</label>
                        <input type="text" id="treatment" name="treatment">
                    </div>
                    <div class="form-group">
                        <label for="previous_dental_work">🔧 Previous Dental Work:</label>
                        <textarea id="previous_dental_work" name="previous_dental_work" rows="2" placeholder="Previous treatments, procedures"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="chief_complaint">💬 Chief Complaint:</label>
                        <textarea id="chief_complaint" name="chief_complaint" rows="2" placeholder="Main reason for visit"></textarea>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="pain_level">😰 Pain Level (1-10):</label>
                            <select id="pain_level" name="pain_level">
                                <option value="">Select Pain Level</option>
                                <option value="1">1 - No Pain</option>
                                <option value="2">2 - Very Mild</option>
                                <option value="3">3 - Mild</option>
                                <option value="4">4 - Moderate</option>
                                <option value="5">5 - Moderate</option>
                                <option value="6">6 - Moderately Severe</option>
                                <option value="7">7 - Severe</option>
                                <option value="8">8 - Very Severe</option>
                                <option value="9">9 - Extremely Severe</option>
                                <option value="10">10 - Worst Possible</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="last_cleaning_date">🧽 Last Cleaning Date:</label>
                            <input type="date" id="last_cleaning_date" name="last_cleaning_date">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="preferred_appointment_time">⏰ Preferred Appointment Time:</label>
                        <select id="preferred_appointment_time" name="preferred_appointment_time">
                            <option value="">Select Preferred Time</option>
                            <option value="Morning (8-12)">Morning (8-12)</option>
                            <option value="Afternoon (12-17)">Afternoon (12-17)</option>
                            <option value="Evening (17-20)">Evening (17-20)</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>💰 Payment Information</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="treatment_cost">💵 Treatment Cost (₹):</label>
                            <input type="number" id="treatment_cost" name="treatment_cost" min="0" step="0.01" placeholder="Enter cost">
                        </div>
                        <div class="form-group">
                            <label for="doctor_assigned">👨‍⚕️ Doctor Assigned:</label>
                            <select id="doctor_assigned" name="doctor_assigned">
                                <option value="">Select Doctor</option>
                                <option value="Dr. Smith">Dr. Smith</option>
                                <option value="Dr. Johnson">Dr. Johnson</option>
                                <option value="Dr. Williams">Dr. Williams</option>
                                <option value="Dr. Brown">Dr. Brown</option>
                                <option value="Dr. Davis">Dr. Davis</option>
                            </select>
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
                .btn-edit {{ padding: 5px 10px; background: #28a745; color: white; text-decoration: none; border-radius: 3px; margin: 2px; display: inline-block; font-size: 12px; }}
                .btn-view {{ padding: 5px 10px; background: #17a2b8; color: white; text-decoration: none; border-radius: 3px; margin: 2px; display: inline-block; font-size: 12px; }}
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
                        {patients_html if patients_html else "<tr><td colspan='8' style='text-align: center; color: #666;'>No patients found.</td></tr>"}
                    </tbody>
                </table>
                <div style="text-align: center; margin-top: 20px;">
                    <a href="/search_patients?clinic_id={clinic_id}" class="btn">🔍 Search Patients</a>
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
                <h3>🔍 Search Results for "{search_query}" ({len(patients)} found):</h3>
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
                results_section = f'<div style="text-align: center; color: #666; padding: 20px; background: #f8f9fa; border-radius: 10px; margin: 20px 0;">No patients found matching "{search_query}"</div>'
        
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
            .form-row {{ display: grid; grid-template-columns: 2fr 1fr auto; gap: 15px; align-items: end; }}
            .form-group {{ margin-bottom: 15px; }}
            .form-group label {{ display: block; margin-bottom: 5px; color: #495057; font-weight: bold; }}
            .form-group input, .form-group select {{ width: 100%; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px; font-size: 14px; }}
            .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .table th, .table td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
            .table th {{ background: #007bff; color: white; }}
            .table tr:nth-child(even) {{ background: #f8f9fa; }}
            .btn {{ padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; border: none; cursor: pointer; }}
            .btn-search {{ background: #28a745; }}
            .btn-edit {{ padding: 5px 10px; background: #28a745; color: white; text-decoration: none; border-radius: 3px; margin: 2px; display: inline-block; font-size: 12px; }}
            .btn-view {{ padding: 5px 10px; background: #17a2b8; color: white; text-decoration: none; border-radius: 3px; margin: 2px; display: inline-block; font-size: 12px; }}
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

@app.route("/edit_patient", methods=["GET", "POST"])
def edit_patient():
    clinic_id = request.args.get("clinic_id")
    patient_code = request.args.get("patient_code")
    
    if not clinic_id or not patient_code:
        return redirect("/")
    
    if request.method == "POST":
        try:
            # Update patient data with all fields
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
        
        return f'''
        <html>
        <head>
            <title>Edit Patient - {patient_code}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                .patient-header {{ background: #007bff; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
                .form-group {{ margin-bottom: 15px; }}
                .form-group label {{ display: block; margin-bottom: 5px; color: #495057; font-weight: bold; }}
                .form-group input, .form-group select {{ width: 100%; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px; font-size: 14px; }}
                .btn {{ padding: 12px 25px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin-right: 10px; text-decoration: none; display: inline-block; }}
                .btn-primary {{ background: #007bff; color: white; }}
                .btn-secondary {{ background: #6c757d; color: white; }}
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
                                <input type="text" id="name" name="name" value="{patient[3] or ''}" required>
                            </div>
                            <div class="form-group">
                                <label for="age">🎂 Age:</label>
                                <input type="number" id="age" name="age" value="{patient[4] or ''}" min="1" max="120">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="sex">👫 Gender:</label>
                                <select id="sex" name="sex">
                                    <option value="">Select Gender</option>
                                    <option value="Male" {'selected' if patient[5] == 'Male' else ''}>Male</option>
                                    <option value="Female" {'selected' if patient[5] == 'Female' else ''}>Female</option>
                                    <option value="Other" {'selected' if patient[5] == 'Other' else ''}>Other</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="dob">📅 Date of Birth:</label>
                                <input type="date" id="dob" name="dob" value="{patient[8] or ''}">
                            </div>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3>📞 Contact Information</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="phone">📞 Phone:</label>
                                <input type="tel" id="phone" name="phone" value="{patient[6] or ''}">
                            </div>
                            <div class="form-group">
                                <label for="email">📧 Email:</label>
                                <input type="email" id="email" name="email" value="{patient[10] or ''}">
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="address">🏠 Address:</label>
                            <textarea id="address" name="address" rows="2">{patient[11] or ''}</textarea>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3>🚨 Emergency Contact</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="emergency_contact_name">👤 Emergency Contact Name:</label>
                                <input type="text" id="emergency_contact_name" name="emergency_contact_name" value="{patient[12] or ''}">
                            </div>
                            <div class="form-group">
                                <label for="emergency_contact_phone">📞 Emergency Phone:</label>
                                <input type="tel" id="emergency_contact_phone" name="emergency_contact_phone" value="{patient[13] or ''}">
                            </div>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3>🏥 Medical History</h3>
                        <div class="form-group">
                            <label for="medical_history">📋 Medical History:</label>
                            <textarea id="medical_history" name="medical_history" rows="3">{patient[14] or ''}</textarea>
                        </div>
                        <div class="form-group">
                            <label for="current_medications">💊 Current Medications:</label>
                            <textarea id="current_medications" name="current_medications" rows="2">{patient[15] or ''}</textarea>
                        </div>
                        <div class="form-group">
                            <label for="allergies">⚠️ Allergies:</label>
                            <textarea id="allergies" name="allergies" rows="2">{patient[16] or ''}</textarea>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3>💼 Insurance Information</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="insurance_provider">🏢 Insurance Provider:</label>
                                <input type="text" id="insurance_provider" name="insurance_provider" value="{patient[17] or ''}">
                            </div>
                            <div class="form-group">
                                <label for="insurance_number">🔢 Insurance Number:</label>
                                <input type="text" id="insurance_number" name="insurance_number" value="{patient[18] or ''}">
                            </div>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3>🦷 Dental Information</h3>
                        <div class="form-group">
                            <label for="treatment">🦷 Treatment Plan:</label>
                            <input type="text" id="treatment" name="treatment" value="{patient[7] or ''}">
                        </div>
                        <div class="form-group">
                            <label for="previous_dental_work">🔧 Previous Dental Work:</label>
                            <textarea id="previous_dental_work" name="previous_dental_work" rows="2">{patient[19] or ''}</textarea>
                        </div>
                        <div class="form-group">
                            <label for="chief_complaint">💬 Chief Complaint:</label>
                            <textarea id="chief_complaint" name="chief_complaint" rows="2">{patient[20] or ''}</textarea>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="pain_level">😰 Pain Level (1-10):</label>
                                <select id="pain_level" name="pain_level">
                                    <option value="">Select Pain Level</option>
                                    <option value="1" {'selected' if patient[21] == '1' else ''}>1 - No Pain</option>
                                    <option value="2" {'selected' if patient[21] == '2' else ''}>2 - Very Mild</option>
                                    <option value="3" {'selected' if patient[21] == '3' else ''}>3 - Mild</option>
                                    <option value="4" {'selected' if patient[21] == '4' else ''}>4 - Moderate</option>
                                    <option value="5" {'selected' if patient[21] == '5' else ''}>5 - Moderate</option>
                                    <option value="6" {'selected' if patient[21] == '6' else ''}>6 - Moderately Severe</option>
                                    <option value="7" {'selected' if patient[21] == '7' else ''}>7 - Severe</option>
                                    <option value="8" {'selected' if patient[21] == '8' else ''}>8 - Very Severe</option>
                                    <option value="9" {'selected' if patient[21] == '9' else ''}>9 - Extremely Severe</option>
                                    <option value="10" {'selected' if patient[21] == '10' else ''}>10 - Worst Possible</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="last_cleaning_date">🧽 Last Cleaning Date:</label>
                                <input type="date" id="last_cleaning_date" name="last_cleaning_date" value="{patient[22] or ''}">
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="preferred_appointment_time">⏰ Preferred Appointment Time:</label>
                            <select id="preferred_appointment_time" name="preferred_appointment_time">
                                <option value="">Select Preferred Time</option>
                                <option value="Morning (8-12)" {'selected' if patient[23] == 'Morning (8-12)' else ''}>Morning (8-12)</option>
                                <option value="Afternoon (12-17)" {'selected' if patient[23] == 'Afternoon (12-17)' else ''}>Afternoon (12-17)</option>
                                <option value="Evening (17-20)" {'selected' if patient[23] == 'Evening (17-20)' else ''}>Evening (17-20)</option>
                            </select>
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
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                .patient-header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
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
                        <h3>📋 Contact Information</h3>
                        <div class="info-item"><span class="info-label">Phone:</span> {patient[6] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Email:</span> {patient[10] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Address:</span> {patient[11] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Date of Birth:</span> {patient[8] or 'N/A'}</div>
                    </div>
                    
                    <div class="info-section">
                        <h3>🚨 Emergency Contact</h3>
                        <div class="info-item"><span class="info-label">Name:</span> {patient[12] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Phone:</span> {patient[13] or 'N/A'}</div>
                    </div>
                    
                    <div class="info-section">
                        <h3>🏥 Medical Information</h3>
                        <div class="info-item"><span class="info-label">Medical History:</span> {patient[14] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Current Medications:</span> {patient[15] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Allergies:</span> {patient[16] or 'N/A'}</div>
                    </div>
                    
                    <div class="info-section">
                        <h3>💼 Insurance Information</h3>
                        <div class="info-item"><span class="info-label">Provider:</span> {patient[17] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Number:</span> {patient[18] or 'N/A'}</div>
                    </div>
                    
                    <div class="info-section">
                        <h3>🦷 Dental Information</h3>
                        <div class="info-item"><span class="info-label">Current Treatment:</span> {patient[7] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Previous Work:</span> {patient[19] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Chief Complaint:</span> {patient[20] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Pain Level:</span> {patient[21] or 'N/A'}/10</div>
                        <div class="info-item"><span class="info-label">Last Cleaning:</span> {patient[22] or 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Preferred Time:</span> {patient[23] or 'N/A'}</div>
                    </div>
                    
                    <div class="info-section">
                        <h3>📅 Account Information</h3>
                        <div class="info-item"><span class="info-label">Date Added:</span> {patient[24][:10] if patient[24] else 'N/A'}</div>
                        <div class="info-item"><span class="info-label">Patient Code:</span> {patient[2]}</div>
                    </div>
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

@app.route("/advanced_analytics")
def advanced_analytics():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return "<h3>❌ Error: Invalid clinic access!</h3><a href='/'>← Back to Home</a>"
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get comprehensive stats
        cursor.execute("SELECT COUNT(*) FROM patients WHERE clinic_id = ?", (clinic_id,))
        total_patients = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM patient_analytics WHERE clinic_id = ?", (clinic_id,))
        total_visits = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(treatment_cost) FROM patient_analytics WHERE clinic_id = ?", (clinic_id,))
        total_revenue = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(treatment_cost) FROM patient_analytics WHERE clinic_id = ? AND treatment_cost > 0", (clinic_id,))
        avg_cost = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(satisfaction_rating) FROM patient_analytics WHERE clinic_id = ? AND satisfaction_rating > 0", (clinic_id,))
        avg_rating = cursor.fetchone()[0] or 0
        
        # Get gender distribution
        cursor.execute("SELECT sex, COUNT(*) FROM patients WHERE clinic_id = ? AND sex IS NOT NULL GROUP BY sex", (clinic_id,))
        gender_stats = cursor.fetchall()
        
        # Get age distribution
        cursor.execute("SELECT AVG(age) FROM patients WHERE clinic_id = ? AND age IS NOT NULL", (clinic_id,))
        avg_age = cursor.fetchone()[0] or 0
        
        # Get treatment distribution
        cursor.execute("SELECT treatment, COUNT(*) FROM patients WHERE clinic_id = ? AND treatment IS NOT NULL GROUP BY treatment LIMIT 5", (clinic_id,))
        treatment_stats = cursor.fetchall()
        
        # Get doctor performance
        cursor.execute("SELECT doctor_assigned, COUNT(*), SUM(treatment_cost), AVG(satisfaction_rating) FROM patient_analytics WHERE clinic_id = ? AND doctor_assigned IS NOT NULL GROUP BY doctor_assigned", (clinic_id,))
        doctor_stats = cursor.fetchall()
        
        # Get monthly revenue
        cursor.execute("SELECT strftime('%Y-%m', visit_date) as month, SUM(treatment_cost) FROM patient_analytics WHERE clinic_id = ? AND treatment_cost > 0 GROUP BY month ORDER BY month DESC LIMIT 6", (clinic_id,))
        monthly_revenue = cursor.fetchall()
        
        conn.close()
        
        # Build gender stats HTML
        gender_html = ""
        for gender, count in gender_stats:
            percentage = (count / total_patients * 100) if total_patients > 0 else 0
            gender_html += f'<div class="stat-item">👫 {gender}: {count} ({percentage:.1f}%)</div>'
        
        # Build treatment stats HTML
        treatment_html = ""
        for treatment, count in treatment_stats:
            treatment_html += f'<div class="stat-item">🦷 {treatment}: {count} patients</div>'
        
        # Build doctor stats HTML
        doctor_html = ""
        for doctor, visits, revenue, rating in doctor_stats:
            doctor_html += f'''
            <div class="doctor-card">
                <h4>👨‍⚕️ {doctor}</h4>
                <div>Patients: {visits}</div>
                <div>Revenue: ₹{revenue:.2f}</div>
                <div>Rating: {'⭐' * int(rating or 0)} ({rating:.1f})</div>
            </div>
            '''
        
        # Build monthly revenue HTML
        revenue_html = ""
        for month, revenue in monthly_revenue:
            revenue_html += f'<div class="revenue-item">📅 {month}: ₹{revenue:.2f}</div>'
        
        return f'''
        <html>
        <head>
            <title>Advanced Analytics</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f8ff; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .stat-card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; }}
                .metric-value {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
                .analytics-section {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; }}
                .stat-item {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
                .doctor-card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }}
                .revenue-item {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
                .btn {{ padding: 12px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 8px; margin: 5px; display: inline-block; }}
                .analytics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Advanced Analytics Dashboard</h1>
                    <p>Comprehensive clinic insights and metrics</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="metric-value" style="color: #007bff;">{total_patients}</div>
                        <div>👥 Total Patients</div>
                    </div>
                    <div class="stat-card">
                        <div class="metric-value" style="color: #28a745;">{total_visits}</div>
                        <div>🏥 Total Visits</div>
                    </div>
                    <div class="stat-card">
                        <div class="metric-value" style="color: #ffc107;">₹{total_revenue:.2f}</div>
                        <div>💰 Total Revenue</div>
                    </div>
                    <div class="stat-card">
                        <div class="metric-value" style="color: #17a2b8;">₹{avg_cost:.2f}</div>
                        <div>📊 Average Cost</div>
                    </div>
                    <div class="stat-card">
                        <div class="metric-value" style="color: #dc3545;">{'⭐' * int(avg_rating)}</div>
                        <div>⭐ Average Rating ({avg_rating:.1f})</div>
                    </div>
                    <div class="stat-card">
                        <div class="metric-value" style="color: #6f42c1;">{avg_age:.1f}</div>
                        <div>🎂 Average Age</div>
                    </div>
                </div>
                
                <div class="analytics-grid">
                    <div class="analytics-section">
                        <h3>👫 Gender Distribution</h3>
                        {gender_html if gender_html else '<div class="stat-item">No gender data available</div>'}
                    </div>
                    
                    <div class="analytics-section">
                        <h3>🦷 Popular Treatments</h3>
                        {treatment_html if treatment_html else '<div class="stat-item">No treatment data available</div>'}
                    </div>
                    
                    <div class="analytics-section">
                        <h3>👨‍⚕️ Doctor Performance</h3>
                        {doctor_html if doctor_html else '<div class="stat-item">No doctor data available</div>'}
                    </div>
                    
                    <div class="analytics-section">
                        <h3>📈 Monthly Revenue</h3>
                        {revenue_html if revenue_html else '<div class="revenue-item">No revenue data available</div>'}
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/generate_report?clinic_id={clinic_id}" class="btn">📄 Generate Report</a>
                    <a href="/dashboard?clinic_id={clinic_id}" class="btn">🏠 Back to Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3><a href='/dashboard?clinic_id={clinic_id}'>← Back to Dashboard</a>"

@app.route("/address_analytics")
def address_analytics():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return "<h3>❌ Error: Invalid clinic access!</h3><a href='/'>← Back to Home</a>"
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get all patients with addresses
        cursor.execute("SELECT address FROM patients WHERE clinic_id = ? AND address IS NOT NULL AND address != ''", (clinic_id,))
        addresses = cursor.fetchall()
        
        # Parse addresses to extract city and state
        city_stats = {}
        state_stats = {}
        village_town_stats = {}
        
        for addr_tuple in addresses:
            address = addr_tuple[0]
            if address and ',' in address:
                parts = [part.strip() for part in address.split(',')]
                if len(parts) >= 3:
                    village_town = parts[0]
                    city = parts[1]
                    state_part = parts[2]
                    
                    # Extract state (remove "India" if present)
                    state = state_part.replace('India', '').strip()
                    
                    # Count occurrences
                    village_town_stats[village_town] = village_town_stats.get(village_town, 0) + 1
                    city_stats[city] = city_stats.get(city, 0) + 1
                    state_stats[state] = state_stats.get(state, 0) + 1
        
        # Get top locations
        top_villages = sorted(village_town_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        top_cities = sorted(city_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        top_states = sorted(state_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Get patient analytics by location
        cursor.execute("""
            SELECT p.address, COUNT(*), AVG(pa.treatment_cost), AVG(pa.satisfaction_rating)
            FROM patients p
            LEFT JOIN patient_analytics pa ON p.id = pa.patient_id
            WHERE p.clinic_id = ? AND p.address IS NOT NULL
            GROUP BY p.address
            ORDER BY COUNT(*) DESC
            LIMIT 15
        """, (clinic_id,))
        location_analytics = cursor.fetchall()
        
        conn.close()
        
        # Build HTML for statistics
        village_html = ""
        for village, count in top_villages:
            village_html += f'<div class="location-item">🏘️ {village}: {count} patients</div>'
        
        city_html = ""
        for city, count in top_cities:
            city_html += f'<div class="location-item">🏙️ {city}: {count} patients</div>'
        
        state_html = ""
        for state, count in top_states:
            state_html += f'<div class="location-item">🗺️ {state}: {count} patients</div>'
        
        # Build analytics HTML
        analytics_html = ""
        for location, patient_count, avg_cost, avg_rating in location_analytics:
            location_parts = location.split(',') if location else ['Unknown']
            display_location = location_parts[0] if location_parts else 'Unknown'
            analytics_html += f'''
            <div class="analytics-item">
                <h4>📍 {display_location}</h4>
                <div>👥 Patients: {patient_count}</div>
                <div>💰 Avg Cost: ₹{avg_cost:.2f if avg_cost else 0}</div>
                <div>⭐ Avg Rating: {avg_rating:.1f if avg_rating else 0}/5</div>
            </div>
            '''
        
        return f'''
        <html>
        <head>
            <title>Address Analytics</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f8ff; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; }}
                .analytics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .analytics-section {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                .location-item {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
                .analytics-item {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }}
                .btn {{ padding: 12px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 8px; margin: 5px; display: inline-block; }}
                .stats-overview {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }}
                .stat-card {{ background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                .stat-value {{ font-size: 2em; font-weight: bold; color: #28a745; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📍 Address Analytics Dashboard</h1>
                    <p>Patient distribution and analysis by location</p>
                </div>
                
                <div class="stats-overview">
                    <div class="stat-card">
                        <div class="stat-value">{len(village_town_stats)}</div>
                        <div>🏘️ Villages/Towns</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len(city_stats)}</div>
                        <div>🏙️ Cities</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len(state_stats)}</div>
                        <div>🗺️ States</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len(addresses)}</div>
                        <div>👥 Total Patients</div>
                    </div>
                </div>
                
                <div class="analytics-grid">
                    <div class="analytics-section">
                        <h3>🏘️ Top Villages/Towns</h3>
                        {village_html if village_html else '<div class="location-item">No village/town data available</div>'}
                    </div>
                    
                    <div class="analytics-section">
                        <h3>🏙️ Top Cities</h3>
                        {city_html if city_html else '<div class="location-item">No city data available</div>'}
                    </div>
                    
                    <div class="analytics-section">
                        <h3>🗺️ States Distribution</h3>
                        {state_html if state_html else '<div class="location-item">No state data available</div>'}
                    </div>
                    
                    <div class="analytics-section">
                        <h3>📊 Location Analytics</h3>
                        {analytics_html if analytics_html else '<div class="analytics-item">No analytics data available</div>'}
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/advanced_analytics?clinic_id={clinic_id}" class="btn">📊 Advanced Analytics</a>
                    <a href="/dashboard?clinic_id={clinic_id}" class="btn">🏠 Back to Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3><a href='/dashboard?clinic_id={clinic_id}'>← Back to Dashboard</a>"

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
        clinic_name = clinic_info[0] if clinic_info else "Unknown Clinic"
        
        # Get patient data
        cursor.execute("SELECT patient_code, name, age, sex, phone, treatment, created_at FROM patients WHERE clinic_id = ? ORDER BY created_at DESC", (clinic_id,))
        patients = cursor.fetchall()
        
        conn.close()
        
        report_rows = ""
        for patient in patients:
            report_rows += f'''
            <tr>
                <td>{patient[0]}</td>
                <td>{patient[1]}</td>
                <td>{patient[2] or 'N/A'}</td>
                <td>{patient[3] or 'N/A'}</td>
                <td>{patient[4] or 'N/A'}</td>
                <td>{patient[5] or 'N/A'}</td>
                <td>{patient[6][:10]}</td>
            </tr>
            '''
        
        return f'''
        <html>
        <head>
            <title>Patient Report - {clinic_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .table th, .table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 12px; }}
                .table th {{ background: #007bff; color: white; }}
                .btn {{ padding: 10px 20px; margin: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }}
                @media print {{ .no-print {{ display: none; }} }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📄 Patient Report</h1>
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
                        <th>Phone</th>
                        <th>Treatment</th>
                        <th>Added Date</th>
                    </tr>
                </thead>
                <tbody>
                    {report_rows if report_rows else "<tr><td colspan='7' style='text-align: center; color: #666;'>No patients found.</td></tr>"}
                </tbody>
            </table>
            
            <div class="no-print" style="text-align: center; margin-top: 30px;">
                <button onclick="window.print()" class="btn">🖨️ Print Report</button>
                <a href="/dashboard?clinic_id={clinic_id}" class="btn">🏠 Back to Dashboard</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3><a href='/dashboard?clinic_id={clinic_id}'>← Back to Dashboard</a>"

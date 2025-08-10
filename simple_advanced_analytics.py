# simple_advanced_analytics.py - Simple advanced analytics route

def create_simple_advanced_analytics():
    return '''
@app.route("/advanced_analytics")
def advanced_analytics():
    clinic_id = request.args.get("clinic_id")
    if not clinic_id:
        return "<h3>❌ Error: Invalid clinic access!</h3><a href='/'>← Back to Home</a>"
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get clinic info
        cursor.execute("SELECT name FROM clinics WHERE id = ?", (clinic_id,))
        clinic_info = cursor.fetchone()
        if not clinic_info:
            return "<h3>❌ Error: Clinic not found!</h3><a href='/'>← Back to Home</a>"
        
        clinic_name = clinic_info[0]
        
        # Basic patient stats
        cursor.execute("SELECT COUNT(*) FROM patients WHERE clinic_id = ?", (clinic_id,))
        total_patients = cursor.fetchone()[0]
        
        # Basic analytics stats
        cursor.execute("SELECT COUNT(*) FROM patient_analytics WHERE clinic_id = ?", (clinic_id,))
        total_analytics = cursor.fetchone()[0]
        
        # Revenue stats
        cursor.execute("SELECT SUM(treatment_cost) FROM patient_analytics WHERE clinic_id = ?", (clinic_id,))
        total_revenue = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return f"""
        <html>
        <head>
            <title>Advanced Analytics - {clinic_name}</title>
            <style>
                body {{ font-family: Arial; margin: 20px; background: #f0f8ff; }}
                .analytics-card {{ background: white; padding: 25px; margin: 20px 0; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
                .metric-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                .metric-value {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="analytics-card">
                <h1 style="color: #2c5aa0; text-align: center;">📊 Advanced Analytics Dashboard - {clinic_name}</h1>
                
                <div class="metrics-grid">
                    <div class="metric-box" style="background: linear-gradient(135deg, #28a745, #20c997);">
                        <div class="metric-value">{total_patients}</div>
                        <div>Total Patients</div>
                    </div>
                    <div class="metric-box" style="background: linear-gradient(135deg, #007bff, #6610f2);">
                        <div class="metric-value">{total_analytics}</div>
                        <div>Analytics Records</div>
                    </div>
                    <div class="metric-box" style="background: linear-gradient(135deg, #ffc107, #fd7e14);">
                        <div class="metric-value">₹{total_revenue:,.0f}</div>
                        <div>Total Revenue</div>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <h2 style="color: #2c5aa0;">🚀 Advanced Features Available:</h2>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0;">
                        <div style="background: #e8f4fd; padding: 20px; border-radius: 8px;">
                            <h3>📅 Appointment Analytics</h3>
                            <p>Track booking patterns, no-shows, and optimal scheduling</p>
                        </div>
                        <div style="background: #d4edda; padding: 20px; border-radius: 8px;">
                            <h3>💰 Revenue Analysis</h3>
                            <p>Financial trends, payment modes, and billing insights</p>
                        </div>
                        <div style="background: #fff3cd; padding: 20px; border-radius: 8px;">
                            <h3>👨‍⚕️ Doctor Performance</h3>
                            <p>Treatment success rates, patient satisfaction, efficiency metrics</p>
                        </div>
                        <div style="background: #f8d7da; padding: 20px; border-radius: 8px;">
                            <h3>🔄 Patient Retention</h3>
                            <p>Churn analysis, loyalty tracking, return visit predictions</p>
                        </div>
                        <div style="background: #e2e3f0; padding: 20px; border-radius: 8px;">
                            <h3>🧠 AI Insights</h3>
                            <p>Diagnosis patterns, treatment recommendations, risk predictions</p>
                        </div>
                        <div style="background: #fce4ec; padding: 20px; border-radius: 8px;">
                            <h3>📝 Feedback Analysis</h3>
                            <p>Sentiment analysis from patient reviews and satisfaction surveys</p>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="/add_patient?clinic_id={clinic_id}" style="background: #28a745; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; margin: 10px; font-size: 16px;">➕ Add Patient with Analytics</a>
                    <a href="/view_patients?clinic_id={clinic_id}" style="background: #007bff; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; margin: 10px; font-size: 16px;">👥 View Patients</a>
                    <a href="/analytics?clinic_id={clinic_id}" style="background: #6610f2; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; margin: 10px; font-size: 16px;">📊 Basic Analytics</a>
                    <a href="/dashboard?clinic_id={clinic_id}" style="background: #6c757d; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; margin: 10px; font-size: 16px;">🏠 Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"""
        <html>
        <body style="font-family: Arial; margin: 40px;">
            <div style="background: #f8d7da; padding: 20px; border-radius: 8px; border: 1px solid #f5c6cb;">
                <h3 style="color: #721c24;">❌ Analytics Error</h3>
                <p style="color: #721c24;">Error: {str(e)}</p>
                <a href="/dashboard?clinic_id={clinic_id}" style="background: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">← Back to Dashboard</a>
            </div>
        </body>
        </html>
        """
'''

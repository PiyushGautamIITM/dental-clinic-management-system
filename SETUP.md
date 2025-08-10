# 🚀 Quick Setup Guide

## Local Development Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/yourusername/dental-clinic-management-system.git
cd dental-clinic-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python enhanced_app.py
```

### 5. Access the Application
- **Local URL:** http://127.0.0.1:5000
- **Sample Data:** Run `python add_patients_clinic2.py` for demo patients

## Public Access Setup (Optional)

### Using ngrok for public access:
```bash
pip install pyngrok
python simple_ngrok.py
```

## Default Clinic Credentials
- **Email:** clinic@example.com
- **Password:** password123

## Quick Commands

```bash
# Start the application
python enhanced_app.py

# Add sample data (50 patients)
python add_patients_clinic2.py

# Start with public access
python simple_ngrok.py

# Check database
python -c "import sqlite3; conn = sqlite3.connect('dental_clinic.db'); print('Patients:', conn.execute('SELECT COUNT(*) FROM patients').fetchone()[0]); conn.close()"
```

## Troubleshooting

### Common Issues:
1. **Port already in use**: Change port in enhanced_app.py
2. **Database errors**: Delete .db files and restart
3. **Module not found**: Ensure virtual environment is activated

### Support:
- Create GitHub issue for bugs
- Email: piyushgautam8439@gmail.com

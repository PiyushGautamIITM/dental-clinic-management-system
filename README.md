# Dental Clinic Management System

A comprehensive web-based dental clinic management system built with Flask, featuring patient management, analytics, search functionality, and geographic insights.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![SQLite](https://img.shields.io/badge/sqlite-v3.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

### **Patient Management**
- **Complete Patient Registration** - 25+ comprehensive fields including medical history, insurance details, and emergency contacts
- **Advanced Search & Filter** - Multi-criteria search by name, phone, treatment, location, age, and more
- **Patient Edit & Update** - Full editing capabilities for all patient information
- **Patient Analytics** - Detailed patient insights and treatment history

### **Geographic Analytics**
- **Address-Based Analytics** - Separate fields for Village/Town, City, and State
- **Geographic Distribution** - Visual analysis of patient distribution by location
- **Location-Based Insights** - Understand patient demographics by geography

### **Multi-Clinic Support**
- **Clinic Management** - Support for multiple dental clinics
- **Clinic-Specific Data** - Isolated patient data per clinic
- **User Authentication** - Secure login system for different clinics

### **Analytics & Reporting**
- **Patient Demographics** - Age, gender, and location distribution
- **Treatment Analytics** - Popular treatments and procedures
- **Revenue Insights** - Treatment costs and financial analytics
- **Visit Patterns** - Patient visit frequency and scheduling insights

### **Advanced Search Features**
- **Multi-Field Search** - Search across name, phone, email, treatment, symptoms
- **Location-Based Search** - Filter by village/town, city, or state
- **Date Range Filters** - Search by registration date, visit date, or age range
- **Real-Time Results** - Instant search results with highlighting

##  Quick Start

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/dental-clinic-management-system.git
cd dental-clinic-management-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python enhanced_app.py
```

5. **Access the application**
```
http://127.0.0.1:5000
```

## Usage

### **For Local Development**
```bash
python enhanced_app.py
```

### **For Public Access (with ngrok)**
```bash
python simple_ngrok.py
```

### **Add Sample Data**
```bash
python add_patients_clinic2.py
```

## Project Structure

```
dental-clinic-management-system/
├── enhanced_app.py          # Main Flask application
├── patient_routes.py        # Patient management routes
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── dental_clinic.db        # SQLite database
├── add_patients_clinic2.py # Sample data generator
├── simple_ngrok.py         # Public access setup
└── templates/              # HTML templates (inline)
```

## Database Schema

### **Clinics Table**
- Clinic information and authentication
- Contact details and location

### **Patients Table**
- Comprehensive patient information (25+ fields)
- Medical history and insurance details
- Geographic data (village/town, city, state)
- Emergency contact information

### **Analytics Tables**
- Patient visit history
- Treatment records and costs
- Satisfaction ratings and feedback

## Configuration

### **Environment Variables**
Create a `.env` file:
```env
FLASK_ENV=development
DATABASE_URL=sqlite:///dental_clinic.db
SECRET_KEY=your-secret-key-here
```

### **Database Configuration**
- **Default Database**: `dental_clinic.db` (SQLite)
- **Auto-initialization**: Creates tables on first run
- **Sample Data**: Use `add_patients_clinic2.py` for demo data

## Key Features Breakdown

### **Patient Registration Form**
- Personal Information (Name, Age, Sex, DOB)
- Contact Details (Phone, Email, Address with separate fields)
- Medical Information (History, Medications, Allergies)
- Insurance Information (Provider, Policy Number)
- Emergency Contacts
- Treatment History and Preferences

### **Search Functionality**
- **Quick Search**: Instant patient lookup
- **Advanced Filters**: Multiple criteria selection
- **Geographic Search**: Location-based filtering
- **Export Options**: Search results download

### **Analytics Dashboard**
- **Patient Demographics**: Visual charts and graphs
- **Treatment Statistics**: Popular procedures and costs
- **Geographic Distribution**: Patient location mapping
- **Revenue Analytics**: Financial insights and trends

## Security Features

- **Session Management**: Secure user sessions
- **Data Validation**: Input sanitization and validation
- **Clinic Isolation**: Secure data separation between clinics
- **Error Handling**: Comprehensive error management

## Deployment

### **Local Deployment**
```bash
python enhanced_app.py
```

### **Public Access (ngrok)**
```bash
pip install pyngrok
python simple_ngrok.py
```

### **Production Deployment**
- Use WSGI server like Gunicorn
- Configure environment variables
- Set up proper database (PostgreSQL/MySQL for production)
- Enable HTTPS with SSL certificates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask framework for web development
- SQLite for database management
- Bootstrap for responsive UI design
- Chart.js for analytics visualization

## Support

For support and questions:
- Create an issue on GitHub
- Email: piyushgautam8439@gmail.com

## Future Enhancements

- [ ] **Appointment Scheduling** - Calendar integration
- [ ] **SMS/Email Notifications** - Automated reminders
- [ ] **Payment Integration** - Online payment processing
- [ ] **Mobile App** - React Native companion app
- [ ] **Advanced Analytics** - Machine learning insights
- [ ] **Inventory Management** - Dental supplies tracking
- [ ] **Document Management** - Patient file uploads
- [ ] **Multi-language Support** - Internationalization

---

**Made with ❤️ for dental professionals worldwide**

## Screenshots

### Dashboard Overview
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

### Patient Management
![Patient Management](https://via.placeholder.com/800x400?text=Patient+Management+Screenshot)

### Analytics View
![Analytics](https://via.placeholder.com/800x400?text=Analytics+Screenshot)

---

**Star this repository if you find it helpful!**

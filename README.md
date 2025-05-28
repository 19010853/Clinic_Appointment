# 🏥 Clinic Appointment System with Django

A comprehensive clinic appointment system built with Django, designed to manage patients, doctors, appointments, and medical records efficiently. The system includes secure email notifications and authentication management for patients and doctors.

---

## 📋 Features

- **Authentication Management:**
  - Separate login and registration for patients and doctors
  - Secure and role-based access to the system

- **Patient Management:**
  - Register and manage patient profiles
  - Securely store patient medical records
  - View appointment history and upcoming appointments

- **Doctor Management:**
  - Register and manage doctor profiles and schedules
  - Notifications for new appointments
  - Manage patient appointments and medical records

- **Appointments:**
  - Patients can book appointments with doctors
  - Email notifications sent to both patient and doctor upon appointment confirmation
  - View and manage appointment schedules

- **Lab Tests:**
  - Manage lab test records and results
  - Track patient test history

- **Prescriptions:**
  - Generate and store prescriptions for patients
  - Digital prescription management

- **Admin Panel:**
  - Jazzmin-powered admin interface for managing the system
  - Full control over patients, doctors, appointments, and lab tests

---

## 🛠️ Technologies Used

- **Backend:** Django (Python Framework)
- **Frontend:** HTML, CSS, JavaScript (Django templates)
- **Database:** SQLite (default for development)
- **Email Service:** Brevo (formerly Sendinblue)
- **Notifications:** Email notifications for appointments

---

## 🚀 Installation and Setup

Follow these steps to set up the project locally:

### Prerequisites
1. Install Python
2. Install `pipenv` or `virtualenv`
3. Create a Brevo account for email services

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/19010853/Clinic_Appointment.git
   cd clinic_appointment_system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Configure Brevo Email:**
   - Create a `.env` file in the project root directory
   - Add the following keys to the `.env` file:
     ```
     EMAIL_BACKEND=anymail.backends.sendinblue.EmailBackend
     DEFAULT_FROM_EMAIL= your_brevo_email
     SERVER_EMAIL= your_brevo_email
     BREVO_API_KEY= your_brevo_api_key
     ```
   - Replace the placeholder values with your actual Brevo credentials

6. **Configure Email Templates:**
   - Create email templates in `templates/email/`:
     - `appointment_booked.html` - For appointment confirmation
     - `new_appointment.html` - For new appointment notifications
   - Customize the templates according to your needs

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Open your browser and navigate to `http://127.0.0.1:8000`
   - Use the superuser credentials to log in to the admin panel at `http://127.0.0.1:8000/admin/`

---

## 📧 Email Integration with Brevo

### Setting up Brevo

1. **Create a Brevo Account:**
   - Sign up at [Brevo](https://www.brevo.com)
   - Verify your email address
   - Create an API key in the SMTP & API section

2. **Configure Django Settings:**
   ```python
   # settings.py
   ANYMAIL = {
    "SENDINBLUE_API_KEY": env("BREVO_API_KEY"),
    }

    EMAIL_BACKEND = env('EMAIL_BACKEND')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
    SERVER_EMAIL = env('SERVER_EMAIL')
    BREVO_API_KEY = env('BREVO_API_KEY')
   ```

3. **Create Email Templates:**
   - Use Django templates for email content
   - Include dynamic content like appointment details
   - Style your emails using HTML and CSS

4. **Send Emails:**
   ```python
   from django.core.mail import send_mail
   from django.template.loader import render_to_string
   from django.utils.html import strip_tags

   def send_appointment_confirmation(appointment):
       subject = 'Appointment Confirmation'
       html_message = render_to_string('email/appointment_booked.html', {
           'appointment': appointment,
           'patient': appointment.patient,
           'doctor': appointment.doctor,
       })
       plain_message = strip_tags(html_message)
       
       send_mail(
           subject,
           plain_message,
           'from@yourdomain.com',
           [appointment.patient.email],
           html_message=html_message,
       )
   ```
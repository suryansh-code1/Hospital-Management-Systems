# Hospital Management System

## Short Description

A Flask-based web application that enables hospitals to efficiently manage doctors, patients, and appointments. The system provides role-based access for administrators, doctors, and patients, allowing seamless appointment scheduling, treatment documentation, and hospital resource management.

## Key Features

- **Role-Based Access Control**: Separate dashboards and functionality for Admin, Doctor, and Patient roles
- **Appointment Management**: Patients can book appointments with available doctors; doctors can view and manage their schedule
- **Doctor Management**: Admins can add, edit, and manage doctor profiles with specialization
- **Department/Specialization Management**: Create and organize medical departments
- **Treatment Documentation**: Doctors can record diagnosis, prescriptions, and notes for completed appointments
- **User Authentication**: Secure login system with email/username support and password hashing
- **Search Functionality**: Admins can search for doctors and patients across the system
- **Responsive UI**: Modern Bootstrap 5 design with accessible components and dark mode support
- **Session Management**: Remember-me functionality with 7-day session duration

## Tech Stack

- **Backend**: Python, Flask 3.0.3
- **Database**: SQLite (configurable via DATABASE_URL)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login with role-based decorators
- **Forms**: Flask-WTF with email validation
- **Frontend**: Bootstrap 5.3.2, Bootstrap Icons, HTML5
- **Security**: CSRF protection, password hashing with Werkzeug
- **Environment Management**: python-dotenv

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Steps

1. Clone or navigate to the project directory

2. Create a virtual environment

3. Activate the virtual environment
   - **Windows:**
   - **macOS/Linux:**

4. Install dependencies

5. Initialize the database
   - This will create the SQLite database and seed a default admin user (username: admin, password: admin123)

6. Set environment variables (optional, defaults are provided)
   - Create a `.env` file in the project root:
   - **Required .env variables**: None (sensible defaults are configured)

## How to Use / Running the Project

### Starting the Application

The application will start at `http://127.0.0.1:5000/` by default.

### Default Login Credentials

- **Admin**: username `admin`, password `admin123`

### User Workflows

#### Admin Workflow:

1. Login with admin credentials
2. Access Admin Dashboard to view system metrics (doctors, patients, appointments)
3. Manage doctors (add/edit/delete with specialization)
4. Create and manage departments/specializations
5. View all appointments in the system
6. Search for doctors and patients

#### Doctor Workflow:

1. Register/be added by admin
2. Login with email and password
3. View scheduled appointments on dashboard
4. Open individual appointments to add diagnosis, prescription, and notes
5. Update appointment status (Booked/Completed/Cancelled)

#### Patient Workflow:

1. Register on the patient registration page
2. Login with email and password
3. View upcoming appointments on dashboard
4. Book new appointments by selecting a doctor, date, and time slot
5. Cancel booked appointments if needed

## File & Directory Structure

### Root Level Files

- **run.py**: Entry point of the Flask application; creates and runs the app instance
- **create_db.py**: Database initialization script that creates all tables and seeds an admin user
- **requirements.txt**: Lists all Python dependencies needed to run the project
- **.flaskenv**: Flask configuration file (app name and environment settings)
- **PR.md**: Documentation of UI improvements and design changes

### app Directory

Core application package containing models, routes, forms, templates, and static assets.

- **__init__.py**: Application factory function that initializes Flask, SQLAlchemy, Flask-Login, and CSRF protection; registers blueprints and defines user loader
- **models.py**: SQLAlchemy ORM models for Admin, Doctor, Patient, Appointment, Department, and Treatment with role properties and relationships
- **forms.py**: WTForms classes for login, patient registration, doctor management, appointments, and treatment documentation
- **utils.py**: Helper decorators including `role_required()` for role-based access control

### routes Directory

Modular route blueprints for different user roles.

- **auth_routes.py**: Authentication endpoints (login, register, logout) with support for multi-role authentication
- **admin_routes.py**: Admin-only endpoints for managing doctors, departments, viewing appointments, and searching users
- **doctor_routes.py**: Doctor endpoints for viewing scheduled appointments and documenting treatment
- **patient_routes.py**: Patient endpoints for booking appointments, viewing dashboard, and canceling bookings

### templates Directory

Jinja2 HTML templates for rendering pages.

#### Layout & Partials:

- **base.html**: Master template with navbar, sidebar, and footer; all pages extend this
- **_navbar.html**: Sticky navigation bar with user menu and branding
- **_sidebar.html**: Collapsible sidebar with role-specific navigation links
- **_alerts.html**: Flash message display and toast notification container
- **_footer.html**: Application footer
- **macros.html**: Reusable Jinja macros for avatar circles, metric cards, and appointment rows

#### Authentication:

- **login.html**: Login page supporting email or username
- **register.html**: Patient self-registration form

#### Patient Pages:

- **dashboard.html**: Lists patient's upcoming appointments with cancel option
- **book.html**: Appointment booking form with doctor selection and date/time picker

#### Doctor Pages:

- **dashboard.html**: Lists doctor's scheduled appointments
- **appointment_detail.html**: Form for documenting diagnosis, prescription, notes, and status updates

#### Admin Pages:

- **dashboard.html**: Displays metrics (doctor/patient/appointment counts) and recent appointments
- **doctors.html**: Lists all doctors with edit/delete actions
- **doctor_form.html**: Form for adding/editing doctor profiles
- **departments.html**: Department/specialization management interface
- **appointments.html**: View all system appointments
- **search.html**: Search interface for finding doctors and patients

#### Partials:

- **availability.html**: 7-day appointment availability grid with time slots
- **confirm_booking_modal.html**: Modal for confirming appointment booking

### static Directory

Static assets (CSS, JavaScript, images).

- **theme.css**: Custom theme with CSS variables (colors, shadows, spacing), responsive design for sidebar, and component styling
- **style.css**: Additional base styles
- **ui.js**: Client-side interactions including tooltip initialization, sidebar toggle, slot selection, and form validation

### myenv Directory

Python virtual environment directory (auto-generated; contains isolated dependencies).

## Additional Notes

- **Database**: By default uses SQLite stored as `hms.db` in the project root. Can be configured via `DATABASE_URL` environment variable.
- **Development Mode**: The `.flaskenv` file enables Flask development mode with auto-reload on code changes.
- **Security**: The application uses CSRF protection on all forms and password hashing with Werkzeug. Ensure `SECRET_KEY` is set securely in production.
- **Deployment**: For production, use a production WSGI server (e.g., Gunicorn) and configure a robust database (PostgreSQL).

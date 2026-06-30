# Hospital Management System

A Django-based hospital management web application built as a semester project. Supports three user roles (Admin, Doctor, Receptionist) with role-based dashboards, patient registration, appointment scheduling, prescriptions (with inline medicine items), and medical records.

## Features

- **Role-Based Access Control** — Admin, Doctor, and Receptionist roles with per-role dashboards and navigation
- **Patient Management** — Register, view, edit, and search patients; view full appointment and medical history per patient
- **Doctor Management** — Add/edit doctors, assign to departments, set availability and consultation fees
- **Department Management** — CRUD departments with assignable head of department
- **Appointment Scheduling** — Book appointments with double-booking prevention; status flow: Pending → Confirmed → Completed/Cancelled
- **Prescriptions** — Create prescriptions tied to completed appointments with inline medicine line-items (name, dosage, frequency, duration, instructions)
- **Medical Records** — Log diagnosis, treatment, test results per visit; searchable per patient
- **Search & Filtering** — Search patients by name/ID/phone; filter appointments by date/doctor/department/status; filter doctors by department/specialization
- **Pagination** — All list views paginated (20 per page)
- **Responsive UI** — Bootstrap 5, mobile-friendly
- **Custom Error Pages** — 404 and 500 error handling

## Tech Stack

- Python 3.12
- Django 6.0.6
- SQLite
- Bootstrap 5 (CDN)
- HTML5, CSS3, vanilla JavaScript

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd hospital-management-system

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_data

# Start the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## Demo Login Credentials

| Role         | Username      | Password        |
|--------------|---------------|-----------------|
| Admin        | admin         | admin123        |
| Doctor (1)   | doctor1       | doctor123       |
| Doctor (2)   | doctor2       | doctor123       |
| Doctor (3)   | doctor3       | doctor123       |
| Receptionist | receptionist  | reception123    |

## Project Structure

```
hospital/
├── accounts/          # Custom User model, authentication, dashboards
├── departments/       # Department CRUD
├── doctors/           # Doctor CRUD, doctor-specific views
├── patients/          # Patient CRUD
├── appointments/      # Appointment scheduling
├── records/           # Prescriptions (with inline items), Medical Records
├── hospital/          # Project settings, URL configuration
├── templates/         # All HTML templates (Bootstrap 5)
│   ├── base.html      # Base template with role-aware navbar
│   ├── registration/  # Login page
│   ├── accounts/      # Role dashboards
│   ├── departments/   # Department templates
│   ├── doctors/       # Doctor templates
│   ├── patients/      # Patient templates
│   ├── appointments/  # Appointment templates
│   └── records/       # Prescription & Medical Record templates
├── static/            # Static files
├── manage.py
└── requirements.txt
```

## Database Schema

### Models and Relationships

- **User** (custom, extends `AbstractUser`) — role (Admin/Doctor/Receptionist), phone_number
- **Department** — name, description, head_of_department (FK → Doctor, nullable)
- **Doctor** — user (OneToOne → User), department (FK → Department), specialization, qualification, experience_years, consultation_fee, available_days/times, is_active
- **Patient** — first/last name, DOB, gender, blood_group, phone, email, address, emergency contact, registered_date
- **Appointment** — patient (FK), doctor (FK), department (FK), date, time, status (Pending/Confirmed/Completed/Cancelled), reason, notes
- **Prescription** — appointment (FK), patient (FK), doctor (FK), date, diagnosis, notes
- **PrescriptionItem** — prescription (FK), medicine_name, dosage, frequency, duration, instructions
- **MedicalRecord** — patient (FK), doctor (FK), appointment (FK, nullable), date, diagnosis, treatment, test_results, notes

### Key Design Decisions

- `on_delete=CASCADE` for tightly-dependent child records (e.g., PrescriptionItem → Prescription)
- `on_delete=SET_NULL` or `PROTECT` for records that should survive deletion of a related entity (e.g., Appointments → Doctor)
- Circular reference between Department and Doctor handled by adding `head_of_department` in a separate migration
- Custom User model set up before first migration to avoid migration complexity

## ER Diagram

```
User ──1:1── Doctor ──N:1── Department (head: 1:N)
 │                              │
 │                              │
Receptionist/Admin         Appointment ──N:1── Patient
                                      │
                                      └── Prescription ──1:N── PrescriptionItem
                                      └── MedicalRecord
```

## Presentation Outline (10-15 min)

1. **Introduction** (1 min) — Problem statement, project goals
2. **Tech Stack & Architecture** (2 min) — Django, SQLite, Bootstrap; apps structure
3. **Database Design** (2 min) — Models, relationships, key decisions
4. **Authentication & RBAC** (2 min) — Custom User model, role-based views
5. **Core Modules Demo** (5 min) — Walk through each module (Departments → Doctors → Patients → Appointments → Prescriptions → Records)
6. **Search & Filtering** (1 min)
7. **Challenges & Solutions** (2 min) — Circular reference handling, double-booking prevention
8. **Q&A** (1 min)

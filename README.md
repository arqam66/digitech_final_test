<div align="center">
  <h1>🏥 Hospital Management System</h1>
  <p>A full-featured Django web application for managing hospital operations with role-based access control.</p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Django-6.0.6-092E20?logo=django&logoColor=white" alt="Django">
    <img src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
    <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white" alt="Bootstrap">
  </p>
</div>

---

## ✨ Features

| Module | Capabilities |
|--------|-------------|
| **Role-Based Access** | Admin, Doctor, and Receptionist roles with distinct dashboards and navigation |
| **Patient Management** | Register, view, edit, search patients; full appointment & medical history per patient |
| **Doctor Management** | Add/edit doctors, assign to departments, set availability and consultation fees |
| **Department Management** | CRUD departments with assignable head of department |
| **Appointment Scheduling** | Book appointments with double-booking prevention; status flow: Pending → Confirmed → Completed/Cancelled |
| **Prescriptions** | Create prescriptions tied to completed appointments with inline medicine line-items (name, dosage, frequency, duration, instructions) |
| **Medical Records** | Log diagnosis, treatment, test results per visit; searchable per patient |
| **Search & Filtering** | Search patients by name/ID/phone; filter appointments by date/doctor/department/status; filter doctors by department/specialization |
| **Pagination** | All list views paginated (20 per page) |
| **Responsive UI** | Bootstrap 5 with mobile-friendly design |

### Bonus

- 📄 **PDF Prescriptions** — Download prescription as PDF via `xhtml2pdf`
- 📧 **Email Reminders** — `python manage.py send_reminders` sends reminders for tomorrow's appointments
- 📊 **Patient Reports** — Summary dashboard with per-patient appointment/prescription/record counts
- 📅 **Doctor Calendar** — Weekly availability view for all doctors

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Django 6.0.6 |
| Database | SQLite |
| Frontend | Bootstrap 5 (CDN), HTML5, CSS3, vanilla JavaScript |
| PDF | xhtml2pdf |

## 🚀 Quick Start

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

Visit **http://127.0.0.1:8000/** to access the application.

## 🔐 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `admin123` |
| **Doctor (1)** | `doctor1` | `doctor123` |
| **Doctor (2)** | `doctor2` | `doctor123` |
| **Doctor (3)** | `doctor3` | `doctor123` |
| **Receptionist** | `receptionist` | `reception123` |

## 📁 Project Structure

```
hospital/
├── accounts/              # Custom User model, authentication, dashboards
├── departments/           # Department CRUD
├── doctors/               # Doctor CRUD, doctor-specific views
├── patients/              # Patient CRUD
├── appointments/          # Appointment scheduling
├── records/               # Prescriptions (with inline items), Medical Records
├── hospital/              # Project settings, URL configuration
├── templates/             # All HTML templates (Bootstrap 5)
│   ├── base.html          # Base template with role-aware navbar
│   ├── registration/      # Login page
│   ├── accounts/          # Role dashboards
│   ├── departments/       # Department templates
│   ├── doctors/           # Doctor templates + calendar
│   ├── patients/          # Patient templates
│   ├── appointments/      # Appointment templates
│   └── records/           # Prescription & Medical Record templates
├── static/                # Static files
├── manage.py
└── requirements.txt
```

## ✅ Requirements Checklist

| Requirement | Status |
|------------|--------|
| User Authentication (Login, Logout) | Implemented — custom `login_view`, `LogoutView`, password toggle on login form |
| Role-Based Access Control | Implemented — Admin, Doctor, Receptionist roles with distinct dashboards and navigation |
| CRUD Operations | Implemented — Create/Read/Update/Delete for Departments, Doctors, Patients, Appointments, Prescriptions, MedicalRecords |
| Django Models with Relationships | Implemented — 8 models across 6 apps with OneToOne, ForeignKey, and cascading/deferred delete patterns |
| Django Forms or ModelForms | Implemented — 7 ModelForms with Bootstrap widgets, inline formset for PrescriptionItems, double-booking validation |
| Django Admin Panel | Implemented — All models registered with custom display, filters, search, and inlines |
| Search and Filtering | Implemented — Search by name/ID/phone; filter by department/specialization/date/status |
| Pagination | Implemented — 20 items per page on all list views with `paginate_by` |
| Responsive User Interface | Implemented — Bootstrap 5.3 with mobile navbar, responsive tables, tab panels |
| Form Validation | Implemented — Django built-in + custom `clean()` for double-booking prevention, `PrescriptionItemFormSet` validation |
| Error Handling | Implemented — Custom `handler404` and `handler500` views, `get_object_or_404` throughout, try/except for doctor profile |
| Proper Navigation | Implemented — Role-aware navbar with active-state highlighting, dropdown profile menu |
| Clean Code Structure | Implemented — 6 Django apps with separation of concerns, CBVs and FBVs, reusable mixins, templatetags |
| README Documentation | Complete — features, tech stack, quick start, credentials, project structure, ER diagram, presentation outline |

## 📊 Database Schema

### Entity Relationship Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│        User         │ 1:1   │       Doctor        │
│─────────────────────│───────│─────────────────────│
│ username (unique)   │       │ user (OneToOne)     │──┐
│ password            │       │ department (FK)     │  │
│ email               │       │ specialization      │  │
│ role (Admin/Doctor/ │       │ qualification       │  │
│       Receptionist) │       │ experience_years    │  │
│ phone_number        │       │ consultation_fee    │  │
└─────────────────────┘       │ available_days      │  │
                              │ available_time_start│  │
                              │ available_time_end  │  │
                              │ is_active           │  │
                              └─────────┬───────────┘  │
                                        │              │
                          ┌─────────────┘              │
                          │                            │
                          ▼                            │
              ┌─────────────────────┐       ┌──────────┘
              │     Department      │       │ N:1
              │─────────────────────│       │
              │ name (unique)       │◄──────┘
              │ description         │
              │ head_of_department  │◄──1:N (head)
              │     (FK→Doctor)     │
              └─────────────────────┘

┌─────────────────────┐       ┌─────────────────────┐
│       Patient       │ 1:N   │     Appointment     │
│─────────────────────│───────│─────────────────────│
│ first_name          │       │ patient (FK)        │
│ last_name           │       │ doctor (FK→Doctor)  │
│ date_of_birth       │       │ department (FK)     │
│ gender (M/F/O)      │       │ appointment_date    │
│ blood_group         │       │ appointment_time    │
│ phone_number        │       │ status (Pending/    │
│ email               │       │   Confirmed/        │
│ address             │       │   Completed/        │
│ emergency_contact_  │       │   Cancelled)        │
│   _name/_phone      │       │ reason_for_visit    │
│ registered_date     │       │ notes               │
└─────────────────────┘       └────────┬────────────┘
       │ 1:N                           │ 1:N
       │                               │
       ▼                               ▼
┌─────────────────────┐       ┌─────────────────────┐
│    MedicalRecord    │       │    Prescription     │
│─────────────────────│       │─────────────────────│
│ patient (FK)        │       │ appointment (FK)    │
│ doctor (FK)         │       │ patient (FK)        │
│ appointment (FK)    │       │ doctor (FK)         │
│ record_date         │       │ date_prescribed     │
│ diagnosis           │       │ diagnosis           │
│ treatment           │       │ notes               │
│ test_results        │       └────────┬────────────┘
│ notes               │                │ 1:N
└─────────────────────┘                │
                                        ▼
                               ┌─────────────────────┐
                               │  PrescriptionItem   │
                               │─────────────────────│
                               │ prescription (FK)   │
                               │ medicine_name       │
                               │ dosage              │
                               │ frequency           │
                               │ duration            │
                               │ instructions        │
                               └─────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `on_delete=CASCADE` | Tightly-dependent child records (e.g., PrescriptionItem → Prescription, Appointment → Patient) |
| `on_delete=SET_NULL` | Records that should survive deletion (e.g., Appointments → Doctor, Department → Doctor) |
| Circular reference (Department ↔ Doctor) | Resolved by adding `head_of_department` FK in a separate migration (0002) after Doctor model exists |
| Custom User model (`AUTH_USER_MODEL`) | Set up before first migration to avoid migration complexity; allows `role` field directly on User |
| `available_days` as CharField | Stored as comma-separated string; split via custom template filter `record_extras.py` |
| Inline Formset for PrescriptionItems | Enables dynamic add/remove of multiple medicine items per prescription on a single form |

## 📋 Presentation Outline (10–15 min)

1. **Introduction** (1 min) — Problem statement, project goals
2. **Tech Stack & Architecture** (2 min) — Django, SQLite, Bootstrap; apps structure
3. **Database Design** (2 min) — Models, relationships, key decisions
4. **Authentication & RBAC** (2 min) — Custom User model, role-based views
5. **Core Modules Demo** (5 min) — Walk through each module (Departments → Doctors → Patients → Appointments → Prescriptions → Records)
6. **Search & Filtering** (1 min)
7. **Challenges & Solutions** (2 min) — Circular reference handling, double-booking prevention
8. **Q&A** (1 min)

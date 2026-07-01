<div align="center">
  <h1>🏥 Hospital Management System</h1>
  <p>A full-featured Django web application for managing hospital operations with role-based access control, appointment scheduling, prescription management, and digital medical records.</p>

  <p>
    <a href="https://www.python.org/downloads/release/python-3129/">
      <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12">
    </a>
    <a href="https://docs.djangoproject.com/en/6.0/releases/6.0.6/">
      <img src="https://img.shields.io/badge/Django-6.0.6-092E20?logo=django&logoColor=white" alt="Django 6.0.6">
    </a>
    <a href="https://www.sqlite.org/">
      <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
    </a>
    <a href="https://getbootstrap.com/docs/5.3/">
      <img src="https://img.shields.io/badge/UI-Bootstrap_5.3-7952B3?logo=bootstrap&logoColor=white" alt="Bootstrap 5.3">
    </a>
    <a href="https://xhtml2pdf.readthedocs.io/">
      <img src="https://img.shields.io/badge/PDF-xhtml2pdf-EC1C24?logo=adobeacrobatreader&logoColor=white" alt="xhtml2pdf">
    </a>
    <br>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
    </a>
    <img src="https://img.shields.io/badge/status-production--ready-00C853" alt="Status: Production Ready">
    <img src="https://img.shields.io/badge/tests-playwright-45ba4b?logo=playwright&logoColor=white" alt="Playwright Tests">
    <br>
    <a href="Hospital_Management_System.pdf" target="_blank" rel="noopener noreferrer">
      <img src="https://img.shields.io/badge/📄-Project_Report-2E86C1?logo=adobeacrobatreader&logoColor=white" alt="Project Report PDF">
    </a>
  </p>

  <h3>
    <a href="#features">Features</a>
    <span> · </span>
    <a href="#tech-stack">Tech Stack</a>
    <span> · </span>
    <a href="#quick-start">Quick Start</a>
    <span> · </span>
    <a href="#demo-credentials">Demo Credentials</a>
    <span> · </span>
    <a href="#project-structure">Structure</a>
    <span> · </span>
    <a href="#requirements-checklist">Checklist</a>
    <span> · </span>
    <a href="#database-schema">Schema</a>
  </h3>
</div>

---

## 📋 Table of Contents

- [Target Audience](#-target-audience)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Demo Credentials](#-demo-credentials)
- [Project Structure](#-project-structure)
- [Request Data Flow](#-request-data-flow-mvt-pattern)
- [End-to-End Patient Journey](#-end-to-end-patient-journey)
- [Architecture & Design Decisions](#-architecture--design-decisions)
- [Modules Reference](#-modules-reference)
  - [Accounts & Authentication](#accounts--authentication)
  - [Departments](#departments-module)
  - [Doctors](#doctors-module)
  - [Patients](#patients-module)
  - [Appointments](#appointments-module)
  - [Medical Records & Prescriptions](#medical-records--prescriptions)
- [API Routes](#-api-routes)
- [Bonus Features](#-bonus-features)
- [Testing](#-testing)
- [Management Commands](#-management-commands)
- [Deployment](#-deployment)
- [Requirements Checklist](#-requirements-checklist)
- [Database Schema](#-database-schema)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Target Audience

This system is designed for the following user groups in a hospital or clinical setting:

| Persona | Role in System | Primary Goals |
|---------|---------------|--------------|
| **🏥 Hospital Administrator** | `Admin` | Oversee all operations — manage departments, doctors, staff accounts; view system-wide analytics; ensure data integrity across all modules |
| **👨‍⚕️ Doctor / Physician** | `Doctor` | View daily appointment schedule; record diagnoses, prescriptions, and medical notes; access patient history; manage availability calendar |
| **🖥️ Receptionist / Front Desk** | `Receptionist` | Register new patients; book, reschedule, and cancel appointments; manage front-desk scheduling; view today's patient queue |
| **🧑‍💼 IT / System Admin** | `Admin` | Configure system settings; manage user accounts and role assignments; monitor system health through Django Admin panel |

---

## 🏗 System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                                │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                 Bootstrap 5.3 UI (Templates)                          │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  │  │ Dashboards│ │  CRUD    │ │  Forms   │ │ Calendar │ │   PDF    │   │  │
│  │  │  (Role)   │ │  Tables  │ │ (Inline) │ │   View   │ │   View   │   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────────┤
│                           APPLICATION LAYER                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────┐ │
│  │ accounts │ │departments│ │  doctors │ │ patients │ │appointm. │ │records │
│  │          │ │          │ │          │ │          │ │          │ │     │ │
│  │ • Auth   │ │ • CRUD   │ │ • CRUD   │ │ • CRUD   │ │ • CRUD   │ │ • Rx│ │
│  │ • RBAC   │ │ • HOD    │ │ • Avail. │ │ • Search │ │ • Workfl.│ │ • MR│ │
│  │ • Dashboard│ │  Mgmt   │ │ • Filter │ │ • Tabs   │ │ • Dbl-Bk │ │ • PDF│ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └─────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│                           DATA LAYER                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         SQLite Database                                │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │  │
│  │  │ User │ │Doctor│ │Dept. │ │Patient│ │Appt. │ │  Rx  │ │ RxItem│   │  │
│  │  │      │ │      │ │      │ │      │ │      │ │      │ │       │   │  │
│  │  │  8   │ │  11  │ │  3   │ │  12  │ │  9   │ │  5   │ │   5   │   │  │
│  │  │fields│ │fields│ │fields│ │fields│ │fields│ │fields│ │fields │   │  │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Application-to-Model Mapping

```
┌────────────┐    ┌─────────────┐
│  accounts  │───▶│  User       │  (custom AbstractUser + role)
└────────────┘    └─────────────┘
                       │ 1:1
                       ▼
┌────────────┐    ┌─────────────┐    N:1    ┌──────────────┐
│  doctors   │───▶│  Doctor     │◀──────────│  Department  │◀────┐
└────────────┘    └─────────────┘           └──────────────┘     │
                       │ 1:N         head_of_department (1:N)────┘
                       │
              ┌────────┼────────┐
              │        │        │
              ▼        ▼        ▼
       ┌──────────┐ ┌──────┐ ┌──────────────┐
       │Appointm. │ │  Rx  │ │MedicalRecord │
       └──────────┘ └──────┘ └──────────────┘
            │ 1:N      │ 1:N         │ 1:N
            │          │             │
            ▼          ▼             ▼
       ┌──────────┐ ┌──────────────┐
       │ Patient  │ │ Presc. Item  │
       └──────────┘ └──────────────┘
```

### User Role Hierarchy & Access Control

```
                    ┌──────────────────────┐
                    │   Unauthenticated    │
                    │   (Login Page Only)  │
                    └──────────┬───────────┘
                               │ login
                               ▼
                    ┌──────────────────────┐
                    │    Authenticated     │
                    │   (Any Valid User)   │
                    └──────────┬───────────┘
                               │ redirect by role
             ┌─────────────────┼──────────────────┐
             ▼                 ▼                  ▼
    ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
    │     Admin      │ │    Doctor    │ │  Receptionist  │
    │                │ │              │ │                │
    │ Full access    │ │ Doctor's own │ │ Patient CRUD   │
    │ All CRUD       │ │ appointments │ │ Appointment CRUD│
    │ All modules    │ │ Prescriptions│ │ Search/View    │
    │ User mgmt     │ │ Med Records  │ │ ❌ Delete      │
    │ System config  │ │ ❌ Admin     │ │ ❌ Doctor mgmt │
    └────────────────┘ └──────────────┘ └────────────────┘
```

---

## ✨ Features

### Feature Module Map

```
                        ┌─────────────────────────────┐
                        │    HOSPITAL MANAGEMENT       │
                        │         SYSTEM              │
                        └─────────────┬───────────────┘
                                      │
            ┌────────────┬────────────┼────────────┬────────────┐
            ▼            ▼            ▼            ▼            ▼
    ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  AUTH &    │ │ MASTER   │ │ CLINICAL │ │  REPORTS │ │  UTILS   │
    │   RBAC     │ │ DATA     │ │  MODULES │ │ & ANALYT.│ │          │
    ├────────────┤ ├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤
    │ • Login    │ │ • Dept.  │ │ • Appt.  │ │ • Patient│ │ • PDF    │
    │ • Logout   │ │ • Doctor │ │ • Presc. │ │   Report │ │   Gen.   │
    │ • 3 Roles  │ │ • Patient│ │ • MedRec │ │ • Doctor │ │ • Email  │
    │ • Dashboard│ │   CRUD   │ │ • Calend.│ │   Dashbd │ │   Remind.│
    │ • Redirect │ │ • Search │ │ • Status │ │ • System │ │ • Paginat│
    └────────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### Core Modules

| Module | Capabilities |
|--------|-------------|
| **🔐 Role-Based Access** | Three distinct roles (Admin, Doctor, Receptionist) with separate dashboards, navigation menus, and permission boundaries |
| **👥 Patient Management** | Full CRUD with search by name, ID, or phone; detailed patient profiles with linked appointment history, prescriptions, and medical records in tabbed views |
| **👨‍⚕️ Doctor Management** | CRUD with department assignment, specialization, qualifications, experience tracking, consultation fees, and configurable weekly availability schedules |
| **🏢 Department Management** | CRUD with hierarchical head-of-department assignment (circular reference resolved via deferred migration) |
| **📅 Appointment Scheduling** | Status workflow (Pending → Confirmed → Completed/Cancelled); double-booking prevention via custom form validation; role-filtered listing with date range, doctor, department, and status filters |
| **💊 Prescriptions** | Tied to completed appointments; inline dynamic formset for multiple medicine line-items (name, dosage, frequency, duration, instructions); PDF generation |
| **📋 Medical Records** | Per-visit diagnosis, treatment plans, and test result logging; fully searchable by patient |
| **🔍 Search & Filtering** | Global search across patients; multi-criteria filtering for appointments (date, doctor, department, status) and doctors (department, specialization) |
| **📄 Pagination** | All list views paginated at 20 records per page |
| **📱 Responsive UI** | Bootstrap 5.3 with mobile-first design; role-aware navbar with active-link highlighting and Bootstrap Icons |

### Bonus Features

| Feature | Description |
|---------|-------------|
| **📄 PDF Prescriptions** | Download formatted prescriptions as PDF via `xhtml2pdf` — includes hospital letterhead, doctor signature, formatted medicine table |
| **📧 Email Reminders** | Scheduled command (`send_reminders`) sends automated reminders for next-day appointments; supports `--dry-run` for preview |
| **📊 Patient Reports** | Summary dashboard with aggregate counts (appointments, prescriptions, medical records) per patient across the entire system |
| **📅 Doctor Calendar** | Weekly availability view displaying all active doctors' schedules — days, time slots, consultation fees, and quick-book actions |

---

## 🛠 Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend** | Python + Django | 3.12 / 6.0.6 |
| **Database** | SQLite | 3.x |
| **Frontend** | Bootstrap 5 (CDN), HTML5, CSS3, Vanilla JS | 5.3 |
| **PDF Rendering** | xhtml2pdf | ^0.2.15 |
| **E2E Testing** | Playwright | latest |
| **WSGI Server** | Gunicorn (via Procfile) | — |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip
- virtualenv (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/arqam66/digitech_final_test.git
cd digitech_final_test

# Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Seed demo data (creates users, departments, doctors, patients, appointments)
python manage.py seed_data

# Start the development server
python manage.py runserver
```

### Access

Open **http://127.0.0.1:8000/** in your browser. You will be redirected to the login page.

---

## 🔐 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| **Administrator** | `admin` | `admin123` |
| **Doctor (Cardiology)** | `doctor1` | `doctor123` |
| **Doctor (Neurology)** | `doctor2` | `doctor123` |
| **Doctor (Pediatrics)** | `doctor3` | `doctor123` |
| **Receptionist** | `receptionist` | `reception123` |

> **Note:** The `seed_data` management command is idempotent — running it multiple times will not duplicate data.

---

## 📁 Project Structure

### Feature-to-Directory Layout

```
  FEATURE                              DJANGO APP / FILE            PROVIDES
  ─────────────────────────────────────────────────────────────────────────────
  🔐 Authentication & Role Control   accounts/              Login, logout, 3 role dashboards
  🏢 Department Management            departments/           CRUD + Head of Department
  👨‍⚕️ Doctor Profiles & Calendar     doctors/               CRUD, availability, weekly calendar
  👥 Patient Registration & History   patients/              CRUD, tabs, search
  📅 Appointment Scheduling           appointments/          CRUD, status workflow, reminders
  💊 Prescriptions & Medical Records  records/               CRUD, inline formset, PDF
  ⚙️ Project Configuration           hospital/              Settings, root URLs, error pages
  🎨 UI Templates                     templates/             base.html, pagination, error pages
  📄 Static Assets                    static/                CSS, JS, images
  🧪 E2E Testing                      check_all.py           Playwright automated tests
  🐳 Deployment                       Procfile, runtime.txt  Gunicorn WSGI, Python version
```

### File Tree with Annotations

```
hospital/
│
├── 📁 accounts/                          🔐 AUTHENTICATION & AUTHORIZATION
│   ├── 📁 management/commands/
│   │   └── 📄 seed_data.py               → python manage.py seed_data (idempotent demo seeder)
│   ├── 📁 migrations/
│   │   └── 📄 0001_initial.py            → Initial User model migration
│   ├── 📁 templates/accounts/
│   │   ├── 📄 admin_dashboard.html       → KPI cards: patients, doctors, today's appointments
│   │   ├── 📄 doctor_dashboard.html      → Personal stats: my appointments, patient count
│   │   └── 📄 receptionist_dashboard.html → Front-desk: today's schedule, quick actions
│   ├── 📄 admin.py                       → CustomUserAdmin (role filter, fieldset)
│   ├── 📄 models.py                      → User(AbstractUser) + role, phone_number
│   ├── 📄 urls.py                        → 6 URL routes (login, logout, 3 dashboards, redirect)
│   └── 📄 views.py                       → login_view, logout_view, 3 role-specific dashboards
│
├── 📁 departments/                       🏢 DEPARTMENT MANAGEMENT
│   ├── 📁 templates/departments/
│   │   ├── 📄 department_list.html       → Paginated table with edit/delete (admin)
│   │   ├── 📄 department_form.html       → Create/edit form
│   │   └── 📄 department_confirm_delete.html → Confirmation prompt
│   ├── 📄 admin.py                       → DepartmentAdmin (search by name)
│   ├── 📄 forms.py                       → DepartmentForm (ModelForm)
│   ├── 📄 models.py                      → Department(name unique, description, head FK→Doctor)
│   ├── 📄 urls.py                        → 4 CRUD routes
│   └── 📄 views.py                       → ListView, CreateView, UpdateView, DeleteView
│
├── 📁 doctors/                           👨‍⚕️ DOCTOR PROFILES & SCHEDULING
│   ├── 📁 templates/doctors/
│   │   ├── 📄 doctor_list.html           → Filterable table (dept, specialization, search)
│   │   ├── 📄 doctor_form.html           → Full profile form with availability
│   │   ├── 📄 doctor_detail.html         → Profile info + recent appointments
│   │   ├── 📄 doctor_calendar.html       → Weekly grid view for all active doctors
│   │   └── 📄 doctor_confirm_delete.html → Confirmation prompt
│   ├── 📄 admin.py                       → DoctorAdmin (filters, search)
│   ├── 📄 forms.py                       → DoctorForm (ModelForm)
│   ├── 📄 models.py                      → Doctor(user O2O, dept FK, specialization, fee, availability)
│   ├── 📄 urls.py                        → 9 routes (CRUD + 4 doctor-specific + calendar)
│   └── 📄 views.py                       → CRUD + doctor-specific filtered views + calendar
│
├── 📁 patients/                          👥 PATIENT REGISTRATION & HISTORY
│   ├── 📁 templates/patients/
│   │   ├── 📄 patient_list.html          → Searchable table with pagination
│   │   ├── 📄 patient_form.html          → Full registration form (demographics + emergency)
│   │   ├── 📄 patient_detail.html        → Info + 3 Bootstrap tabs (Appts, Rx, MedRecords)
│   │   └── 📄 patient_confirm_delete.html → Warning about cascading deletions
│   ├── 📄 admin.py                       → PatientAdmin (gender/blood group filters, search)
│   ├── 📄 forms.py                       → PatientForm (ModelForm)
│   ├── 📄 models.py                      → Patient(name, DOB, gender, blood, contact, emergency)
│   ├── 📄 urls.py                        → 5 CRUD routes
│   └── 📄 views.py                       → CRUD (delete restricted to Admin)
│
├── 📁 appointments/                      📅 APPOINTMENT SCHEDULING & WORKFLOW
│   ├── 📁 management/commands/
│   │   └── 📄 send_reminders.py          → python manage.py send_reminders [--dry-run]
│   ├── 📁 templates/appointments/
│   │   ├── 📄 appointment_list.html      → Filterable table (date, doctor, dept, status)
│   │   ├── 📄 appointment_form.html      → Booking form with double-booking validation
│   │   ├── 📄 appointment_detail.html    → Status badge + action buttons (confirm/complete/cancel)
│   │   └── 📄 appointment_confirm_delete.html → Confirmation prompt
│   ├── 📄 admin.py                       → AppointmentAdmin (status/date/dept filters, date_hierarchy)
│   ├── 📄 forms.py                       → AppointmentForm with custom clean() for double-booking
│   ├── 📄 models.py                      → Appointment(patient FK, doctor FK, date, time, status)
│   ├── 📄 urls.py                        → 8 routes (CRUD + 3 status transitions)
│   └── 📄 views.py                       → CRUD + confirm/complete/cancel action views
│
├── 📁 records/                           💊 PRESCRIPTIONS & MEDICAL RECORDS
│   ├── 📁 templatetags/
│   │   └── 📄 record_extras.py           → Custom {% split %} filter for available_days
│   ├── 📁 templates/records/
│   │   ├── 📄 prescription_list.html     → Table with patient, diagnosis, items count
│   │   ├── 📄 prescription_form.html     → Form + inline formset (dynamic medicine rows)
│   │   ├── 📄 prescription_detail.html   → Full prescription + Download PDF button
│   │   ├── 📄 prescription_pdf.html      → PDF-only template (letterhead, table, signature)
│   │   ├── 📄 prescription_confirm_delete.html → Confirmation prompt
│   │   ├── 📄 medical_record_list.html   → Filterable list with diagnosis/treatment/tests
│   │   ├── 📄 medical_record_form.html   → Create/edit form
│   │   ├── 📄 medical_record_detail.html → Full detail view
│   │   ├── 📄 medical_record_confirm_delete.html → Confirmation prompt
│   │   └── 📄 patient_report.html        → Summary stats: patients, appts, Rx, records
│   ├── 📄 admin.py                       → PrescriptionAdmin + PrescriptionItemInline, MedicalRecordAdmin
│   ├── 📄 forms.py                       → 3 ModelForms + PrescriptionItemFormSet (inlineformset_factory)
│   ├── 📄 models.py                      → Prescription, PrescriptionItem, MedicalRecord
│   ├── 📄 urls.py                        → 12 routes (6 per module)
│   ├── 📄 utils.py                       → render_pdf() using xhtml2pdf
│   └── 📄 views.py                       → CRUD + inline formset handling + PDF generation
│
├── 📁 hospital/                          ⚙️ PROJECT CONFIGURATION
│   ├── 📄 settings.py                    → 60+ settings: 6 apps, SQLite, auth_user_model, email, etc.
│   ├── 📄 urls.py                        → Root URLconf: includes 6 apps + admin + error handlers
│   ├── 📄 wsgi.py                        → WSGI entrypoint for Gunicorn
│   └── 📄 views.py                       → Custom handler404() and handler500()
│
├── 📁 templates/                         🎨 GLOBAL UI TEMPLATES
│   ├── 📄 base.html                      → Role-aware navbar (Bootstrap 5.3), messages, footer
│   ├── 📄 pagination.html                → Reusable pagination: First/Prev/Next/Last
│   ├── 📄 404.html                       → "Page Not Found" with navigation links
│   ├── 📄 500.html                       → "Server Error" with fallback links
│   └── 📁 registration/
│       └── 📄 login.html                 → Login form with show/hide password toggle
│
├── 📁 static/                            📦 STATIC ASSETS
│
├── 📄 check_all.py                       🧪 Playwright E2E test suite (41+ test scenarios)
├── 📄 manage.py                          🐍 Django management entrypoint
├── 📄 requirements.txt                   📋 Python dependencies
├── 📄 runtime.txt                        🐍 Python version constraint (3.12.9)
├── 📄 Procfile                           🐳 Gunicorn WSGI deploy config
└── 📄 .gitignore
```

---

## ⚡ Request Data Flow (MVT Pattern)

Every user action in the system follows Django's Model-View-Template (MVT) architecture. Below is the complete request lifecycle for a typical operation (e.g., creating a prescription):

```
  USER ACTION                          DJANGO REQUEST LIFECYCLE
  ════════════════════════════════════════════════════════════════════════

  Browser / Form Submit
        │
        ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                     URL DISPATCHER                               │
  │  hospital/urls.py → records/urls.py                              │
  │  MATCH: /records/prescriptions/create/                           │
  │  → routes to records/views.py:prescription_create               │
  └──────────────────────────────────────────────────────────────────┘
        │
        ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                     VIEW (Controller)                            │
  │  records/views.py:prescription_create()                          │
  │                                                                  │
  │  Step 1: Check authentication & authorization                   │
  │  Step 2: Fetch related data (patients, doctors, appointments)    │
  │  Step 3: Instantiate PrescriptionForm + PrescriptionItemFormSet  │
  │  Step 4: Validate on POST → if valid, save model instance        │
  │  Step 5: Redirect to detail view on success                      │
  └──────────────────────────────────────────────────────────────────┘
        │
        ├──────────────────────────────────┐
        ▼                                  ▼
  ┌────────────────────┐       ┌────────────────────────┐
  │      MODEL         │       │        FORM            │
  │  records/models.py │       │  records/forms.py      │
  │                    │       │                        │
  │  Prescription      │       │  PrescriptionForm      │
  │  ├── appointment   │       │  ├── appointment (FK)  │
  │  ├── patient       │       │  ├── patient (FK)      │
  │  ├── doctor        │       │  ├── doctor (FK)       │
  │  ├── diagnosis     │       │  ├── diagnosis (Text)  │
  │  └── notes         │       │  └── notes (Text)      │
  │                    │       │                        │
  │  PrescriptionItem  │       │  PrescriptionItemForm  │
  │  ├── medicine_name │       │  ├── medicine_name     │
  │  ├── dosage        │       │  ├── dosage            │
  │  ├── frequency     │       │  ├── frequency         │
  │  ├── duration      │       │  ├── duration          │
  │  └── instructions  │       │  └── instructions      │
  │                    │       │                        │
  │  SQLite: INSERT    │       │  PrescriptionItemFormSet│
  │  INTO prescriptions│       │  (inlineformset_factory,│
  │  INTO rx_items     │       │   extra=3, can_delete) │
  └────────────────────┘       └────────────────────────┘
        │                                │
        └──────────────┬─────────────────┘
                       ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                   TEMPLATE (Rendering)                           │
  │                                                                  │
  │  GET request  → prescription_form.html                           │
  │                  ├── Bootstrap 5.3 form controls                 │
  │                  ├── Inline formset table for medicine items     │
  │                  ├── Dynamic add/remove via JavaScript           │
  │                  └── CSRF token, action URL                      │
  │                                                                  │
  │  POST success  → Redirect to prescription_detail.html            │
  │                  ├── Patient info, doctor, date                  │
  │                  ├── Medicine items table                        │
  │                  └── Download PDF button                         │
  └──────────────────────────────────────────────────────────────────┘
        │
        ▼
  Browser Response (HTML page or PDF)
```

This pattern is repeated consistently across all 6 apps, with the following variations:

| App | Primary View Pattern | Distinctive Feature |
|-----|---------------------|-------------------|
| **accounts** | Function-Based Views | Login/logout session management |
| **departments** | Class-Based Views (CRUD) | Admin-only mixin protection |
| **doctors** | Mixed CBV + FBV | Doctor-specific filtered queries |
| **patients** | Class-Based Views (CRUD) | Tabbed detail template |
| **appointments** | Class-Based Views + FBV actions | Status transition endpoints + double-booking `clean()` |
| **records** | Function-Based Views (with inline formsets) | Formset handling + PDF generation |

---

## 🔄 End-to-End Patient Journey

Below is the complete lifecycle of a patient within the system — from first registration to receiving a prescription — showing exactly which modules, views, and templates are involved at each step.

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                       PATIENT LIFECYCLE                                 │
  └─────────────────────────────────────────────────────────────────────────┘

  STEP 1: PATIENT REGISTRATION
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Receptionist/Doctor logs in          accounts/views.py:login_view  │
  │  → Clicks "Register Patient"          template: patient_form.html   │
  │  → Fills: name, DOB, gender, blood,   patients/forms.py:PatientForm │
  │    phone, email, address, emergency   patients/views.py:create_view  │
  │  → Submits → Patient record created   patients/models.py:Patient     │
  └──────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
  STEP 2: APPOINTMENT BOOKING
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Receptionist/Doctor selects patient  appointments/forms.py:ApptForm │
  │  → Picks department, doctor, date,    appointments/views.py:create   │
  │    time slot, reason for visit        appointments/models.py:Appt.   │
  │  → Double-booking check passes        AppointmentForm.clean()         │
  │  → Appointment created (Pending)      templates: appointment_form    │
  └──────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
  STEP 3: APPOINTMENT CONFIRMATION
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Admin/Receptionist confirms           appointments/views.py:confirm │
  │  → Status: Pending → Confirmed        POST /appointments/<id>/confirm│
  │  → Patient can now receive care       template: appointment_detail  │
  └──────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
  STEP 4: DOCTOR VISIT
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Doctor logs in → sees appointment    accounts/views.py:doctor_dash  │
  │  → Marks as Completed                 appointments/views.py:complete │
  │  → Status: Confirmed → Completed      POST /appointments/<id>/compl. │
  └──────────────────────────────────────────────────────────────────────┘
                                      │
                         ┌────────────┼────────────┐
                         ▼            ▼            ▼
  STEP 5a:               │ STEP 5b:   │ STEP 5c:   │
  PRESCRIPTION           │ MEDICAL    │ PATIENT    │
                         │ RECORD     │ REPORT     │
  ┌──────────────────┐   ┌─────────┐  ┌─────────┐  │
  │ Doctor creates   │   │ Doctor  │  │ Any role │  │
  │ prescription     │   │ logs    │  │ views    │  │
  │ with inline      │   │ diagno- │  │ patient  │  │
  │ medicine items   │   │ sis,    │  │ summary  │  │
  │                   │   │ treatm. │  │ with all │  │
  │ records/views.py  │   │ tests   │  │ counts   │  │
  │ → prescription_   │   │          │  │          │  │
  │   create          │   │ records/ │  │ records/ │  │
  │                   │   │ views.py │  │ views.py │  │
  │ PrescriptionForm  │   │ → create │  │ → report │  │
  │ + ItemFormSet     │   │          │  │          │  │
  └────────┬─────────┘   └──────────┘  └──────────┘  │
           │                                          │
           ▼                                          │
  STEP 6: PDF DOWNLOAD                                │
  ┌─────────────────────────────────────────────┐     │
  │  Any role views prescription detail         │     │
  │  → Clicks "Download PDF"                    │     │
  │  → xhtml2pdf renders prescription_pdf.html  │     │
  │  → PDF includes: letterhead, medicine       │     │
  │    table, doctor signature area             │     │
  │  records/utils.py:render_pdf()              │     │
  └─────────────────────────────────────────────┘     │
                                                      │
                      ◄────────────────────────────────┘
```

### End-to-End Scenario Walkthrough

| Step | Action | Actor | Module | Key Files |
|------|--------|-------|--------|-----------|
| 1 | Patient walks in → Receptionist registers them | Receptionist | Patients | `patients/views.py`, `patient_form.html` |
| 2 | Receptionist schedules a doctor appointment | Receptionist | Appointments | `appointments/views.py`, `appointment_form.html` |
| 3 | Admin confirms the appointment | Admin | Appointments | `appointments/views.py:confirm` |
| 4 | Doctor marks appointment as Completed | Doctor | Appointments | `appointments/views.py:complete` |
| 5a | Doctor creates prescription with medicines | Doctor | Records | `records/views.py`, `prescription_form.html`, `PrescriptionItemFormSet` |
| 5b | Doctor logs medical record (diagnosis + treatment) | Doctor | Records | `records/views.py`, `medical_record_form.html` |
| 6 | Staff downloads prescription PDF | Any | Records | `records/utils.py`, `prescription_pdf.html` |

---

## 🏗 Architecture & Design Decisions

### Key Design Patterns

| Decision | Implementation | Rationale |
|----------|---------------|-----------|
| **Custom User Model** | `AUTH_USER_MODEL = 'accounts.User'` with `role` field (CharField) | Established before first migration to avoid complex database migration; enables role checks directly on the user object without additional queries |
| **Role-Based Access Control** | `AdminRequiredMixin` (two variants: `UserPassesTestMixin` and `LoginRequiredMixin`) + template-level `user.role` checks | Separates authorization logic at both view and template layers; prevents unauthorized URL access and hides restricted UI elements |
| **Delete Strategy** | `CASCADE` for tightly-dependent children (e.g., `PrescriptionItem → Prescription`); `SET_NULL` for records that should survive parent deletion (e.g., `Appointment → Doctor`) | Balances data integrity with graceful degradation when referenced entities are removed |
| **Circular Reference** | `Department.head_of_department` FK added in a separate migration (`0002`) after `Doctor` model exists | Django cannot create circular FKs in a single migration; deferred migration resolves this cleanly |
| **Inline Formset** | `PrescriptionItemFormSet` using `inlineformset_factory` with `extra=3` and `can_delete=True` | Enables dynamic addition and removal of multiple medicine items on a single prescription form |
| **Comma-Separated Days** | `Doctor.available_days` stored as a CharField; split via custom `record_extras.py:split` template filter | Keeps the model schema simple for a list-based field that doesn't require relational queries |
| **PDF Generation** | Dedicated `prescription_pdf.html` template rendered via `xhtml2pdf` through `records/utils.py:render_pdf()` | Separates PDF layout from screen layout; enables professional print formatting with letterhead and signatures |
| **Email Backend** | Console email backend (`django.core.mail.backends.console.EmailBackend`) during development | Outputs emails to the console for easy debugging; swap to SMTP in production |

### Model Relationship Map

```
User (1:1) → Doctor
Doctor (N:1) → Department
Department (1:N) → Doctor (as head_of_department)
Patient (1:N) → Appointment
Patient (1:N) → MedicalRecord
Patient (1:N) → Prescription
Doctor (1:N) → Appointment
Doctor (1:N) → Prescription
Doctor (1:N) → MedicalRecord
Appointment (1:N) → Prescription
Appointment (1:1) ↔ MedicalRecord
Prescription (1:N) → PrescriptionItem
```

---

## 📚 Modules Reference

### Accounts & Authentication

- **User Model**: Extends Django's `AbstractUser` with a `role` field (`Admin`, `Doctor`, `Receptionist`) and `phone_number`
- **Authentication**: Custom `login_view` with support for `next` parameter redirection; `logout_view` via Django's `LogoutView`
- **Dashboard Routing**: After login, users are redirected to role-specific dashboards that display relevant KPIs and quick actions
- **Admin Dashboard**: Aggregated statistics — total patients, total doctors, today's appointments, pending appointments
- **Doctor Dashboard**: Personal stats — today's appointments, total appointments assigned, unique patient count
- **Receptionist Dashboard**: Front-desk view — today's full schedule, total patients in system, pending appointments with quick action buttons

### Departments Module

- **Access**: Full CRUD restricted to Admin role only
- **Head of Department**: FK relationship to Doctor; resolved after Doctor model exists (migration `0002`)
- **Listing**: Sorted alphabetically; paginated at 20 per page
- **Validation**: Department names are unique

### Doctors Module

- **Access**: Admin can perform all CRUD; all authenticated users can view listing and details
- **Profile Fields**: User account linkage, department, specialization, qualifications, experience, consultation fee, weekly availability (days + time range), active status
- **Filtering**: By department, specialization, and text search on name/specialization
- **Doctor-Specific Views**: Filtered to the logged-in doctor's profile — appointments, prescriptions, medical records
- **Calendar**: Weekly grid view showing availability for all active doctors, with fee badges and book-action links

### Patients Module

- **Access**: All authenticated users can create, view, update; delete restricted to Admin
- **Registration Fields**: Name, DOB, gender, blood group, phone, email, address, emergency contact
- **Detail Tabs**: Three Bootstrap tab panels — Appointments (full history), Prescriptions, Medical Records — all filtered by the current patient
- **Search**: Across first name, last name, phone number, and patient ID

### Appointments Module

- **Access**: All authenticated users with role-based query filtering (doctors see only their own)
- **Double-Booking Prevention**: Custom `AppointmentForm.clean()` checks for existing appointments with the same doctor on the same date and time
- **Filtering**: By patient name, appointment date, doctor, department, and status
- **Status Actions**: Dedicated URL endpoints for `confirm`, `complete`, and `cancel` transitions

#### Appointment Status Lifecycle

```
                    ┌──────────┐
                    │  Pending │  (initial state on booking)
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
        ┌─────────┐ ┌─────────┐ ┌──────────┐
        │Confirmed│ │Cancelled│ │(continue)│
        └────┬────┘ └─────────┘ └──────────┘
             │
             ▼
        ┌──────────┐
        │Completed │  (prescription/record can be added)
        └──────────┘

  Action endpoints:
    /appointments/<id>/confirm/   → Confirmed
    /appointments/<id>/complete/  → Completed
    /appointments/<id>/cancel/    → Cancelled
```

#### Prescription Creation Flow (Post-Appointment)

```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
  │ Appointment  │────▶│ Prescription │────▶│ PrescriptionItem │
  │  Completed   │     │   Created    │     │   (inline x N)   │
  └──────────────┘     └──────┬───────┘     └──────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   PDF Download   │  via xhtml2pdf
                     │  (Prescription)  │
                     └──────────────────┘
```

### Medical Records & Prescriptions

- **Prescriptions**: Created against completed appointments; includes diagnosis, notes, and multiple medicine items
- **Prescription Items**: Inline formset supports dynamic add/remove; fields include medicine name, dosage, frequency, duration, instructions
- **Medical Records**: Separate from prescriptions; captures diagnosis, treatment plan, and test results per visit
- **PDF Output**: Dedicated `prescription_pdf.html` template rendered via `xhtml2pdf`; includes hospital branding, formatted prescription table, and doctor signature area
- **Patient Reports**: Aggregate report showing total appointments, prescriptions, and medical records per patient

---

## 🧭 API Routes

### Authentication

| Method | URL | View | Access | Description |
|--------|-----|------|--------|-------------|
| GET/POST | `/login/` | `login_view` | Public | Login form |
| GET | `/logout/` | `logout_view` | Authenticated | Logout |

### Dashboards

| Method | URL | View | Access | Description |
|--------|-----|------|--------|-------------|
| GET | `/dashboard/` | `dashboard_redirect` | Authenticated | Redirects to role dashboard |
| GET | `/dashboard/admin/` | `admin_dashboard` | Admin | System-wide statistics |
| GET | `/dashboard/doctor/` | `doctor_dashboard` | Doctor | Personal appointment stats |
| GET | `/dashboard/receptionist/` | `receptionist_dashboard` | Receptionist | Front-desk overview |

### Departments

| Method | URL | View | Access | Description |
|--------|-----|------|--------|-------------|
| GET | `/departments/` | `DepartmentListView` | Any auth | List all departments |
| GET/POST | `/departments/create/` | `DepartmentCreateView` | Admin | Create department |
| GET/POST | `/departments/<id>/update/` | `DepartmentUpdateView` | Admin | Edit department |
| POST | `/departments/<id>/delete/` | `DepartmentDeleteView` | Admin | Delete department |

### Doctors

| Method | URL | View | Access | Description |
|--------|-----|------|--------|-------------|
| GET | `/doctors/` | `DoctorListView` | Any auth | List all doctors |
| GET/POST | `/doctors/create/` | `DoctorCreateView` | Admin | Register doctor |
| GET | `/doctors/<id>/` | `DoctorDetailView` | Any auth | Doctor profile |
| GET/POST | `/doctors/<id>/update/` | `DoctorUpdateView` | Admin | Edit doctor |
| POST | `/doctors/<id>/delete/` | `DoctorDeleteView` | Admin | Delete doctor |
| GET | `/doctors/my/appointments/` | `doctor_appointments_view` | Doctor | My appointments |
| GET | `/doctors/my/prescriptions/` | `doctor_prescriptions_view` | Doctor | My prescriptions |
| GET | `/doctors/my/records/` | `doctor_medical_records_view` | Doctor | My medical records |
| GET | `/doctors/calendar/` | `doctor_calendar` | Any auth | Weekly availability calendar |

### Patients

| Method | URL | View | Access | Description |
|--------|-----|------|--------|-------------|
| GET | `/patients/` | `PatientListView` | Any auth | List all patients |
| GET/POST | `/patients/create/` | `PatientCreateView` | Any auth | Register patient |
| GET | `/patients/<id>/` | `PatientDetailView` | Any auth | Patient profile + tabs |
| GET/POST | `/patients/<id>/update/` | `PatientUpdateView` | Any auth | Edit patient |
| POST | `/patients/<id>/delete/` | `PatientDeleteView` | Admin | Delete patient |

### Appointments

| Method | URL | View | Access | Description |
|--------|-----|------|--------|-------------|
| GET | `/appointments/` | `AppointmentListView` | Any auth | List all appointments |
| GET/POST | `/appointments/create/` | `AppointmentCreateView` | Any auth | Book appointment |
| GET | `/appointments/<id>/` | `AppointmentDetailView` | Any auth | Appointment details |
| GET/POST | `/appointments/<id>/update/` | `AppointmentUpdateView` | Any auth | Edit appointment |
| POST | `/appointments/<id>/delete/` | `AppointmentDeleteView` | Any auth | Delete appointment |
| POST | `/appointments/<id>/confirm/` | `appointment_confirm` | Any auth | Confirm appointment |
| POST | `/appointments/<id>/complete/` | `appointment_complete` | Any auth | Complete appointment |
| POST | `/appointments/<id>/cancel/` | `appointment_cancel` | Any auth | Cancel appointment |

### Records (Prescriptions & Medical Records)

| Method | URL | View | Access | Description |
|--------|-----|------|--------|-------------|
| GET | `/records/prescriptions/` | `PrescriptionListView` | Any auth | List prescriptions |
| GET/POST | `/records/prescriptions/create/` | `prescription_create` | Any auth | Create prescription (inline formset) |
| GET | `/records/prescriptions/<id>/` | `PrescriptionDetailView` | Any auth | Prescription details |
| GET/POST | `/records/prescriptions/<id>/update/` | `prescription_update` | Any auth | Edit prescription |
| GET | `/records/prescriptions/<id>/pdf/` | `prescription_pdf` | Any auth | Download PDF |
| POST | `/records/prescriptions/<id>/delete/` | `PrescriptionDeleteView` | Admin | Delete prescription |
| GET | `/records/records/` | `MedicalRecordListView` | Any auth | List medical records |
| GET/POST | `/records/records/create/` | `MedicalRecordCreateView` | Any auth | Create record |
| GET | `/records/records/<id>/` | `MedicalRecordDetailView` | Any auth | Record details |
| GET/POST | `/records/records/<id>/update/` | `MedicalRecordUpdateView` | Any auth | Edit record |
| POST | `/records/records/<id>/delete/` | `MedicalRecordDeleteView` | Admin | Delete record |
| GET | `/records/patient-report/` | `patient_report` | Any auth | Patient summary report |

### Error Pages

| Status Code | Handler | Description |
|-------------|---------|-------------|
| 404 | `hospital.views.handler404` | Custom "Page Not Found" with navigation |
| 500 | `hospital.views.handler500` | Custom "Server Error" with fallback links |

---

## 🧪 Testing

### End-to-End Tests (Playwright)

An automated Playwright test script is available at `check_all.py`. It covers:

- User login for all three roles
- Role-based navigation and dashboard access
- CRUD operations for all modules
- Appointment status transitions
- Search and filtering functionality
- Custom error page rendering
- Form validation and error states

```bash
# Run the Playwright test suite
python check_all.py
```

> **Note:** Unit tests are stubbed in each app's `tests.py` and ready for implementation. Contributions are welcome.

---

## ⚙️ Management Commands

| Command | Description |
|---------|-------------|
| `python manage.py seed_data` | Seeds the database with demo data (users, departments, doctors, patients, appointments, prescriptions, medical records). Idempotent — safe to re-run. |
| `python manage.py send_reminders` | Sends email reminders for tomorrow's confirmed/pending appointments. Use `--dry-run` to preview without sending. |

---

## 🌐 Deployment

The project includes a `Procfile` for deployment on platforms supporting Gunicorn:

```
web: gunicorn hospital.wsgi --log-file -
```

### Production Considerations

1. **Set `DEBUG = False`** in `settings.py`
2. **Configure `ALLOWED_HOSTS`** with your domain
3. **Switch to a production email backend** (e.g., SMTP with SendGrid, Mailgun)
4. **Use a production-grade database** (PostgreSQL recommended; update `DATABASES` in settings)
5. **Serve static files** via a CDN or web server (e.g., WhiteNoise, Nginx)
6. **Rotate the `SECRET_KEY`** to a secure, environment-specific value
7. **Set up HTTPS** with a reverse proxy (Nginx + Let's Encrypt)

---

## ✅ Requirements Checklist

| Requirement | Status | Implementation Details |
|------------|--------|----------------------|
| User Authentication (Login, Logout) | ✅ **Implemented** | Custom `login_view` with `next` param support; `LogoutView`; show/hide password toggle on login form |
| Role-Based Access Control | ✅ **Implemented** | Three roles (Admin, Doctor, Receptionist) with distinct dashboards, navigation menus, and `AdminRequiredMixin` for authorization |
| CRUD Operations | ✅ **Implemented** | Full Create/Read/Update/Delete for Departments, Doctors, Patients, Appointments, Prescriptions, MedicalRecords |
| Django Models with Relationships | ✅ **Implemented** | 8 models across 6 apps with OneToOne, ForeignKey, CASCADE, SET_NULL, and resolved circular reference patterns |
| Django Forms or ModelForms | ✅ **Implemented** | 7 ModelForms with Bootstrap CSS classes; inline formset for PrescriptionItems; custom `clean()` for double-booking validation |
| Django Admin Panel | ✅ **Implemented** | All models registered with custom display fields, list filters, search fields, date hierarchy, and TabularInline for PrescriptionItems |
| Search and Filtering | ✅ **Implemented** | Patient search by name/ID/phone; appointment filtering by date/doctor/department/status; doctor filtering by department/specialization |
| Pagination | ✅ **Implemented** | 20 items per page on all list views with Django generic `paginate_by` and reusable pagination template |
| Responsive User Interface | ✅ **Implemented** | Bootstrap 5.3 with mobile-responsive navbar, responsive tables, tab panels, and collapsible navigation |
| Form Validation | ✅ **Implemented** | Django built-in field validation + custom `AppointmentForm.clean()` for double-booking prevention + `PrescriptionItemFormSet` validation |
| Error Handling | ✅ **Implemented** | Custom `handler404` and `handler500` views; `get_object_or_404` throughout; try/except guards for doctor profile access |
| Proper Navigation | ✅ **Implemented** | Role-aware navbar with active-state highlighting, dropdown profile menu, conditional menu items based on user role |
| Clean Code Structure | ✅ **Implemented** | 6 Django apps with clear separation of concerns; mix of Class-Based Views and Function-Based Views; reusable mixins; custom templatetags |
| README Documentation | ✅ **Implemented** | Comprehensive documentation: features, tech stack, setup guide, credentials, project structure, architecture decisions, full API route table, ER diagram, deployment guide, testing instructions |

---

## 📊 Database Schema

### Entity Relationship Diagram

```
┌──────────────────────┐       ┌──────────────────────┐
│         User         │ 1:1   │       Doctor         │
│──────────────────────│───────│──────────────────────│
│ username (unique)    │       │ user (OneToOne)      │──┐
│ password             │       │ department (FK)      │  │
│ email                │       │ specialization       │  │
│ role (Admin/Doctor/  │       │ qualification        │  │
│       Receptionist)  │       │ experience_years     │  │
│ phone_number         │       │ consultation_fee     │  │
└──────────────────────┘       │ available_days       │  │
                               │ available_time_start │  │
                               │ available_time_end   │  │
                               │ is_active            │  │
                               └──────────┬───────────┘  │
                                           │              │
                             ┌─────────────┘              │
                             │                            │
                             ▼                            │
                 ┌──────────────────────┐       ┌─────────┘
                 │     Department       │       │ N:1
                 │──────────────────────│       │
                 │ name (unique)        │◄──────┘
                 │ description          │
                 │ head_of_department   │◄──────1:N (head)
                 │      (FK→Doctor)     │
                 └──────────────────────┘


┌──────────────────────┐       ┌──────────────────────┐
│       Patient        │ 1:N   │     Appointment      │
│──────────────────────│───────│──────────────────────│
│ first_name           │       │ patient (FK)         │
│ last_name            │       │ doctor (FK→Doctor)   │
│ date_of_birth        │       │ department (FK)      │
│ gender (M/F/O)       │       │ appointment_date     │
│ blood_group          │       │ appointment_time     │
│ phone_number         │       │ status (Pending/     │
│ email                │       │   Confirmed/         │
│ address              │       │   Completed/         │
│ emergency_contact_   │       │   Cancelled)         │
│   _name/_phone       │       │ reason_for_visit     │
│ registered_date      │       │ notes                │
└──────────────────────┘       └──────────┬───────────┘
       │ 1:N                              │ 1:N
       │                                  │
       ▼                                  ▼
┌──────────────────────┐       ┌──────────────────────┐
│    MedicalRecord     │       │    Prescription      │
│──────────────────────│       │──────────────────────│
│ patient (FK)         │       │ appointment (FK)     │
│ doctor (FK)          │       │ patient (FK)         │
│ appointment (FK)     │       │ doctor (FK)          │
│ record_date          │       │ date_prescribed      │
│ diagnosis            │       │ diagnosis            │
│ treatment            │       │ notes                │
│ test_results         │       └──────────┬───────────┘
│ notes                │                  │ 1:N
└──────────────────────┘                  │
                                           ▼
                                  ┌──────────────────────┐
                                  │  PrescriptionItem   │
                                  │──────────────────────│
                                  │ prescription (FK)    │
                                  │ medicine_name        │
                                  │ dosage               │
                                  │ frequency            │
                                  │ duration             │
                                  │ instructions         │
                                  └──────────────────────┘
```

### Entity Relationship Summary

| Entity | Fields | Relationships |
|--------|--------|--------------|
| **User** | 5 fields (inherits AbstractUser) | 1:1 → Doctor |
| **Doctor** | 11 fields | N:1 → Department; 1:N → Appointment, Prescription, MedicalRecord |
| **Department** | 3 fields | 1:N → Doctor (members); 1:N → Doctor (head) — circular reference |
| **Patient** | 12 fields | 1:N → Appointment, Prescription, MedicalRecord |
| **Appointment** | 9 fields | N:1 → Patient, Doctor, Department |
| **Prescription** | 5 fields | N:1 → Appointment, Patient, Doctor; 1:N → PrescriptionItem |
| **PrescriptionItem** | 5 fields | N:1 → Prescription |
| **MedicalRecord** | 7 fields | N:1 → Patient, Doctor, Appointment |

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `on_delete=CASCADE` | Used for tightly-dependent child records (e.g., `PrescriptionItem → Prescription`, `Appointment → Patient`) to maintain referential integrity |
| `on_delete=SET_NULL` | Used for records that should survive parent deletion (e.g., `Appointment → Doctor`, `Department → Doctor`) to preserve historical data |
| Circular reference `Department ↔ Doctor` | Resolved by adding `head_of_department` FK in a separate migration (`0002`) after the `Doctor` model exists |
| Custom `AUTH_USER_MODEL` | Configured before the first migration to avoid complex migrations later; enables `role` field directly on the User model |
| `available_days` as CharField | Stored as a comma-separated string and split via a custom template filter (`record_extras.py:split`) — pragmatic choice for a list field that doesn't need relational queries |
| Inline Formset for PrescriptionItems | `inlineformset_factory` enables dynamic add/remove of multiple medicine items per prescription on a single form |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the Playwright tests to verify functionality (`python check_all.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <sub>Built with ❤️ using Django 6.0 & Bootstrap 5.3</sub>
  <br>
  <sub>© 2026 — Hospital Management System</sub>
</div>

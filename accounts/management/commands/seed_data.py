from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from departments.models import Department
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from records.models import Prescription, PrescriptionItem, MedicalRecord
from datetime import time, date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        if User.objects.filter(username='admin').exists():
            self.stdout.write('Data already exists, skipping.')
            return

        admin_user = User.objects.create_superuser(
            username='admin', email='admin@hospital.com', password='admin123',
            role='Admin', phone_number='1234567890'
        )
        self.stdout.write('  Admin user created')

        doc1_user = User.objects.create_user(
            username='doctor1', email='doctor1@hospital.com', password='doctor123',
            role='Doctor', first_name='John', last_name='Smith', phone_number='1111111111'
        )
        doc2_user = User.objects.create_user(
            username='doctor2', email='doctor2@hospital.com', password='doctor123',
            role='Doctor', first_name='Sarah', last_name='Johnson', phone_number='2222222222'
        )
        doc3_user = User.objects.create_user(
            username='doctor3', email='doctor3@hospital.com', password='doctor123',
            role='Doctor', first_name='Mike', last_name='Brown', phone_number='3333333333'
        )
        self.stdout.write('  Doctor user accounts created')

        receptionist_user = User.objects.create_user(
            username='receptionist', email='receptionist@hospital.com', password='reception123',
            role='Receptionist', first_name='Emma', last_name='Wilson', phone_number='4444444444'
        )
        self.stdout.write('  Receptionist user created')

        dept1 = Department.objects.create(
            name='Cardiology', description='Heart and cardiovascular system'
        )
        dept2 = Department.objects.create(
            name='Neurology', description='Brain and nervous system'
        )
        dept3 = Department.objects.create(
            name='Pediatrics', description='Medical care for children'
        )
        dept4 = Department.objects.create(
            name='Orthopedics', description='Musculoskeletal system'
        )
        dept5 = Department.objects.create(
            name='General Medicine', description='General health and primary care'
        )
        self.stdout.write('  Departments created')

        doctor1 = Doctor.objects.create(
            user=doc1_user, department=dept1, specialization='Interventional Cardiology',
            qualification='MD, DM Cardiology', experience_years=12,
            consultation_fee=150, available_days='Monday,Tuesday,Thursday,Friday',
            available_time_start=time(9, 0), available_time_end=time(17, 0), is_active=True
        )
        doctor2 = Doctor.objects.create(
            user=doc2_user, department=dept2, specialization='Neurology',
            qualification='MD, DM Neurology', experience_years=8,
            consultation_fee=200, available_days='Monday,Tuesday,Wednesday,Thursday',
            available_time_start=time(10, 0), available_time_end=time(18, 0), is_active=True
        )
        doctor3 = Doctor.objects.create(
            user=doc3_user, department=dept3, specialization='Pediatric Medicine',
            qualification='MD Pediatrics', experience_years=6,
            consultation_fee=100, available_days='Monday,Wednesday,Friday',
            available_time_start=time(9, 0), available_time_end=time(15, 0), is_active=True
        )
        self.stdout.write('  Doctors created')

        dept1.head_of_department = doctor1
        dept2.head_of_department = doctor2
        dept3.head_of_department = doctor3
        dept1.save()
        dept2.save()
        dept3.save()
        self.stdout.write('  Department heads assigned')

        patients_data = [
            ('Alice', 'Williams', '1990-05-15', 'Female', 'A+', '5551111111', 'alice@email.com', '123 Main St', 'Bob Williams', '5551111112'),
            ('David', 'Miller', '1985-08-22', 'Male', 'O+', '5552222222', 'david@email.com', '456 Oak Ave', 'Jane Miller', '5552222223'),
            ('Sophia', 'Taylor', '2019-03-10', 'Female', 'B+', '5553333333', '', '789 Pine Rd', 'Mark Taylor', '5553333334'),
            ('James', 'Anderson', '1972-11-30', 'Male', 'AB+', '5554444444', 'james@email.com', '321 Elm St', 'Lisa Anderson', '5554444445'),
            ('Olivia', 'Thomas', '2000-07-18', 'Female', 'A-', '5555555555', 'olivia@email.com', '654 Birch Ln', 'Tom Thomas', '5555555556'),
            ('William', 'Jackson', '1965-02-28', 'Male', 'O-', '5556666666', 'william@email.com', '987 Cedar Dr', 'Mary Jackson', '5556666667'),
            ('Emma', 'White', '1995-09-12', 'Female', 'B-', '5557777777', 'emma@email.com', '147 Walnut Ct', 'John White', '5557777778'),
            ('Lucas', 'Harris', '2015-06-05', 'Male', 'AB-', '5558888888', '', '258 Spruce Way', 'Nancy Harris', '5558888889'),
            ('Ava', 'Martin', '1988-04-20', 'Female', 'A+', '5559999999', 'ava@email.com', '369 Ash Blvd', 'Paul Martin', '5559999990'),
            ('Daniel', 'Garcia', '1978-12-01', 'Male', 'O+', '5550000000', 'daniel@email.com', '159 Maple Ave', 'Laura Garcia', '5550000001'),
        ]
        patients = []
        for data in patients_data:
            patient = Patient.objects.create(
                first_name=data[0], last_name=data[1], date_of_birth=data[2],
                gender=data[3], blood_group=data[4], phone_number=data[5],
                email=data[6], address=data[7], emergency_contact_name=data[8],
                emergency_contact_phone=data[9]
            )
            patients.append(patient)
        self.stdout.write(f'  {len(patients)} patients created')

        today = timezone.now().date()
        appointments_data = [
            (patients[0], doctor1, dept1, today, time(9, 0), 'Confirmed'),
            (patients[1], doctor1, dept1, today, time(10, 0), 'Pending'),
            (patients[2], doctor2, dept2, today, time(11, 0), 'Confirmed'),
            (patients[3], doctor2, dept2, today, time(14, 0), 'Completed'),
            (patients[4], doctor3, dept3, today, time(9, 30), 'Completed'),
            (patients[5], doctor3, dept3, today, time(10, 30), 'Cancelled'),
            (patients[6], doctor1, dept1, today + timedelta(days=1), time(9, 0), 'Pending'),
            (patients[7], doctor2, dept2, today + timedelta(days=1), time(11, 0), 'Pending'),
            (patients[8], doctor3, dept3, today + timedelta(days=1), time(14, 0), 'Pending'),
            (patients[9], doctor1, dept1, today + timedelta(days=2), time(10, 0), 'Pending'),
        ]
        appointments = []
        for data in appointments_data:
            apt = Appointment.objects.create(
                patient=data[0], doctor=data[1], department=data[2],
                appointment_date=data[3], appointment_time=data[4],
                status=data[5], reason_for_visit='Routine checkup and consultation'
            )
            appointments.append(apt)
        self.stdout.write(f'  {len(appointments)} appointments created')

        rx = Prescription.objects.create(
            appointment=appointments[3], patient=patients[3], doctor=doctor2,
            diagnosis='Migraine with aura. Patient reports frequent headaches with visual disturbances.',
            notes='Follow up in 2 weeks if symptoms persist.'
        )
        PrescriptionItem.objects.create(
            prescription=rx, medicine_name='Sumatriptan', dosage='50mg',
            frequency='As needed, max 2/day', duration='7 days',
            instructions='Take at first sign of migraine attack'
        )
        PrescriptionItem.objects.create(
            prescription=rx, medicine_name='Ibuprofen', dosage='400mg',
            frequency='3 times daily after meals', duration='5 days',
            instructions='Do not take on empty stomach'
        )

        rx2 = Prescription.objects.create(
            appointment=appointments[4], patient=patients[4], doctor=doctor3,
            diagnosis='Upper respiratory tract infection with fever.',
            notes='Plenty of rest and fluids recommended.'
        )
        PrescriptionItem.objects.create(
            prescription=rx2, medicine_name='Amoxicillin', dosage='250mg',
            frequency='3 times daily', duration='7 days',
            instructions='Complete the full course even if symptoms improve'
        )
        PrescriptionItem.objects.create(
            prescription=rx2, medicine_name='Paracetamol', dosage='500mg',
            frequency='As needed for fever, max 4/day', duration='3 days',
            instructions='Take if temperature exceeds 101°F'
        )
        self.stdout.write('  Prescriptions with items created')

        MedicalRecord.objects.create(
            patient=patients[3], doctor=doctor2, appointment=appointments[3],
            diagnosis='Chronic migraine with aura',
            treatment='Prescribed Sumatriptan for acute attacks. Advised lifestyle modifications including regular sleep schedule and hydration.',
            test_results='CT scan: Normal. No abnormalities detected.',
            notes='Patient advised to maintain headache diary.'
        )
        MedicalRecord.objects.create(
            patient=patients[4], doctor=doctor3, appointment=appointments[4],
            diagnosis='Acute upper respiratory tract infection',
            treatment='Prescribed antibiotics and antipyretics. Advised rest and increased fluid intake.',
            test_results='Chest X-ray: Clear. CBC: Elevated WBC count indicating infection.',
            notes='Follow up if no improvement in 72 hours.'
        )
        self.stdout.write('  Medical records created')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('Demo Login Credentials:')
        self.stdout.write('  Admin:         username: admin         password: admin123')
        self.stdout.write('  Doctor 1:      username: doctor1       password: doctor123')
        self.stdout.write('  Doctor 2:      username: doctor2       password: doctor123')
        self.stdout.write('  Doctor 3:      username: doctor3       password: doctor123')
        self.stdout.write('  Receptionist:  username: receptionist  password: reception123')

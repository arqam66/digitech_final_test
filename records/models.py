from django.db import models


class Prescription(models.Model):
    appointment = models.ForeignKey(
        'appointments.Appointment', on_delete=models.CASCADE, related_name='prescriptions'
    )
    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='prescriptions'
    )
    doctor = models.ForeignKey(
        'doctors.Doctor', on_delete=models.SET_NULL, null=True, related_name='prescriptions'
    )
    date_prescribed = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription for {self.patient} by {self.doctor} on {self.date_prescribed.date()}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name='items'
    )
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='medical_records'
    )
    doctor = models.ForeignKey(
        'doctors.Doctor', on_delete=models.SET_NULL, null=True, related_name='medical_records'
    )
    appointment = models.ForeignKey(
        'appointments.Appointment', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='medical_records'
    )
    record_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField(blank=True)
    test_results = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-record_date']

    def __str__(self):
        return f"Record for {self.patient} on {self.record_date.date()}"

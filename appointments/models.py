from django.db import models


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        CONFIRMED = 'Confirmed', 'Confirmed'
        COMPLETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'

    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='appointments'
    )
    doctor = models.ForeignKey(
        'doctors.Doctor', on_delete=models.SET_NULL, null=True, related_name='appointments'
    )
    department = models.ForeignKey(
        'departments.Department', on_delete=models.SET_NULL, null=True
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reason_for_visit = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.patient} - {self.doctor} on {self.appointment_date}"

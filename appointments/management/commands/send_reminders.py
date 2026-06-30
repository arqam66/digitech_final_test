from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from appointments.models import Appointment


class Command(BaseCommand):
    help = 'Send email reminders for tomorrow\'s appointments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print reminders without sending emails',
        )

    def handle(self, *args, **options):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        appointments = Appointment.objects.filter(
            appointment_date=tomorrow,
            status__in=['Pending', 'Confirmed']
        ).select_related('patient', 'doctor__user')

        if not appointments:
            self.stdout.write(f'No appointments scheduled for {tomorrow}.')
            return

        sent = 0
        for apt in appointments:
            patient_email = apt.patient.email
            if not patient_email:
                self.stdout.write(f'  SKIP {apt.patient} — no email address')
                continue

            subject = f'Appointment Reminder - {apt.appointment_date}'
            message = (
                f'Dear {apt.patient.first_name} {apt.patient.last_name},\n\n'
                f'This is a reminder of your appointment:\n\n'
                f'  Doctor: {apt.doctor}\n'
                f'  Department: {apt.department}\n'
                f'  Date: {apt.appointment_date}\n'
                f'  Time: {apt.appointment_time}\n'
                f'  Status: {apt.status}\n\n'
                f'Please arrive 15 minutes early.\n\n'
                f'Thank you,\nCity Hospital'
            )

            if options['dry_run']:
                self.stdout.write(f'  [DRY-RUN] Would send to {patient_email}: {subject}')
            else:
                try:
                    send_mail(
                        subject, message,
                        settings.DEFAULT_FROM_EMAIL or 'noreply@hospital.com',
                        [patient_email],
                        fail_silently=False,
                    )
                    self.stdout.write(f'  SENT to {patient_email}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  FAILED to {patient_email}: {e}'))
            sent += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n{f"Dry run — {sent} reminders" if options["dry_run"] else f"{sent} reminder emails sent."}'
        ))

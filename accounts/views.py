from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_redirect(request):
    role = request.user.role
    if role == 'Admin':
        return redirect('admin_dashboard')
    elif role == 'Doctor':
        return redirect('doctor_dashboard')
    elif role == 'Receptionist':
        return redirect('receptionist_dashboard')
    return redirect('login')


@login_required
def admin_dashboard(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'today_appointments': Appointment.objects.filter(
            appointment_date=timezone.now().date()
        ).count(),
        'pending_appointments': Appointment.objects.filter(
            status='Pending'
        ).count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
    except ObjectDoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('dashboard_redirect')
    today = timezone.now().date()
    context = {
        'today_appointments': Appointment.objects.filter(
            doctor=doctor, appointment_date=today
        ).order_by('appointment_time'),
        'total_appointments': Appointment.objects.filter(doctor=doctor).count(),
        'recent_patients': Appointment.objects.filter(
            doctor=doctor
        ).values('patient').distinct().count(),
    }
    return render(request, 'accounts/doctor_dashboard.html', context)


@login_required
def receptionist_dashboard(request):
    today = timezone.now().date()
    context = {
        'today_appointments': Appointment.objects.filter(
            appointment_date=today
        ).order_by('appointment_time'),
        'total_patients': Patient.objects.count(),
        'pending_appointments': Appointment.objects.filter(
            status='Pending'
        ).count(),
    }
    return render(request, 'accounts/receptionist_dashboard.html', context)

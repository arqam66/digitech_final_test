from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.db.models import Q
from .models import Doctor
from .forms import DoctorForm
from appointments.models import Appointment
from records.models import Prescription, MedicalRecord


class AdminRequiredMixin(LoginRequiredMixin):
    def test_func(self):
        return self.request.user.role == 'Admin'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.test_func():
            from django.shortcuts import redirect
            return redirect('dashboard_redirect')
        return super().dispatch(request, *args, **kwargs)


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        department = self.request.GET.get('department')
        specialization = self.request.GET.get('specialization')
        search = self.request.GET.get('search')
        if department:
            qs = qs.filter(department_id=department)
        if specialization:
            qs = qs.filter(specialization__icontains=specialization)
        if search:
            qs = qs.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(specialization__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from departments.models import Department
        context['departments'] = Department.objects.all()
        context['specializations'] = Doctor.objects.values_list(
            'specialization', flat=True
        ).distinct().order_by('specialization')
        return context


class DoctorCreateView(AdminRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

    def form_valid(self, form):
        from django.contrib import messages
        messages.success(self.request, 'Doctor added successfully.')
        return super().form_valid(form)


class DoctorUpdateView(AdminRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

    def form_valid(self, form):
        from django.contrib import messages
        messages.success(self.request, 'Doctor updated successfully.')
        return super().form_valid(form)


class DoctorDeleteView(AdminRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'doctors/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')

    def delete(self, request, *args, **kwargs):
        from django.contrib import messages
        messages.success(request, 'Doctor deleted successfully.')
        return super().delete(request, *args, **kwargs)


class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'doctors/doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()
        context['appointments'] = Appointment.objects.filter(doctor=doctor)[:10]
        return context


@login_required
def doctor_appointments_view(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('dashboard_redirect')
    appointments = Appointment.objects.filter(doctor=doctor).select_related(
        'patient', 'department'
    ).order_by('-appointment_date', '-appointment_time')
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'doctors': Doctor.objects.none(),
        'departments': [],
        'status_choices': Appointment.Status.choices,
    })


@login_required
def doctor_prescriptions_view(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('dashboard_redirect')
    prescriptions = Prescription.objects.filter(doctor=doctor).select_related(
        'patient'
    ).order_by('-date_prescribed')
    return render(request, 'records/prescription_list.html', {
        'prescriptions': prescriptions,
    })


@login_required
def doctor_medical_records_view(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('dashboard_redirect')
    records = MedicalRecord.objects.filter(doctor=doctor).select_related(
        'patient'
    ).order_by('-record_date')
    return render(request, 'records/medical_record_list.html', {
        'medical_records': records,
    })


@login_required
def doctor_calendar(request):
    doctors = Doctor.objects.filter(is_active=True).select_related('department', 'user')
    for doc in doctors:
        doc.day_list = [d.strip() for d in doc.available_days.split(',')] if doc.available_days else []
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return render(request, 'doctors/doctor_calendar.html', {
        'doctors': doctors,
        'weekdays': weekdays,
    })

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.db import models
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 20

    def get_queryset(self):
        qs = Appointment.objects.select_related('patient', 'doctor__user', 'department')
        user = self.request.user
        if user.role == 'Doctor':
            qs = qs.filter(doctor=user.doctor)
        elif user.role == 'Receptionist':
            pass  # see all
        date = self.request.GET.get('date')
        doctor_id = self.request.GET.get('doctor')
        department_id = self.request.GET.get('department')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        if date:
            qs = qs.filter(appointment_date=date)
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        if department_id:
            qs = qs.filter(department_id=department_id)
        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(
                models.Q(patient__first_name__icontains=search) |
                models.Q(patient__last_name__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from doctors.models import Doctor
        from departments.models import Department
        context['doctors'] = Doctor.objects.filter(is_active=True)
        context['departments'] = Department.objects.all()
        context['status_choices'] = Appointment.Status.choices
        return context


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Appointment scheduled successfully.')
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Appointment updated successfully.')
        return super().form_valid(form)


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Appointment cancelled successfully.')
        return super().delete(request, *args, **kwargs)


@login_required
def appointment_complete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'Completed'
    appointment.save()
    messages.success(request, 'Appointment marked as completed.')
    return redirect('appointment_detail', pk=pk)


@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'Cancelled'
    appointment.save()
    messages.success(request, 'Appointment cancelled.')
    return redirect('appointment_detail', pk=pk)


@login_required
def appointment_confirm(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'Confirmed'
    appointment.save()
    messages.success(request, 'Appointment confirmed.')
    return redirect('appointment_detail', pk=pk)

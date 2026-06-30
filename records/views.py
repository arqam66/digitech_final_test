from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.forms import inlineformset_factory
from django.contrib import messages
from .models import Prescription, PrescriptionItem, MedicalRecord
from .forms import PrescriptionForm, PrescriptionItemForm, MedicalRecordForm
from .utils import render_pdf
from django.http import HttpResponse
from patients.models import Patient
from appointments.models import Appointment


PrescriptionItemFormSet = inlineformset_factory(
    Prescription, PrescriptionItem,
    form=PrescriptionItemForm,
    extra=3, can_delete=True
)


class PrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = 'records/prescription_list.html'
    context_object_name = 'prescriptions'
    paginate_by = 20

    def get_queryset(self):
        qs = Prescription.objects.select_related('patient', 'doctor__user')
        user = self.request.user
        if user.role == 'Doctor':
            qs = qs.filter(doctor=user.doctor)
        elif user.role == 'Receptionist':
            pass
        return qs.order_by('-date_prescribed')


class PrescriptionDetailView(LoginRequiredMixin, DetailView):
    model = Prescription
    template_name = 'records/prescription_detail.html'
    context_object_name = 'prescription'


@login_required
def prescription_create(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        formset = PrescriptionItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            prescription = form.save()
            formset.instance = prescription
            formset.save()
            messages.success(request, 'Prescription created successfully.')
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionForm()
        formset = PrescriptionItemFormSet()
    return render(request, 'records/prescription_form.html', {
        'form': form,
        'formset': formset,
    })


@login_required
def prescription_update(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        formset = PrescriptionItemFormSet(request.POST, instance=prescription)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Prescription updated successfully.')
            return redirect('prescription_detail', pk=pk)
    else:
        form = PrescriptionForm(instance=prescription)
        formset = PrescriptionItemFormSet(instance=prescription)
    return render(request, 'records/prescription_form.html', {
        'form': form,
        'formset': formset,
    })


class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'records/medical_record_list.html'
    context_object_name = 'medical_records'
    paginate_by = 20

    def get_queryset(self):
        qs = MedicalRecord.objects.select_related('patient', 'doctor__user')
        user = self.request.user
        if user.role == 'Doctor':
            qs = qs.filter(doctor=user.doctor)
        return qs.order_by('-record_date')


class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'records/medical_record_form.html'
    success_url = reverse_lazy('medical_record_list')

    def form_valid(self, form):
        messages.success(self.request, 'Medical record created successfully.')
        return super().form_valid(form)


class MedicalRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'records/medical_record_form.html'
    success_url = reverse_lazy('medical_record_list')

    def form_valid(self, form):
        messages.success(self.request, 'Medical record updated successfully.')
        return super().form_valid(form)


@login_required
def prescription_pdf(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    pdf = render_pdf('records/prescription_pdf.html', {'prescription': prescription})
    if pdf is None:
        messages.error(request, 'Error generating PDF.')
        return redirect('prescription_detail', pk=pk)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prescription_{pk}.pdf"'
    return response


@login_required
def patient_report(request):
    patients = Patient.objects.all()
    patient_data = []
    for p in patients:
        patient_data.append({
            'patient': p,
            'appt_count': Appointment.objects.filter(patient=p).count(),
            'rx_count': Prescription.objects.filter(patient=p).count(),
            'rec_count': MedicalRecord.objects.filter(patient=p).count(),
        })
    context = {
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_prescriptions': Prescription.objects.count(),
        'total_records': MedicalRecord.objects.count(),
        'patient_data': patient_data,
    }
    return render(request, 'records/patient_report.html', context)

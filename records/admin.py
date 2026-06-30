from django.contrib import admin
from .models import Prescription, PrescriptionItem, MedicalRecord


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_prescribed', 'diagnosis')
    list_filter = ('date_prescribed',)
    search_fields = ('patient__first_name', 'patient__last_name', 'diagnosis')
    inlines = [PrescriptionItemInline]


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'prescription', 'dosage', 'frequency')
    search_fields = ('medicine_name',)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'record_date', 'diagnosis')
    list_filter = ('record_date',)
    search_fields = ('patient__first_name', 'patient__last_name', 'diagnosis')

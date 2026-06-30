from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'specialization', 'consultation_fee', 'is_active')
    list_filter = ('department', 'is_active', 'specialization')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')

from django.urls import path
from . import views

urlpatterns = [
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/create/', views.prescription_create, name='prescription_create'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('prescriptions/<int:pk>/update/', views.prescription_update, name='prescription_update'),
    path('prescriptions/<int:pk>/pdf/', views.prescription_pdf, name='prescription_pdf'),
    path('prescriptions/<int:pk>/delete/', views.PrescriptionDeleteView.as_view(), name='prescription_delete'),
    path('records/', views.MedicalRecordListView.as_view(), name='medical_record_list'),
    path('records/create/', views.MedicalRecordCreateView.as_view(), name='medical_record_create'),
    path('records/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('records/<int:pk>/update/', views.MedicalRecordUpdateView.as_view(), name='medical_record_update'),
    path('records/<int:pk>/delete/', views.MedicalRecordDeleteView.as_view(), name='medical_record_delete'),
    path('patient-report/', views.patient_report, name='patient_report'),
]

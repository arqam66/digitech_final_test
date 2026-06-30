from django.urls import path
from . import views

urlpatterns = [
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/create/', views.prescription_create, name='prescription_create'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('prescriptions/<int:pk>/update/', views.prescription_update, name='prescription_update'),
    path('records/', views.MedicalRecordListView.as_view(), name='medical_record_list'),
    path('records/create/', views.MedicalRecordCreateView.as_view(), name='medical_record_create'),
    path('records/<int:pk>/update/', views.MedicalRecordUpdateView.as_view(), name='medical_record_update'),
]

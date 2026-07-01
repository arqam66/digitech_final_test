from django.urls import path
from . import views

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('create/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('<int:pk>/update/', views.DoctorUpdateView.as_view(), name='doctor_update'),
    path('<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
    path('my/appointments/', views.doctor_appointments_view, name='doctor_appointments'),
    path('my/prescriptions/', views.doctor_prescriptions_view, name='doctor_prescriptions'),
    path('my/records/', views.doctor_medical_records_view, name='doctor_medical_records'),
    path('calendar/', views.doctor_calendar, name='doctor_calendar'),
]

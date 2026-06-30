from django.contrib import admin
from django.urls import path, include
from . import views

handler404 = 'hospital.views.handler404'
handler500 = 'hospital.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('departments/', include('departments.urls')),
    path('doctors/', include('doctors.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('records/', include('records.urls')),
]

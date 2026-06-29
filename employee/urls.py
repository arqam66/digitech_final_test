"""DjangoJavaTpointCRUD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

# URL patterns routing requests to views inside the 'employee' application
urlpatterns = [
    # Redirect base URL to the employee list view
    path('', views.show),
    
    # URL to handle adding new employees (both form display and POST handling)
    path('emp', views.emp),
    
    # URL to show the list of all employees
    path('show', views.show),
    
    # URL to show the edit form for a specific employee by ID
    path('edit/<int:id>', views.edit),
    
    # URL to handle updating an employee's details in the database by ID
    path('update/<int:id>', views.update),
    
    # URL to handle deleting an employee record by ID
    path('delete/<int:id>', views.destroy),
]

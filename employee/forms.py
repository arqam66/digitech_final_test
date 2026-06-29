from django import forms
from .models import Employee

# ModelForm for creating and editing Employee records
class EmployeeForm(forms.ModelForm):
    class Meta:
        # Connect this form to the Employee model
        model = Employee
        
        # Include all fields from the Employee model in the form
        fields = "__all__"
        
        # Add Bootstrap classes ('form-control') to form widgets for modern styling
        widgets = {
            'eid': forms.TextInput(attrs={'class': 'form-control'}),
            'ename': forms.TextInput(attrs={'class': 'form-control'}),
            'eemail': forms.EmailInput(attrs={'class': 'form-control'}),
            'econtact': forms.TextInput(attrs={'class': 'form-control'}),
        }
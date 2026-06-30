from django import forms
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user', 'department', 'specialization', 'qualification',
                  'experience_years', 'consultation_fee', 'available_days',
                  'available_time_start', 'available_time_end', 'is_active']
        widgets = {
            'available_time_start': forms.TimeInput(attrs={'type': 'time'}),
            'available_time_end': forms.TimeInput(attrs={'type': 'time'}),
            'available_days': forms.TextInput(attrs={'placeholder': 'e.g., Monday,Tuesday,Wednesday'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs.setdefault('class', 'form-control')

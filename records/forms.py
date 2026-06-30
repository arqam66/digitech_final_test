from django import forms
from .models import Prescription, PrescriptionItem, MedicalRecord


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medicine_name', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs.setdefault('class', 'form-control form-control-sm')


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['appointment', 'patient', 'doctor', 'diagnosis', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs.setdefault('class', 'form-control')


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'appointment', 'diagnosis', 'treatment', 'test_results', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'test_results': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs.setdefault('class', 'form-control')

from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            "title",
            "requiredEducationLevel",
            "requiredExperienceYears",
            "salary",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Full Name "},
            ),
            "requiredExperienceYears": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Experience Years"},
            ),
            "salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Experience Years"},
            ),
        }

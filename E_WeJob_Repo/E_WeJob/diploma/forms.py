from django import forms
from .models import Diploma


class DiplomaForm(forms.ModelForm):
    class Meta:
        model = Diploma
        fields = ("diplomaTitle",)
        widgets = {
            "diplomaTitle": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Diploma Ttile "},
            ),
        }

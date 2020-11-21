from django.contrib.auth import get_user_model, forms, password_validation
from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    NumberInput,
    Select,
    EmailField,
    CharField,
    PasswordInput,
)
from django.core.exceptions import ValidationError

from .models import CompanyProfile, CandidateProfile, Message
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    password1 = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "name": "dzName",
            },
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = CharField(
        label=_("Password confirmation"),
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password confirmation",
                "name": "dzName",
            },
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "User Name ",
                    "name": "dzName",
                },
            ),
            "email": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "E-MAIL",
                    "name": "dzName",
                },
            ),
        }

    error_message = forms.UserCreationForm.error_messages.update(
        {
            "duplicate_username": ("This username has already been taken."),
            "duplicate_email": ("This email is already in use."),
        }
    )

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])


class CompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        fields = (
            "cName",
            "tel",
        )

        widgets = {
            "cName": TextInput(
                attrs={"class": "form-control", "placeholder": "Company Name "},
            ),
            "tel": TextInput(
                attrs={"class": "form-control", "placeholder": "Telephone"},
            ),
        }


class CandidateProfileForm(ModelForm):
    class Meta:
        model = CandidateProfile
        fields = (
            "fullName",
            "tel",
            "experienceYears",
        )

        widgets = {
            "fullName": TextInput(
                attrs={"class": "form-control", "placeholder": "Full Name "},
            ),
            "tel": TextInput(
                attrs={"class": "form-control", "placeholder": "Telephone"},
            ),
            "experienceYears": NumberInput(
                attrs={"class": "form-control", "placeholder": "Experience Years"},
            ),
        }


class UserLoginForm(forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = CharField(
        widget=TextInput(attrs={"class": "form-control", "placeholder": "username"})
    )
    password = CharField(
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "password",
            }
        )
    )


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = (
            "subject",
            "message",
        )
        widgets = {
            "subject": TextInput(
                attrs={
                    "name": "dzName",
                    "class": "form-control",
                    "placeholder": "Subject ",
                },
            ),
            "message": Textarea(
                attrs={
                    "name": "dzMessage",
                    "class": "form-control",
                    "placeholder": "Your Message...",
                    "rows": "4",
                },
            ),
        }

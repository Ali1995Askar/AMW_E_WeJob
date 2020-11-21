from django.contrib import admin
from django.urls import path, include
from .forms import UserLoginForm
from django.contrib.auth.views import LoginView
from . import views

# CompanyCreationView, CandidateCreationView, UserDetailView

app_name = "user"


urlpatterns = [
    path(
        "company/signup/", views.CompanyCreationView.as_view(), name="company-sign-up"
    ),
    path(
        "candidate/signup/",
        views.CandidateCreationView.as_view(),
        name="candidate-sign-up",
    ),
    path(
        "login/",
        view=LoginView.as_view(form_class=UserLoginForm),
        name="login",
    ),
    path("<int:pk>/", view=views.UserDetailView.as_view(), name="detail"),
    path("", include("django.contrib.auth.urls")),
]

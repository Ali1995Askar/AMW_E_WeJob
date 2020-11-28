from rest_framework.routers import SimpleRouter

from django.urls import path, include
from . import views

app_name = "job_api"


urlpatterns = [
    path("jobs/<int:pk>/", views.SuitableUsers.as_view(), name="details"),
    path("jobs/", views.JobListCreateView.as_view(), name="jobs"),
    path("suitable-jobs/", views.SuitableJobs.as_view(), name="suitable-jobs"),
]

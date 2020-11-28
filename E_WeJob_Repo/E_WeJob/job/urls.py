from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "job"

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("jobs", views.JobListView, basename="jobs")

urlpatterns = [
    path("create/", views.JobCreateView.as_view(), name="create"),
    path("update/<int:pk>", views.JobUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", views.JobDeleteView.as_view(), name="delete"),
    path("<int:pk>/", views.JobDetailView.as_view(), name="detail"),
    path("<str:username>/jobs/", views.MyJobView.as_view(), name="my-jobs"),
]
urlpatterns += router.urls

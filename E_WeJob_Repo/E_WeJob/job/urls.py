from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "job"


urlpatterns = [
    path("all/", views.JobListView.as_view(), name="all"),
    path("create/", views.JobCreateView.as_view(), name="create"),
    path("update/<int:pk>", views.JobUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", views.JobDeleteView.as_view(), name="delete"),
    path("<int:pk>/", views.JobDetailView.as_view(), name="detail"),
    path("<str:username>/jobs/", views.MyJoBView.as_view(), name="my-jobs"),
]

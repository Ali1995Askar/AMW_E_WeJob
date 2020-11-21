from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "diploma"


urlpatterns = [
    path("all/", views.DiplomaListView.as_view(), name="all"),
    path("create/", views.DiplomaCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.DiplomaUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.DiplomaDeleteView.as_view(), name="delete"),
    path("<int:pk>/", views.DiplomaDetailView.as_view(), name="detail"),
]

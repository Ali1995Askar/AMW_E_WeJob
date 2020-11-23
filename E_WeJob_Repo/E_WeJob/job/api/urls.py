from rest_framework.routers import SimpleRouter

from django.urls import path, include
from .views import JobViewSet

app_name = "job_api"

router = SimpleRouter()

router.register("jobs", JobViewSet, basename="jobs")

urlpatterns = router.urls
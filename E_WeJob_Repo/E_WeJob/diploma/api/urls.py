from rest_framework.routers import SimpleRouter

from django.urls import path, include

from .views import DiplomaViewSet

app_name = "diploma_api"

router = SimpleRouter()

router.register("diploma", DiplomaViewSet)

urlpatterns = router.urls
from rest_framework.routers import SimpleRouter

from django.urls import path, include

from .views import (
    CompanySignupView,
    CandidateSignupView,
    UserLoginView,
    UserDetailView,
)
from django.urls import path

app_name = "user_api"

# router = SimpleRouter()
# router.register("diplomas", DiplomaViewSet)


urlpatterns = [
    path("company/signup", CompanySignupView.as_view(), name="comapany-signup"),
    path("candidate/signup", CandidateSignupView.as_view(), name="candidate-signup"),
    path("user/login", UserLoginView.as_view(), name="user-login"),
    path("user/<int:pk>", UserDetailView.as_view(), name="user-detail"),
]

# urlpatterns += router.urls

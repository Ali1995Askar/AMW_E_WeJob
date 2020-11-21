from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from utils.views import SignupWizardView
from utils.permissions import IsDiplomaOwnerOrReadOnly, IsCandidate
from utils.serializers import UserDetailsSerializer
from ..models import CompanyProfile

from .serializers import (
    UserLoginSerializer,
    SignupCompanySerializer,
    SignupCandidateSerializer,
)

User = get_user_model()


class CompanySignupView(SignupWizardView):
    permission_classes = (AllowAny,)
    serializer_class = SignupCompanySerializer
    queryset = User.objects.all()


class CandidateSignupView(SignupWizardView):
    permission_classes = (AllowAny,)
    serializer_class = SignupCandidateSerializer
    queryset = User.objects.all()


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    # to fo make post to get method
    def post(self, request, *args, **kwargs):
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "username": user.username,
                    "email": user.email,
                    "token": token.key,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "Auth_error": "username and password doesn't match!",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()

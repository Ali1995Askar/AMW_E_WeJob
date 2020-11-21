from rest_framework import serializers
from django.contrib.auth import get_user_model
from utils.serializers import (
    SignupWizardSerializer,
    UserSerializer,
    CompanyProfileSerializer,
    CandidateProfileSerializer,
)
from ..models import CompanyProfile, CandidateProfile


User = get_user_model()

"""
Models Serializers
"""


"""
    Users Registration Serializers
"""


class SignupCompanySerializer(SignupWizardSerializer):

    profile = CompanyProfileSerializer()

    def create(self, validated_data):
        user = super().create(validated_data)
        user.user_type = User.COMPANY
        user.save()
        company_data = validated_data.pop("profile")
        CompanyProfile.objects.create(
            user=user,
            cName=company_data["cName"],
            tel=company_data["tel"],
        )
        return user


class SignupCandidateSerializer(SignupWizardSerializer):

    profile = CandidateProfileSerializer()

    def create(self, validated_data):
        user = super().create(validated_data)
        user.user_type = User.CANDIDATE
        user.save()
        candidate_data = validated_data.pop("profile")
        CandidateProfile.objects.create(
            user=user,
            fullName=candidate_data["fullName"],
            tel=candidate_data["tel"],
            experienceYears=candidate_data["experienceYears"],
        )
        return user


"""
User Login Serializer
"""


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

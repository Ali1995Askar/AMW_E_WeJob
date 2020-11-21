from rest_framework import serializers
from django.contrib.auth import get_user_model

# from user.api.serializers import CompanyProfileSerializer
from user.models import CompanyProfile, CandidateProfile

# from user.api.serializers import CompanyProfileSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "url"]

        extra_kwargs = {
            "url": {"view_name": "user_api:user-detail", "lookup_field": "pk"}
        }


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ["cName", "tel"]


class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = ["fullName", "tel", "experienceYears"]


class UserDetailsSerializer(serializers.ModelSerializer):
    def get_profile(self, obj):
        if obj.is_candidate:
            profile = CandidateProfileSerializer(obj.profile).data
        elif obj.is_company:
            profile = CompanyProfileSerializer(obj.profile).data
        else:
            profile = "Admin"
        return profile

    profile = serializers.SerializerMethodField("get_profile")

    class Meta:
        model = User
        fields = [
            "profile",
            "username",
            "email",
            "user_type",
            "is_active",
            "is_superuser",
            "date_joined",
        ]


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class SignupWizardSerializer(serializers.Serializer):
    user = UserSignupSerializer()
    token = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(
            username=user_data["username"],
            email=user_data["email"],
        )
        user.set_password(user_data["password"])
        return user

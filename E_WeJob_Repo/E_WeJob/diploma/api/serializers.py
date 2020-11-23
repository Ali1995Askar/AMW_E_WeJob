from rest_framework import serializers

from utils.serializers import UserSerializer
from ..models import Diploma


class DiplomaSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    depth = 1

    class Meta:
        model = Diploma
        fields = [
            "id",
            "diplomaTitle",
            "user",
        ]
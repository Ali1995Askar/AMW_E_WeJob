from rest_framework import serializers
from django.shortcuts import get_object_or_404

from diploma.models import Diploma
from diploma.api.serializers import DiplomaSerializer

from user.api.serializers import UserSerializer
from ..models import Job


class JobSerializer(serializers.ModelSerializer):

    company = UserSerializer(read_only=True)
    requiredEducationLevel = DiplomaSerializer(read_only=True)

    class Meta:
        model = Job
        depth = 1
        fields = [
            "id",
            "company",
            "title",
            "requiredExperienceYears",
            "salary",
            "requiredEducationLevel",
        ]

    # to do set pk to slug
    def create(self, validated_data):
        diploma_pk = validated_data.pop("requiredEducationLevel")
        diploma = get_object_or_404(Diploma, pk=diploma_pk.get("diplomaTitle"))
        job = Job.objects.create(**validated_data, requiredEducationLevel=diploma)
        return job

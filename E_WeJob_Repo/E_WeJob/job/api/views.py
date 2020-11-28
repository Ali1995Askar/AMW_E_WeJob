# from rest_framework import viewsets
# from rest_framework import permissions
# from rest_framework.response import Response
# from utils.permissions import IsJobOwnerOrReadOnly, IsCompany, IsCandidate
# from .serializers import JobSerializer

# from ..models import Job

from rest_framework import filters

# from rest_framework import status

import django_filters.rest_framework

# from utils.serializers import UserDetailsSerializer

from rest_framework.response import Response
from .filters import JobFilter
from rest_framework import status
from rest_framework import permissions

from rest_framework import generics
from django.contrib.auth import get_user_model

from utils.serializers import UserDetailsSerializer
from utils.permissions import IsCompany
from .serializers import JobSerializer
from ..models import Job

User = get_user_model()


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany]
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = JobFilter
    ordering_fields = ["requiredExperienceYears"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)


class SuitableJobs(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_suitable_Jobs(self, request):
        user = self.request.user
        EducationLevel = user.diplomas.all()
        ExperienceYears = user.profile.experienceYears
        jobs = self.get_queryset()
        suitable_jobs = []
        for job in list(jobs):
            if job.requiredExperienceYears <= ExperienceYears:
                diplomas = user.diplomas.filter(diplomaTitle=job.requiredEducationLevel)
                if diplomas:
                    suitable_jobs += [job]
        return suitable_jobs

    def get(self, request, *args, **kwargs):
        queryset = self.get_suitable_Jobs(self.request)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SuitableUsers(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def suitable_users(self, request, *args, **kwargs):
        instance = self.get_object()
        requiredEducationLevel = instance.requiredEducationLevel
        requiredExperienceYears = instance.requiredExperienceYears
        users = User.objects.filter(user_type=User.CANDIDATE)
        suitable_users = []
        for user in list(users):
            if user.profile.experienceYears >= requiredExperienceYears:
                diplomas = user.diplomas.filter(
                    diplomaTitle=requiredEducationLevel.diplomaTitle
                )
                if diplomas:
                    suitable_users += [user]
        return suitable_users

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        job_serializer = self.get_serializer(instance)
        suitable_users_serializer = UserDetailsSerializer(
            self.suitable_users(request), many=True
        )
        response = {
            "job": job_serializer.data,
            "suitable_users": suitable_users_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""
 {
 'id': 44,
  "company": {
        "username": "company",
        "url": "http://127.0.0.1:8000/api/v1/user/63"
    },
    "title": "postman",
    "requiredExperienceYears": 12,
    "salary": 1222,
    "requiredEducationLevel": {
        "id": 1,
        "diplomaTitle": "itlllkk",
        "candidate": {
            "username": "admin",
            "url": "http://127.0.0.1:8000/api/v1/user/1"
        }
    }
}
"""

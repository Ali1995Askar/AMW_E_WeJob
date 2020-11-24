from rest_framework import viewsets
from rest_framework import permissions

from utils.permissions import IsJobOwnerOrReadOnly, IsCompany
from .filters import JobFilter
from .serializers import JobSerializer

from ..models import Job

from rest_framework import filters

import django_filters.rest_framework


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticated, IsCompany, IsJobOwnerOrReadOnly)
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = JobFilter

    ordering_fields = ["requiredExperienceYears"]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

    def perform_update(self, serializer):
        serializer.save(company=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


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

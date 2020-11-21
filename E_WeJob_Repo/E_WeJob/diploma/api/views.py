from rest_framework import viewsets
from rest_framework import permissions

from utils.permissions import IsDiplomaOwnerOrReadOnly, IsCandidate
from .serializers import DiplomaSerializer
from ..models import Diploma


class DiplomaViewSet(viewsets.ModelViewSet):
    paginator = None
    queryset = Diploma.objects.all()
    serializer_class = DiplomaSerializer
    permission_classes = (IsDiplomaOwnerOrReadOnly, IsCandidate)
    # to do redirect to 404 not found
    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

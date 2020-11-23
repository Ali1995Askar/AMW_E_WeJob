from rest_framework import viewsets
from rest_framework import permissions

from utils.permissions import IsDiplomaOwnerOrReadOnly, IsCandidate
from .serializers import DiplomaSerializer
from ..models import Diploma


class DiplomaViewSet(viewsets.ModelViewSet):
    paginator = None
    permission_classes = (permissions.IsAuthenticated, IsDiplomaOwnerOrReadOnly)
    queryset = Diploma.objects.all()
    serializer_class = DiplomaSerializer
    # to do redirect to 404 not found
    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

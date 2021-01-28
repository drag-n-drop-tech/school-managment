from rest_framework import viewsets, permissions, status

from .serializers import fees_collectionSerializer
from .models import fees_collection


class fees_collection_view(viewsets.ModelViewSet):
    queryset = fees_collection.objects.all()

    serializer_class = fees_collectionSerializer
    permissions = [
        permissions.AllowAny
    ]
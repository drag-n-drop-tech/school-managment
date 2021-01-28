from rest_framework import viewsets, permissions, status

from .serializers import fees_collectionSerializer, feesDataSerializer
from .models import fees_collection, fees_data


class fees_collection_view(viewsets.ModelViewSet):
    queryset = fees_collection.objects.all()

    serializer_class = fees_collectionSerializer
    permissions = [
        permissions.AllowAny
    ]


class feesDataView(viewsets.ModelViewSet):
    queryset = fees_data.objects.all()
    serializer_class = feesDataSerializer
    permission_classes = [permissions.AllowAny]
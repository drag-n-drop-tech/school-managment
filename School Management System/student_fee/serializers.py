from rest_framework import serializers
from .models import fees_collection


class fees_collectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = fees_collection
        fields = '__all__'

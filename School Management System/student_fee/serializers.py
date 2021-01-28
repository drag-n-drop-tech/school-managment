from rest_framework import serializers
from .models import fees_collection, fees_data


class feesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = fees_data
        fields = '__all__'


    






class fees_collectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = fees_collection
        fields = '__all__'

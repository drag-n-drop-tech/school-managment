from rest_framework import serializers

from .models import Students, Parents, Classes



class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields="__all__"


class ParentsSerialier(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = '__all__'



class StudentsSerializer(serializers.ModelSerializer):
    parent=ParentsSerialier(many=False)
    ClassNo = ClassesSerializer(many=False)
    class Meta:
        model = Students
        fields = '__all__'


        
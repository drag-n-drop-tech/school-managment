from rest_framework import viewsets, permissions

from .models import Students
from .serializers import StudentsSerializer

class Studentsviewset(viewsets.ModelViewSet):
    serializer_class = StudentsSerializer
    permissions = [permissions.AllowAny]


    def get_queryset(self):
        admission_data = self.request.GET.get('admission')
        queryset=Students.objects.filter(admission_no=admission_data)

        return queryset
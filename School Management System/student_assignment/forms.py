from django import forms
from django.forms import ClearableFileInput
from .models import assignment_files

class assignmentFileForm(forms.ModelForm):
    class Meta:
        model = assignment_files
        fields = ['assignmnt_file']
        widgets = {
            'assignmnt_file': ClearableFileInput(attrs={'multiple': True}),
        }
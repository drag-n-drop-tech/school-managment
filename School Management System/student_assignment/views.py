from django.shortcuts import render

def add_assignment(request):
    return render(request,'add_assignment_template.html')
